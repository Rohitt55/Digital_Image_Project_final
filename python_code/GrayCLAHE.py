import cv2
import matplotlib.pyplot as plt
from pathlib import Path


# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)

if img is None:
    raise SystemExit("Image not found! Check Img_path.")

# Calculation
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
result = clahe.apply(gray)


# Display
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title('Original Image')
plt.axis("off")

plt.subplot(2, 2, 2)
plt.hist(gray.ravel(), bins=256, range=(0, 256))
plt.title('Original Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.subplot(2, 2, 3)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title('CLAHE Image')
plt.axis("off")

plt.subplot(2, 2, 4)
plt.hist(result.ravel(), bins=256, range=(0, 256))
plt.title('Processed Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.tight_layout()

plt.show()
