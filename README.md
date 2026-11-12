# PixelLab - Digital Image Processing

A local DIP lab app with **59 operations** and **86 source-linked course topics**. Upload an image, choose an operation and compare the original and processed output, histograms, CDF and statistics.

## Android APK

Install [PixelLab-offline.apk](output/android/PixelLab-offline.apk) on a 64-bit Android 7.0+ phone. All 59 operations run entirely on the phone using bundled Python/OpenCV libraries. No computer, server, Wi-Fi, mobile data or first-run download is required. Photo selection, reference images, figures, tables, Python examples, zoom and saving work offline.

See [Android setup and build instructions](android_app/README.md) or [বাংলা installation guide](output/android/INSTALL_BN.md).

The Android sidebar includes chapter 1–8 filters, search within a chapter, operation counts, Clear filters and a scrollable feature list. Open it using ☰, then select an operation to return to the workspace. Image selection, experiment settings and results stay in separate cards.

## Run

On Windows, double-click `start.bat`. The first run needs Python 3.12 and installs the packages in `requirements.txt` into `.venv`. The app opens at http://127.0.0.1:5000. Keep the terminal open while using it.

To run with an existing environment:

```powershell
.\.venv\Scripts\python.exe python_code\web_app.py --open-browser
```

## Retained operations

| Area | Operations |
| --- | --- |
| Fundamentals and color | Read/save, full statistics, indexed images, connectivity graph, KNN interpolation, RGB/HSV/Lab/YCrCb and HSI conversion, grayscale, negative, brightness/contrast, gamma, intensity quantization, color-space channels, pixel matrix, log/inverse-log, bit-plane slicing |
| Histograms | Contrast stretching, histogram analysis, basic and normalized equalization, CLAHE, distribution matching, exact PDF matrix examples |
| Geometry | Resize, crop, rotate, flip |
| Filters and restoration | Mean, Gaussian, median, bilateral, unsharp masking, Laplacian, noise models, inverse/Wiener restoration |
| Edges and segmentation | Sobel, Prewitt, Roberts, Canny, binary threshold, Otsu, adaptive mean/Gaussian threshold, Watershed, Region Growing, K-means |
| Morphology | Erosion, dilation, opening, closing and gradient in one operation |
| Transforms and comparison | FFT/DFT, IDFT, frequency filtering, DCT/inverse DCT, pixel matching |
| Compression | JPEG compression; RLE, Huffman, arithmetic and LZW coding in one lossless operation |

Advanced recognition, medical-imaging, 3D/signal demonstrations have been removed. Lab 2 Watershed, Region Growing and K-means are included. The course catalog only links to retained operations. Original chapter and lab PDFs remain in `pdfs/`.

## Use

1. Upload an image or choose **Try a sample**.
2. Choose an operation, adjust its settings and run it.
3. Compare the output, inspect the plots or Python implementation, and download the result.

Pixel similarity and histogram distribution matching need a second reference image. Use **Use as next input** to chain operations. History lasts for the current page session. JPEG exports contain actual JPEG bytes. Lossless teaching exports encode a bounded grayscale analysis image and include decoding metadata; they are JSON teaching formats.

The total upload limit is 24 MB. Input and resized images are limited to 12 million pixels. Images are processed in memory. OpenCV uses BGR internally; histograms and shared intensity statistics use grayscale. The dedicated measurements experiment can also measure all RGB channel values.

## Files

| Path | Purpose |
| --- | --- |
| `python_code/ImageResize.py`, `ImageNegative.py`, etc. | 83 standalone lab scripts: image input, calculation and plots |
| `python_code/web_app.py` | Launches the web app |
| `python_code/app_backend/` | App routes, operation registry, validation and configurable algorithms |
| `python_code/test_*.py` | App, algorithm and standalone lab checks |
| `images/sample.png` | Included sample image for running the labs |
| `static/` | JavaScript, CSS and favicon |
| `data/course_topics.json` | Course topics, presets and PDF references |
| `pdfs/` | Original chapter, lab and course PDFs |

The standalone scripts follow `Lab_code`: `cv2.imread()` reads the image, simple variables control the calculation, and `plt.show()` displays the result. Image-based scripts have an editable `Img_path`; fixed-matrix PDF examples use their exact data directly. See [the Python lab guide](python_code/README.md) for the complete list and run commands. The web app's code tab shows a default standalone lab example; its controls use the configurable implementations in `app_backend/`.

Lab plots and printed measurements follow the selected operation: geometry shows dimensions or crop regions, histogram work shows distributions, transforms show spectra or reconstruction, restoration shows degraded and restored images, and compression shows decoded images and storage sizes. The app updates the plot caption for each result.

## Verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s python_code -p "test_*.py"
```

The tests cover every retained operation and selectable variant, course presets, pixel math, validation errors, compression round trips, DCT reconstruction, morphology properties, and image and figure output from all 83 standalone lab scripts.

See [Lab 1 and Lab 2 coverage](python_code/LabCoverage.md) for the added methods, exact example data and PDF page references.
