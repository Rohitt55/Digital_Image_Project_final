package com.pixellab.dip;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.os.Bundle;
import android.net.Uri;
import android.util.Base64;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Spinner;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.lang.reflect.Field;

/** Included only with build_apk.py --device-test, never in the delivered APK. */
public final class SmokeInstrumentation extends Instrumentation {
    private int checks;

    @Override public void onCreate(Bundle arguments) {
        super.onCreate(arguments);
        start();
    }

    private void check(boolean value, String message) {
        if (!value) throw new AssertionError(message);
        checks++;
    }

    private Bitmap decode(String data) {
        byte[] bytes = Base64.decode(data.substring(data.indexOf(',') + 1), Base64.DEFAULT);
        return BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
    }

    @Override public void onStart() {
        Bundle output = new Bundle();
        try {
            android.content.pm.PackageInfo info = getTargetContext().getPackageManager().getPackageInfo(
                "com.pixellab.dip", android.content.pm.PackageManager.GET_PERMISSIONS);
            if (info.requestedPermissions != null) for (String permission : info.requestedPermissions)
                check(!"android.permission.INTERNET".equals(permission), "No Internet permission");
            check(android.provider.Settings.Global.getInt(getTargetContext().getContentResolver(), "wifi_on", 0) == 0,
                "Emulator Wi-Fi is disabled");
            OfflineClient client = new OfflineClient(getTargetContext());
            check("ok".equals(new JSONObject(client.get("/api/health")).getString("status")), "Offline engine health");
            JSONArray catalog = new JSONArray(client.get("/api/operations?include_code=false"));
            JSONArray chapters = new JSONArray(client.get("/api/chapters"));
            check(chapters.length() == 8, "All eight course chapters are bundled");
            for (int i = 0; i < catalog.length(); i++) {
                JSONArray memberships = catalog.getJSONObject(i).getJSONArray("chapters");
                check(memberships.length() > 0, "Chapter membership: " + catalog.getJSONObject(i).getString("id"));
            }
            check(catalog.length() >= 59, "Operation catalog");
            check(!catalog.getJSONObject(0).has("code"), "Compact catalog");
            check(new JSONObject(client.get("/api/health")).getBoolean("offline"), "Engine is local");
            byte[] sample = Base64.decode(new JSONObject(client.get("/api/demo")).getString("image").split(",", 2)[1], Base64.DEFAULT);
            for (int i = 0; i < catalog.length(); i++) {
                String id = catalog.getJSONObject(i).getString("id");
                JSONObject result = new JSONObject(client.process(id, new JSONObject(), sample, "sample.png", sample, "reference.png"));
                check(decode(result.getString("result")) != null, "Offline operation: " + id);
                check(result.getJSONObject("lab").has("console"), "Lab output: " + id);
                check(new JSONObject(client.get("/api/operations/" + id)).getString("code").length() > 20, "Bundled code: " + id);
            }
            Bitmap input = Bitmap.createBitmap(8, 8, Bitmap.Config.ARGB_8888);
            input.eraseColor(Color.RED);
            ByteArrayOutputStream buffer = new ByteArrayOutputStream();
            input.compress(Bitmap.CompressFormat.PNG, 100, buffer);
            byte[] png = buffer.toByteArray();
            JSONObject negative = new JSONObject(client.process("negative", new JSONObject(), png, "sample.png", null, null));
            check(negative.isNull("original"), "Mobile responses omit duplicate original image");
            Bitmap inverted = decode(negative.getString("result"));
            check((inverted.getPixel(0, 0) & 255) == 179, "Known red-to-gray negative pixel");
            JSONObject resizeParams = new JSONObject().put("width", 17).put("height", 11);
            JSONObject resized = new JSONObject(client.process("resize", resizeParams, png, "sample.png", null, null));
            Bitmap resizedImage = decode(resized.getString("result"));
            check(resizedImage.getWidth() == 17 && resizedImage.getHeight() == 11, "Selected resize dimensions");
            check(resized.getJSONObject("lab").getJSONArray("panels").length() == 6, "PDF comparison figure");
            JSONObject fixed = new JSONObject(client.process("lab_normalized_equalization", new JSONObject(), png, "sample.png", null, null));
            JSONArray rows = fixed.getJSONObject("lab").getJSONArray("tables").getJSONObject(0).getJSONArray("rows");
            boolean correctMapping = false;
            for (int i = 0; i < rows.length(); i++) {
                JSONArray row = rows.getJSONArray(i);
                if (row.getInt(0) == 55) correctMapping = row.getInt(4) == 12;
            }
            check(correctMapping, "PDF mapping table");
            JSONObject copy = new JSONObject(client.process("image_read_save", new JSONObject(), png, "sample.png", null, null));
            Bitmap saved = decode(copy.getJSONObject("artifact").getString("data"));
            check(saved.getPixel(0, 0) == Color.RED, "PNG save artifact preserves pixels");
            boolean rejected = false;
            try { client.process("gamma", new JSONObject().put("gamma", 0), png, "sample.png", null, null); }
            catch (IOException e) { rejected = e.getMessage().contains("Gamma"); }
            check(rejected, "Local validation error is shown as a message");

            Intent intent = new Intent(getTargetContext(), MainActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            MainActivity activity = (MainActivity) startActivitySync(intent);
            await(activity, "workspaceReady");
            check(true, "Native offline startup loads catalog");
            runOnMainSync(() -> findButton(activity.getWindow().getDecorView(), "☰").performClick());
            waitForIdleSync();
            check((boolean) field(activity, "drawerOpen"), "Menu opens the sidebar");
            runOnMainSync(activity::onBackPressed);
            check(!(boolean) field(activity, "drawerOpen") && !activity.isFinishing(), "Back closes sidebar without leaving app");
            runOnMainSync(() -> findButton(activity.getWindow().getDecorView(), "Browse operations  →").performClick());
            waitForIdleSync();
            check((boolean) field(activity, "drawerOpen"), "Experiment card also opens sidebar");
            for (int chapter = 1; chapter <= 8; chapter++) {
                final int position = chapter;
                runOnMainSync(() -> {
                    try { ((Spinner) field(activity, "chapterPicker")).setSelection(position); }
                    catch (Exception e) { throw new RuntimeException(e); }
                });
                waitForIdleSync();
                int expected = 0;
                for (int i = 0; i < catalog.length(); i++) {
                    JSONArray memberships = catalog.getJSONObject(i).getJSONArray("chapters");
                    for (int j = 0; j < memberships.length(); j++) if (memberships.getInt(j) == chapter) { expected++; break; }
                }
                check(((java.util.List<?>) field(activity, "visibleOperations")).size() == expected && expected > 0,
                    "Chapter " + chapter + " filters the visible operations");
            }
            runOnMainSync(() -> findButton(activity.getWindow().getDecorView(), "Clear filters").performClick());
            waitForIdleSync();
            check(((java.util.List<?>) field(activity, "visibleOperations")).size() == catalog.length(), "Clear restores all operations");
            runOnMainSync(() -> {
                try { ((android.widget.ListView) field(activity, "operationList")).performItemClick(null, 1, 1); }
                catch (Exception e) { throw new RuntimeException(e); }
            });
            waitForIdleSync();
            check(!(boolean) field(activity, "drawerOpen"), "Selecting an operation closes sidebar");
            check(((TextView) field(activity, "selectedTitle")).getText().toString().equals(catalog.getJSONObject(1).getString("name")),
                "Selected sidebar operation appears in main workspace");
            runOnMainSync(() -> findButton(activity.getWindow().getDecorView(), "Use sample image").performClick());
            awaitImage(activity);
            File picked = new File(getTargetContext().getCacheDir(), "picked-test.png");
            try (FileOutputStream stream = new FileOutputStream(picked)) { stream.write(png); }
            runOnMainSync(() -> activity.onActivityResult(11, Activity.RESULT_OK, new Intent().setData(Uri.fromFile(picked))));
            awaitImage(activity);
            check(true, "Selected-photo callback reads image bytes");
            runOnMainSync(() -> findButton(activity.getWindow().getDecorView(), "☰").performClick());
            runOnMainSync(() -> {
                try {
                    ((Spinner) field(activity, "chapterPicker")).setSelection(2);
                    ((EditText) field(activity, "search")).setText("no such experiment 987");
                } catch (Exception e) { throw new RuntimeException(e); }
            });
            waitForIdleSync();
            check(((java.util.List<?>) field(activity, "visibleOperations")).isEmpty(), "Empty chapter/search intersection");
            check(!((Button) field(activity, "runButton")).isEnabled(), "Cannot run without a matching operation");
            runOnMainSync(() -> findButton(activity.getWindow().getDecorView(), "Clear filters").performClick());
            waitForIdleSync();
            check(field(activity, "imageBytes") != null, "Changing or clearing filters preserves the chosen image");
            runOnMainSync(() -> {
                try {
                    ((Spinner) field(activity, "chapterPicker")).setSelection(2);
                    ((EditText) field(activity, "search")).setText("8x8 normalized");
                }
                catch (Exception e) { throw new RuntimeException(e); }
            });
            waitForIdleSync();
            check(((java.util.List<?>) field(activity, "visibleOperations")).size() == 1, "Chapter and search combine");
            final byte[] chosenImage = (byte[]) field(activity, "imageBytes");
            runOnMainSync(() -> {
                try { ((android.widget.ListView) field(activity, "operationList")).performItemClick(null, 0, 0); }
                catch (Exception e) { throw new RuntimeException(e); }
            });
            check(field(activity, "imageBytes") == chosenImage, "Sidebar selection preserves image bytes");
            runOnMainSync(() -> findButton(activity.getWindow().getDecorView(), "Run operation").performClick());
            awaitResult(activity);
            check(true, "Native UI renders processed image, figure and mapping table");
            File savedFile = new File(getTargetContext().getCacheDir(), "saved-test.png");
            runOnMainSync(() -> {
                try {
                    Field pending = MainActivity.class.getDeclaredField("pendingSave");
                    pending.setAccessible(true); pending.set(activity, png);
                    activity.onActivityResult(13, Activity.RESULT_OK, new Intent().setData(Uri.fromFile(savedFile)));
                } catch (Exception e) { throw new RuntimeException(e); }
            });
            long saveDeadline = System.currentTimeMillis() + 15000;
            while ((!savedFile.exists() || savedFile.length() != png.length) && System.currentTimeMillis() < saveDeadline) Thread.sleep(100);
            Bitmap savedFileBitmap = BitmapFactory.decodeFile(savedFile.getAbsolutePath());
            check(savedFileBitmap != null && savedFileBitmap.getPixel(0, 0) == Color.RED, "Native save callback preserves image bytes");
            Bitmap screenshot = getUiAutomation().takeScreenshot();
            if (screenshot != null) {
                File file = new File(getTargetContext().getExternalFilesDir(null), "smoke-result.png");
                try (FileOutputStream stream = new FileOutputStream(file)) { screenshot.compress(Bitmap.CompressFormat.PNG, 100, stream); }
                output.putString("screenshot", file.getAbsolutePath());
            }
            runOnMainSync(activity::finish);
            output.putString("stream", "PixelLab Android integration passed: " + checks + " checks.\n");
            finish(Activity.RESULT_OK, output);
        } catch (Throwable error) {
            output.putString("stream", "FAILED: " + error + "\n");
            finish(Activity.RESULT_CANCELED, output);
        }
    }

    private static Object field(MainActivity activity, String name) throws Exception {
        Field field = MainActivity.class.getDeclaredField(name);
        field.setAccessible(true);
        return field.get(activity);
    }

    private void await(MainActivity activity, String name) throws Exception {
        long deadline = System.currentTimeMillis() + 45000;
        while (System.currentTimeMillis() < deadline) {
            final boolean[] ready = {false};
            runOnMainSync(() -> { try { ready[0] = (boolean) field(activity, name); } catch (Exception ignored) { } });
            if (ready[0]) return;
            Thread.sleep(100);
        }
        throw new AssertionError("Timed out waiting for " + name);
    }

    private void awaitImage(MainActivity activity) throws Exception {
        long deadline = System.currentTimeMillis() + 45000;
        while (System.currentTimeMillis() < deadline) {
            final boolean[] ready = {false};
            runOnMainSync(() -> { try { ready[0] = field(activity, "imageBytes") != null && !(boolean) field(activity, "busy"); } catch (Exception ignored) { } });
            if (ready[0]) return;
            Thread.sleep(100);
        }
        throw new AssertionError("Timed out loading sample");
    }

    private void awaitResult(MainActivity activity) throws Exception {
        long deadline = System.currentTimeMillis() + 60000;
        while (System.currentTimeMillis() < deadline) {
            final boolean[] ready = {false};
            runOnMainSync(() -> ready[0] = findText(activity.getWindow().getDecorView(), "Intensity and equalization mapping"));
            if (ready[0]) return;
            Thread.sleep(100);
        }
        throw new AssertionError("Timed out rendering table");
    }

    private static Button findButton(View view, String label) {
        if (view instanceof Button && label.contentEquals(((Button) view).getText())) return (Button) view;
        if (view instanceof ViewGroup) {
            ViewGroup group = (ViewGroup) view;
            for (int i = 0; i < group.getChildCount(); i++) {
                Button found = findButton(group.getChildAt(i), label);
                if (found != null) return found;
            }
        }
        return null;
    }

    private static boolean findText(View view, String value) {
        if (view instanceof TextView && value.contentEquals(((TextView) view).getText())) return true;
        if (view instanceof ViewGroup) for (int i = 0; i < ((ViewGroup) view).getChildCount(); i++) {
            if (findText(((ViewGroup) view).getChildAt(i), value)) return true;
        }
        return false;
    }
}
