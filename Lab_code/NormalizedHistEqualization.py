# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 01:08:34 2026

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

# Number of gray levels
L = 256

# Total number of pixels
MN = pixels.size

# Display as grayscale image 
plt.figure(figsize=(8, 8))
plt.imshow(pixels, cmap='gray', vmin=0, vmax=255) 


# Histogram
hist = np.bincount(pixels.ravel(),minlength=L)

# Cumulative frequency
cdf = np.cumsum(hist)

# Minimum non-zero CDF
cdf_min = cdf[cdf > 0][0]

print("Total Pixels =", MN)
print("CDF_min =", cdf_min)

# Normalized histogram equalization
mapping = np.round(((cdf - cdf_min) /(MN - cdf_min)) * (L - 1))

# Keep values between 0 and 255
mapping = np.clip(mapping, 0, 255).astype(np.uint8)

# Apply mapping
equalized = mapping[pixels]

print("\nOriginal Image:")
print(pixels)

print("\nNormalized Equalized Image:")
print(equalized)

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

plt.subplot(2,3,6)
print("\nIntensity Mapping:")

for v in np.unique(pixels):
    print(f"{v:3d}  "
        f"Frequency={hist[v]:2d}  "
        f"CDF={cdf[v]:2d}  "
        f"New Value={mapping[v]:3d}"
    )

plt.tight_layout()
plt.show()


