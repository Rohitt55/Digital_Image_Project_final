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
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
low = 100
high = 200
result = cv2.Canny(blurred, low, high)

# Display the results needed for this experiment.
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title("Grayscale input")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title('Canny Edge Detection')
plt.axis("off")

plt.tight_layout()
plt.show()
