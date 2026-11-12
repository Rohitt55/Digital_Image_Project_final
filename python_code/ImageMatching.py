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
# Set Reference_path to the second image you want to compare.
Reference_path = Img_path
reference = cv2.imread(Reference_path)
if reference is None:
    raise SystemExit("Reference image not found! Check Reference_path.")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
target = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
target = cv2.resize(target, (gray.shape[1], gray.shape[0]))
difference = np.abs(gray.astype(np.int16) - target.astype(np.int16))
tolerance = 5
similar = np.count_nonzero(difference <= tolerance)
print('PIXEL SIMILARITY RESULT')
print('Original Source Shape:', gray.shape)
print('Resized Reference Shape:', target.shape)
print('Similar pixels:', similar)
print('Different pixels:', gray.size - similar)
print('Total pixels:', gray.size)
print('Tolerance:', tolerance)
print('Similarity (%):', 100 * similar / gray.size)
result = difference.astype(np.uint8)


# Display
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title('Source Image')
plt.axis("off")

plt.subplot(2, 2, 2)
plt.hist(gray.ravel(), bins=256, range=(0, 256))
plt.title('Source Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.subplot(2, 2, 3)
plt.imshow(target, cmap="gray", vmin=0, vmax=255)
plt.title('Reference Image')
plt.axis("off")

plt.subplot(2, 2, 4)
plt.hist(target.ravel(), bins=256, range=(0, 256))
plt.title('Reference Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.tight_layout()

plt.show()
