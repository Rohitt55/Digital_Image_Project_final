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


import bisect
from collections import Counter



def arithmetic_encode(values):
    """Narrow a 32-bit interval for each symbol and emit its stable bits."""
    counts = Counter(values)
    symbols = sorted(counts)
    frequencies = []
    for symbol in symbols:
        frequencies.append(counts[symbol])
    cumulative = [0]
    for frequency in frequencies:
        cumulative.append(cumulative[-1] + frequency)
    indexes = {}
    for index, symbol in enumerate(symbols):
        indexes[symbol] = index
    total = len(values)
    low = 0
    high = (1 << 32) - 1
    pending = 0
    bits = []
    half = 1 << 31
    quarter = 1 << 30
    three_quarters = 3 * quarter

    def emit(bit):
        nonlocal pending
        bits.append(bit)
        bits.extend([1 - bit] * pending)
        pending = 0
    for value in values:
        # Select this symbol's subinterval using cumulative frequencies.
        index = indexes[value]
        width = high - low + 1
        high = low + width * cumulative[index + 1] // total - 1
        low = low + width * cumulative[index] // total
        while True:
            # Emit a stable leading bit, or defer bits near the midpoint.
            if high < half:
                emit(0)
            elif low >= half:
                emit(1)
                low -= half
                high -= half
            elif low >= quarter and high < three_quarters:
                pending += 1
                low -= quarter
                high -= quarter
            else:
                break
            low *= 2
            high = high * 2 + 1
    pending += 1
    emit(0 if low < quarter else 1)
    payload, count = pack_bits(bits)
    return (payload, {'symbols': symbols, 'frequencies': frequencies, 'symbol_count': total, 'bit_count': count})


def arithmetic_decode(payload, metadata):
    """Reverse interval updates using the frequencies stored in metadata."""
    symbols = metadata['symbols']
    cumulative = [0]
    for frequency in metadata['frequencies']:
        cumulative.append(cumulative[-1] + frequency)
    total = cumulative[-1]
    bits = unpack_bits(payload, metadata['bit_count'])
    position = 0

    def read():
        nonlocal position
        if position < len(bits):
            bit = bits[position]
        else:
            bit = 0
        position += 1
        return bit
    code = 0
    for _ in range(32):
        code = code * 2 + read()
    low = 0
    high = (1 << 32) - 1
    half = 1 << 31
    quarter = 1 << 30
    three_quarters = 3 * quarter
    result = []
    for _ in range(metadata['symbol_count']):
        width = high - low + 1
        scaled = ((code - low + 1) * total - 1) // width
        index = bisect.bisect_right(cumulative, scaled) - 1
        result.append(symbols[index])
        high = low + width * cumulative[index + 1] // total - 1
        low = low + width * cumulative[index] // total
        while True:
            if high < half:
                pass
            elif low >= half:
                low -= half
                high -= half
                code -= half
            elif low >= quarter and high < three_quarters:
                low -= quarter
                high -= quarter
                code -= quarter
            else:
                break
            low *= 2
            high = high * 2 + 1
            code = code * 2 + read()
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
payload, metadata = arithmetic_encode(pixels)
decoded = arithmetic_decode(payload, metadata)
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
