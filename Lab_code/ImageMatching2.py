# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 20:26:51 2026

@author: Administrator
"""
import cv2
import matplotlib.pyplot as plt
import os
import numpy as np

# ============================================================
# Image Paths
# ============================================================

Img1 = r"D:/DIPLab/Image/sunflower1.jpg"   # Source image
Img2 = r"D:/DIPLab/Image/sunflower2.jpg"   # Reference image

# ============================================================
# Check Files
# ============================================================

if not os.path.isfile(Img1):
    raise FileNotFoundError(
        f"Source image not found: {Img1}"
    )

if not os.path.isfile(Img2):
    raise FileNotFoundError(
        f"Reference image not found: {Img2}"
    )

# ============================================================
# Read Images as Grayscale
# ============================================================

sourceImage = cv2.imread(
    Img1,
    cv2.IMREAD_GRAYSCALE
)

referenceImage = cv2.imread(
    Img2,
    cv2.IMREAD_GRAYSCALE
)

# ============================================================
# Check Image Loading
# ============================================================

if sourceImage is None:
    raise ValueError("Could not load source image.")

if referenceImage is None:
    raise ValueError("Could not load reference image.")

# ============================================================
# Display Original Image Sizes
# ============================================================

print("Original Source Shape   :", sourceImage.shape)
print("Original Reference Shape:", referenceImage.shape)

# ============================================================
# Resize Reference Image
# Make both images the same size
# ============================================================

height, width = sourceImage.shape

referenceImage = cv2.resize(
    referenceImage,
    (width, height)
)

print("After Resize:")
print("Source Shape   :", sourceImage.shape)
print("Reference Shape:", referenceImage.shape)

# ============================================================
# Display Images
# ============================================================

plt.figure(figsize=(10, 4))

plt.subplot(2, 2, 1)
plt.imshow(sourceImage, cmap="gray")
plt.title("Source Image")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(referenceImage, cmap="gray")
plt.title("Reference Image")
plt.axis("off")

# ============================================================
# Display Histograms
# ============================================================

plt.subplot(2, 2, 2)
plt.hist(sourceImage.ravel(), 256, [0, 256])
plt.title("Source Histogram")
plt.xlabel("Intensity")
plt.ylabel("Frequency")

plt.subplot(2, 2, 4)
plt.hist(referenceImage.ravel(), 256, [0, 256])
plt.title("Reference Histogram")
plt.xlabel("Intensity")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()

# ============================================================
# Pixel Comparison
# ============================================================

# Tolerance
tolerance = 5

# Convert to int16 to avoid uint8 overflow
source = sourceImage.astype(np.int16)
reference = referenceImage.astype(np.int16)

# Absolute pixel difference
difference = np.abs(source - reference)

# ============================================================
# Find Similar Pixels
# ============================================================

# A pixel is similar if difference <= tolerance
similar = difference <= tolerance

# ============================================================
# Calculate Pixel Statistics
# ============================================================

similar_pixels = np.sum(similar)

total_pixels = similar.size

different_pixels = total_pixels - similar_pixels

similarity_percentage = (
    similar_pixels / total_pixels
) * 100

# ============================================================
# Display Results
# ============================================================

print("\n====================================")
print("       PIXEL SIMILARITY RESULT")
print("====================================")

print("Similar pixels  :", similar_pixels)
print("Different pixels:", different_pixels)
print("Total pixels    :", total_pixels)
print("Tolerance       :", tolerance)
print("Similarity (%)  :", similarity_percentage)

print("====================================")






