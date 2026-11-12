# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 08:03:55 2026

@author: Administrator
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

Img_path=r"D:\DIPLab\Image\car1.jpg";

img = cv2.imread(Img_path)

# Sobel
sx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
sy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
sobel = cv2.magnitude(sx.astype(np.float32),
                      sy.astype(np.float32))

# Prewitt
kx = np.array([[-1, 0, 1],
               [-1, 0, 1],
               [-1, 0, 1]], dtype=np.float32)

ky = np.array([[-1, -1, -1],
               [ 0,  0,  0],
               [ 1,  1,  1]], dtype=np.float32)

px = cv2.filter2D(img, cv2.CV_32F, kx)
py = cv2.filter2D(img, cv2.CV_32F, ky)

prewitt = cv2.magnitude(px, py)

# Roberts
rx_kernel = np.array([[1, 0],
                      [0, -1]], dtype=np.float32)

ry_kernel = np.array([[0, 1],
                      [-1, 0]], dtype=np.float32)

rx = cv2.filter2D(img, cv2.CV_32F, rx_kernel)
ry = cv2.filter2D(img, cv2.CV_32F, ry_kernel)

roberts = cv2.magnitude(rx, ry)

# Canny
canny = cv2.Canny(img, 100, 200)

# Normalize gradient results for display
sobel = cv2.normalize(sobel, None, 0, 255,
                      cv2.NORM_MINMAX).astype(np.uint8)

prewitt = cv2.normalize(prewitt, None, 0, 255,
                        cv2.NORM_MINMAX).astype(np.uint8)

roberts = cv2.normalize(roberts, None, 0, 255,
                        cv2.NORM_MINMAX).astype(np.uint8)

# Display
titles = ["Original", "Sobel", "Prewitt",
          "Roberts", "Canny"]

images = [img, sobel, prewitt, roberts, canny]

plt.figure(figsize=(12, 8))

for i in range(5):
    plt.subplot(2, 3, i + 1)
    plt.imshow(images[i], cmap="gray")
    plt.title(titles[i])
    plt.axis("off")

plt.tight_layout()
plt.show()