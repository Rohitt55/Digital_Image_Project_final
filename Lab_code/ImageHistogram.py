# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 09:26:32 2026

@author: Administrator
"""

import numpy as np
import matplotlib.pyplot as plt

# 5×5 grayscale image
image = np.array([
    [2, 3, 4, 4, 6],
    [1, 2, 4, 5, 6],
    [1, 1, 5, 6, 6],
    [0, 1, 3, 3, 4],
    [0, 1, 2, 3, 4]
])

# Calculate histogram
hist = np.bincount(image.flatten(), minlength=7)

print("Histogram")
print("----------------")
print("Pixel Value\tCount")
for i, count in enumerate(hist):
    print(f"{i}\t\t{count}")

# Display Image and Histogram
plt.figure(figsize=(10,4))

# Image
plt.subplot(1,2,1)
plt.imshow(image, cmap='gray', vmin=0, vmax=6)
plt.title("Grayscale Image")
plt.xticks(range(5))
plt.yticks(range(5))

# Histogram
plt.subplot(1,2,2)
plt.bar(range(len(hist)), hist, width=0.8, color='gray', edgecolor='black')
plt.title("Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Count")
plt.xticks(range(7))
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()