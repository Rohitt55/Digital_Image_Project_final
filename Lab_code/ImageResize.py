# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 17:18:36 2026

@author: Administrator
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

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

# Down sampling
small = cv2.resize(img,(100,100))

# Display
plt.subplot(1,2,1)
plt.imshow(img, cmap='gray')
plt.title("Original")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(small, cmap='gray')
plt.title("Sampled Image")
plt.axis("off")

plt.show()