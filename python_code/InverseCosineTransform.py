import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import fft


# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)

if img is None:
    raise SystemExit("Image not found! Check Img_path.")

# Calculation
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(float)
coefficients = fft.dctn(gray, type=2, norm='ortho')
h, w = gray.shape
retain = 50
rows = max(1, round(h * retain / 100))
cols = max(1, round(w * retain / 100))
retained = np.zeros_like(coefficients)
retained[:rows, :cols] = coefficients[:rows, :cols]
reconstructed = fft.idctn(retained, type=2, norm='ortho')
result = np.clip(np.round(reconstructed), 0, 255).astype(np.uint8)
print("Reconstruction MSE:", np.mean((gray - reconstructed) ** 2))

retained_spectrum = np.log1p(np.abs(retained))
retained_spectrum = cv2.normalize(retained_spectrum, None, 0, 255, cv2.NORM_MINMAX)

# Display the results needed for this experiment.
plt.figure(figsize=(15, 4))

plt.subplot(1, 3, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title("Grayscale input")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(retained_spectrum, cmap="gray", vmin=0, vmax=255)
plt.title("Retained DCT magnitude")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title("IDCT reconstruction")
plt.axis("off")

plt.tight_layout()
plt.show()
