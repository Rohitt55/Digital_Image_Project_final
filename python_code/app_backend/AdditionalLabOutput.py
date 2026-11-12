"""Plots for the missing Lab 1 and Lab 2 experiments."""
import cv2
import numpy as np


def additional_panels(key, original, result, params, details, reference):
    from LabOutput import image_panel, histogram_panel, cdf_panel

    if key == 'image_read_save':
        return [image_panel('Read image', original), image_panel('PNG copy for download', result)]
    if key == 'image_measurements':
        rows = [[name.replace('_', ' '), f'{value:.6g}' if isinstance(value, float) else str(value)] for name, value in details.items() if name != 'processing_ms']
        return [image_panel('Measurement input', result), {'kind': 'table', 'title': 'Statistics and contrast', 'rows': rows}]
    if key == 'indexed_image':
        if details['index_matrix'] is not None:
            indexed = np.array(details['index_matrix'], dtype=np.uint8)
        else:
            gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            indexed = (gray.astype(np.uint16) * 4 // 256).astype(np.uint8)
        palette = np.array(details['palette_rgb'], dtype=np.uint8)[np.newaxis, :, ::-1]
        matrix = image_panel('Index matrix', indexed)
        matrix['vmax'] = 3
        return [matrix, image_panel('Palette-mapped image', result), image_panel('Palette: black / red / green / blue', palette)]
    if key == 'pixel_connectivity':
        return [image_panel('Pixel values', result), {'kind': 'graph', 'title': params['connectivity'] + '-connectivity graph',
                                                     'pixels': result, 'edges': details['edges']}]
    if key == 'knn_interpolation':
        source = np.array(details['source_matrix'], dtype=np.uint8)
        return [image_panel('Spatial sample values', source), image_panel('KNN interpolated values', result)]
    if key == 'color_spaces':
        methods = {'RGB': cv2.COLOR_BGR2RGB, 'Gray': cv2.COLOR_BGR2GRAY, 'HSV': cv2.COLOR_BGR2HSV,
                   'Lab': cv2.COLOR_BGR2LAB, 'YCrCb': cv2.COLOR_BGR2YCrCb}
        space = params['space']
        values = cv2.cvtColor(original, methods[space])
        panels = [image_panel('Original RGB display', original)]
        for index, label in enumerate(details['channel_order']):
            channel = values if values.ndim == 2 else values[:, :, index]
            panel = image_panel(space + ': ' + label, channel)
            panel['colorbar'] = True
            if space == 'HSV' and index == 0:
                panel['vmax'] = 179
            panels.append(panel)
        return panels
    if key in ('rgb_to_hsi', 'hsi_to_rgb'):
        from RGBToHSI import hsi_components
        H, S, I = hsi_components(original)
        if key == 'hsi_to_rgb' and params['input'] == 'Numeric HSI':
            H = np.full(original.shape[:2], params['hue'])
            S = np.full(original.shape[:2], params['saturation'])
            I = np.full(original.shape[:2], params['intensity'])
        panels = []
        for title, values, maximum, cmap in [('Hue (degrees)', H, 360, 'hsv'), ('Saturation', S, 1, 'gray'), ('Intensity', I, 1, 'gray')]:
            panel = image_panel(title, values)
            panel.update(vmax=maximum, cmap=cmap, colorbar=True, annotate=False)
            panels.append(panel)
        if key == 'rgb_to_hsi':
            panels.insert(0, image_panel('Original RGB display', original))
        else:
            panels.append(image_panel('Reconstructed RGB', result))
        return panels
    if key == 'adaptive_mean':
        return [image_panel('Grayscale input', cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)), image_panel('Adaptive mean threshold', result)]
    if key == 'watershed':
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
        distance = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, foreground = cv2.threshold(distance, params['fraction'] * distance.max(), 255, cv2.THRESH_BINARY)
        return [image_panel('Original', original), image_panel('Inverted Otsu mask', binary),
                image_panel('Foreground markers', foreground.astype(np.uint8)), image_panel('Watershed boundaries (red)', result)]
    if key == 'region_growing':
        analysis = cv2.resize(original, (result.shape[1], result.shape[0]), interpolation=cv2.INTER_AREA)
        marked = analysis.copy()
        x, y = details['seed_xy']
        cv2.circle(marked, (x, y), max(1, min(result.shape) // 50), (0, 0, 255), -1)
        segmented = cv2.bitwise_and(analysis, analysis, mask=result)
        return [image_panel('Selected seed (red)', marked), image_panel('Grown region mask', result), image_panel('Selected region', segmented)]
    if key == 'kmeans':
        analysis = cv2.resize(original, (result.shape[1], result.shape[0]), interpolation=cv2.INTER_AREA)
        palette = np.array(details['centers_rgb'], dtype=np.uint8)[np.newaxis, :, ::-1]
        return [image_panel('Analysis input', analysis), image_panel('K-means segmentation', result), image_panel('Cluster colors', palette)]
    if key == 'histogram_matching':
        source = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        target = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
        return [image_panel('Source grayscale', source), image_panel('Reference grayscale', target), image_panel('Histogram-matched image', result),
                histogram_panel('Source histogram', source), histogram_panel('Reference histogram', target), histogram_panel('Matched histogram', result)]
    if key == 'lab_histogram_matrix':
        matrix = image_panel('PDF 5 x 5 pixel values', result)
        matrix['vmax'] = 6
        return [matrix, {'kind': 'histogram', 'title': 'Exact counts for intensities 0 to 6', 'values': details['histogram']}]
    if key in ('lab_basic_equalization', 'lab_normalized_equalization'):
        source = np.array(details['original_matrix'], dtype=np.uint8)
        return [image_panel('PDF original 8 x 8 values', source), histogram_panel('Original histogram', source), cdf_panel('Original CDF probability', source),
                image_panel('Equalized 8 x 8 values', result), histogram_panel('Equalized histogram', result), cdf_panel('Equalized CDF probability', result)]
    if key == 'binary_matrix':
        values = np.array(details['binary_matrix'], dtype=np.uint8)
        matrix = image_panel('PDF binary values', values)
        matrix['vmax'] = 1
        return [matrix, {'kind': 'table', 'title': 'Binary pixel counts',
                         'rows': [['Foreground (1)', str(details['foreground_pixels'])],
                                  ['Background (0)', str(values.size - details['foreground_pixels'])]]}]
    return None
