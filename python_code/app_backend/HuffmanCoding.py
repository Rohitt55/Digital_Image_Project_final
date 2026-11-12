import heapq
from collections import Counter
from BitPacking import pack_bits, unpack_bits


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
