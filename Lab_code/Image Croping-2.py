# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 12:35:20 2026

@author: Administrator
"""

import cv2
import matplotlib.pyplot as plt
import os

Img_path=r"D:/DIPLab/Image/rice.tiff";

img = cv2.imread(Img_path)

if img is None:
    print("Image not found!")
else:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.imshow(img)
    plt.axis("off")
    plt.show()
    

# -----------------------------------
# Smoothing Filters
# -----------------------------------

# 1. Average (Mean) Filter
average = cv2.blur(img, (5,5))

# 2. Gaussian Filter
gaussian = cv2.GaussianBlur(img, (5,5), 0)

# 3. Median Filter
median = cv2.medianBlur(img, 5)

# 4. Bilateral Filter
bilateral = cv2.bilateralFilter(img, 9, 75, 75)

# -----------------------------------
# Display Results
# -----------------------------------

plt.figure(figsize=(15,10))

plt.subplot(2,3,1)
plt.imshow(img)
plt.title("Original")
plt.axis("off")

plt.subplot(2,3,2)
plt.imshow(average)
plt.title("Average")

plt.axis("off")

plt.subplot(2,3,3)
plt.imshow(gaussian)
plt.title("Gaussian")
plt.axis("off")

plt.subplot(2,3,4)
plt.imshow(median)
plt.title("Median")
plt.axis("off")

plt.subplot(2,3,5)
plt.imshow(bilateral)
plt.title("Bilateral")
plt.axis("off")

plt.tight_layout()
plt.show()



# -------------------------------------------------
# Crop Image
# -------------------------------------------------
cropped = img[100:350, 150:450]

# -------------------------------------------------
# Resize Image
# -------------------------------------------------
resized = cv2.resize(img, (300, 300))

# -------------------------------------------------
# Rotate Image (90° Clockwise)
# -------------------------------------------------
rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# -------------------------------------------------
# Flip Image
# -------------------------------------------------

# Horizontal Flip
flip_horizontal = cv2.flip(img, 1)

# Vertical Flip
flip_vertical = cv2.flip(img, 0)

# Both Horizontal and Vertical
flip_both = cv2.flip(img, -1)

# -------------------------------------------------
# Display Images
# -------------------------------------------------

plt.figure(figsize=(15,10))

plt.subplot(2,3,1)
plt.imshow(img)
plt.title("Original")
plt.axis("off")

plt.subplot(2,3,2)
plt.imshow(cropped)
plt.title("Cropped")
plt.axis("off")

plt.subplot(2,3,3)
plt.imshow(resized)
plt.title("Resized")
plt.axis("off")

plt.subplot(2,3,4)
plt.imshow(rotated)
plt.title("Rotated")
plt.axis("off")

plt.subplot(2,3,5)
plt.imshow(flip_horizontal)
plt.title("Horizontal Flip")
plt.axis("off")

plt.subplot(2,3,6)
plt.imshow(flip_vertical)
plt.title("Vertical Flip")
plt.axis("off")

plt.tight_layout()
plt.show()

# -------------------------------------------------
# Save Images
# -------------------------------------------------

output_folder = r"D:\DIPLab\Results"
os.makedirs(output_folder, exist_ok=True)

cv2.imwrite(os.path.join(output_folder, "cropped.jpg"),
            cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR))

cv2.imwrite(os.path.join(output_folder, "resized.jpg"),
            cv2.cvtColor(resized, cv2.COLOR_RGB2BGR))

cv2.imwrite(os.path.join(output_folder, "rotated.jpg"),
            cv2.cvtColor(rotated, cv2.COLOR_RGB2BGR))

cv2.imwrite(os.path.join(output_folder, "flip_horizontal.jpg"),
            cv2.cvtColor(flip_horizontal, cv2.COLOR_RGB2BGR))

cv2.imwrite(os.path.join(output_folder, "flip_vertical.jpg"),
            cv2.cvtColor(flip_vertical, cv2.COLOR_RGB2BGR))

cv2.imwrite(os.path.join(output_folder, "flip_both.jpg"),
            cv2.cvtColor(flip_both, cv2.COLOR_RGB2BGR))

print("Image transformations completed successfully.")