import numpy as np
from OperationRegistry import operation, choice
from ConvertToGray import gray
from LimitImageSize import bounded
from SaveEncodedImage import artifact
from RunLengthCoding import rle_encode, rle_decode
from HuffmanCoding import huffman_encode, huffman_decode
from ArithmeticCoding import arithmetic_encode, arithmetic_decode
from LZWCoding import lzw_encode, lzw_decode


SOURCE='Chap7-Image Compression.pdf'

GROUP='Compression'

@operation('lossless_coding','RLE / Huffman / arithmetic / LZW coding',GROUP,'Encode and independently decode a bounded grayscale image. Report payload size and exported file size separately.', 'Lossless decode(encode(pixels)) = pixels',SOURCE,
           [
               choice('codec','Coding method','Huffman',['RLE','Huffman','Arithmetic','LZW']),
               choice('size','Maximum analysis side','128',['32','64','128'])
           ])
def lossless_coding(image, params, reference):
    # Prepare a small grayscale image for the teaching 
    maximum = int(params['size'])
    small = bounded(image, maximum)
    values = gray(small)
    pixels = values.ravel().tolist()
    method = params['codec']
    if method == 'RLE':
        payload, metadata = rle_encode(pixels)
        decoded = rle_decode(payload)
    elif method == 'Huffman':
        payload, metadata = huffman_encode(pixels)
        decoded = huffman_decode(payload, metadata)
    elif method == 'Arithmetic':
        payload, metadata = arithmetic_encode(pixels)
        decoded = arithmetic_decode(payload, metadata)
    else:
        payload, metadata = lzw_encode(pixels)
        decoded = lzw_decode(payload)
    # Restore the decoded pixel list to the original analysis shape.
    decoded_pixels = np.array(decoded, dtype=np.uint8)
    output = decoded_pixels.reshape(values.shape)
    download, size = artifact(method, values.shape, payload, metadata)
    return (output, {
        'raw_grayscale_bytes': int(values.size),
        'coded_payload_bytes': len(payload),
        'exported_file_bytes': size,
        'payload_compression_ratio': values.size / max(1, len(payload)),
        'file_compression_ratio': values.size / size,
        'payload_bits_per_pixel': len(payload) * 8 / values.size,
        'relative_payload_redundancy': 1 - len(payload) / values.size,
        'lossless_round_trip': bool(np.array_equal(output, values)),
        'artifact': download,
        'note': 'Losslessness is relative to the bounded grayscale analysis image. Export includes dimensions, code metadata and base64 payload; metadata overhead can exceed any compression saving. LZW uses fixed 16-bit codes.'
    })
