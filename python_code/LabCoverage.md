# Lab 1 and Lab 2 additions

The 17 previously missing experiments are now registered in the web app and provided as separate standalone lab scripts. App entries link to their lab PDF and pages through the course catalog. The app now has 59 operations, 86 course topics, and 83 standalone scripts.

| Standalone file | PDF | Pages | Added work |
| --- | --- | --- | --- |
| [ImageReadSave.py](ImageReadSave.py) | [Lab 1](../pdfs/DIP-Lab1.pdf) | 14, 15, 18 | Read, display and save image |
| [ImageMeasurements.py](ImageMeasurements.py) | [Lab 1](../pdfs/DIP-Lab1.pdf) | 21 | Mean, variance and contrast measurements |
| [IndexedImage.py](IndexedImage.py) | [Lab 1](../pdfs/DIP-Lab1.pdf) | 28, 29, 30 | Indexed image and color palette |
| [PixelConnectivity.py](PixelConnectivity.py) | [Lab 1](../pdfs/DIP-Lab1.pdf) | 43, 44, 45 | Pixel connectivity graph |
| [KNNInterpolation.py](KNNInterpolation.py) | [Lab 1](../pdfs/DIP-Lab1.pdf) | 46, 47, 48, 49 | Distance-weighted KNN interpolation |
| [ColorSpaceConversion.py](ColorSpaceConversion.py) | [Lab 1](../pdfs/DIP-Lab1.pdf) | 52, 54, 55, 56, 57, 58 | RGB, Gray, HSV, Lab and YCrCb conversion |
| [RGBToHSI.py](RGBToHSI.py) | [Lab 1](../pdfs/DIP-Lab1.pdf) | 59, 60, 61, 62, 63, 64, 65 | RGB to HSI |
| [HSIToRGB.py](HSIToRGB.py) | [Lab 1](../pdfs/DIP-Lab1.pdf) | 66, 67, 68 | HSI to RGB |
| [AdaptiveMeanThreshold.py](AdaptiveMeanThreshold.py) | [Lab 2](../pdfs/DIP-Lab2.pdf) | 47, 49 | Adaptive mean threshold |
| [WatershedSegmentation.py](WatershedSegmentation.py) | [Lab 2](../pdfs/DIP-Lab2.pdf) | 51, 52, 53, 54, 55 | Marker-based Watershed segmentation |
| [RegionGrowing.py](RegionGrowing.py) | [Lab 2](../pdfs/DIP-Lab2.pdf) | 55, 56, 57 | Seed-based Region Growing |
| [KMeansSegmentation.py](KMeansSegmentation.py) | [Lab 2](../pdfs/DIP-Lab2.pdf) | 58, 59 | K-means color segmentation |
| [HistogramMatching.py](HistogramMatching.py) | [Lab 2](../pdfs/DIP-Lab2.pdf) | 30, 31, 32, 33, 34, 35, 36 | Histogram distribution matching |
| [LabHistogramMatrix.py](LabHistogramMatrix.py) | [Lab 2](../pdfs/DIP-Lab2.pdf) | 11, 12 | 5x5 histogram matrix |
| [LabBasicEqualization.py](LabBasicEqualization.py) | [Lab 2](../pdfs/DIP-Lab2.pdf) | 23, 24, 25, 26, 27, 28, 29 | 8x8 basic histogram equalization |
| [LabNormalizedEqualization.py](LabNormalizedEqualization.py) | [Lab 2](../pdfs/DIP-Lab2.pdf) | 15, 16, 17, 18, 19, 20, 21, 22 | 8x8 normalized histogram equalization |
| [BinaryImageMatrix.py](BinaryImageMatrix.py) | [Lab 1](../pdfs/DIP-Lab1.pdf) | 22 | Binary image matrix |

The 5x5 histogram matrix is exactly the PDF data; its counts for values 0 through 6 are `[2, 5, 3, 4, 5, 2, 4]`. The two 8x8 equalization labs use the full PDF intensity matrix, print the frequency/CDF/mapping table, and label the original and equalized pixel values. The normalized example has 64 pixels and CDF minimum 1: intensity 52 maps to 0 and intensity 55 maps to 12.

`ImageMeasurements.py` covers the Lab 1 mean/variance/standard-deviation example and the Lab 2 intensity-range, Michelson and RMS contrast calculations (Lab 2 pages 4-9). Measurements can use all RGB values or grayscale. Constant black images report finite zero contrast.

The indexed-image lab uses the exact PDF index matrix and palette. Connectivity uses the PDF 3x3 values and draws 12 edges for 4-connectivity. KNN uses the PDF four corner values; its center is 25 when K=4. Uploaded-image variants are also available in the app. Only four neighbors exist in the 2x2 example, so larger requested K values use the available four samples.

HSI calculations use hue in degrees, saturation in 0-1 and intensity in 0-1. Achromatic pixels have hue zero. Inverse conversion preserves the intensity equation before clipping values outside the RGB gamut; the app reports clipping. Some numeric HSI examples in the slides are inconsistent with the stated intensity definition, so the implementation follows the equations and supports an exact RGB-HSI-RGB image round trip.

The color-space experiment displays each numerical channel with its proper label; OpenCV YCrCb channel order is Y, Cr, Cb. The downloadable processed image is the selected space's first numerical channel. The sample-layout figure also reproduces the encoded-channel color displays from the PDF; these are explicitly labeled and are not presented as natural RGB colors.

The PDF heading ?Histogram Matching? contains pixel comparison, which remains `ImageMatching.py`. `HistogramMatching.py` adds actual CDF-based distribution matching as a separate experiment; it is identified as an extension in the catalog.

Watershed follows the PDF's inverted Otsu mask, opening, distance-transform markers and red boundaries. Region Growing uses 4-connected neighbors and the selected seed intensity. Region Growing and K-means analyze at most a 512-pixel side; their outputs and seed coordinates refer to that analysis image. K-means uses reproducible initialization.

Image saving writes a PNG in the standalone lab. The app offers the same lossless PNG as a downloadable artifact rather than writing a server-side output file. The four fixed-matrix app entries still use the app's usual image/sample workflow, but their calculations use PDF data independently of that upload.

Verification checks PDF histogram counts, equalization mappings, graph edges, KNN samples, statistics, known color conversions, HSI round trips and gamut clipping, 4-connected region growth, Watershed markers, K-means colors, histogram matching and lossless PNG export. The complete suite also runs every standalone script and renders every app operation's lab output.

Reference layout details and the seven dedicated sample-comparison scripts are listed in [the Python lab guide](README.md#reference-sample-layouts). Matching and threshold/segmentation family figures follow the sample arrangements, while selected outputs and scores are calculated from the current image.
