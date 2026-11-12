import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

sample32 = cv2.resize(img, (32, 32), interpolation=cv2.INTER_NEAREST)
sample64 = cv2.resize(img, (64, 64), interpolation=cv2.INTER_NEAREST)
result = cv2.resize(img, (1024, 1024), interpolation=cv2.INTER_NEAREST)
print('Sampling sizes: 32 x 32, 64 x 64, 1024 x 1024')

# Display
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(cv2.cvtColor(sample32, cv2.COLOR_BGR2RGB))
plt.title('Sampled 32 x 32')
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(cv2.cvtColor(sample64, cv2.COLOR_BGR2RGB))
plt.title('Sampled 64 x 64')
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('Sampled 1024 x 1024')
plt.axis("off")

plt.tight_layout()

plt.show()
