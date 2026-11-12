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
quality = 80
ok, encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality])
if not ok:
    raise SystemExit("JPEG compression failed.")
result = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
mse = np.mean((img.astype(float) - result.astype(float)) ** 2)
print("JPEG bytes:", encoded.size)
print("Raw pixel bytes:", img.nbytes)
print("MSE:", mse)

# Display the results needed for this experiment.
plt.figure(figsize=(15, 4))

plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('JPEGCompression')
plt.axis("off")

plt.subplot(1, 3, 3)
bars = plt.bar(["Raw pixels", "JPEG file"], [img.nbytes, encoded.size])
plt.bar_label(bars, padding=3)
plt.title("Storage size")
plt.ylabel("Bytes")
plt.margins(y=0.2)

plt.tight_layout()
plt.show()
