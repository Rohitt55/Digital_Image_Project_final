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
values = img.astype(float)
sigma = 20
rng = np.random.default_rng(42)
noise = rng.exponential(sigma, img.shape) - sigma
result = np.clip(np.round(values + noise), 0, 255).astype(np.uint8)

applied_noise = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY).astype(float) - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(float)

# Display the results needed for this experiment.
plt.figure(figsize=(15, 4))

plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('Exponential Noise')
plt.axis("off")

plt.subplot(1, 3, 3)
plt.hist(applied_noise.ravel(), bins=61, range=(-255, 255))
plt.title("Applied grayscale noise")
plt.xlabel("Intensity change")
plt.ylabel("Pixel count")

plt.tight_layout()
plt.show()
