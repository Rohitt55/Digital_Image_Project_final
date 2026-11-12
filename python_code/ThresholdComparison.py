import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
basic_T = 128
global_T = 100
_, basic = cv2.threshold(gray, basic_T, 255, cv2.THRESH_BINARY)
_, global_mask = cv2.threshold(gray, global_T, 255, cv2.THRESH_BINARY)
mean = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
gaussian = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
otsu_T, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
result = otsu
print('THRESHOLDING RESULTS')
print('Basic Threshold:', basic_T)
print('Global Threshold:', global_T)
print('Adaptive Threshold: Local mean')
print('Gaussian Adaptive: Local Gaussian')
print('Otsu Optimal Threshold:', otsu_T)

# Display
plt.figure(figsize=(15, 8))

plt.subplot(2, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(basic, cmap="gray", vmin=0, vmax=255)
plt.title('Thresholding (T=128)')
plt.axis("off")

plt.subplot(2, 3, 3)
plt.imshow(global_mask, cmap="gray", vmin=0, vmax=255)
plt.title('Global Thresholding (T=100)')
plt.axis("off")

plt.subplot(2, 3, 4)
plt.imshow(mean, cmap="gray", vmin=0, vmax=255)
plt.title('Adaptive Thresholding (Mean)')
plt.axis("off")

plt.subplot(2, 3, 5)
plt.imshow(gaussian, cmap="gray", vmin=0, vmax=255)
plt.title('Gaussian Adaptive Thresholding')
plt.axis("off")

plt.subplot(2, 3, 6)
plt.imshow(otsu, cmap="gray", vmin=0, vmax=255)
plt.title('Otsu Thresholding')
plt.axis("off")

plt.tight_layout()

plt.show()
