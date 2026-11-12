def pack_bits(bits):
    """Store eight bits in each byte, starting with the highest bit."""
    bits = list(bits)
    output = bytearray((len(bits) + 7) // 8)
    for index, bit in enumerate(bits):
        byte_index = index // 8
        bit_position = 7 - index % 8
        output[byte_index] |= int(bit) << bit_position
    return (bytes(output), len(bits))


def unpack_bits(data, count):
    bits = []
    for index in range(count):
        byte_index = index // 8
        bit_position = 7 - index % 8
        bit = (data[byte_index] >> bit_position) & 1
        bits.append(bit)
    return bits


import heapq
from collections import Counter



def huffman_encode(values):
    """Merge the two least frequent nodes until one coding tree remains."""
    counts = Counter(values)
    heap = []
    for index, (value, count) in enumerate(sorted(counts.items())):
        heap.append((count, index, value))
    heapq.heapify(heap)
    serial = len(heap)
    while len(heap) > 1:
        left_count, _, left_node = heapq.heappop(heap)
        right_count, _, right_node = heapq.heappop(heap)
        parent = (left_node, right_node)
        heapq.heappush(heap, (left_count + right_count, serial, parent))
        serial += 1
    table = {}

    def visit(node, prefix):
        if isinstance(node, int):
            table[node] = prefix or '0'
        else:
            visit(node[0], prefix + '0')
            visit(node[1], prefix + '1')
    visit(heap[0][2], '')
    bits = []
    for value in values:
        for bit in table[value]:
            bits.append(int(bit))
    payload, count = pack_bits(bits)
    codes = {}
    for symbol, code in table.items():
        codes[str(symbol)] = code
    return payload, {'bit_count': count, 'codes': codes}


def huffman_decode(payload, metadata):
    reverse = {}
    for symbol, code in metadata['codes'].items():
        reverse[code] = int(symbol)
    prefix = ''
    result = []
    for bit in unpack_bits(payload, metadata['bit_count']):
        prefix += str(bit)
        if prefix in reverse:
            result.append(reverse[prefix])
            prefix = ''
    if prefix:
        raise ValueError('Incomplete Huffman stream.')
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
payload, metadata = huffman_encode(pixels)
decoded = huffman_decode(payload, metadata)
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
