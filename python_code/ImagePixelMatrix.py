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
result = cv2.resize(gray, (8, 8), interpolation=cv2.INTER_AREA)
print("Pixel values:")
print(result)


# Display
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title('Original Grayscale Image')
plt.xlabel("Column")
plt.ylabel("Row")

plt.subplot(1, 2, 2)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title('8 x 8 Digital Image with Pixel Values')
plt.xlabel("Column")
plt.ylabel("Row")
for y in range(result.shape[0]):
    for x in range(result.shape[1]):
        value = int(result[y, x])
        plt.text(x, y, str(value), ha='center', va='center',
                 color='black' if value > 127.5 else 'white', fontsize=8)

plt.tight_layout()

plt.show()
