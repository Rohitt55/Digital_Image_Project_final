"""Image-scale KNN interpolation and measured comparison scores."""
import cv2
import numpy as np
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter


def image_scores(original, output):
    reference = cv2.resize(original, (output.shape[1], output.shape[0]), interpolation=cv2.INTER_LINEAR).astype(float)
    values = output.astype(float)
    mse = float(np.mean((reference - values) ** 2))
    psnr = float(10 * np.log10(255 ** 2 / mse)) if mse > 0 else 'infinity'
    mu1 = gaussian_filter(reference, (1.5, 1.5, 0), truncate=3.5)
    mu2 = gaussian_filter(values, (1.5, 1.5, 0), truncate=3.5)
    variance1 = np.maximum(0, gaussian_filter(reference ** 2, (1.5, 1.5, 0), truncate=3.5) - mu1 ** 2)
    variance2 = np.maximum(0, gaussian_filter(values ** 2, (1.5, 1.5, 0), truncate=3.5) - mu2 ** 2)
    covariance = gaussian_filter(reference * values, (1.5, 1.5, 0), truncate=3.5) - mu1 * mu2
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2
    ssim_map = ((2 * mu1 * mu2 + c1) * (2 * covariance + c2)) / ((mu1 ** 2 + mu2 ** 2 + c1) * (variance1 + variance2 + c2))
    ssim = float(np.mean(ssim_map[5:-5, 5:-5]))
    return {'mse': mse, 'psnr_db': psnr, 'ssim': ssim}


def interpolate_image(image, neighbors, size):
    samples = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
    yy, xx = np.mgrid[:8, :8]
    positions = np.column_stack((yy.ravel() / 7, xx.ravel() / 7))
    grid_y, grid_x = np.mgrid[:size, :size]
    queries = np.column_stack((grid_y.ravel() / (size - 1), grid_x.ravel() / (size - 1)))
    distances, indices = cKDTree(positions).query(queries, k=neighbors)
    if neighbors == 1:
        distances = distances[:, np.newaxis]
        indices = indices[:, np.newaxis]
    weights = 1 / np.maximum(distances, 1e-12)
    sample_values = samples.reshape((-1, 3)).astype(float)
    estimated = np.sum(sample_values[indices] * weights[:, :, np.newaxis], axis=1) / weights.sum(axis=1)[:, np.newaxis]
    exact = distances[:, 0] < 1e-12
    estimated[exact] = sample_values[indices[exact, 0]]
    result = np.clip(np.round(estimated), 0, 255).astype(np.uint8).reshape((size, size, 3))
    nearest = cv2.resize(samples, (size, size), interpolation=cv2.INTER_NEAREST)
    details = {'input_mode': 'Uploaded 8x8 image', 'downsample_size': [8, 8], 'output_size': [size, size],
               'effective_neighbors': neighbors, 'nearest_neighbor_scores': image_scores(image, nearest),
               'knn_scores': image_scores(image, result)}
    return result, details
