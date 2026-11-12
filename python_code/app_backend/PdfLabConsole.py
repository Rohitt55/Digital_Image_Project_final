"""Printed results corresponding to the PDF example figures."""
import cv2
import numpy as np

from ConvertToGray import gray
from LimitImageSize import bounded
from OperationRegistry import OPERATIONS
from RunOperation import execute


def pdf_console(key, original, result, params, details, reference):
    lines = [f">>> Operation: {OPERATIONS[key]['name']}", f'Parameters: {params}', '']
    if key == 'knn_interpolation' and params['input'] == 'Uploaded 8x8 image':
        lines += ['KNN IMAGE INTERPOLATION RESULTS', '-' * 42,
                  f"K Value: {params['neighbors']} (inverse-distance weights)", 'Downsample Size: 8 x 8',
                  f'Upsample Size: {result.shape[1]} x {result.shape[0]}']
        for label, scores in [('Nearest Neighbor', details['nearest_neighbor_scores']), ('KNN', details['knn_scores'])]:
            lines.append(f"{label}: PSNR={scores['psnr_db']} dB; SSIM={scores['ssim']:.6f}; MSE={scores['mse']:.6f}")
    elif key == 'image_measurements':
        for label, name in [('Maximum Intensity', 'maximum'), ('Minimum Intensity', 'minimum'), ('Mean Intensity', 'mean'),
                            ('Variance', 'variance'), ('Standard Deviation', 'standard_deviation'),
                            ('Simple Contrast', 'simple_contrast'), ('Michelson Contrast', 'michelson_contrast'), ('RMS Contrast', 'rms_contrast')]:
            lines.append(f'{label:<20}: {details[name]:.6g}')
    elif key == 'matching':
        lines += ['PIXEL SIMILARITY RESULT', '-' * 42,
                  f'Original Source Shape   : {gray(original).shape}', f'Original Reference Shape: {gray(reference).shape}',
                  f'After Resize            : {gray(original).shape}',
                  f"Similar pixels  : {details['similar_pixels']}", f"Different pixels: {details['different_pixels']}",
                  f'Total pixels    : {result.size}', f"Tolerance       : {params['tolerance']}",
                  f"Similarity (%)  : {details['similarity_percent']}"]
    elif key == 'noise_models':
        before = gray(original).astype(float)
        after = gray(result).astype(float)
        samples = cv2.resize(before, (3, 3), interpolation=cv2.INTER_AREA)
        noisy = cv2.resize(after, (3, 3), interpolation=cv2.INTER_AREA)
        lines += [f'Image Shape: {before.shape}', '3 x 3 sampled pixel values:', np.array2string(samples, precision=3),
                  '3 x 3 applied grayscale noise (after clipping):', np.array2string(noisy - samples, precision=3),
                  '3 x 3 image with noisy values:', np.array2string(noisy, precision=3),
                  'These samples are measured from the current input and actual output.']
        for name in ('unclipped_noise_mean', 'unclipped_noise_std', 'snr_db'):
            lines.append(f'{name}: {details[name]}')
    elif key in ('threshold', 'adaptive', 'adaptive_mean', 'otsu'):
        if key == 'otsu':
            cutoff = details['selected_threshold']
        else:
            _, info = execute('otsu', original, {})
            cutoff = info['selected_threshold']
        lines += ['THRESHOLDING RESULTS', '-' * 42,
                  f"Basic Threshold       : {params['threshold'] if key == 'threshold' else 128}",
                  'Global Threshold      : 100', 'Adaptive Threshold    : Local mean',
                  'Gaussian Adaptive     : Local Gaussian', f'Otsu Optimal Threshold: {cutoff:g}',
                  f'Selected output foreground pixels: {np.count_nonzero(result)}',
                  f'Selected output background pixels: {result.size - np.count_nonzero(result)}']
    elif key in ('watershed', 'region_growing', 'kmeans'):
        analysis = bounded(original, 512)
        seed = details['seed_xy'] if key == 'region_growing' else [analysis.shape[1] // 2, analysis.shape[0] // 2]
        lines += ['IMAGE SEGMENTATION RESULTS', '-' * 42,
                  'Watershed      : Marker-based segmentation', 'Region Growing : Seed-based segmentation',
                  'K-Means        : Clustering-based segmentation',
                  f"K              : {params['clusters'] if key == 'kmeans' else 3}",
                  f'Seed Point     : ({seed[0]}, {seed[1]})',
                  f"Region Threshold: {params['tolerance'] if key == 'region_growing' else 15}"]
        for name, value in details.items():
            if name != 'processing_ms':
                lines.append(f'{name}: {value}')
    elif key == 'lab_histogram_matrix':
        lines += ['5 x 5 grayscale image:', np.array2string(result), 'Histogram', '-' * 30, 'Pixel Value    Count']
        lines += [f'{value:<14} {count}' for value, count in enumerate(details['histogram'])]
    elif key in ('binary_matrix', 'indexed_image', 'pixel_connectivity'):
        matrix = details.get('binary_matrix', details.get('index_matrix', details.get('pixel_matrix')))
        if matrix is not None:
            lines += ['Pixel Values:', np.array2string(np.array(matrix))]
        for name in ('palette_rgb', 'node_count', 'edge_count', 'connectivity', 'foreground_pixels'):
            if name in details:
                lines.append(f'{name}: {details[name]}')
    else:
        return None
    if key in ('threshold', 'adaptive', 'adaptive_mean', 'otsu', 'watershed', 'region_growing', 'kmeans'):
        lines += ['', 'The selected method uses your settings; companion methods use the example defaults.']
    lines += [f"processing_ms: {details.get('processing_ms', 0)}", '', 'Process finished successfully.']
    return '\n'.join(lines)
