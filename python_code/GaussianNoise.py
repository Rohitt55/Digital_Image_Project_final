import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    raise SystemExit("Image not found! Check Img_path.")

# Calculation
values = img.astype(float)
sigma = 2
rng = np.random.default_rng(42)
noise = rng.normal(0, sigma, img.shape)
result = np.clip(np.round(values + noise), 0, 255).astype(np.uint8)


# Sample the actual original and noisy images for printed output.
original_sample = cv2.resize(img.astype(float), (3, 3), interpolation=cv2.INTER_AREA)
noisy_sample = cv2.resize(result.astype(float), (3, 3), interpolation=cv2.INTER_AREA)
print('Image Shape:', img.shape)
print('3 x 3 Pixel Values:')
print(original_sample)
print('3 x 3 Applied Noise (after clipping):')
print(noisy_sample - original_sample)
print('3 x 3 Image with Noisy Values:')
print(noisy_sample)

# Display
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(img, cmap="gray", vmin=0, vmax=255)
plt.title('Original Image')
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title('Gaussian Noise Added')
plt.axis("off")

plt.tight_layout()

plt.show()
