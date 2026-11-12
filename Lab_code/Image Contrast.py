# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 12:40:14 2026

@author: Administrator
"""

import cv2
import matplotlib.pyplot as plt
import os

Img_path=r"D:/DIPLab/Image/Multicolor-MagnificFlower.bmp";

img = cv2.imread(Img_path)

if img is None:
    print("Image not found!")
else:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.imshow(img)
    plt.axis("off")
    plt.show()
    
# --------------------------------
# Contrast Adjustment
# --------------------------------

contrast_low = cv2.convertScaleAbs(img, alpha=0.5, beta=0)
contrast_high = cv2.convertScaleAbs(img, alpha=1.8, beta=0)

# --------------------------------
# Display
# --------------------------------

plt.figure(figsize=(12,5))

plt.subplot(3,3,1)
plt.imshow(img)
plt.title("Original")
plt.axis("off")

plt.subplot(3,3,2)
plt.imshow(contrast_low)
plt.title("Low Contrast")
plt.axis("off")

plt.subplot(3,3,3)
plt.imshow(contrast_high)
plt.title("High Contrast")
plt.axis("off")

plt.tight_layout()
plt.show()

# -------------------------------------------------
# Convert to RGB and Grayscale
# -------------------------------------------------
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

plt.imshow(gray, cmap='gray')
plt.title("Gray Image")
plt.axis("off")

hist = cv2.calcHist([gray], [0], None, [256], [0, 220])
equalized = cv2.equalizeHist(gray)
clahe = cv2.createCLAHE(clipLimit=20.0, tileGridSize=(8,8))
result = clahe.apply(gray)
clahe_hist = cv2.calcHist([result], [0], None, [256], [0, 220])

plt.figure(figsize=(10,5))

#plt.subplot(2,2,1)
#plt.imshow(img, cmap='gray')
#plt.title("Original")
#plt.axis("off")

plt.subplot(2,2,1)
plt.imshow(gray, cmap='gray')
plt.title("Gray Image")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.plot(hist)
plt.title("Image Histogram")
#plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")

plt.subplot(2,2,3)
plt.imshow(equalized, cmap='gray')
plt.title("Histogram Equalized")
plt.axis("off")

#plt.subplot(2,2,4)
#plt.imshow(img, cmap="gray")
#plt.title("Original")
#plt.axis("off")

plt.subplot(2,2,4)
plt.plot(clahe_hist)
#plt.title("CLAHE Histogram")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")

plt.show()



