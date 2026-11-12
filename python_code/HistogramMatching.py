import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab2.pdf, pages 30, 31, 32, 33, 34, 35, 36.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

# Change Reference_path to a different image for a matching experiment.
Reference_path = Img_path
reference = cv2.imread(Reference_path)
if reference is None:
    raise SystemExit('Reference image not found! Check Reference_path.')


# Calculation
if reference is None:
    raise ValueError('Upload a reference image for histogram matching.')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
target = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
source_hist = np.bincount(gray.ravel(), minlength=256)
target_hist = np.bincount(target.ravel(), minlength=256)
source_cdf = np.cumsum(source_hist / gray.size)
target_cdf = np.cumsum(target_hist / target.size)
mapping = np.searchsorted(target_cdf, source_cdf, side='left')
mapping = np.clip(mapping, 0, 255).astype(np.uint8)
result = mapping[gray]
matched_cdf = np.cumsum(np.bincount(result.ravel(), minlength=256) / result.size)
details = {'cdf_distance_before': float(np.mean(np.abs(source_cdf - target_cdf))),
           'cdf_distance_after': float(np.mean(np.abs(matched_cdf - target_cdf))),
           'note': 'Discrete intensity distributions may not admit an exact histogram match.'}

print("CDF distance before:", details["cdf_distance_before"])
print("CDF distance after:", details["cdf_distance_after"])


# Display the results of this experiment.
plt.figure(figsize=(15, 9.0))

plt.subplot(2, 3, 1)
plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
plt.title('Source grayscale')
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(target, cmap='gray', vmin=0, vmax=255)
plt.title('Reference grayscale')
plt.axis("off")

plt.subplot(2, 3, 3)
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title('Histogram-matched image')
plt.axis("off")

plt.subplot(2, 3, 4)
plt.hist(gray.ravel(), bins=256, range=(0, 256))
plt.title('Source histogram')
plt.xlabel('Pixel intensity')
plt.ylabel('Count')

plt.subplot(2, 3, 5)
plt.hist(target.ravel(), bins=256, range=(0, 256))
plt.title('Reference histogram')
plt.xlabel('Pixel intensity')
plt.ylabel('Count')

plt.subplot(2, 3, 6)
plt.hist(result.ravel(), bins=256, range=(0, 256))
plt.title('Matched histogram')
plt.xlabel('Pixel intensity')
plt.ylabel('Count')

plt.tight_layout()
plt.show()
