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
