import cv2
import numpy as np
from OperationRegistry import operation, field, choice


def hsi_components(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(float) / 255
    R, G, B = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    I = (R + G + B) / 3
    total = R + G + B
    S = np.zeros_like(I)
    mask = total > 0
    S[mask] = 1 - 3 * np.minimum(np.minimum(R, G), B)[mask] / total[mask]
    numerator = 0.5 * ((R - G) + (R - B))
    denominator = np.sqrt((R - G) ** 2 + (R - B) * (G - B))
    ratio = np.divide(numerator, denominator, out=np.ones_like(I), where=denominator > 1e-12)
    theta = np.arccos(np.clip(ratio, -1, 1))
    H = np.degrees(np.where(B <= G, theta, 2 * np.pi - theta))
    H[S <= 1e-12] = 0
    return H, S, I


@operation('rgb_to_hsi', 'RGB to HSI', 'Color & intensity',
           'Calculate hue in degrees, saturation and intensity; hue is zero for achromatic pixels.', 'I=(R+G+B)/3; S=1-3*min(R,G,B)/(R+G+B); H from RGB angle', 'DIP-Lab1.pdf',
           [choice('channel', 'Output channel', 'Intensity', ['Hue', 'Saturation', 'Intensity'])], requires_reference=False)
def rgb_to_hsi(image, params, reference):
    channel = params['channel']
    H, S, I = hsi_components(image)
    selected = {'Hue': H / 360, 'Saturation': S, 'Intensity': I}[channel]
    result = np.clip(np.round(selected * 255), 0, 255).astype(np.uint8)
    cy, cx = I.shape[0] // 2, I.shape[1] // 2
    details = {'hue_degrees': float(H[cy, cx]), 'saturation': float(S[cy, cx]), 'intensity': float(I[cy, cx])}
    return result, details
