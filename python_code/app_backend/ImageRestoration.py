from InverseFilter import inverse_filter
from WienerFilter import wiener_filter
import numpy as np
from OperationRegistry import operation, field, choice
from ConvertToGray import gray
from LimitImageSize import bounded
from ConvertToUint8 import u8
from BlurKernel import psf
from BlurTransferFunction import otf


SOURCE='Chap6-Image Restoration.pdf'

GROUP='Filters & restoration'

BLUR_FIELDS=[
    choice('blur','Point-spread function','Gaussian',['Gaussian','motion']),
    field('kernel','Blur kernel size (odd)',5,3,31)
]

@operation('inverse_wiener','Inverse / Wiener / minimum-MSE deconvolution',GROUP,'Restore using a known PSF. Demo mode first degrades the input; uploaded-degraded mode treats the input as the measured observation.', 'Inverse=G/H; Wiener=H*G/(|H|²+K)',SOURCE,BLUR_FIELDS+
           [
               choice('method','Restoration','Wiener',['inverse','Wiener']),
               choice(
                   'input_mode',
                   'Input interpretation',
                   'degrade then restore',
                   ['degrade then restore','uploaded degraded image']
               ),
               field('noise','Demo Gaussian noise sigma',3,0,40),
               field('regularization','Wiener K / inverse cutoff',.01,.0001,.5,.0001)
           ])
def inverse_wiener(image, params, reference):
    values = gray(bounded(image, 1024)).astype(float)
    transfer = otf(psf(params['kernel'], params['blur']), values.shape)
    observed = values
    if params['input_mode'] == 'degrade then restore':
        # Blur in frequency space, then add repeatable Gaussian noise.
        spectrum = np.fft.fft2(values)
        blurred = np.fft.ifft2(spectrum * transfer).real
        rng = np.random.default_rng(42)
        noise = rng.normal(0, params['noise'], values.shape)
        observed = blurred + noise
    if params['method'] == 'inverse':
        inverse = inverse_filter(transfer, params['regularization'])
    else:
        inverse = wiener_filter(transfer, params['regularization'])
    # Apply the restoration filter and return to image space.
    observed_spectrum = np.fft.fft2(observed)
    restored_spectrum = observed_spectrum * inverse
    restored = np.fft.ifft2(restored_spectrum).real
    details = {'note': 'Known-PSF circular-convolution demo, limited to a 1024-pixel side. Wiener K approximates the noise-to-signal power ratio.'}
    if params['input_mode'] == 'degrade then restore':
        details.update(
            degraded_mse=float(np.mean((observed - values) ** 2)),
            restored_mse=float(np.mean((restored - values) ** 2))
        )
    return (u8(restored), details)
