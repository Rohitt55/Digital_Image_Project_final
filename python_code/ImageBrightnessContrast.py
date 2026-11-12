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
alpha = 1.3
beta = 0
values = img.astype(float)
adjusted = alpha * values + beta
result = np.clip(adjusted, 0, 255).astype(np.uint8)

low = np.clip(img.astype(float) * 0.5, 0, 255).astype(np.uint8)
high = np.clip(img.astype(float) * 1.8, 0, 255).astype(np.uint8)
plt.figure(figsize=(10, 8))
for position, (values, title) in enumerate([(img, 'Original Image'), (low, 'Low Contrast (alpha=0.5)'),
                                           (high, 'High Contrast (alpha=1.8)'), (result, 'Selected Brightness / Contrast')], 1):
    plt.subplot(2, 2, position)
    plt.imshow(cv2.cvtColor(values, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
plt.tight_layout()
plt.show()
