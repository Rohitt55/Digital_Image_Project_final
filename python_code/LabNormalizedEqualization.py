import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab2.pdf, pages 15, 16, 17, 18, 19, 20, 21, 22.
# This experiment uses the exact matrix from the PDF.


# Calculation
pixels = np.array([
    [52, 55, 61, 59, 79, 61, 76, 61],
    [62, 59, 55, 104, 94, 85, 59, 71],
    [63, 65, 66, 113, 144, 104, 63, 72],
    [64, 70, 70, 126, 154, 109, 71, 69],
    [67, 73, 68, 106, 122, 88, 68, 68],
    [68, 79, 60, 70, 77, 66, 58, 75],
    [69, 85, 64, 58, 55, 61, 65, 83],
    [70, 87, 69, 68, 65, 73, 78, 90]
], dtype=np.uint8)
hist = np.bincount(pixels.ravel(), minlength=256)
cumulative = np.cumsum(hist)
cdf_min = int(cumulative[cumulative > 0][0])
mapped = (cumulative - cdf_min) / (pixels.size - cdf_min) * 255
mapping = np.clip(np.round(mapped), 0, 255).astype(np.uint8)
result = mapping[pixels]
details = {'original_matrix': pixels.tolist(), 'equalized_matrix': result.tolist(),
           'cdf_min': cdf_min, 'total_pixels': int(pixels.size),
           'intensities': np.flatnonzero(hist).tolist(), 'histogram': hist.tolist(),
           'cumulative_counts': cumulative.tolist(), 'mapping': mapping.tolist()}

print("Original PDF pixels:")
print(pixels)
print("CDF minimum:", cdf_min)
print("Equalized pixels:")
print(result)

print('Intensity  Count  Cumulative count  Mapped intensity')
for value in np.flatnonzero(hist):
    print(value, hist[value], cumulative[value], mapping[value])

counts = np.bincount(pixels.ravel(), minlength=256)
cumulative_counts = np.cumsum(counts)
cdf_values = cumulative_counts

# Display
plt.figure(figsize=(15, 8))

plt.subplot(2, 3, 1)
plt.imshow(pixels, cmap="gray", vmin=0, vmax=255)
plt.title('Original Image + Pixel Values')
plt.xlabel("Column")
plt.ylabel("Row")
for y in range(pixels.shape[0]):
    for x in range(pixels.shape[1]):
        value = int(pixels[y, x])
        plt.text(x, y, str(value), ha='center', va='center',
                 color='black' if value > 127.5 else 'white', fontsize=8)

plt.subplot(2, 3, 2)
plt.hist(pixels.ravel(), bins=256, range=(0, 256))
plt.title('Original Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.subplot(2, 3, 3)
plt.plot(cdf_values)
plt.title('Cumulative Distribution Function')
plt.xlabel('Pixel Intensity')
plt.ylabel('Cumulative Count')
plt.grid(alpha=0.25)

plt.subplot(2, 3, 4)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title('Equalized')
plt.xlabel("Column")
plt.ylabel("Row")
for y in range(result.shape[0]):
    for x in range(result.shape[1]):
        value = int(result[y, x])
        plt.text(x, y, str(value), ha='center', va='center',
                 color='black' if value > 127.5 else 'white', fontsize=8)

plt.subplot(2, 3, 5)
plt.hist(result.ravel(), bins=256, range=(0, 256))
plt.title('Equalized Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.tight_layout()

# Display the mapping table in three readable blocks, as in the example.
present = np.flatnonzero(counts)
table_rows = [[int(value), int(counts[value]), int(cumulative_counts[value]), int(mapping[value])]
              for value in present]
plt.figure(figsize=(15, 6))
for block, rows in enumerate(np.array_split(np.array(table_rows), 3)):
    plt.subplot(1, 3, block + 1)
    plt.axis('off')
    table = plt.table(cellText=rows.tolist(), colLabels=['Intensity', 'Count', 'CDF count', 'Mapped'],
                      loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.8)
plt.suptitle('Intensity and Equalization Mapping')
plt.tight_layout()
plt.show()
