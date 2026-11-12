import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab1.pdf, pages 52, 54, 55, 56, 57, 58.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

space = 'YCrCb'

# Calculation
methods = {'RGB': cv2.COLOR_BGR2RGB, 'Gray': cv2.COLOR_BGR2GRAY,
           'HSV': cv2.COLOR_BGR2HSV, 'Lab': cv2.COLOR_BGR2LAB, 'YCrCb': cv2.COLOR_BGR2YCrCb}
converted = cv2.cvtColor(img, methods[space])
# The result is the first numerical channel; lab plots show all channels.
result = converted.copy() if space == 'Gray' else converted[:, :, 0].copy()
center = converted[converted.shape[0] // 2, converted.shape[1] // 2]
details = {'color_space': space, 'center_pixel': center.tolist(),
           'channel_order': {'RGB': ['R', 'G', 'B'], 'Gray': ['Gray'], 'HSV': ['H', 'S', 'V'],
                             'Lab': ['L', 'a', 'b'], 'YCrCb': ['Y', 'Cr', 'Cb']}[space]}

print("Color space:", space)
print("Channel order:", details["channel_order"])
print("Center pixel:", center)

# Compare the color-space displays shown in the example.
hsv_display = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lab_display = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
gray_display = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# HSV and Lab here are encoded-channel visualizations, not natural RGB colors.

# Display
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('RGB')
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(gray_display, cmap="gray", vmin=0, vmax=255)
plt.title('Grayscale')
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(hsv_display)
plt.title('HSV (encoded channel display)')
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(lab_display)
plt.title('LAB (encoded channel display)')
plt.axis("off")

plt.tight_layout()

# Inspect Y, Cr and Cb separately when YCrCb is selected.
if space == 'YCrCb':
    plt.figure(figsize=(15, 4))
    for index, name in enumerate(['Y', 'Cr', 'Cb']):
        plt.subplot(1, 3, index + 1)
        plt.imshow(converted[:, :, index], cmap='gray', vmin=0, vmax=255)
        plt.title('YCrCb: ' + name)
        plt.colorbar()
        plt.axis('off')
    plt.tight_layout()
plt.show()
