# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 14:06:10 2026

@author: Administrator
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read grayscale image
Img_path=r"D:/DIPLab/Image/Multicolor-MagnificFlower.bmp";

image = cv2.imread(Img_path)

if image is None:
    print("Image not found!")
else:
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Find minimum and maximum intensity
r_min = np.min(image)
r_max = np.max(image)

print("Minimum Intensity =", r_min)
print("Maximum Intensity =", r_max)

# Contrast Stretching
stretched = ((image - r_min) / (r_max - r_min) * 255).astype(np.uint8)

# Plot Results
plt.figure(figsize=(12,8))

# Original Image
plt.subplot(2,2,1)
plt.imshow(image, cmap='gray')
plt.title("Original Low Contrast Image")
plt.axis("off")

# Original Histogram
plt.subplot(2,2,2)
plt.hist(image.ravel(), bins=20, range=[0,20], color='black')
plt.title("Histogram of Original Image")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")

# Stretched Image
plt.subplot(2,2,3)
plt.imshow(stretched, cmap='gray')
plt.title("Histogram Stretched Image")
plt.axis("off")

# Stretched Histogram
plt.subplot(2,2,4)
plt.hist(stretched.ravel(), bins=20, range=[0,20], color='blue')
plt.title("Histogram After Stretching")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()