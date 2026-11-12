import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')

mean = cv2.blur(img, (5, 5))
gaussian = cv2.GaussianBlur(img, (5, 5), 0)
median = cv2.medianBlur(img, 5)
bilateral = cv2.bilateralFilter(img, 9, 75, 75)
result = mean

# Display
plt.figure(figsize=(15, 8))

plt.subplot(2, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original')
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(cv2.cvtColor(mean, cv2.COLOR_BGR2RGB))
plt.title('Mean Filter')
plt.axis("off")

plt.subplot(2, 3, 3)
plt.imshow(cv2.cvtColor(gaussian, cv2.COLOR_BGR2RGB))
plt.title('Gaussian Filter')
plt.axis("off")

plt.subplot(2, 3, 4)
plt.imshow(cv2.cvtColor(median, cv2.COLOR_BGR2RGB))
plt.title('Median Filter')
plt.axis("off")

plt.subplot(2, 3, 5)
plt.imshow(cv2.cvtColor(bilateral, cv2.COLOR_BGR2RGB))
plt.title('Bilateral Filter')
plt.axis("off")

plt.tight_layout()

plt.show()
