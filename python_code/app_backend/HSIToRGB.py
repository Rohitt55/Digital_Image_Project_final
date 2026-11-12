import cv2
import numpy as np
from RGBToHSI import hsi_components
from OperationRegistry import operation, field, choice


@operation('hsi_to_rgb', 'HSI to RGB', 'Color & intensity',
           'Reconstruct RGB from an image-derived HSI array, or from numeric H/S/I values. Uses intensity-preserving HSI sector equations.', 'HSI sector equations preserve R+G+B = 3I before gamut clipping', 'DIP-Lab1.pdf',
           [choice('input', 'HSI input', 'Image round trip', ['Image round trip', 'Numeric HSI']), field('hue', 'Hue (degrees)', 60, 0, 360, 0.1), field('saturation', 'Saturation', 0.5, 0, 1, 0.01), field('intensity', 'Intensity', 0.5, 0, 1, 0.01)], requires_reference=False)
def hsi_to_rgb(image, params, reference):
    input_mode = params['input']
    hue = params['hue']
    saturation = params['saturation']
    intensity = params['intensity']
    H, S, I = hsi_components(image)
    if input_mode == 'Numeric HSI':
        H = np.full(image.shape[:2], hue, dtype=float)
        S = np.full(image.shape[:2], saturation, dtype=float)
        I = np.full(image.shape[:2], intensity, dtype=float)
    angle = np.radians(H % 360)
    R = np.zeros_like(I)
    G = np.zeros_like(I)
    B = np.zeros_like(I)
    for sector in range(3):
        selected = (angle >= sector * 2 * np.pi / 3) & (angle < (sector + 1) * 2 * np.pi / 3)
        local = angle[selected] - sector * 2 * np.pi / 3
        low = I[selected] * (1 - S[selected])
        high = I[selected] * (1 + S[selected] * np.cos(local) / np.cos(np.pi / 3 - local))
        middle = 3 * I[selected] - low - high
        if sector == 0:
            R[selected], G[selected], B[selected] = high, middle, low
        elif sector == 1:
            R[selected], G[selected], B[selected] = low, high, middle
        else:
            R[selected], G[selected], B[selected] = middle, low, high
    rgb_values = np.stack((R, G, B), axis=2)
    clipped = int(np.count_nonzero((rgb_values < -1e-10) | (rgb_values > 1 + 1e-10)))
    rgb_result = np.clip(np.round(rgb_values * 255), 0, 255).astype(np.uint8)
    result = cv2.cvtColor(rgb_result, cv2.COLOR_RGB2BGR)
    details = {'clipped_channel_values': clipped, 'note': 'HSI combinations outside the RGB gamut are clipped for display.'}
    details['input'] = input_mode
    details['center_rgb'] = rgb_result[result.shape[0] // 2, result.shape[1] // 2].tolist()
    if input_mode == 'Image round trip':
        details['reconstruction_mse'] = float(np.mean((image.astype(float) - result.astype(float)) ** 2))
    return result, details
