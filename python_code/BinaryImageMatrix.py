import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab1.pdf, pages 22.
# This experiment uses the exact matrix from the PDF.


# Calculation
pixels = np.array([[0, 1, 0, 0], [1, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]], dtype=np.uint8)
result = pixels * 255
details = {'binary_matrix': pixels.tolist(), 'foreground_pixels': int(np.count_nonzero(pixels))}

print("Binary pixels:")
print(pixels)
print("Foreground pixels:", details["foreground_pixels"])


# Display
plt.figure(figsize=(5, 4))

plt.subplot(1, 1, 1)
plt.imshow(pixels, cmap="gray", vmin=0, vmax=1)
plt.title('Binary Image')
plt.xlabel("Column")
plt.ylabel("Row")

plt.tight_layout()

plt.show()
