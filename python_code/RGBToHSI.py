import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab1.pdf, pages 59, 60, 61, 62, 63, 64, 65.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

channel = 'Intensity'

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
selected = {'Hue': H / 360, 'Saturation': S, 'Intensity': I}[channel]
result = np.clip(np.round(selected * 255), 0, 255).astype(np.uint8)
cy, cx = I.shape[0] // 2, I.shape[1] // 2
details = {'hue_degrees': float(H[cy, cx]), 'saturation': float(S[cy, cx]), 'intensity': float(I[cy, cx])}

print("Center pixel H, S, I:", H[cy, cx], S[cy, cx], I[cy, cx])


# Display the results of this experiment.
plt.figure(figsize=(10, 9.0))

plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original RGB display')
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(H, cmap='hsv', vmin=0, vmax=360)
plt.title('Hue (degrees)')
plt.axis("off")
plt.colorbar()

plt.subplot(2, 2, 3)
plt.imshow(S, cmap='gray', vmin=0, vmax=1)
plt.title('Saturation')
plt.axis("off")
plt.colorbar()

plt.subplot(2, 2, 4)
plt.imshow(I, cmap='gray', vmin=0, vmax=1)
plt.title('Intensity')
plt.axis("off")
plt.colorbar()

plt.tight_layout()
plt.show()
