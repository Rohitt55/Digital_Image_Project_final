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
pdf = hist / gray.size
cdf = np.cumsum(pdf)
print("Histogram:")
print(hist)
print("CDF:")
print(cdf)
result = gray


# Display
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title('Grayscale Image')
plt.axis("off")

plt.subplot(1, 2, 2)
plt.hist(gray.ravel(), bins=256, range=(0, 256))
plt.title('Image Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.tight_layout()

plt.show()
