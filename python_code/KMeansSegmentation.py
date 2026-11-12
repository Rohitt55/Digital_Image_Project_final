import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab2.pdf, pages 58, 59.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

clusters = 3

# Calculation
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

print("Cluster centers (RGB):")
print(colors[:, ::-1])
print("Compactness:", compactness)


# Display the results of this experiment.
plt.figure(figsize=(15, 4.5))

plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(analysis, cv2.COLOR_BGR2RGB))
plt.title('Analysis input')
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('K-means segmented image')
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(colors[np.newaxis, :, ::-1])
plt.xticks(range(clusters))
plt.yticks([])
plt.title('Cluster colors')

plt.tight_layout()
plt.show()
