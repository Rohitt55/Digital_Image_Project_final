import struct


def lzw_encode(values):
    """Build a dictionary of byte sequences and output 16-bit codes."""
    dictionary = {}
    for index in range(256):
        dictionary[bytes([index])] = index
    next_code = 256
    current = b''
    codes = []
    for value in values:
        symbol = bytes([value])
        combined = current + symbol
        if combined in dictionary:
            current = combined
        else:
            codes.append(dictionary[current])
            if next_code < 65536:
                dictionary[combined] = next_code
                next_code += 1
            current = symbol
    if current:
        codes.append(dictionary[current])
    output = bytearray()
    for code in codes:
        output.extend(struct.pack('>H', code))
    payload = bytes(output)
    return (payload, {
        'code_count': len(codes),
        'dictionary_size': next_code,
        'code_width_bits': 16
    })


def lzw_decode(payload):
    codes = []
    for index in range(0, len(payload), 2):
        code = struct.unpack('>H', payload[index:index + 2])[0]
        codes.append(code)
    if not codes:
        return []
    dictionary = {}
    for index in range(256):
        dictionary[index] = bytes([index])
    current = dictionary[codes[0]]
    output = bytearray(current)
    next_code = 256
    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = current + current[:1]
        else:
            raise ValueError('Invalid LZW code.')
        output.extend(entry)
        if next_code < 65536:
            dictionary[next_code] = current + entry[:1]
            next_code += 1
        current = entry
    return list(output)


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
payload, metadata = lzw_encode(pixels)
decoded = lzw_decode(payload)
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
