import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# DIP-Lab1.pdf, pages 14, 15, 18.
# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)
if img is None:
    raise SystemExit('Image not found! Check Img_path.')


# Calculation
result = img.copy()
ok, encoded = cv2.imencode('.png', result)
if not ok:
    raise ValueError('Could not encode the image.')
details = {'width': img.shape[1], 'height': img.shape[0], 'png_bytes': int(encoded.size)}

# Save the result to the project Results folder.
Output_folder = Path(__file__).resolve().parents[1] / 'Results'
Output_folder.mkdir(exist_ok=True)
Output_path = Output_folder / 'LabImageCopy.png'
if not cv2.imwrite(str(Output_path), result):
    raise SystemExit('Could not save the image.')
print('Saved image:', Output_path)
print("Image shape:", img.shape)
print("PNG bytes:", encoded.size)


# Display the results of this experiment.
plt.figure(figsize=(10, 4.5))

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Read image')
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('Saved PNG copy')
plt.axis("off")

plt.tight_layout()
plt.show()
