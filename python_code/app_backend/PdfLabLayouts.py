"""Presentation layouts checked against the rendered lab PDF sample figures."""
import cv2
import numpy as np

from ConvertToGray import gray
from RunOperation import execute
from LimitImageSize import bounded


def layout_reference(key):
    references = {
        'negative': (1, [19]), 'noise_models': (1, [24, 26, 27]), 'binary_matrix': (1, [22]),
        'indexed_image': (1, [28, 29]), 'pixel_connectivity': (1, [43, 45]),
        'pixel_matrix': (1, [32, 35, 36]), 'sampling': (1, [38, 41]), 'quantization': (1, [38, 42]),
        'knn_interpolation': (1, [47, 50, 51]), 'color_spaces': (1, [56]),
        'rgb_to_hsi': (1, [59, 65]), 'hsi_to_rgb': (1, [66]), 'contrast': (2, [3, 5]),
        'image_measurements': (2, [8, 9]), 'histogram': (2, [11, 12]), 'lab_histogram_matrix': (2, [11, 12]),
        'stretch': (2, [13, 14]), 'clahe': (2, [10]), 'matching': (2, [30, 33, 34, 36]),
        'equalize_basic': (2, [23, 26, 28, 29]), 'lab_basic_equalization': (2, [23, 26, 28, 29]),
        'equalize': (2, [16, 20, 21, 22]), 'lab_normalized_equalization': (2, [16, 20, 21, 22])
    }
    for operation in ('resize', 'crop', 'rotate', 'flip', 'mean', 'gaussian', 'median', 'bilateral'):
        references[operation] = (2, [37, 38, 41])
    for operation in ('sobel', 'prewitt', 'roberts', 'canny'):
        references[operation] = (2, [42, 46])
    for operation in ('threshold', 'adaptive', 'adaptive_mean', 'otsu'):
        references[operation] = (2, [47, 50])
    for operation in ('watershed', 'region_growing', 'kmeans'):
        references[operation] = (2, [51, 59])
    if key not in references:
        return None
    lab, pages = references[key]
    return {'source': f'DIP-Lab{lab}.pdf', 'pages': pages,
            'url': f'/api/lab/source/{lab}#page={pages[0]}'}


