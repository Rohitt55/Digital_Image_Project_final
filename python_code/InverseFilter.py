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
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(float)
kernel_size = 5
g = cv2.getGaussianKernel(kernel_size, max(kernel_size / 6, 0.5))
psf = g @ g.T
kernel = np.zeros(gray.shape, dtype=float)
kernel[:kernel_size, :kernel_size] = psf
kernel = np.roll(kernel, (-(kernel_size // 2), -(kernel_size // 2)), axis=(0, 1))
transfer = np.fft.fft2(kernel)

# Blur the image and add repeatable Gaussian noise.
blurred = np.fft.ifft2(np.fft.fft2(gray) * transfer).real
rng = np.random.default_rng(42)
observed = blurred + rng.normal(0, 3, gray.shape)
regularization = 0.01

inverse = np.divide(1, transfer, out=np.zeros_like(transfer),
                    where=np.abs(transfer) >= regularization)

restored = np.fft.ifft2(np.fft.fft2(observed) * inverse).real
result = np.clip(np.round(restored), 0, 255).astype(np.uint8)
print("Degraded MSE:", np.mean((observed - gray) ** 2))
print("Restored MSE:", np.mean((restored - gray) ** 2))

# Display the results needed for this experiment.
plt.figure(figsize=(15, 4))

plt.subplot(1, 3, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title("Original grayscale")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(np.clip(observed, 0, 255), cmap="gray", vmin=0, vmax=255)
plt.title("Blurred + noisy observation")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title('Inverse Filter restoration')
plt.axis("off")

plt.tight_layout()
plt.show()
