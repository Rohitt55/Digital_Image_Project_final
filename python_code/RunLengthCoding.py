import struct


def rle_encode(values):
    # Count consecutive repetitions of each value.
    pairs = []
    for value in values:
        if pairs and pairs[-1][1] == value:
            count = pairs[-1][0] + 1
            pairs[-1] = (count, value)
        else:
            pairs.append((1, value))

    # Store each count in four bytes and its pixel value in one byte.
    output = bytearray()
    for count, value in pairs:
        output.extend(struct.pack('>IB', count, value))
    payload = bytes(output)
    metadata = {'runs': len(pairs)}
    return payload, metadata


def rle_decode(payload):
    result = []
    for index in range(0, len(payload), 5):
        count, value = struct.unpack('>IB', payload[index:index + 5])
        result.extend([value] * count)
    return result


import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# Change Img_path to use your own image.
Img_path = str(Path(__file__).resolve().parents[1] / 'images' / 'sample.png')
img = cv2.imread(Img_path)

if img is None:
    raise SystemExit("Image not found! Check Img_path.")

# Encode and decode a small grayscale image.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
small = cv2.resize(gray, (128, 128), interpolation=cv2.INTER_AREA)
pixels = small.ravel().tolist()
payload, metadata = rle_encode(pixels)
decoded = rle_decode(payload)
result = np.array(decoded, dtype=np.uint8).reshape(small.shape)
print("Raw bytes:", small.nbytes)
print("Encoded payload bytes:", len(payload))
print("Lossless round trip:", np.array_equal(small, result))

# Display the results needed for this experiment.
plt.figure(figsize=(15, 4))

plt.subplot(1, 3, 1)
plt.imshow(small, cmap="gray", vmin=0, vmax=255)
plt.title("Grayscale encoding input")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(result, cmap="gray", vmin=0, vmax=255)
plt.title("Decoded image")
plt.axis("off")

plt.subplot(1, 3, 3)
bars = plt.bar(["Raw pixels", "Coded payload"], [small.nbytes, len(payload)])
plt.bar_label(bars, padding=3)
plt.title("Storage size")
plt.ylabel("Bytes")
plt.margins(y=0.2)

plt.tight_layout()
plt.show()
