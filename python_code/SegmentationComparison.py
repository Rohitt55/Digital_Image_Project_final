import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

fraction = 0.5
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


watershed_result = result.copy()
seed_x = 50
seed_y = 50
tolerance = 15
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


region_result = result.copy()
clusters = 3
h, w = img.shape[:2]
scale = min(1.0, 512 / max(h, w))
analysis = cv2.resize(img, (max(1, round(w * scale)), max(1, round(h * scale))), interpolation=cv2.INTER_AREA)
pixels = analysis.reshape((-1, 3)).astype(np.float32)
if len(pixels) < clusters:
    raise ValueError('K must not exceed the number of image pixels.')
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
cv2.setRNGSeed(42)
compactness, labels, centers = cv2.kmeans(pixels, clusters, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
colors = np.clip(np.round(centers), 0, 255).astype(np.uint8)
result = colors[labels.ravel()].reshape(analysis.shape)
details = {'clusters': clusters, 'centers_rgb': colors[:, ::-1].tolist(),
           'compactness': float(compactness), 'analysis_size': [analysis.shape[1], analysis.shape[0]]}


distance_display = cv2.normalize(distance, None, 0, 255, cv2.NORM_MINMAX)
print('IMAGE SEGMENTATION RESULTS')
print('Watershed: Marker-based segmentation')
print('Region Growing: Seed-based segmentation')
print('K-Means: Clustering-based segmentation')
print('K:', clusters)
print('Seed Point:', (sx, sy))
print('Region Threshold:', tolerance)

# Display
plt.figure(figsize=(15, 8))

plt.subplot(2, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(binary, cmap="gray", vmin=0, vmax=255)
plt.title('Binary Image')
plt.axis("off")

plt.subplot(2, 3, 3)
plt.imshow(cv2.cvtColor(watershed_result, cv2.COLOR_BGR2RGB))
plt.title('Watershed Segmentation')
plt.axis("off")

plt.subplot(2, 3, 4)
plt.imshow(region_result, cmap="gray", vmin=0, vmax=255)
plt.title('Region Growing')
plt.axis("off")

plt.subplot(2, 3, 5)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('K-Means Segmentation (K=3)')
plt.axis("off")

plt.subplot(2, 3, 6)
plt.imshow(distance_display, cmap="gray", vmin=0, vmax=255)
plt.title('Distance Transform')
plt.axis("off")

plt.tight_layout()

plt.show()
