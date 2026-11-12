import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('pixel_connectivity', 'Pixel connectivity graph', 'Fundamentals',
           'Draw 4-connected or 8-connected pixel neighbors for the PDF matrix or a small sampled image.', '4-neighbors: (x+/-1,y), (x,y+/-1); 8-neighbors also include diagonals', 'DIP-Lab1.pdf',
           [choice('input', 'Input', 'PDF matrix', ['PDF matrix', 'Uploaded image']), choice('connectivity', 'Connectivity', '4', ['4', '8'])], requires_reference=False)
def pixel_connectivity(image, params, reference):
    input_mode = params['input']
    connectivity = params['connectivity']
    if input_mode == 'PDF matrix':
        pixels = np.array([[10, 20, 30], [15, 25, 35], [20, 30, 40]], dtype=np.uint8)
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        pixels = cv2.resize(gray, (3, 3), interpolation=cv2.INTER_AREA)
    h, w = pixels.shape
    offsets = [(1, 0), (0, 1)]
    if connectivity == '8':
        offsets += [(1, 1), (1, -1)]
    edges = []
    for y in range(h):
        for x in range(w):
            for dy, dx in offsets:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w:
                    edges.append([[y, x], [ny, nx]])
    result = pixels.copy()
    details = {'pixel_matrix': pixels.tolist(), 'node_count': int(pixels.size),
               'edge_count': len(edges), 'edges': edges, 'connectivity': connectivity}
    return result, details
