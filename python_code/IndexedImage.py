import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab1.pdf, pages 28, 29, 30.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

input_mode = 'PDF matrix'

# Calculation
if input_mode == 'PDF matrix':
    indexed = np.array([[0, 1, 1, 2], [2, 3, 1, 0], [1, 2, 3, 3], [0, 1, 2, 3]], dtype=np.uint8)
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    indexed = (gray.astype(np.uint16) * 4 // 256).astype(np.uint8)
palette = np.array([[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255]], dtype=np.uint8)
rgb = palette[indexed]
result = rgb[:, :, ::-1].copy()
details = {'index_matrix': indexed.tolist() if indexed.size <= 256 else None,
           'palette_rgb': palette.tolist(), 'input': input_mode}

print("Index matrix:")
print(indexed)
print("RGB palette:")
print(palette)


# Display
plt.figure(figsize=(5, 4))

plt.subplot(1, 1, 1)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('Indexed Image')
plt.xlabel("Column")
plt.ylabel("Row")
if indexed.size <= 256:
    for y in range(indexed.shape[0]):
        for x in range(indexed.shape[1]):
            plt.text(x, y, str(indexed[y, x]), ha='center', va='center', color='white', fontweight='bold')

plt.tight_layout()

plt.show()
