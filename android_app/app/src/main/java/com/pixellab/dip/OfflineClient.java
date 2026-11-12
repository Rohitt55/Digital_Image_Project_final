package com.pixellab.dip;

import android.content.Context;
import android.util.Base64;
import com.chaquo.python.Python;
import com.chaquo.python.PyObject;
import com.chaquo.python.android.AndroidPlatform;
import org.json.JSONObject;
import java.io.InputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;

/** Calls the bundled Python engine directly. No server or network connection. */
public final class OfflineClient {
    private static PyObject engine;
    public OfflineClient(Context context) throws IOException {
        synchronized (OfflineClient.class) {
            try {
                if (!Python.isStarted()) Python.start(new AndroidPlatform(context.getApplicationContext()));
                if (engine == null) {
                    PyObject module = Python.getInstance().getModule("pixellab_engine.offline");
                    module.callAttr("initialize", context.getCacheDir().getAbsolutePath());
                    engine = module;
                }
            } catch (Exception e) { throw new IOException("Cannot start the offline engine: " + e.getMessage(), e); }
        }
    }
    private String call(String method, Object... args) throws IOException {
        synchronized (OfflineClient.class) {
            try {
                String value = engine.callAttr(method, args).toString();
                if (value.startsWith("{")) {
                    JSONObject object = new JSONObject(value);
                    if (object.has("error")) throw new IOException(object.getString("error"));
                }
                return value;
            } catch (IOException e) { throw e; }
            catch (Exception e) { throw new IOException(e.getMessage(), e); }
        }
    }
    public String get(String path) throws IOException { return call("get_json", path); }
    public String process(String operation, JSONObject params, byte[] image, String imageName,
                          byte[] reference, String referenceName) throws IOException {
        return call("process_json", operation, params.toString(), Base64.encodeToString(image, Base64.NO_WRAP),
                    reference == null ? "" : Base64.encodeToString(reference, Base64.NO_WRAP));
    }
    public static byte[] readLimited(InputStream input, int maximum) throws IOException {
        if (input == null) throw new IOException("Cannot open this file.");
        try (InputStream stream = input; ByteArrayOutputStream bytes = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[16384];
            int count;
            while ((count = stream.read(buffer)) != -1) {
                if (bytes.size() > maximum - count) throw new IOException("The image is too large. Try a smaller image.");
                bytes.write(buffer, 0, count);
            }
            return bytes.toByteArray();
        }
    }
}
