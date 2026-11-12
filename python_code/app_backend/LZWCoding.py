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
