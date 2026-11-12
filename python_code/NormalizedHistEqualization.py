import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)

if img is None:
    raise SystemExit("Image not found! Check Img_path.")

# Calculation
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hist = np.bincount(gray.ravel(), minlength=256)
cdf = np.cumsum(hist)
first = cdf[cdf > 0][0]
if gray.size == first:
    result = gray.copy()
else:
    scaled = (cdf - first) / (gray.size - first) * 255
    mapping = np.clip(np.round(scaled), 0, 255).astype(np.uint8)
    result = mapping[gray]

counts = np.bincount(gray.ravel(), minlength=256)
cumulative_counts = np.cumsum(counts)
cdf_values = cumulative_counts

# Display
plt.figure(figsize=(15, 8))

plt.subplot(2, 3, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title('Original Image')
plt.axis("off")

plt.subplot(2, 3, 2)
plt.hist(gray.ravel(), bins=256, range=(0, 256))
plt.title('Original Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.subplot(2, 3, 3)
plt.plot(cdf_values)
plt.title('Cumulative Distribution Function')
plt.xlabel('Pixel Intensity')
plt.ylabel('Cumulative Count')
plt.grid(alpha=0.25)

plt.subplot(2, 3, 4)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title('Equalized')
plt.axis("off")

plt.subplot(2, 3, 5)
plt.hist(result.ravel(), bins=256, range=(0, 256))
plt.title('Equalized Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.tight_layout()

plt.show()
