package com.pixellab.dip;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.os.Build;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.ScaleGestureDetector;
import android.view.View;
import android.view.WindowInsets;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import java.io.File;
import java.io.FileInputStream;

/** Pinch-zoom and pan for the lab's high-resolution plots. */
public final class ImageViewerActivity extends Activity {
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.WHITE);
        root.setOnApplyWindowInsetsListener((view, insets) -> {
            if (Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets bars = insets.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                view.setPadding(bars.left, bars.top, bars.right, bars.bottom);
            } else view.setPadding(insets.getSystemWindowInsetLeft(), insets.getSystemWindowInsetTop(), insets.getSystemWindowInsetRight(), insets.getSystemWindowInsetBottom());
            return insets;
        });
        Button back = new Button(this);
        back.setText("Back · " + getIntent().getStringExtra("title")); back.setAllCaps(false);
        back.setOnClickListener(v -> finish()); root.addView(back);
        TextView hint = new TextView(this); hint.setText("Pinch to zoom · Drag to move · Double-tap to reset");
        hint.setPadding(16, 8, 16, 8); root.addView(hint);
        try {
            File file = new File(getIntent().getStringExtra("file"));
            if (!file.getCanonicalPath().startsWith(getCacheDir().getCanonicalPath() + File.separator)) throw new IllegalArgumentException();
            byte[] bytes = OfflineClient.readLimited(new FileInputStream(file), 96 * 1024 * 1024);
            BitmapFactory.Options options = new BitmapFactory.Options();
            options.inJustDecodeBounds = true;
            BitmapFactory.decodeByteArray(bytes, 0, bytes.length, options);
            options.inSampleSize = 1;
            while (options.outWidth / options.inSampleSize > 4096 || options.outHeight / options.inSampleSize > 4096) options.inSampleSize *= 2;
            options.inJustDecodeBounds = false;
            Bitmap bitmap = BitmapFactory.decodeByteArray(bytes, 0, bytes.length, options);
            if (bitmap == null) throw new IllegalArgumentException();
            root.addView(new ZoomView(bitmap), new LinearLayout.LayoutParams(-1, 0, 1));
        } catch (Exception e) { hint.setText("Could not open this image. Return to the result and try again."); }
        setContentView(root);
    }

    private final class ZoomView extends View {
        private final Bitmap bitmap;
        private final Matrix transform = new Matrix();
        private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG | Paint.FILTER_BITMAP_FLAG);
        private final ScaleGestureDetector detector;
        private float lastX, lastY, scale = 1, minimum = 1;
        private long lastTap = 0;
        ZoomView(Bitmap bitmap) {
            super(ImageViewerActivity.this); this.bitmap = bitmap;
            detector = new ScaleGestureDetector(getContext(), new ScaleGestureDetector.SimpleOnScaleGestureListener() {
                @Override public boolean onScale(ScaleGestureDetector source) {
                    float next = Math.max(minimum * 0.5f, Math.min(minimum * 12, scale * source.getScaleFactor()));
                    transform.postScale(next / scale, next / scale, source.getFocusX(), source.getFocusY());
                    scale = next; invalidate(); return true;
                }
            });
        }
        private void reset() {
            minimum = Math.min(getWidth() / (float) bitmap.getWidth(), getHeight() / (float) bitmap.getHeight());
            scale = minimum;
            transform.reset(); transform.postScale(scale, scale);
            transform.postTranslate((getWidth() - bitmap.getWidth() * scale) / 2, (getHeight() - bitmap.getHeight() * scale) / 2);
            invalidate();
        }
        @Override protected void onSizeChanged(int w, int h, int oldw, int oldh) { reset(); }
        @Override protected void onDraw(Canvas canvas) { super.onDraw(canvas); canvas.drawColor(Color.WHITE); canvas.drawBitmap(bitmap, transform, paint); }
        @Override public boolean onTouchEvent(MotionEvent event) {
            detector.onTouchEvent(event);
            if (event.getActionMasked() == MotionEvent.ACTION_DOWN) {
                if (event.getEventTime() - lastTap < 300) reset();
                lastTap = event.getEventTime(); lastX = event.getX(); lastY = event.getY();
            } else if (event.getActionMasked() == MotionEvent.ACTION_MOVE && !detector.isInProgress() && event.getPointerCount() == 1) {
                transform.postTranslate(event.getX() - lastX, event.getY() - lastY);
                lastX = event.getX(); lastY = event.getY(); invalidate();
            } else if (event.getActionMasked() == MotionEvent.ACTION_UP) performClick();
            return true;
        }
        @Override public boolean performClick() { super.performClick(); return true; }
    }
}
