# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 13:07:35 2026

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
    
    # -------------------------------------------------
    # Convert to RGB and Grayscale
    # -------------------------------------------------
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
# Create CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8, 8))

# Apply CLAHE
clahe_img = clahe.apply(gray)

# Calculate histogram
hist = cv2.calcHist([gray], [0], None, [256], [0, 150])
equalized = cv2.equalizeHist(gray)
equalized_hist = cv2.calcHist([clahe_img], [0], None, [256], [0, 150])

# Display
plt.figure(figsize=(10, 4))

plt.subplot(2, 2, 1)
plt.imshow(gray, cmap="gray")
plt.title("Original Grayscale")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(clahe_img, cmap="gray")
plt.title("CLAHE Enhanced")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.plot(hist)
plt.title("Gray Histogram")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.plot(equalized_hist)
plt.title("CLAHE Histogram")
plt.axis("off")
plt.tight_layout()
plt.show()









