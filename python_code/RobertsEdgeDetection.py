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
kx = np.array([[1, 0], [0, -1]], dtype=np.float32)
ky = np.array([[0, 1], [-1, 0]], dtype=np.float32)
rx = cv2.filter2D(gray, cv2.CV_32F, kx)
ry = cv2.filter2D(gray, cv2.CV_32F, ky)
magnitude = cv2.magnitude(rx, ry)
result = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Display the results needed for this experiment.
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title("Grayscale input")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title('Roberts Edge Detection')
plt.axis("off")

plt.tight_layout()
plt.show()
