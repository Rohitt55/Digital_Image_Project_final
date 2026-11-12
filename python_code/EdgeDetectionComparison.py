import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
sx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
sy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
sobel_values = cv2.magnitude(sx, sy)
sobel = cv2.normalize(sobel_values, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
kx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
px = cv2.filter2D(gray, cv2.CV_32F, kx)
py = cv2.filter2D(gray, cv2.CV_32F, kx.T)
prewitt = cv2.normalize(cv2.magnitude(px, py), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
rx = cv2.filter2D(gray, cv2.CV_32F, np.array([[1, 0], [0, -1]], np.float32))
ry = cv2.filter2D(gray, cv2.CV_32F, np.array([[0, 1], [-1, 0]], np.float32))
roberts = cv2.normalize(cv2.magnitude(rx, ry), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
canny = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 100, 200)
result = sobel

# Display
plt.figure(figsize=(15, 8))

plt.subplot(2, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original')
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(sobel, cmap="gray", vmin=0, vmax=255)
plt.title('Sobel')
plt.axis("off")

plt.subplot(2, 3, 3)
plt.imshow(prewitt, cmap="gray", vmin=0, vmax=255)
plt.title('Prewitt')
plt.axis("off")

plt.subplot(2, 3, 4)
plt.imshow(roberts, cmap="gray", vmin=0, vmax=255)
plt.title('Roberts')
plt.axis("off")

plt.subplot(2, 3, 5)
plt.imshow(canny, cmap="gray", vmin=0, vmax=255)
plt.title('Canny')
plt.axis("off")

plt.tight_layout()

plt.show()
