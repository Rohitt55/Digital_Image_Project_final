import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('kmeans', 'K-means color segmentation', 'Edges & segmentation',
           'Group RGB pixels into K clusters and replace each pixel with its cluster center. Analysis is limited to a 512-pixel side.', 'Minimize sum of squared distances to K cluster centers', 'DIP-Lab2.pdf',
           [field('clusters', 'Color clusters (K)', 3, 2, 12, 1)], requires_reference=False)
def kmeans(image, params, reference):
    clusters = params['clusters']
    h, w = image.shape[:2]
    scale = min(1.0, 512 / max(h, w))
    analysis = cv2.resize(image, (max(1, round(w * scale)), max(1, round(h * scale))), interpolation=cv2.INTER_AREA)
    pixels = analysis.reshape((-1, 3)).astype(np.float32)
    if len(pixels) < clusters:
        raise ValueError('K must not exceed the number of image pixels.')
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    cv2.setRNGSeed(42)
    compactness, labels, centers = cv2.kmeans(pixels, clusters, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    colors = np.clip(np.round(centers), 0, 255).astype(np.uint8)
    result = colors[labels.ravel()].reshape(analysis.shape)
    details = {'clusters': clusters, 'centers_rgb': colors[:, ::-1].tolist(),
               'compactness': float(compactness), 'analysis_size': [analysis.shape[1], analysis.shape[0]]}
    return result, details
