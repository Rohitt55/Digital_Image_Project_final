import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab1.pdf, pages 66, 67, 68.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

input_mode = 'Image round trip'
hue = 60
saturation = 0.5
intensity = 0.5

# Calculation
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(float) / 255
R, G, B = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
I = (R + G + B) / 3
total = R + G + B
S = np.zeros_like(I)
mask = total > 0
S[mask] = 1 - 3 * np.minimum(np.minimum(R, G), B)[mask] / total[mask]
numerator = 0.5 * ((R - G) + (R - B))
denominator = np.sqrt((R - G) ** 2 + (R - B) * (G - B))
ratio = np.divide(numerator, denominator, out=np.ones_like(I), where=denominator > 1e-12)
theta = np.arccos(np.clip(ratio, -1, 1))
H = np.degrees(np.where(B <= G, theta, 2 * np.pi - theta))
H[S <= 1e-12] = 0
if input_mode == 'Numeric HSI':
    H = np.full(img.shape[:2], hue, dtype=float)
    S = np.full(img.shape[:2], saturation, dtype=float)
    I = np.full(img.shape[:2], intensity, dtype=float)
angle = np.radians(H % 360)
R = np.zeros_like(I)
G = np.zeros_like(I)
B = np.zeros_like(I)
for sector in range(3):
    selected = (angle >= sector * 2 * np.pi / 3) & (angle < (sector + 1) * 2 * np.pi / 3)
    local = angle[selected] - sector * 2 * np.pi / 3
    low = I[selected] * (1 - S[selected])
    high = I[selected] * (1 + S[selected] * np.cos(local) / np.cos(np.pi / 3 - local))
    middle = 3 * I[selected] - low - high
    if sector == 0:
        R[selected], G[selected], B[selected] = high, middle, low
    elif sector == 1:
        R[selected], G[selected], B[selected] = low, high, middle
    else:
        R[selected], G[selected], B[selected] = middle, low, high
rgb_values = np.stack((R, G, B), axis=2)
clipped = int(np.count_nonzero((rgb_values < -1e-10) | (rgb_values > 1 + 1e-10)))
rgb_result = np.clip(np.round(rgb_values * 255), 0, 255).astype(np.uint8)
result = cv2.cvtColor(rgb_result, cv2.COLOR_RGB2BGR)
details = {'clipped_channel_values': clipped, 'note': 'HSI combinations outside the RGB gamut are clipped for display.'}
details['input'] = input_mode
details['center_rgb'] = rgb_result[result.shape[0] // 2, result.shape[1] // 2].tolist()
if input_mode == 'Image round trip':
    details['reconstruction_mse'] = float(np.mean((img.astype(float) - result.astype(float)) ** 2))

print("Input mode:", input_mode)
print("Center RGB:", details["center_rgb"])
print("Clipped channel values:", clipped)
if input_mode == "Image round trip":
    print("Reconstruction MSE:", details["reconstruction_mse"])


# Display
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(I, cmap="gray", vmin=0, vmax=1)
plt.title('Original Intensity (I)')
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('HSI to RGB')
plt.axis("off")

plt.tight_layout()

plt.show()
