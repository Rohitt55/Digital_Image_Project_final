# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 09:07:36 2026

@author: Administrator
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read image in grayscale
Img_path=r"D:/DIPLab/Image/Multicolor-MagnificFlower.bmp";

img = cv2.imread(Img_path)

if img is None:
    print("Image not found!")
else:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# -----------------------------
# Calculate Contrast
# -----------------------------
I_max = np.max(img)
I_min = np.min(img)
mean = np.mean(img)

# Simple Contrast
simple_contrast = I_max - I_min

# Michelson Contrast
michelson = (I_max - I_min) / (I_max + I_min)

# RMS Contrast
rms = np.sqrt(np.mean((img - mean) ** 2))

# -----------------------------
# Display Image and Histogram
# -----------------------------
plt.figure(figsize=(10,4))

# Original Image
plt.subplot(1,2,1)
plt.imshow(img, cmap='gray')
plt.title("Original Image")
plt.axis("off")

# Histogram
plt.subplot(1,2,2)
plt.hist(img.ravel(), bins=20, range=(0,20), color='red')
plt.title("Image Histogram")
plt.xlabel("Pixel Intensity")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()

# -----------------------------
# Print Results
# -----------------------------
print("Maximum Intensity :", I_max)
print("Minimum Intensity :", I_min)
print("Mean Intensity    :", mean)

print("\nSimple Contrast   :", simple_contrast)
print("Michelson Contrast:", round(michelson,4))
print("RMS Contrast      :", round(rms,4))