import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab1.pdf, pages 46, 47, 48, 49.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

input_mode = 'PDF matrix'
neighbors = 4
size = 3

# Calculation
if input_mode == 'PDF matrix':
    pixels = np.array([[10, 20], [30, 40]], dtype=np.uint8)
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pixels = cv2.resize(gray, (3, 3), interpolation=cv2.INTER_AREA)
h, w = pixels.shape
yy, xx = np.mgrid[:h, :w]
positions = np.column_stack((yy.ravel() / (h - 1), xx.ravel() / (w - 1)))
values = pixels.ravel().astype(float)
if neighbors > len(values):
    # The 2x2 PDF example has only four available samples.
    neighbors = len(values)
interpolated = np.zeros((size, size), dtype=float)
for y in range(size):
    for x in range(size):
        point = np.array([y / (size - 1), x / (size - 1)])
        distances = np.sqrt(np.sum((positions - point) ** 2, axis=1))
        nearest = np.argsort(distances, kind='stable')[:neighbors]
        if distances[nearest[0]] == 0:
            interpolated[y, x] = values[nearest[0]]
        else:
            weights = 1 / distances[nearest]
            interpolated[y, x] = np.sum(weights * values[nearest]) / weights.sum()
result = np.clip(np.round(interpolated), 0, 255).astype(np.uint8)
details = {'source_matrix': pixels.tolist(), 'interpolated_values': interpolated.tolist(),
           'effective_neighbors': neighbors, 'center_value': float(interpolated[size // 2, size // 2])}

print("Source pixels:")
print(pixels)
print("K used:", neighbors)
print("Rounded output:")
print(result)

print('Interpolated floating-point values:')
print(interpolated)

# Display the results of this experiment.
plt.figure(figsize=(10, 4.5))

plt.subplot(1, 2, 1)
plt.imshow(pixels, cmap='gray', vmin=0, vmax=255)
plt.title('Original sample values')
plt.axis("off")
for y in range(pixels.shape[0]):
    for x in range(pixels.shape[1]):
        value = int(pixels[y, x])
        text_color = 'black' if value > 127.5 else 'white'
        plt.text(x, y, str(value), ha='center', va='center', color=text_color, fontsize=8)

plt.subplot(1, 2, 2)
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title('KNN interpolated values')
plt.axis("off")
for y in range(result.shape[0]):
    for x in range(result.shape[1]):
        value = int(result[y, x])
        text_color = 'black' if value > 127.5 else 'white'
        plt.text(x, y, str(value), ha='center', va='center', color=text_color, fontsize=8)

plt.tight_layout()
plt.show()
