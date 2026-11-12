import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)

if img is None:
    raise SystemExit("Image not found! Check Img_path.")

# Calculation
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bits = 3
levels = 2 ** bits
indices = np.floor(gray.astype(float) * levels / 256)
result = np.round(indices * 255 / (levels - 1)).astype(np.uint8)
print("Intensity levels:", levels)

# Compare 8-bit through 1-bit quantization, as in the example.
plt.figure(figsize=(16, 8))
for position, bit in enumerate(range(8, 0, -1), 1):
    level_count = 2 ** bit
    q = np.floor(gray.astype(float) * level_count / 256)
    quantized = np.round(q * 255 / (level_count - 1)).astype(np.uint8)
    plt.subplot(2, 4, position)
    plt.imshow(quantized, cmap='gray', vmin=0, vmax=255)
    plt.title(str(bit) + '-bit')
    plt.axis('off')
plt.tight_layout()
plt.show()
