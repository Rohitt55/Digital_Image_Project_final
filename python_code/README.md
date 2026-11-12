# Standalone Python lab scripts

These files follow `Lab_code`: read an image with `cv2.imread`, set simple variables, calculate the output, and display it with `matplotlib.pyplot`. There are no app decorators or parameter dictionaries in the standalone scripts. The four codec labs define their encoder and decoder functions before running their image experiment.

## Run a lab

From the project root:

```powershell
.\.venv\Scripts\python.exe python_code\ImageResize.py
.\.venv\Scripts\python.exe python_code\ImageNegative.py
```

Image-based scripts use the included `images/sample.png`, resolved relative to the project so it also runs from an IDE or another working directory. Change `Img_path` to your own image path and edit variables such as `width`, `height`, `gamma` or `sigma` directly in the file. `ImageMatching.py` and `HistogramMatching.py` also have `Reference_path`; the default compares the sample with itself.

Each experiment shows its relevant output. Resize reports dimensions; cropping marks the selected region; histogram and equalization show their distributions; pixel matrices display values on the image; transforms show spectra, masks or reconstruction; noise shows its applied distribution; restoration compares the observation with the restored image; matching shows the reference and difference; compression compares decoded pixels and storage sizes. Related measurements are printed, with no blanket histogram, CDF or pixel-matrix dump. Experiments use fixed example settings; adjust them in the script to study different results. The web app follows the same operation-specific approach using its selected settings.

The fixed PDF matrix labs need no image file. `ImageReadSave.py` writes `Results/LabImageCopy.png`. See [LabCoverage.md](LabCoverage.md) for the 17 additions and source pages.

## Lab files

- [AdaptiveMeanThreshold.py](AdaptiveMeanThreshold.py)
- [AdaptiveThreshold.py](AdaptiveThreshold.py)
- [ArithmeticCoding.py](ArithmeticCoding.py)
- [AverageFilter.py](AverageFilter.py)
- [BasicHistEqualization.py](BasicHistEqualization.py)
- [BilateralFilter.py](BilateralFilter.py)
- [BinaryImageMatrix.py](BinaryImageMatrix.py)
- [BinaryThreshold.py](BinaryThreshold.py)
- [BitPlaneSlicing.py](BitPlaneSlicing.py)
- [CannyEdgeDetection.py](CannyEdgeDetection.py)
- [ColorChannel.py](ColorChannel.py)
- [ColorSpaceConversion.py](ColorSpaceConversion.py)
- [CosineTransform.py](CosineTransform.py)
- [EdgeDetectionComparison.py](EdgeDetectionComparison.py)
- [ExponentialNoise.py](ExponentialNoise.py)
- [FourierTransform.py](FourierTransform.py)
- [FrequencyFilter.py](FrequencyFilter.py)
- [GammaCorrection.py](GammaCorrection.py)
- [GammaNoise.py](GammaNoise.py)
- [GaussianFilter.py](GaussianFilter.py)
- [GaussianNoise.py](GaussianNoise.py)
- [GrayCLAHE.py](GrayCLAHE.py)
- [HistogramMatching.py](HistogramMatching.py)
- [HistogramStretching.py](HistogramStretching.py)
- [HSIToRGB.py](HSIToRGB.py)
- [HuffmanCoding.py](HuffmanCoding.py)
- [ImageBrightnessContrast.py](ImageBrightnessContrast.py)
- [ImageCropping.py](ImageCropping.py)
- [ImageDilation.py](ImageDilation.py)
- [ImageErosion.py](ImageErosion.py)
- [ImageFlip.py](ImageFlip.py)
- [ImageGrayscale.py](ImageGrayscale.py)
- [ImageHistogram.py](ImageHistogram.py)
- [ImageMatching.py](ImageMatching.py)
- [ImageMeasurements.py](ImageMeasurements.py)
- [ImageNegative.py](ImageNegative.py)
- [ImagePixelMatrix.py](ImagePixelMatrix.py)
- [ImageQuantization.py](ImageQuantization.py)
- [ImageReadSave.py](ImageReadSave.py)
- [ImageResize.py](ImageResize.py)
- [ImageRotation.py](ImageRotation.py)
- [ImageSampling.py](ImageSampling.py)
- [ImageTransformComparison.py](ImageTransformComparison.py)
- [IndexedImage.py](IndexedImage.py)
- [InverseCosineTransform.py](InverseCosineTransform.py)
- [InverseFilter.py](InverseFilter.py)
- [InverseFourierTransform.py](InverseFourierTransform.py)
- [InverseLogTransformation.py](InverseLogTransformation.py)
- [JPEGCompression.py](JPEGCompression.py)
- [KMeansSegmentation.py](KMeansSegmentation.py)
- [KNNImageInterpolation.py](KNNImageInterpolation.py)
- [KNNInterpolation.py](KNNInterpolation.py)
- [LabBasicEqualization.py](LabBasicEqualization.py)
- [LabHistogramMatrix.py](LabHistogramMatrix.py)
- [LabNormalizedEqualization.py](LabNormalizedEqualization.py)
- [LaplacianEdgeDetection.py](LaplacianEdgeDetection.py)
- [LaplacianFilter.py](LaplacianFilter.py)
- [LogTransformation.py](LogTransformation.py)
- [LZWCoding.py](LZWCoding.py)
- [MedianFilter.py](MedianFilter.py)
- [MorphologicalClosing.py](MorphologicalClosing.py)
- [MorphologicalGradient.py](MorphologicalGradient.py)
- [MorphologicalOpening.py](MorphologicalOpening.py)
- [NormalizedHistEqualization.py](NormalizedHistEqualization.py)
- [OtsuThreshold.py](OtsuThreshold.py)
- [PixelConnectivity.py](PixelConnectivity.py)
- [PoissonNoise.py](PoissonNoise.py)
- [PrewittEdgeDetection.py](PrewittEdgeDetection.py)
- [RayleighNoise.py](RayleighNoise.py)
- [RegionGrowing.py](RegionGrowing.py)
- [RGBToHSI.py](RGBToHSI.py)
- [RobertsEdgeDetection.py](RobertsEdgeDetection.py)
- [RunLengthCoding.py](RunLengthCoding.py)
- [SaltPepperNoise.py](SaltPepperNoise.py)
- [SegmentationComparison.py](SegmentationComparison.py)
- [SmoothingFilterComparison.py](SmoothingFilterComparison.py)
- [SobelEdgeDetection.py](SobelEdgeDetection.py)
- [SpeckleNoise.py](SpeckleNoise.py)
- [ThresholdComparison.py](ThresholdComparison.py)
- [UniformNoise.py](UniformNoise.py)
- [UnsharpMasking.py](UnsharpMasking.py)
- [WatershedSegmentation.py](WatershedSegmentation.py)
- [WienerFilter.py](WienerFilter.py)

