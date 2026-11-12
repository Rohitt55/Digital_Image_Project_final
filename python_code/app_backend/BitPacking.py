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