def pdf_panels(key, original, result, params, details, reference):
    from LabOutput import image_panel, histogram_panel, cdf_panel

    def calculated(operation, settings=None):
        return execute(operation, original, settings or {}, reference)[0]

    source = gray(original)
    if key == 'negative':
        values = source if result.ndim == 2 else original
        return [image_panel('Original Image', values), image_panel('Negative Image', result)]
    if key == 'sampling':
        return [image_panel('Original Image', original),
                image_panel('Sampled 32 x 32', cv2.resize(original, (32, 32), interpolation=cv2.INTER_NEAREST)),
                image_panel('Sampled 64 x 64', cv2.resize(original, (64, 64), interpolation=cv2.INTER_NEAREST)),
                image_panel('Sampled 1024 x 1024', result)]
    if key == 'knn_interpolation' and params['input'] == 'Uploaded 8x8 image':
        size = result.shape[0]
        values = cv2.resize(original, (size, size), interpolation=cv2.INTER_LINEAR)
        samples = cv2.resize(original, (8, 8), interpolation=cv2.INTER_AREA)
        nearest = cv2.resize(samples, (size, size), interpolation=cv2.INTER_NEAREST)
        low, high = size // 3, size * 2 // 3
        return [image_panel('Original Image', values), image_panel('Downsampled to 8 x 8', samples),
                image_panel(f"KNN Interpolated (K={params['neighbors']})", result),
                image_panel('Original Close-up', values[low:high, low:high]),
                image_panel('Nearest Neighbor Close-up', nearest[low:high, low:high]),
                image_panel('KNN Close-up', result[low:high, low:high]),
                image_panel('Original Comparison', values), image_panel('Nearest Neighbor Comparison', nearest),
                image_panel('KNN Comparison', result)]
    if key == 'histogram':
        return [image_panel('Grayscale Image', source), histogram_panel('Image Histogram', source)]
    if key in ('equalize_basic', 'equalize', 'lab_basic_equalization', 'lab_normalized_equalization'):
        fixed = key.startswith('lab_')
        values = np.array(details['original_matrix'], np.uint8) if fixed else source
        cdf = cdf_panel('Cumulative Distribution Function', values)
        if key in ('equalize', 'lab_normalized_equalization'):
            cdf['values'] = np.cumsum(np.bincount(values.ravel(), minlength=256))
            cdf['probability'] = False
            cdf['ylabel'] = 'Cumulative pixel count'
        return [image_panel('Original Image + Pixel Values', values), histogram_panel('Original Histogram', values), cdf,
                image_panel('Equalized', result), histogram_panel('Equalized Histogram', result)]
    if key in ('stretch', 'clahe'):
        before = original if key == 'stretch' else source
        return [image_panel('Original Image', before), histogram_panel('Original Histogram', before),
                image_panel('Stretched Image' if key == 'stretch' else 'CLAHE Image', result), histogram_panel('Processed Histogram', result)]
    if key == 'image_measurements':
        values = result.ravel()
        counts = np.bincount(values, minlength=256)
        return [image_panel('Original Image', result), {'kind': 'histogram', 'title': 'Image Histogram', 'values': counts}]
    if key == 'matching':
        target = cv2.resize(gray(reference), (source.shape[1], source.shape[0]))
        return [image_panel('Source Image', source), histogram_panel('Source Histogram', source),
                image_panel('Reference Image', target), histogram_panel('Reference Histogram', target)]
    if key == 'pixel_matrix':
        left = image_panel('Original Grayscale Image', source)
        left['axes'] = True
        right = image_panel(f'{result.shape[1]} x {result.shape[0]} Digital Image with Pixel Values', result)
        right.update(axes=True, matrix_ticks=True)
        return [left, right]
    if key == 'binary_matrix':
        values = np.array(details['binary_matrix'], np.uint8)
        panel = image_panel('Binary Image', values)
        panel.update(vmax=1, axes=True, annotate=False, matrix_ticks=True)
        return [panel]
    if key == 'indexed_image':
        if details['index_matrix'] is not None:
            indices = np.array(details['index_matrix'])
        else:
            indices = (source.astype(np.uint16) * 4 // 256).astype(np.uint8)
        panel = image_panel('Indexed Image', result)
        panel.update(axes=True, matrix_ticks=indices.size <= 256,
                     index_labels=indices if indices.size <= 256 else None)
        return [panel]
    if key == 'pixel_connectivity':
        return [{'kind': 'graph', 'title': params['connectivity'] + '-connectivity graph',
                 'pixels': result, 'edges': details['edges'], 'coordinate_labels': True}]
    if key == 'noise_models':
        return [image_panel('Original Image', source), image_panel(params['model'] + ' Noise Added', gray(result))]
    if key == 'contrast':
        low = np.clip(original.astype(float) * 0.5, 0, 255).astype(np.uint8)
        high = np.clip(original.astype(float) * 1.8, 0, 255).astype(np.uint8)
        return [image_panel('Original Image', original), image_panel('Low Contrast (alpha=0.5)', low),
                image_panel('High Contrast (alpha=1.8)', high), image_panel(f"Selected: alpha={params['alpha']}, beta={params['beta']}", result)]
    if key in ('resize', 'crop', 'rotate', 'flip'):
        # The six-view transformation comparison in the second PDF.
        crop = result if key == 'crop' else calculated('crop')
        resized = result if key == 'resize' else calculated('resize', {'width': 300, 'height': 300})
        rotated = result if key == 'rotate' else calculated('rotate', {'angle': '90'})
        horizontal = result if key == 'flip' and params['axis'] == 'horizontal' else cv2.flip(original, 1)
        vertical = result if key == 'flip' and params['axis'] == 'vertical' else cv2.flip(original, 0)
        panels = [image_panel('Original', original), image_panel('Cropped', crop),
                  image_panel(f'Resized ({resized.shape[1]} x {resized.shape[0]})', resized),
                  image_panel(f"Rotated ({params['angle'] if key == 'rotate' else '90'} degrees)", rotated),
                  image_panel('Horizontal Flip', horizontal), image_panel('Vertical Flip', vertical)]
        if key == 'flip' and params['axis'] == 'both':
            panels.append(image_panel('Both-axis Flip (selected)', result))
        return panels
    if key == 'quantization':
        values = source if params['domain'] == 'grayscale' else original
        panels = []
        for bit in range(8, 0, -1):
            if bit == int(params['bits']):
                output = result
            else:
                levels = 2 ** bit
                indices = np.floor(values.astype(float) * levels / 256)
                output = np.round(indices * 255 / (levels - 1)).astype(np.uint8)
            panels.append(image_panel(f'{bit}-bit' + (' (selected)' if bit == int(params['bits']) else ''), output))
        return panels
    if key in ('mean', 'gaussian', 'median', 'bilateral'):
        panels = [image_panel('Original', original)]
        for operation, label in [('mean', 'Mean Filter'), ('gaussian', 'Gaussian Filter'), ('median', 'Median Filter'), ('bilateral', 'Bilateral Filter')]:
            output = result if operation == key else calculated(operation)
            panels.append(image_panel(label + (' (selected)' if operation == key else ''), output))
        return panels
    if key in ('sobel', 'prewitt', 'roberts', 'canny') or key == 'laplacian' and params['mode'] == 'edge magnitude':
        panels = [image_panel('Original', original)]
        for operation, label in [('sobel', 'Sobel'), ('prewitt', 'Prewitt'), ('roberts', 'Roberts'), ('canny', 'Canny')]:
            output = result if operation == key else calculated(operation)
            panels.append(image_panel(label + (' (selected)' if operation == key else ''), output))
        if key == 'laplacian':
            panels.append(image_panel('Laplacian (selected)', result))
        return panels
    if key in ('threshold', 'adaptive', 'adaptive_mean', 'otsu'):
        basic_t = params['threshold'] if key == 'threshold' else 128
        basic = result if key == 'threshold' else calculated('threshold', {'threshold': basic_t})
        global_mask = calculated('threshold', {'threshold': 100})
        mean = result if key == 'adaptive_mean' else calculated('adaptive_mean')
        gaussian = result if key == 'adaptive' else calculated('adaptive')
        if key == 'otsu':
            otsu, cutoff = result, details['selected_threshold']
        else:
            otsu, info = execute('otsu', original, {})
            cutoff = info['selected_threshold']
        return [image_panel('Original Image', original), image_panel(f'Thresholding (T={basic_t})', basic),
                image_panel('Global Thresholding (T=100)', global_mask), image_panel('Adaptive Thresholding (Mean)', mean),
                image_panel('Gaussian Adaptive Thresholding', gaussian), image_panel(f'Otsu Threshold (T={cutoff:g})', otsu)]
    if key in ('watershed', 'region_growing', 'kmeans'):
        analysis = bounded(original, 512)
        gray_values = gray(analysis)
        _, binary = cv2.threshold(gray_values, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
        distance = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        distance_display = cv2.normalize(distance, None, 0, 255, cv2.NORM_MINMAX)
        watershed = result if key == 'watershed' else execute('watershed', analysis, {})[0]
        region = result if key == 'region_growing' else execute('region_growing', analysis, {})[0]
        clustered = result if key == 'kmeans' else execute('kmeans', analysis, {})[0]
        k = params['clusters'] if key == 'kmeans' else 3
        return [image_panel('Original Image', analysis), image_panel('Binary Image', binary), image_panel('Watershed Segmentation', watershed),
                image_panel('Region Growing', region), image_panel(f'K-Means Segmentation (K={k})', clustered), image_panel('Distance Transform', distance_display)]
    if key == 'color_spaces':
        hsv = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(original, cv2.COLOR_BGR2LAB)
        encoded_hsv = image_panel('HSV (encoded channel display)', hsv)
        encoded_lab = image_panel('LAB (encoded channel display)', lab)
        encoded_hsv['encoded_rgb'] = True
        encoded_lab['encoded_rgb'] = True
        panels = [image_panel('RGB', original), image_panel('Grayscale', source), encoded_hsv, encoded_lab]
        if params['space'] == 'YCrCb':
            encoded = image_panel('YCrCb (encoded channel display)', cv2.cvtColor(original, cv2.COLOR_BGR2YCrCb))
            encoded['encoded_rgb'] = True
            panels += [encoded, image_panel('Y luminance (selected output)', result)]
        return panels
    if key == 'hsi_to_rgb':
        from RGBToHSI import hsi_components
        _, _, intensity = hsi_components(original)
        if params['input'] == 'Numeric HSI':
            intensity = np.full(original.shape[:2], params['intensity'])
        left = image_panel('Original Intensity (I)', intensity)
        left.update(vmax=1, annotate=False)
        return [left, image_panel('HSI to RGB', result)]
    return None


def mapping_tables(key, original, result, details):
    """Keep long mapping tables legible beside the figure instead of squeezing them into an image panel."""
    if key not in ('equalize_basic', 'equalize', 'lab_basic_equalization', 'lab_normalized_equalization'):
        return []
    values = np.array(details['original_matrix'], np.uint8) if key.startswith('lab_') else gray(original)
    hist = np.bincount(values.ravel(), minlength=256)
    cumulative = np.cumsum(hist)
    normalized = key in ('equalize', 'lab_normalized_equalization')
    first = int(cumulative[cumulative > 0][0])
    if normalized and first == values.size:
        mapped = np.arange(256)
    elif normalized:
        mapped = np.clip(np.round((cumulative - first) / (values.size - first) * 255), 0, 255)
    else:
        mapped = np.round(cumulative * 255 / values.size)
    rows = []
    for value in np.flatnonzero(hist):
        rows.append([int(value), int(hist[value]), int(cumulative[value]), round(float(cumulative[value] / values.size), 6), int(mapped[value])])
    return [{'title': 'Intensity and equalization mapping',
             'columns': ['Pixel intensity', 'Frequency', 'Cumulative count', 'CDF probability', 'Equalized intensity'], 'rows': rows}]
