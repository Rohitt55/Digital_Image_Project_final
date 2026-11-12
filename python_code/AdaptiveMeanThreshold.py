import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab2.pdf, pages 47, 49.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

kernel = 11
constant = 2

# Calculation
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
result = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, kernel, constant)
details = {'foreground_pixels': int(np.count_nonzero(result)), 'background_pixels': int(result.size - np.count_nonzero(result))}

print("Foreground pixels:", details["foreground_pixels"])
print("Background pixels:", details["background_pixels"])


# Display the results of this experiment.
plt.figure(figsize=(10, 4.5))

plt.subplot(1, 2, 1)
plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
plt.title('Grayscale input')
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title('Adaptive mean threshold')
plt.axis("off")

plt.tight_layout()
plt.show()
