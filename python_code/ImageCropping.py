import cv2
import matplotlib.pyplot as plt
from pathlib import Path


# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)

if img is None:
    raise SystemExit("Image not found! Check Img_path.")

# Calculation
# Crop using percentages of the original dimensions.
h, w = img.shape[:2]
left = int(w * 10 / 100)
top = int(h * 10 / 100)
right = max(left + 1, int(w * 90 / 100))
bottom = max(top + 1, int(h * 90 / 100))
result = img[top:bottom, left:right].copy()

marked = img.copy()
cv2.rectangle(marked, (left, top), (right - 1, bottom - 1), (0, 0, 255), 1)

# Display the results needed for this experiment.
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(marked, cv2.COLOR_BGR2RGB))
plt.title("Selected crop region")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title("Cropped image")
plt.axis("off")

plt.tight_layout()
plt.show()
