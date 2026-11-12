import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

h, w = img.shape[:2]
cropped = img[int(h * 0.1):max(1, int(h * 0.9)), int(w * 0.1):max(1, int(w * 0.9))]
resized = cv2.resize(img, (300, 300))
rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
horizontal = cv2.flip(img, 1)
vertical = cv2.flip(img, 0)
result = resized
print('Original shape:', img.shape)
print('Cropped shape:', cropped.shape)
print('Resized shape:', resized.shape)

# Display
plt.figure(figsize=(15, 8))

plt.subplot(2, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original')
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
plt.title('Cropped')
plt.axis("off")

plt.subplot(2, 3, 3)
plt.imshow(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
plt.title('Resized')
plt.axis("off")

plt.subplot(2, 3, 4)
plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
plt.title('Rotated')
plt.axis("off")

plt.subplot(2, 3, 5)
plt.imshow(cv2.cvtColor(horizontal, cv2.COLOR_BGR2RGB))
plt.title('Horizontal Flip')
plt.axis("off")

plt.subplot(2, 3, 6)
plt.imshow(cv2.cvtColor(vertical, cv2.COLOR_BGR2RGB))
plt.title('Vertical Flip')
plt.axis("off")

plt.tight_layout()

plt.show()
