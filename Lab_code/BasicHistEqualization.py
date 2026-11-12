# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 00:26:07 2026

@author: Administrator
"""

import numpy as np 
import matplotlib.pyplot as plt 

# 8×8 pixel intensity matrix 
pixels = np.array([ 
[52, 55, 61, 59, 79, 61, 76, 61], 
[62, 59, 55, 104, 94, 85, 59, 71], 
[63, 65, 66, 113, 144, 104, 63, 72], 
[64, 70, 70, 126, 154, 109, 71, 69], 
[67, 73, 68, 106, 122, 88, 68, 68], 
[68, 79, 60, 70, 77, 66, 58, 75], 
[69, 85, 64, 58, 55, 61, 65, 83], 
[70, 87, 69, 68, 65, 73, 78, 90] ], dtype=np.uint8) 


#Show pixels
print("Pixel Values:") 
print(pixels)

# Display as grayscale image 
plt.figure(figsize=(8, 8))
plt.imshow(pixels, cmap='gray', vmin=0, vmax=255) 

for i in range(8):
    for j in range(8):
        value = int(pixels[i, j])
        plt.text(j, i,str(pixels[i, j]),ha="center",va="center",
            color="black" if pixels[i,j] > 127 else "white"
        )
plt.xticks(range(8))
plt.yticks(range(8))
plt.title("8×8 Image Pixel Values")
plt.grid()

plt.show()

# Count each intensity value
values, counts = np.unique(pixels, return_counts=True)

for value, count in zip(values, counts):
    print(f"Pixel Value = {value}, Count = {count}")
 
     # Histogram
    L=256
hist = np.bincount(pixels.ravel(), minlength=L)

print("Histogram:")
print(hist)

# --------------------------------------------------
# 8. Four Plots
# --------------------------------------------------

plt.figure(figsize=(16, 8))

plt.subplot(2,3,1)
plt.imshow(pixels, cmap='gray', vmin=0, vmax=255) 

for i in range(pixels.shape[0]):
    for j in range(pixels.shape[1]):

        value = int(pixels[i, j])

        if value > 127:
            text_color = "black"
        else:
            text_color = "white"

        plt.text(
            j,
            i,
            str(value),
            ha="center",
            va="center",
            color=text_color,
            fontsize=9
        )

plt.xticks(range(8))
plt.yticks(range(8))
plt.title("Original Image + Pixel Values")
#plt.grid()

plt.subplot(2,3,2)
plt.hist(pixels)

# Probability
pdf = hist / pixels.size

# CDF
cdf = np.cumsum(pdf)

# Print CDF for values that actually occur
for intensity in np.unique(pixels):
    print(
        f"Intensity = {intensity:3d}, "
        f"Frequency = {hist[intensity]:2d}, "
        f"CDF = {cdf[intensity]:.4f}"
    )

# Plot CDF
plt.subplot(2,3,3)
plt.plot(cdf)
plt.xlabel("Pixel Intensity")
plt.ylabel("CDF")
plt.title("Cumulative Distribution Function")
plt.grid()

# Histogram equalization formula
s = (L - 1) * cdf

# Convert to integer pixel values
s_round = np.round(s).astype(np.uint8)

# Apply mapping to image
equalized = s[pixels]

plt.tight_layout()

plt.subplot(2,3,4)
plt.imshow(equalized, cmap='gray', vmin=0, vmax=255)
plt.title("Equalized")
for i in range(equalized.shape[0]):
    for j in range(equalized.shape[1]):

        value = int(equalized[i, j])

        if value > 127:
            text_color = "black"
        else:
            text_color = "white"

        plt.text(
            j,
            i,
            str(value),
            ha="center",
            va="center",
            color=text_color,
            fontsize=9
        )
        
plt.subplot(2,3,5)
plt.hist(equalized)
plt.title("Equalized")

plt.tight_layout()
plt.show()
#eqlized_hist = np.bincount(equalized.ravel(), minlength=L)
print("Original:")
print(pixels)

print("\nEqualized:")
print(equalized)
