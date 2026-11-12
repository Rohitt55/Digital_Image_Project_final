from LogIntensityMapping import log_mapping
from InverseLogTransformation import inverse_log_mapping

import numpy as np
from OperationRegistry import operation, field, choice
from ConvertToUint8 import u8


SOURCE = 'Chap2 Image Enhancement.pdf'

@operation('log_transform', 'Log / inverse-log transformation', 'Color & intensity', 'Expand dark intensities with a logarithm, or emphasize bright intensities with its inverse.', 'log: s = 255 log(1+r)/log(256); inverse: s = 255(expm1(a r/255))/expm1(a)', SOURCE,
           [
               choice('mode','Transform','log',['log','inverse-log']),
               field('strength','Inverse-log strength',3,.1,8,.1)
           ])
def log_transform(image, params, reference):
    values = image.astype(float)
    if params['mode'] == 'log':
        transformed = log_mapping(values)
    else:
        transformed = inverse_log_mapping(values, params['strength'])
    result = u8(transformed)
    return result
