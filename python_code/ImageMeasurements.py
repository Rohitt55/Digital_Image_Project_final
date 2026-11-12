import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab1.pdf, pages 21.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

domain = 'RGB channels'

# Calculation
if domain == 'grayscale':
    result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
else:
    result = img.copy()
values = result.astype(float)
low = float(values.min())
high = float(values.max())
mean = float(values.mean())
variance = float(np.var(values))
std = float(np.std(values))
michelson = (high - low) / (high + low) if high + low else 0.0
details = {'domain': domain, 'mean': mean, 'variance': variance, 'standard_deviation': std,
           'minimum': low, 'maximum': high, 'simple_contrast': high - low,
           'michelson_contrast': michelson, 'rms_contrast': std}

for name, value in details.items():
    print(name + ":", value)


# Display
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
if result.ndim == 3:
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
else:
    plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.hist(result.ravel(), bins=256, range=(0, 256))
plt.title('Image Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

plt.tight_layout()

plt.show()
