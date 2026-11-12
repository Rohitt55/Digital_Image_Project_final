import numpy as np
import cv2
import matplotlib.pyplot as plt
from pathlib import Path


# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)

if img is None:
    raise SystemExit("Image not found! Check Img_path.")

# Calculation
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
threshold, result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print("Selected threshold:", threshold)

print("Foreground pixels:", np.count_nonzero(result))
print("Background pixels:", result.size - np.count_nonzero(result))

# Display the results needed for this experiment.
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(gray, cmap="gray", vmin=0, vmax=255)
plt.title("Grayscale input")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title('Otsu Threshold')
plt.axis("off")

plt.tight_layout()
plt.show()
