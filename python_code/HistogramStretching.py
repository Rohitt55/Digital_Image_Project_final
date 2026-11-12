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
low = float(img.min())
high = float(img.max())
if high == low:
    result = img.copy()
else:
    values = img.astype(float)
    stretched = (values - low) / (high - low) * 255
    result = np.round(stretched).astype(np.uint8)


# Display
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis("off")

plt.subplot(2, 2, 2)
plt.hist(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).ravel(), bins=256, range=(0, 256))
plt.title('Original Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.subplot(2, 2, 3)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('Stretched Image')
plt.axis("off")

plt.subplot(2, 2, 4)
plt.hist(cv2.cvtColor(result, cv2.COLOR_BGR2GRAY).ravel(), bins=256, range=(0, 256))
plt.title('Processed Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.tight_layout()

plt.show()
