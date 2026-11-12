import cv2
import numpy as np
from OperationRegistry import operation, field, choice


@operation('image_measurements', 'Mean, variance and contrast measurements', 'Fundamentals',
           'Calculate mean, variance, standard deviation, intensity-range contrast, Michelson contrast and RMS contrast.', 'variance = mean((r - mean(r))^2); RMS = sqrt(variance); C = max - min', 'DIP-Lab1.pdf',
           [choice('domain', 'Measurement domain', 'RGB channels', ['RGB channels', 'grayscale'])], requires_reference=False)
def image_measurements(image, params, reference):
    domain = params['domain']
    if domain == 'grayscale':
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        result = image.copy()
    values = result.astype(float)
    low = float(values.min())
    high = float(values.max())
    mean = float(values.mean())
    variance = float(np.var(values))
    std = float(np.std(values))
    michelson = (high - low) / (high + low) if high + low else 0.0
    details = {'domain': domain, 'mean': mean, 'variance': variance, 'standard_deviation': std,
               'minimum': low, 'maximum': high, 'simple_contrast': high - low,
               'michelson_contrast': michelson, 'rms_contrast': std}
    return result, details
