import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab1.pdf, pages 43, 44, 45.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

input_mode = 'PDF matrix'
connectivity = '4'

# Calculation
if input_mode == 'PDF matrix':
    pixels = np.array([[10, 20, 30], [15, 25, 35], [20, 30, 40]], dtype=np.uint8)
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pixels = cv2.resize(gray, (3, 3), interpolation=cv2.INTER_AREA)
h, w = pixels.shape
offsets = [(1, 0), (0, 1)]
if connectivity == '8':
    offsets += [(1, 1), (1, -1)]
edges = []
for y in range(h):
    for x in range(w):
        for dy, dx in offsets:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w:
                edges.append([[y, x], [ny, nx]])
result = pixels.copy()
details = {'pixel_matrix': pixels.tolist(), 'node_count': int(pixels.size),
           'edge_count': len(edges), 'edges': edges, 'connectivity': connectivity}

print("Pixel matrix:")
print(pixels)
print("Nodes:", pixels.size)
print("Edges:", len(edges))


# Display
plt.figure(figsize=(5, 4))

plt.subplot(1, 1, 1)
for first, second in edges:
    y1, x1 = first
    y2, x2 = second
    plt.plot([x1, x2], [-y1, -y2], color='gray')
for y in range(h):
    for x in range(w):
        plt.scatter(x, -y, s=800, color='lightblue', edgecolors='black', zorder=3)
        plt.text(x, -y, f'({y},{x})', ha='center', va='center', zorder=4)
plt.title(connectivity + '-connectivity graph')
plt.axis('equal')
plt.axis('off')
plt.margins(0.25)

plt.tight_layout()

plt.show()