## Web app

`mobile_server.py` starts the same API on the local network for the Android APK. Run `start_mobile.bat` from the project root and use the printed Wi-Fi address in the phone app. This launcher is server infrastructure, separate from the 83 standalone algorithm/example scripts.

`web_app.py` launches the existing app. Its registration, validation, configurable algorithms and plotting support are in `app_backend/`. These backend files are separate from the standalone labs. The app's code tab shows a runnable standalone example with default settings; the app controls still run the configurable backend implementation.

```powershell
.\.venv\Scripts\python.exe python_code\web_app.py --open-browser
```

## Verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s python_code -p "test_*.py"
```

The suite checks the web app and algorithms, verifies relevant lab panels across every selectable variant, and runs all 83 standalone scripts with a noninteractive plotting backend. Each lab must produce a uint8 image and render its figures; codecs must reconstruct their analysis image exactly.

## Reference sample layouts

Output layouts were checked against rendered pages of both lab PDFs. Matching uses source/reference images and histograms in a 2x2 grid. Equalization uses the image/histogram/CDF arrangement and a separate readable mapping table. Transformation, edge, threshold and segmentation displays use their corresponding comparison grids. Sampling compares 32x32, 64x64 and 1024x1024; quantization compares 8-bit through 1-bit. Result captions link to the relevant source PDF pages.

Individual algorithm files still perform one primary operation. Dedicated `ImageTransformComparison.py`, `SmoothingFilterComparison.py`, `EdgeDetectionComparison.py`, `ThresholdComparison.py` and `SegmentationComparison.py` reproduce grouped sample experiments. `ImageSampling.py` reproduces the sampling grid. `KNNImageInterpolation.py` adds the 8x8 image reconstruction, close-ups and measured MSE/PSNR/SSIM comparison. In the app, select "Uploaded 8x8 image" in KNN to run this experiment.

Current input pixels and selected parameters determine the results. Companion comparison methods use example defaults. Numeric slide inconsistencies are not copied: normalized CDF count and probability are labeled separately, and basic equalization uses the documented rounding rule. Gaussian noise and negative examples default to grayscale; the app also offers RGB channel mode.

Matplotlib figures and API responses are verified by tests. Browser preview was unavailable in this session; the result-table JavaScript passes a syntax check and the table data and source links are covered by API tests.
