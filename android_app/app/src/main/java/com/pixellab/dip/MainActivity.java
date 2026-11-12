package com.pixellab.dip;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.ImageDecoder;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.RippleDrawable;
import android.content.res.ColorStateList;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.OpenableColumns;
import android.text.Editable;
import android.text.InputType;
import android.text.TextWatcher;
import android.util.Base64;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowInsets;
import android.view.inputmethod.InputMethodManager;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.HorizontalScrollView;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.ScrollView;
import android.widget.Spinner;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class MainActivity extends Activity {
    private static final int PICK_IMAGE = 11, PICK_REFERENCE = 12, SAVE_FILE = 13;
    private static final int NAVY = Color.rgb(20, 38, 61), GREEN = Color.rgb(8, 127, 120);
    private static final int MUTED = Color.rgb(103, 120, 140), PALE = Color.rgb(243, 247, 250);
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private final List<Button> buttons = new ArrayList<>();
    private final List<Button> resultButtons = new ArrayList<>();
    private final List<JSONObject> visibleOperations = new ArrayList<>();
    private final Map<String, View> fields = new LinkedHashMap<>();
    private LinearLayout content, parameters, resultArea;
    private TextView status, imageLabel, referenceLabel, operationInfo, filterCount, selectedTitle;
    private ImageView imagePreview, referencePreview;
    private ProgressBar progress;
    private EditText search;
    private Spinner chapterPicker;
    private ListView operationList;
    private FrameLayout root, drawerLayer;
    private LinearLayout mainFrame, drawerPanel;
    private Button menuButton;
    private boolean drawerOpen;
    private final List<Integer> chapterIds = new ArrayList<>();
    private int activeChapter = 0;
    private ScrollView mainScroll;
    private Button referenceButton, runButton, clearFilters;
    private JSONArray operations = new JSONArray(), chapters = new JSONArray();
    private JSONObject selected;
    private String imageName = "image.png", referenceName = "reference.png";
    private byte[] imageBytes, referenceBytes, pendingSave;
    private boolean busy = false, workspaceReady = false;
    private int generation = 0;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        if (Build.VERSION.SDK_INT >= 33) getOnBackInvokedDispatcher().registerOnBackInvokedCallback(
            android.window.OnBackInvokedDispatcher.PRIORITY_DEFAULT, () -> {
                if (drawerOpen) closeDrawer(); else finish();
            });
        startOffline();
    }

    private int dp(int value) { return Math.round(value * getResources().getDisplayMetrics().density); }

    private LinearLayout column() {
        LinearLayout view = new LinearLayout(this);
        view.setOrientation(LinearLayout.VERTICAL);
        return view;
    }

    private void shell(String title, String subtitle) {
        buttons.clear();
        resultButtons.clear();
        LinearLayout frame = column();
        mainFrame = frame;
        frame.setBackgroundColor(PALE);
        frame.setPadding(dp(16), dp(12), dp(16), dp(12));
        frame.setOnApplyWindowInsetsListener((view, insets) -> {
            int top, bottom, left, right;
            if (Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets bars = insets.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                top = bars.top; bottom = bars.bottom; left = bars.left; right = bars.right;
            } else {
                top = insets.getSystemWindowInsetTop(); bottom = insets.getSystemWindowInsetBottom();
                left = insets.getSystemWindowInsetLeft(); right = insets.getSystemWindowInsetRight();
            }
            view.setPadding(dp(16) + left, dp(10) + top, dp(16) + right, dp(10) + bottom);
            return insets;
        });
        LinearLayout toolbar = new LinearLayout(this);
        toolbar.setGravity(Gravity.CENTER_VERTICAL);
        menuButton = button(toolbar, "☰", false, v -> openDrawer());
        menuButton.setContentDescription("Open navigation");
        menuButton.setTextSize(22);
        menuButton.setLayoutParams(new LinearLayout.LayoutParams(dp(48), dp(48)));
        LinearLayout identity = column();
        identity.setPadding(dp(12), 0, 0, 0);
        TextView appName = text(identity, "PixelLab", 19, true);
        appName.setPadding(0, 0, 0, 0);
        TextView local = text(identity, "IMAGE PROCESSING · OFFLINE", 10, false);
        local.setPadding(0, dp(2), 0, 0);
        toolbar.addView(identity, new LinearLayout.LayoutParams(0, -2, 1));
        LinearLayout.LayoutParams toolbarSpace = new LinearLayout.LayoutParams(-1, dp(58));
        toolbarSpace.setMargins(0, 0, 0, dp(8));
        frame.addView(toolbar, toolbarSpace);
        ScrollView scroll = new ScrollView(this);
        mainScroll = scroll;
        scroll.setFillViewport(true);
        scroll.setVerticalScrollBarEnabled(false);
        content = column();
        content.setFocusableInTouchMode(true);
        content.requestFocus();
        content.setPadding(0, 0, 0, dp(20));
        scroll.addView(content);
        frame.addView(scroll, new LinearLayout.LayoutParams(-1, 0, 1));
        root = new FrameLayout(this);
        root.addView(frame, new FrameLayout.LayoutParams(-1, -1));
        setContentView(root);
        LinearLayout hero = column();
        hero.setPadding(dp(20), dp(18), dp(20), dp(20));
        GradientDrawable heroBackground = new GradientDrawable(GradientDrawable.Orientation.TL_BR,
            new int[]{NAVY, Color.rgb(29, 73, 87)});
        heroBackground.setCornerRadius(dp(22));
        hero.setBackground(heroBackground);
        content.addView(hero, new LinearLayout.LayoutParams(-1, -2));
        TextView badge = text(hero, "●  OFFLINE STUDIO", 11, true);
        badge.setTextColor(Color.rgb(133, 225, 204));
        TextView brand = text(hero, title, workspaceReady ? 23 : 30, true);
        brand.setTextColor(Color.WHITE);
        TextView caption = text(hero, subtitle, 13, false);
        caption.setTextColor(Color.rgb(210, 227, 235));
        progress = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progress.setIndeterminate(true);
        progress.setVisibility(View.GONE);
        content.addView(progress, new LinearLayout.LayoutParams(-1, dp(6)));
        status = text(content, "", 12, false);
        status.setPadding(dp(4), dp(12), dp(4), dp(2));
    }

    private TextView text(LinearLayout parent, String value, int size, boolean bold) {
        TextView view = new TextView(this);
        view.setText(value);
        view.setTextSize(size);
        view.setTextColor(bold ? NAVY : MUTED);
        view.setLineSpacing(dp(2), 1f);
        view.setPadding(0, dp(4), 0, dp(4));
        if (bold) view.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        parent.addView(view, new LinearLayout.LayoutParams(-1, -2));
        return view;
    }

    private LinearLayout card(String title) {
        LinearLayout card = column();
        GradientDrawable background = new GradientDrawable();
        background.setColor(Color.WHITE);
        background.setCornerRadius(dp(20));
        background.setStroke(dp(1), Color.rgb(228, 235, 240));
        card.setBackground(background);
        card.setPadding(dp(18), dp(16), dp(18), dp(18));
        card.setElevation(dp(1));
        LinearLayout.LayoutParams spacing = new LinearLayout.LayoutParams(-1, -2);
        spacing.setMargins(dp(1), dp(14), dp(1), dp(2));
        content.addView(card, spacing);
        text(card, title, 19, true);
        return card;
    }

    private Button button(LinearLayout parent, String label, boolean primary, View.OnClickListener action) {
        Button view = new Button(this);
        view.setText(label);
        view.setAllCaps(false);
        view.setTextColor(primary ? Color.WHITE : NAVY);
        view.setTextSize(15);
        view.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
        view.setMinHeight(dp(48));
        view.setMinimumHeight(dp(48));
        view.setPadding(dp(12), dp(8), dp(12), dp(8));
        view.setStateListAnimator(null);
        GradientDrawable background = new GradientDrawable();
        background.setColor(primary ? GREEN : Color.rgb(235, 245, 243));
        background.setCornerRadius(dp(12));
        view.setBackground(new RippleDrawable(ColorStateList.valueOf(Color.argb(35, 0, 70, 65)), background, null));
        LinearLayout.LayoutParams spacing = new LinearLayout.LayoutParams(-1, -2);
        spacing.setMargins(0, dp(10), 0, 0);
        parent.addView(view, spacing);
        view.setOnClickListener(action);
        buttons.add(view);
        if (parent == resultArea) resultButtons.add(view);
        return view;
    }

    private EditText edit(LinearLayout parent, String hint) {
        EditText field = new EditText(this);
        field.setSingleLine(true);
        field.setTextColor(NAVY);
        field.setTextSize(16);
        field.setHintTextColor(MUTED);
        field.setHint(hint);
        field.setPadding(dp(14), dp(8), dp(14), dp(8));
        GradientDrawable background = new GradientDrawable();
        background.setColor(PALE); background.setCornerRadius(dp(12));
        background.setStroke(dp(1), Color.rgb(222, 231, 237));
        field.setBackground(background);
        LinearLayout.LayoutParams spacing = new LinearLayout.LayoutParams(-1, dp(50));
        spacing.setMargins(0, dp(8), 0, dp(8));
        parent.addView(field, spacing);
        return field;
    }

    private ArrayAdapter<String> choices(List<String> values) {
        return new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, values) {
            private View label(int position, View recycled, boolean dropdown) {
                TextView text = recycled instanceof TextView ? (TextView) recycled : new TextView(MainActivity.this);
                text.setText(getItem(position)); text.setTextColor(NAVY); text.setTextSize(14);
                text.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
                text.setGravity(Gravity.CENTER_VERTICAL); text.setSingleLine(false);
                text.setMaxLines(3); text.setMinHeight(dp(52));
                text.setPadding(dp(12), dp(10), dp(12), dp(10));
                if (dropdown) text.setBackgroundColor(Color.WHITE);
                return text;
            }
            @Override public View getView(int position, View recycled, ViewGroup parent) { return label(position, recycled, false); }
            @Override public View getDropDownView(int position, View recycled, ViewGroup parent) { return label(position, recycled, true); }
        };
    }

    private Spinner spinner(LinearLayout parent, List<String> values) {
        Spinner view = new Spinner(this);
        view.setAdapter(choices(values));
        view.setBackgroundTintList(ColorStateList.valueOf(GREEN));
        LinearLayout container = column();
        GradientDrawable background = new GradientDrawable();
        background.setColor(PALE); background.setCornerRadius(dp(12));
        background.setStroke(dp(1), Color.rgb(222, 231, 237));
        container.setBackground(background);
        container.addView(view, new LinearLayout.LayoutParams(-1, -2));
        LinearLayout.LayoutParams spacing = new LinearLayout.LayoutParams(-1, -2);
        spacing.setMargins(0, dp(6), 0, dp(8));
        parent.addView(container, spacing);
        return view;
    }

    private void startOffline() {
        shell("PixelLab", "Fully offline image processing");
        setBusy(true, "Starting the image engine on your phone...");
        final int request = generation;
        worker.execute(() -> {
            try {
                OfflineClient client = new OfflineClient(getApplicationContext());
                JSONArray catalog = new JSONArray(client.get("/api/operations?include_code=false"));
                JSONArray course = new JSONArray(client.get("/api/chapters"));
                runOnUiThread(() -> {
                    if (request != generation) return;
                    operations = catalog;
                    chapters = course;
                    busy = false;
                    showWorkspace();
                });
            } catch (Exception e) { failure(request, e); }
        });
    }

    private void showWorkspace() {
        workspaceReady = true;
        shell("Explore. Experiment. Learn.", "Browse " + operations.length() + " operations across " + chapters.length() + " chapters from the ☰ menu.");
        LinearLayout experiment = card("CURRENT EXPERIMENT");
        selectedTitle = text(experiment, "Choose an operation", 21, true);
        operationInfo = text(experiment, "", 13, false);
        button(experiment, "Browse operations  →", false, v -> openDrawer());
        buildDrawer();

        LinearLayout input = card("01  Add your image");
        imageLabel = text(input, imageBytes == null ? "PNG, JPG, WebP or another supported image" : imageName, 13, false);
        imagePreview = preview(input);
        if (imageBytes != null) display(imagePreview, imageBytes);
        LinearLayout imageActions = new LinearLayout(this);
        imageActions.setOrientation(LinearLayout.HORIZONTAL);
        input.addView(imageActions, new LinearLayout.LayoutParams(-1, -2));
        Button choose = button(imageActions, "Choose photo", true, v -> pick(PICK_IMAGE));
        Button sample = button(imageActions, "Use sample image", false, v -> demo());
        LinearLayout.LayoutParams left = new LinearLayout.LayoutParams(0, -2, 1);
        left.setMargins(0, dp(10), dp(5), 0); choose.setLayoutParams(left);
        LinearLayout.LayoutParams right = new LinearLayout.LayoutParams(0, -2, 1);
        right.setMargins(dp(5), dp(10), 0, 0); sample.setLayoutParams(right);

        LinearLayout selection = card("02  Set up & run");
        text(selection, "Adjust the settings, then run your experiment.", 13, false);
        parameters = column();
        selection.addView(parameters);
        referenceLabel = text(selection, "A reference photo is required for this operation.", 13, false);
        referencePreview = preview(selection);
        referenceButton = button(selection, "Choose reference photo", false, v -> pick(PICK_REFERENCE));
        button(selection, "View Python example", false, v -> showCode());
        runButton = button(selection, "Run operation", true, v -> process());
        resultArea = card("03  Your results");
        text(resultArea, "Your next discovery starts here", 17, true);
        text(resultArea, "Run an experiment to see its image, relevant plots and measurements. Save what you need to your phone.", 13, false);
        TextView footer = text(content, "Made for learning. Ready wherever you are.", 11, false);
        footer.setGravity(Gravity.CENTER); footer.setPadding(0, dp(20), 0, dp(8));
        filter("");
        setBusy(false, "Everything runs on your phone. No connection needed.");
    }

    private void buildDrawer() {
        drawerLayer = new FrameLayout(this);
        drawerLayer.setVisibility(View.GONE);
        View scrim = new View(this);
        scrim.setBackgroundColor(Color.argb(115, 10, 24, 40));
        scrim.setContentDescription("Close navigation");
        scrim.setOnClickListener(v -> closeDrawer());
        drawerLayer.addView(scrim, new FrameLayout.LayoutParams(-1, -1));
        drawerPanel = column();
        drawerPanel.setFocusableInTouchMode(true);
        drawerPanel.setBackgroundColor(Color.WHITE);
        drawerPanel.setElevation(dp(16));
        drawerPanel.setPadding(dp(16), dp(24), dp(16), dp(16));
        drawerPanel.setOnApplyWindowInsetsListener((view, insets) -> {
            int top = insets.getSystemWindowInsetTop(), bottom = insets.getSystemWindowInsetBottom();
            if (Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets bars = insets.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                top = bars.top; bottom = bars.bottom;
            }
            view.setPadding(dp(16), dp(16) + top, dp(16), dp(12) + bottom);
            return insets;
        });
        // Consume taps inside the panel rather than dismissing through the scrim.
        drawerPanel.setOnClickListener(v -> { });
        int width = Math.min(dp(340), getResources().getDisplayMetrics().widthPixels - dp(32));
        FrameLayout.LayoutParams panelBounds = new FrameLayout.LayoutParams(width, -1, Gravity.START);
        drawerLayer.addView(drawerPanel, panelBounds);
        root.addView(drawerLayer, new FrameLayout.LayoutParams(-1, -1));
        ScrollView filtersScroll = new ScrollView(this) {
            @Override protected void onMeasure(int widthSpec, int heightSpec) {
                int available = View.MeasureSpec.getSize(heightSpec);
                if (available == 0) available = getResources().getDisplayMetrics().heightPixels;
                int maximum = Math.max(dp(100), (int) (available * 0.60f));
                super.onMeasure(widthSpec, View.MeasureSpec.makeMeasureSpec(maximum, View.MeasureSpec.AT_MOST));
            }
        };
        filtersScroll.setVerticalScrollBarEnabled(false);
        LinearLayout browse = column();
        filtersScroll.addView(browse);
        drawerPanel.addView(filtersScroll, new LinearLayout.LayoutParams(-1, -2));
        LinearLayout drawerHeading = new LinearLayout(this);
        drawerHeading.setGravity(Gravity.CENTER_VERTICAL);
        TextView heading = text(drawerHeading, "Explore PixelLab", 21, true);
        heading.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1));
        Button close = button(drawerHeading, "×", false, v -> closeDrawer());
        close.setTextSize(26); close.setContentDescription("Close sidebar");
        close.setLayoutParams(new LinearLayout.LayoutParams(dp(48), dp(48)));
        browse.addView(drawerHeading);
        text(browse, chapters.length() + " chapters · " + operations.length() + " operations · Fully offline", 11, false);
        text(browse, "CHAPTER", 11, true);
        chapterIds.clear(); chapterIds.add(0);
        List<String> chapterNames = new ArrayList<>();
        chapterNames.add("All chapters");
        for (int i = 0; i < chapters.length(); i++) {
            JSONObject chapter = chapters.optJSONObject(i);
            if (chapter == null) continue;
            chapterIds.add(chapter.optInt("id"));
            chapterNames.add(chapter.optInt("id") + " · " + chapter.optString("title"));
        }
        chapterPicker = spinner(browse, chapterNames);
        search = edit(browse, "Search operations…");
        search.setImeOptions(android.view.inputmethod.EditorInfo.IME_ACTION_SEARCH);
        search.setOnEditorActionListener((view, action, event) -> {
            if (action != android.view.inputmethod.EditorInfo.IME_ACTION_SEARCH) return false;
            InputMethodManager keyboard = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);
            if (keyboard != null) keyboard.hideSoftInputFromWindow(search.getWindowToken(), 0);
            search.clearFocus();
            return true;
        });
        filterCount = text(browse, "", 12, false);
        clearFilters = button(browse, "Clear filters", false, v -> {
            activeChapter = 0;
            chapterPicker.setSelection(0);
            search.setText("");
            filter("");
        });
        clearFilters.setVisibility(View.GONE);
        operationList = new ListView(this);
        operationList.setDivider(null);
        operationList.setDividerHeight(dp(5));
        operationList.setVerticalScrollBarEnabled(false);
        operationList.setClipToPadding(false);
        operationList.setPadding(0, dp(8), 0, dp(8));
        operationList.setContentDescription("Image processing operations");
        drawerPanel.addView(operationList, new LinearLayout.LayoutParams(-1, 0, 1));
        TextView empty = text(drawerPanel, "No operations found. Try a different search or clear your filters.", 14, false);
        empty.setPadding(dp(12), dp(24), dp(12), dp(24));
        operationList.setEmptyView(empty);
        operationList.setOnItemClickListener((parent, view, position, id) -> {
            if (busy || position >= visibleOperations.size()) return;
            selected = visibleOperations.get(position);
            renderParameters();
            ((ArrayAdapter<?>) operationList.getAdapter()).notifyDataSetChanged();
            closeDrawer();
            mainScroll.smoothScrollTo(0, 0);
        });
        search.addTextChangedListener(new TextWatcher() {
            @Override public void beforeTextChanged(CharSequence s, int start, int count, int after) { }
            @Override public void onTextChanged(CharSequence s, int start, int before, int count) { filter(s.toString()); }
            @Override public void afterTextChanged(Editable s) { }
        });
        chapterPicker.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                if (position < chapterIds.size()) {
                    activeChapter = chapterIds.get(position);
                    filter(search.getText().toString());
                }
            }
            @Override public void onNothingSelected(AdapterView<?> parent) { }
        });
    }

    private void openDrawer() {
        if (!workspaceReady || busy || drawerLayer == null) return;
        drawerOpen = true;
        drawerLayer.setVisibility(View.VISIBLE);
        drawerLayer.requestApplyInsets();
        mainFrame.setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_NO_HIDE_DESCENDANTS);
        drawerPanel.setTranslationX(-drawerPanel.getLayoutParams().width);
        drawerPanel.animate().translationX(0).setDuration(180).start();
        drawerPanel.requestFocus();
    }

    private void closeDrawer() {
        if (drawerLayer == null) return;
        drawerOpen = false;
        drawerPanel.animate().cancel();
        drawerLayer.setVisibility(View.GONE);
        mainFrame.setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_AUTO);
        InputMethodManager keyboard = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);
        if (keyboard != null) keyboard.hideSoftInputFromWindow(search.getWindowToken(), 0);
        search.clearFocus();
        menuButton.requestFocus();
    }

    @Override public void onBackPressed() {
        if (drawerOpen) closeDrawer(); else super.onBackPressed();
    }

    private ArrayAdapter<String> operationRows(List<String> names) {
        return new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, names) {
            @Override public View getView(int position, View recycled, ViewGroup parent) {
                TextView row = recycled instanceof TextView ? (TextView) recycled : new TextView(MainActivity.this);
                JSONObject operation = visibleOperations.get(position);
                String name = operation.optString("name"), group = operation.optString("group");
                android.text.SpannableString label = new android.text.SpannableString(name + "\n" + group);
                label.setSpan(new android.text.style.RelativeSizeSpan(0.8f), name.length() + 1, label.length(), 0);
                label.setSpan(new android.text.style.ForegroundColorSpan(MUTED), name.length() + 1, label.length(), 0);
                row.setText(label); row.setTextSize(14); row.setMaxLines(4);
                row.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
                row.setPadding(dp(12), dp(12), dp(12), dp(12)); row.setMinHeight(dp(64));
                boolean current = selected != null && selected.optString("id").equals(operation.optString("id"));
                row.setTextColor(current ? GREEN : NAVY);
                GradientDrawable background = new GradientDrawable();
                background.setColor(current ? Color.rgb(227, 244, 240) : Color.WHITE);
                background.setCornerRadius(dp(12));
                row.setBackground(new RippleDrawable(ColorStateList.valueOf(Color.argb(25, 0, 100, 90)), background, null));
                row.setContentDescription(name + ", " + group + (current ? ", selected" : ""));
                return row;
            }
        };
    }

    private void filter(String query) {
        String keep = selected == null ? "" : selected.optString("id");
        visibleOperations.clear();
        List<String> names = new ArrayList<>();
        int choice = 0;
        String needle = query.toLowerCase(Locale.ROOT).trim();
        for (int i = 0; i < operations.length(); i++) {
            JSONObject item = operations.optJSONObject(i);
            if (item == null) continue;
            String label = item.optString("name");
            String haystack = (label + " " + item.optString("group") + " " + item.optString("explanation")).toLowerCase(Locale.ROOT);
            JSONArray memberships = item.optJSONArray("chapters");
            boolean inChapter = activeChapter == 0;
            if (memberships != null) for (int j = 0; j < memberships.length(); j++)
                if (memberships.optInt(j) == activeChapter) inChapter = true;
            if (inChapter && haystack.contains(needle)) {
                if (keep.equals(item.optString("id"))) choice = visibleOperations.size();
                visibleOperations.add(item);
                names.add(label);
            }
        }
        operationList.setAdapter(operationRows(names));
        filterCount.setText(names.size() + (names.size() == 1 ? " operation" : " operations") +
            (activeChapter == 0 ? " · All chapters" : " · Chapter " + activeChapter));
        clearFilters.setVisibility(activeChapter != 0 || !needle.isEmpty() ? View.VISIBLE : View.GONE);
        if (names.isEmpty()) {
            selected = null;
            selectedTitle.setText("Choose an operation from the menu");
            parameters.removeAllViews();
            fields.clear();
            operationInfo.setText("No experiments found. Try another name, chapter, or clear your filters.");
            updateControls();
        } else {
            selected = visibleOperations.get(choice);
            renderParameters();
        }
    }

    private void renderParameters() {
        parameters.removeAllViews();
        fields.clear();
        if (selected == null) return;
        selectedTitle.setText(selected.optString("name"));
        operationInfo.setText(selected.optString("group") + "\n" + selected.optString("explanation"));
        JSONArray specs = selected.optJSONArray("fields");
        if (specs != null) for (int i = 0; i < specs.length(); i++) {
            JSONObject spec = specs.optJSONObject(i);
            if (spec == null) continue;
            String label = spec.optString("label"), key = spec.optString("key");
            text(parameters, label, 13, true);
            if ("select".equals(spec.optString("type"))) {
                JSONArray options = spec.optJSONArray("options");
                List<String> values = new ArrayList<>();
                int initial = 0;
                if (options != null) for (int j = 0; j < options.length(); j++) {
                    values.add(options.optString(j));
                    if (options.optString(j).equals(spec.optString("default"))) initial = j;
                }
                Spinner picker = spinner(parameters, values);
                picker.setSelection(initial);
                fields.put(key, picker);
            } else {
                EditText value = edit(parameters, label);
                if ("number".equals(spec.optString("type"))) {
                    value.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_FLAG_DECIMAL | InputType.TYPE_NUMBER_FLAG_SIGNED);
                    text(parameters, "Range: " + spec.optString("min") + " to " + spec.optString("max") + " · Step: " + spec.optString("step"), 12, false);
                }
                value.setText(spec.optString("default"));
                fields.put(key, value);
            }
        }
        updateControls();
    }

    private boolean needsReference() {
        return selected != null && (selected.optBoolean("requires_reference") || "matching".equals(selected.optString("id")));
    }

    private void updateControls() {
        if (!workspaceReady || runButton == null) return;
        boolean needs = needsReference();
        referenceButton.setVisibility(needs ? View.VISIBLE : View.GONE);
        referenceLabel.setVisibility(needs ? View.VISIBLE : View.GONE);
        referencePreview.setVisibility(needs && referenceBytes != null ? View.VISIBLE : View.GONE);
        if (referenceBytes != null) {
            referenceLabel.setText(referenceName);
            if (needs) display(referencePreview, referenceBytes);
        }
        runButton.setEnabled(!busy && selected != null && imageBytes != null && (!needs || referenceBytes != null));
        operationList.setEnabled(!busy && !visibleOperations.isEmpty());
        menuButton.setEnabled(!busy);
        chapterPicker.setEnabled(!busy);
        search.setEnabled(!busy);
        runButton.setAlpha(runButton.isEnabled() ? 1f : 0.45f);
        for (View field : fields.values()) field.setEnabled(!busy);
    }

    private JSONObject parameters() throws JSONException, IllegalArgumentException {
        JSONObject values = new JSONObject();
        JSONArray specs = selected.optJSONArray("fields");
        if (specs == null) return values;
        for (int i = 0; i < specs.length(); i++) {
            JSONObject spec = specs.getJSONObject(i);
            String key = spec.getString("key");
            View field = fields.get(key);
            if (field instanceof Spinner) {
                Object value = ((Spinner) field).getSelectedItem();
                if (value == null) throw new IllegalArgumentException("Choose " + spec.optString("label"));
                values.put(key, value.toString());
            } else {
                String input = ((EditText) field).getText().toString().trim();
                if ("number".equals(spec.optString("type"))) {
                    double number;
                    try { number = Double.parseDouble(input); }
                    catch (NumberFormatException e) { throw new IllegalArgumentException(spec.optString("label") + " must be a number."); }
                    if (Double.isNaN(number) || Double.isInfinite(number) || number < spec.getDouble("min") || number > spec.getDouble("max"))
                        throw new IllegalArgumentException("Check the range for " + spec.optString("label"));
                    if (spec.optDouble("step", 1) == 1 && number != Math.rint(number))
                        throw new IllegalArgumentException(spec.optString("label") + " must be a whole number.");
                    values.put(key, number);
                } else values.put(key, input);
            }
        }
        return values;
    }

    private void pick(int request) {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("image/*");
        startActivityForResult(intent, request);
    }

    @Override protected void onActivityResult(int request, int resultCode, Intent data) {
        super.onActivityResult(request, resultCode, data);
        if (resultCode != RESULT_OK || data == null || data.getData() == null) return;
        Uri uri = data.getData();
        final int current = generation;
        if (request == SAVE_FILE) {
            final byte[] bytes = pendingSave;
            pendingSave = null;
            if (bytes == null) return;
            setBusy(true, "Saving file…");
            worker.execute(() -> {
                try (OutputStream stream = getContentResolver().openOutputStream(uri)) {
                    if (stream == null) throw new IOException("Could not open the selected location.");
                    stream.write(bytes);
                    runOnUiThread(() -> { if (current == generation) setBusy(false, "File saved."); });
                } catch (Exception e) { failure(current, e); }
            });
            return;
        }
        if (request != PICK_IMAGE && request != PICK_REFERENCE) return;
        setBusy(true, "Reading selected image…");
        worker.execute(() -> {
            try {
                byte[] bytes = OfflineClient.readLimited(getContentResolver().openInputStream(uri), 23 * 1024 * 1024);
                BitmapFactory.Options bounds = new BitmapFactory.Options();
                bounds.inJustDecodeBounds = true;
                BitmapFactory.decodeByteArray(bytes, 0, bytes.length, bounds);
                if ((long) bounds.outWidth * bounds.outHeight > 12000000L)
                    throw new IOException("Choose an image with at most 12 million pixels.");
                String name = filename(uri);
                runOnUiThread(() -> {
                    if (current != generation) return;
                    if (request == PICK_IMAGE) {
                        imageBytes = bytes; imageName = name;
                        imageLabel.setText(name); display(imagePreview, bytes);
                        clearResults();
                    } else {
                        referenceBytes = bytes; referenceName = name;
                    }
                    setBusy(false, "Image ready.");
                });
            } catch (Exception e) { failure(current, e); }
        });
    }

    private String filename(Uri uri) {
        try (Cursor cursor = getContentResolver().query(uri, new String[]{OpenableColumns.DISPLAY_NAME}, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) return cursor.getString(0);
        } catch (Exception ignored) { }
        return "image.png";
    }

    private void demo() {
        final int current = generation;
        setBusy(true, "Loading sample image…");
        worker.execute(() -> {
            try {
                JSONObject response = new JSONObject(new OfflineClient(getApplicationContext()).get("/api/demo"));
                byte[] bytes = dataBytes(response.getString("image"));
                runOnUiThread(() -> {
                    if (current != generation) return;
                    imageBytes = bytes; imageName = "sample.png";
                    imageLabel.setText("Sample image"); display(imagePreview, bytes);
                    clearResults();
                    setBusy(false, "Sample image ready.");
                });
            } catch (Exception e) { failure(current, e); }
        });
    }

    private void process() {
        if (selected == null || imageBytes == null) return;
        final JSONObject values;
        try { values = parameters(); }
        catch (Exception e) { error(e.getMessage()); return; }
        View focused = getCurrentFocus();
        if (focused != null) {
            InputMethodManager keyboard = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);
            keyboard.hideSoftInputFromWindow(focused.getWindowToken(), 0);
            focused.clearFocus();
        }
        content.requestFocus();
        final String operation = selected.optString("id");
        final byte[] input = imageBytes, reference = needsReference() ? referenceBytes : null;
        if ((long) input.length + (reference == null ? 0 : reference.length) > 23 * 1024 * 1024L) {
            error("Choose smaller images. The combined upload limit is 23 MB in the app."); return;
        }
        final int current = generation;
        setBusy(true, "Processing " + selected.optString("name") + "…");
        worker.execute(() -> {
            try {
                JSONObject response = new JSONObject(new OfflineClient(getApplicationContext()).process(operation, values, input, imageName, reference, referenceName));
                runOnUiThread(() -> {
                    if (current != generation) return;
                    try {
                        renderResult(response, operation);
                        setBusy(false, "Complete. Tap a figure to zoom or save your result.");
                    } catch (Exception e) { setBusy(false, ""); error(e.getMessage()); }
                });
            } catch (Exception e) { failure(current, e); }
        });
    }

    private void clearResults() {
        if (resultArea != null) {
            buttons.removeAll(resultButtons);
            resultButtons.clear();
            resultArea.removeAllViews();
            text(resultArea, "03  Your results", 19, true);
            text(resultArea, "Run an operation to see its output here.", 14, false);
        }
    }

    private void renderResult(JSONObject data, String operation) throws JSONException {
        buttons.removeAll(resultButtons);
        resultButtons.clear();
        resultArea.removeAllViews();
        text(resultArea, data.optString("operation", "Result"), 21, true);
        String resultUri = data.getString("result");
        byte[] output = dataBytes(resultUri);
        JSONObject after = data.getJSONObject("after");
        text(resultArea, after.optInt("width") + " × " + after.optInt("height") + " pixels", 13, false);
        ImageView outputView = preview(resultArea); display(outputView, output);
        outputView.setOnClickListener(v -> zoom(output, data.optString("operation")));
        String mime = resultUri.startsWith("data:image/jpeg") ? "image/jpeg" : "image/png";
        button(resultArea, "Save processed image", true, v -> save(output, mime, "PixelLab-" + operation + (mime.equals("image/jpeg") ? ".jpg" : ".png")));
        button(resultArea, "Use result as next input", false, v -> {
            imageBytes = output; imageName = "processed.png";
            imageLabel.setText("Processed result used as input"); display(imagePreview, output);
            setBusy(false, "Result is ready as your next input.");
        });
        JSONObject lab = data.optJSONObject("lab");
        if (lab != null && lab.has("figure")) {
            text(resultArea, "Lab output", 20, true);
            text(resultArea, lab.optString("caption"), 13, false);
            byte[] figure = dataBytes(lab.getString("figure"));
            ImageView plot = preview(resultArea); display(plot, figure);
            plot.setOnClickListener(v -> zoom(figure, "Lab output"));
            text(resultArea, "Tap the figure to pinch-zoom and inspect pixel values.", 12, false);
            button(resultArea, "Save lab figure", false, v -> save(figure, "image/png", "PixelLab-" + operation + "-figure.png"));
            renderTables(lab.optJSONArray("tables"));
            TextView console = text(resultArea, lab.optString("console"), 12, false);
            console.setTypeface(Typeface.MONOSPACE);
            console.setTextIsSelectable(true);
            console.setPadding(dp(12), dp(12), dp(12), dp(12));
            console.setTextColor(Color.rgb(230, 238, 247));
            console.setBackgroundColor(NAVY);
        }
        JSONObject artifact = data.optJSONObject("artifact");
        if (artifact != null && artifact.has("data")) {
            byte[] bytes = dataBytes(artifact.getString("data"));
            button(resultArea, "Save " + artifact.optString("name", "encoded file"), false,
                   v -> save(bytes, artifact.optString("mime", "application/octet-stream"), artifact.optString("name", "PixelLab-file")));
        }
        resultArea.post(() -> mainScroll.smoothScrollTo(0, resultArea.getTop()));
    }

    private void renderTables(JSONArray tables) throws JSONException {
        if (tables == null) return;
        for (int i = 0; i < tables.length(); i++) {
            JSONObject table = tables.getJSONObject(i);
            text(resultArea, table.optString("title"), 17, true);
            HorizontalScrollView scroll = new HorizontalScrollView(this);
            TableLayout grid = new TableLayout(this);
            JSONArray columns = table.getJSONArray("columns");
            grid.addView(tableRow(columns, true));
            JSONArray rows = table.getJSONArray("rows");
            for (int row = 0; row < rows.length(); row++) grid.addView(tableRow(rows.getJSONArray(row), false));
            scroll.addView(grid);
            resultArea.addView(scroll, new LinearLayout.LayoutParams(-1, -2));
        }
    }

    private TableRow tableRow(JSONArray values, boolean header) {
        TableRow row = new TableRow(this);
        row.setBackgroundColor(header ? Color.rgb(224, 234, 243) : Color.rgb(246, 248, 250));
        for (int i = 0; i < values.length(); i++) {
            TextView cell = new TextView(this);
            cell.setText(values.optString(i));
            cell.setTextColor(NAVY);
            cell.setTextSize(12);
            cell.setPadding(dp(10), dp(9), dp(10), dp(9));
            cell.setMinWidth(dp(90));
            cell.setGravity(Gravity.CENTER);
            if (header) cell.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
            row.addView(cell);
        }
        return row;
    }

    private ImageView preview(LinearLayout parent) {
        ImageView view = new ImageView(this);
        view.setAdjustViewBounds(true);
        view.setScaleType(ImageView.ScaleType.FIT_CENTER);
        view.setMaxHeight(dp(360));
        view.setPadding(0, dp(12), 0, dp(8));
        view.setVisibility(View.GONE);
        parent.addView(view, new LinearLayout.LayoutParams(-1, -2));
        return view;
    }

    private void display(ImageView view, byte[] bytes) {
        Bitmap bitmap = decodePreview(bytes);
        view.setImageBitmap(bitmap);
        if (bitmap != null && Math.max(bitmap.getWidth(), bitmap.getHeight()) <= 32 && view.getDrawable() instanceof BitmapDrawable)
            ((BitmapDrawable) view.getDrawable()).setFilterBitmap(false);
        view.setVisibility(bitmap == null ? View.GONE : View.VISIBLE);
    }

    static Bitmap decodePreview(byte[] bytes) {
        // ImageDecoder applies camera EXIF orientation on modern Android versions.
        if (Build.VERSION.SDK_INT >= 28) {
            try {
                return ImageDecoder.decodeBitmap(ImageDecoder.createSource(ByteBuffer.wrap(bytes)), (decoder, info, source) -> {
                    int side = Math.max(info.getSize().getWidth(), info.getSize().getHeight());
                    int sample = 1;
                    while (side / sample > 1600) sample *= 2;
                    decoder.setTargetSampleSize(sample);
                });
            } catch (IOException ignored) { }
        }
        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inJustDecodeBounds = true;
        BitmapFactory.decodeByteArray(bytes, 0, bytes.length, options);
        options.inSampleSize = 1;
        while (options.outWidth / options.inSampleSize > 1600 || options.outHeight / options.inSampleSize > 1600) options.inSampleSize *= 2;
        options.inJustDecodeBounds = false;
        return BitmapFactory.decodeByteArray(bytes, 0, bytes.length, options);
    }

    private static byte[] dataBytes(String uri) {
        int comma = uri.indexOf(',');
        if (!uri.startsWith("data:") || comma < 0) throw new IllegalArgumentException("The image engine returned an invalid image or file.");
        return Base64.decode(uri.substring(comma + 1), Base64.DEFAULT);
    }

    private void zoom(byte[] bytes, String title) {
        final int current = generation;
        worker.execute(() -> {
            try {
                File file = new File(getCacheDir(), "viewer-image.png");
                try (FileOutputStream output = new FileOutputStream(file)) { output.write(bytes); }
                runOnUiThread(() -> {
                    if (current != generation) return;
                    Intent intent = new Intent(this, ImageViewerActivity.class);
                    intent.putExtra("file", file.getAbsolutePath()); intent.putExtra("title", title);
                    startActivity(intent);
                });
            } catch (Exception e) { failure(current, e); }
        });
    }

    private void save(byte[] bytes, String mime, String name) {
        pendingSave = bytes;
        Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType(mime);
        intent.putExtra(Intent.EXTRA_TITLE, name.replaceAll("[^a-zA-Z0-9._-]", "_"));
        startActivityForResult(intent, SAVE_FILE);
    }

    private void showCode() {
        if (selected == null) return;
        final String operation = selected.optString("id");
        final int current = generation;
        setBusy(true, "Loading Python example…");
        worker.execute(() -> {
            try {
                JSONObject response = new JSONObject(new OfflineClient(getApplicationContext()).get("/api/operations/" + operation));
                String code = response.getString("code");
                runOnUiThread(() -> {
                    if (current != generation) return;
                    setBusy(false, "Python example loaded.");
                    TextView text = new TextView(this);
                    text.setText(code); text.setTextIsSelectable(true); text.setTypeface(Typeface.MONOSPACE); text.setTextSize(12);
                    text.setPadding(dp(14), dp(14), dp(14), dp(14));
                    ScrollView scroll = new ScrollView(this); scroll.addView(text);
                    new AlertDialog.Builder(this).setTitle("Python example").setView(scroll).setPositiveButton("Close", null).show();
                });
            } catch (Exception e) { failure(current, e); }
        });
    }

    private void setBusy(boolean value, String message) {
        busy = value;
        progress.setVisibility(value ? View.VISIBLE : View.GONE);
        status.setText(message);
        status.setTextColor(MUTED);
        for (Button button : buttons) {
            button.setEnabled(!value);
            button.setAlpha(value ? 0.45f : 1f);
        }
        menuButton.setEnabled(!value && workspaceReady);
        updateControls();
    }

    private void error(String message) {
        status.setText(message == null ? "Something went wrong. Please try again." : message);
        status.setTextColor(Color.rgb(164, 43, 43));
        Toast.makeText(this, message == null ? "Please try again." : message, Toast.LENGTH_LONG).show();
    }

    private void failure(int request, Exception exception) {
        String message = exception.getMessage();
        if (message == null) message = "Processing failed. Try a smaller image or restart the app.";
        final String finalMessage = message;
        runOnUiThread(() -> { if (request == generation) { setBusy(false, ""); error(finalMessage); } });
    }

    @Override protected void onDestroy() {
        generation++;
        worker.shutdownNow();
        super.onDestroy();
    }
}
