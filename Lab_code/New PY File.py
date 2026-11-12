# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 08:44:04 2026

@author: Administrator
"""

import cv2
import matplotlib.pyplot as plt

# ============================================================
# IMAGE SEGMENTATION USING DIFFERENT THRESHOLDING TECHNIQUES
# ============================================================

# 1. Read image
Img_path=r"D:\DIPLab\Image\sunflower3.jpg";

img = cv2.imread(Img_path)

# Check image
if img is None:
    print("Error: Image not found!")
    exit()

# 2. Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# ============================================================
# 1. BASIC THRESHOLDING
# ============================================================

T = 128

_, basic_threshold = cv2.threshold(
    gray,
    T,
    255,
    cv2.THRESH_BINARY
)


# ============================================================
# 2. GLOBAL THRESHOLDING
# ============================================================

global_T = 100

_, global_threshold = cv2.threshold(
    gray,
    global_T,
    255,
    cv2.THRESH_BINARY
)


# ============================================================
# 3. ADAPTIVE THRESHOLDING - MEAN
# ============================================================

adaptive_threshold = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)


# ============================================================
# 4. GAUSSIAN ADAPTIVE THRESHOLDING
# ============================================================

gaussian_threshold = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)


# ============================================================
# 5. OTSU THRESHOLDING
# ============================================================

otsu_T, otsu_threshold = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
)


# ============================================================
# DISPLAY ALL RESULTS
# ============================================================

plt.figure(figsize=(14, 9))

# Original
plt.subplot(2, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis("off")

# Basic Thresholding
plt.subplot(2, 3, 2)
plt.imshow(basic_threshold, cmap="gray")
plt.title("1. Thresholding (T=128)")
plt.axis("off")

# Global Thresholding
plt.subplot(2, 3, 3)
plt.imshow(global_threshold, cmap="gray")
plt.title("2. Global Thresholding")
plt.axis("off")

# Adaptive Thresholding
plt.subplot(2, 3, 4)
plt.imshow(adaptive_threshold, cmap="gray")
plt.title("3. Adaptive Thresholding")
plt.axis("off")

# Gaussian Adaptive
plt.subplot(2, 3, 5)
plt.imshow(gaussian_threshold, cmap="gray")
plt.title("4. Gaussian Adaptive")
plt.axis("off")

# Otsu
plt.subplot(2, 3, 6)
plt.imshow(otsu_threshold, cmap="gray")
plt.title(f"5. Otsu Threshold (T={otsu_T:.0f})")
plt.axis("off")

plt.tight_layout()
plt.show()


# ============================================================
# PRINT THRESHOLD VALUES
# ============================================================

print("------------------------------------------")
print("       THRESHOLDING RESULTS")
print("------------------------------------------")

print("Basic Threshold       :", T)
print("Global Threshold      :", global_T)
print("Adaptive Threshold    : Local")
print("Gaussian Adaptive     : Local Gaussian")
print("Otsu Optimal Threshold:", otsu_T)

print("------------------------------------------")