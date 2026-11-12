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
# Circular low-pass filter
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h, w = gray.shape
yy, xx = np.ogrid[:h, :w]
radius = min(h, w) * 10 / 100
mask = (xx - w // 2) ** 2 + (yy - h // 2) ** 2 <= radius ** 2
spectrum = np.fft.fftshift(np.fft.fft2(gray))
filtered = spectrum * mask
reconstructed = np.fft.ifft2(np.fft.ifftshift(filtered)).real
result = np.clip(np.round(reconstructed), 0, 255).astype(np.uint8)

# Display the results needed for this experiment.
plt.figure(figsize=(15, 4))

plt.subplot(1, 3, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title("Grayscale input")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(mask.astype(np.uint8) * 255, cmap="gray", vmin=0, vmax=255)
plt.title("Low-pass frequency mask")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title("Low-pass result")
plt.axis("off")

plt.tight_layout()
plt.show()
