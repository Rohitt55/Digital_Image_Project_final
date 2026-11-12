import cv2
import matplotlib.pyplot as plt
from pathlib import Path


# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)

if img is None:
    raise SystemExit("Image not found! Check Img_path.")

# Calculation
# Resize the image
width = 400
height = 300
result = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

print("Original size (width, height):", img.shape[1], img.shape[0])
print("Resized size (width, height):", result.shape[1], result.shape[0])

# Display the results needed for this experiment.
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title(f"Original: {img.shape[1]} x {img.shape[0]}")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title(f"Resized: {result.shape[1]} x {result.shape[0]}")
plt.axis("off")

plt.tight_layout()
plt.show()
