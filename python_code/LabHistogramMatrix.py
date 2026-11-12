import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab2.pdf, pages 11, 12.
# This experiment uses the exact matrix from the PDF.


# Calculation
pixels = np.array([[2, 3, 4, 4, 6], [1, 2, 4, 5, 6], [1, 1, 5, 6, 6],
                   [0, 1, 3, 3, 4], [0, 1, 2, 3, 4]], dtype=np.uint8)
hist = np.bincount(pixels.ravel(), minlength=7)
result = pixels.copy()
details = {'pixel_matrix': pixels.tolist(), 'histogram': hist.tolist(), 'total_pixels': int(pixels.size)}

print("PDF 5 x 5 pixels:")
print(pixels)
print("Pixel value / Count")
for value, count in enumerate(hist):
    print(value, count)


# Display the results of this experiment.
plt.figure(figsize=(10, 4.5))

plt.subplot(1, 2, 1)
plt.imshow(pixels, cmap='gray', vmin=0, vmax=6)
plt.title('PDF 5 x 5 matrix')
plt.axis("off")
for y in range(pixels.shape[0]):
    for x in range(pixels.shape[1]):
        value = int(pixels[y, x])
        text_color = 'black' if value > 3.0 else 'white'
        plt.text(x, y, str(value), ha='center', va='center', color=text_color, fontsize=8)

plt.subplot(1, 2, 2)
plt.bar(np.arange(7), hist)
plt.xticks(range(7))
plt.xlabel('Pixel value')
plt.ylabel('Count')
plt.title('Exact histogram')

plt.tight_layout()
plt.show()
