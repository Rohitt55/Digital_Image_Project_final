# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 17:05:06 2026

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

    plt.subplot(1,2,1)
    plt.imshow(img)
    plt.axis("off")
    plt.show()
    
    
    # -------------------------------------------------
    # Convert to RGB and Grayscale
    # -------------------------------------------------
    #rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# --------------------------------
# Contrast Adjustment
# --------------------------------

contrast_low = cv2.convertScaleAbs(img, alpha=0.8, beta=0.5)

contrast_high = cv2.convertScaleAbs(img, alpha=1.8, beta=0)

# --------------------------------
# Display
# --------------------------------

plt.figure(figsize=(12,5))

plt.subplot(1,3,1)
plt.imshow(img)
plt.title("Original")
plt.axis("off")

plt.subplot(1,3,2)
plt.imshow(contrast_low)
plt.title("Low Contrast")
plt.axis("off")

plt.subplot(1,3,3)
plt.imshow(contrast_high)
plt.title("High Contrast")
plt.axis("off")

plt.tight_layout()
plt.show()