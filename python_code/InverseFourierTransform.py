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
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
transformed = np.fft.fft2(gray)
reconstructed = np.fft.ifft2(transformed).real
result = np.clip(np.round(reconstructed), 0, 255).astype(np.uint8)
mse = np.mean((reconstructed - gray.astype(float)) ** 2)
print("Reconstruction MSE:", mse)

# Display the results needed for this experiment.
plt.figure(figsize=(15, 4))

plt.subplot(1, 3, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title("Grayscale input")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title("IDFT reconstruction")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(np.abs(gray.astype(float) - result.astype(float)), cmap="gray", vmin=0, vmax=255)
plt.title("Absolute error (0 to 255)")
plt.axis("off")

plt.tight_layout()
plt.show()
