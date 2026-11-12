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
# OpenCV hue values range from 0 to 179.
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hue = hsv[:, :, 0]
result = np.round(hue.astype(float) * 255 / 179).astype(np.uint8)

# Display the results needed for this experiment.
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title('Color Channel')
plt.axis("off")

plt.tight_layout()
plt.show()
