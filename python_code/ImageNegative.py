import cv2
import matplotlib.pyplot as plt
from pathlib import Path


# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    raise SystemExit("Image not found! Check Img_path.")

# Calculation
# Negative transformation
result = 255 - img

# Display the results needed for this experiment.
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(img, cmap="gray", vmin=0, vmax=255)
plt.title("Original")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title('Image Negative')
plt.axis("off")

plt.tight_layout()
plt.show()
