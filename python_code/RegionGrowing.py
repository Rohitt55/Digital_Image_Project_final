import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab2.pdf, pages 55, 56, 57.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

seed_x = 50
seed_y = 50
tolerance = 15

# Calculation
h0, w0 = img.shape[:2]
scale = min(1.0, 512 / max(h0, w0))
analysis = cv2.resize(img, (max(1, round(w0 * scale)), max(1, round(h0 * scale))), interpolation=cv2.INTER_AREA)
gray = cv2.cvtColor(analysis, cv2.COLOR_BGR2GRAY)
h, w = gray.shape
sx = min(w - 1, int(w * seed_x / 100))
sy = min(h - 1, int(h * seed_y / 100))
seed_value = int(gray[sy, sx])
result = np.zeros_like(gray)
visited = np.zeros_like(gray, dtype=bool)
stack = [(sx, sy)]
while stack:
    x, y = stack.pop()
    if x < 0 or x >= w or y < 0 or y >= h or visited[y, x]:
        continue
    visited[y, x] = True
    if abs(int(gray[y, x]) - seed_value) <= tolerance:
        result[y, x] = 255
        stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
details = {'seed_xy': [sx, sy], 'seed_intensity': seed_value,
           'region_pixels': int(np.count_nonzero(result)), 'total_pixels': int(result.size)}

print("Seed coordinates:", sx, sy)
print("Seed intensity:", seed_value)
print("Region pixels:", details["region_pixels"])

marked = analysis.copy()
cv2.circle(marked, (sx, sy), max(1, min(h, w) // 50), (0, 0, 255), -1)
segmented = cv2.bitwise_and(analysis, analysis, mask=result)

# Display the results of this experiment.
plt.figure(figsize=(15, 4.5))

plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(marked, cv2.COLOR_BGR2RGB))
plt.title('Seed location')
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title('Grown region mask')
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(segmented, cv2.COLOR_BGR2RGB))
plt.title('Selected region')
plt.axis("off")

plt.tight_layout()
plt.show()
