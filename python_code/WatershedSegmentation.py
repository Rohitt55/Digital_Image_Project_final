import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab2.pdf, pages 51, 52, 53, 54, 55.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

fraction = 0.5

# Calculation
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel = np.ones((3, 3), dtype=np.uint8)
opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
sure_bg = cv2.dilate(opening, kernel, iterations=3)
distance = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, foreground = cv2.threshold(distance, fraction * distance.max(), 255, cv2.THRESH_BINARY)
foreground = foreground.astype(np.uint8)
unknown = cv2.subtract(sure_bg, foreground)
count, markers = cv2.connectedComponents(foreground)
markers = markers + 1
markers[unknown == 255] = 0
markers = cv2.watershed(img.copy(), markers)
result = img.copy()
result[markers == -1] = [0, 0, 255]
details = {'foreground_markers': int(count - 1), 'boundary_pixels': int(np.count_nonzero(markers == -1)),
           'note': 'Uniform or heavily textured images may have no useful foreground markers.'}

print("Foreground markers:", count - 1)
print("Boundary pixels:", details["boundary_pixels"])


# Display the results of this experiment.
plt.figure(figsize=(10, 9.0))

plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original')
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(binary, cmap='gray', vmin=0, vmax=255)
plt.title('Inverted Otsu mask')
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(foreground, cmap='gray', vmin=0, vmax=255)
plt.title('Foreground markers')
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('Watershed boundaries')
plt.axis("off")

plt.tight_layout()
plt.show()
