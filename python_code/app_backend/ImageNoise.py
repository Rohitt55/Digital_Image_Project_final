from GaussianNoise import gaussian_noise
from UniformNoise import uniform_noise
from ExponentialNoise import exponential_noise
from GammaNoise import gamma_noise
from RayleighNoise import rayleigh_noise
from PoissonNoise import poisson_noise
from SpeckleNoise import speckle_noise
from SaltPepperNoise import salt_pepper_noise
import numpy as np
from ConvertToGray import gray
from OperationRegistry import operation, field, choice
from ConvertToUint8 import u8


SOURCE='Chap6-Image Restoration.pdf'

GROUP='Filters & restoration'

@operation('noise_models','Gaussian / uniform / exponential / gamma / Rayleigh / Poisson / speckle / impulse noise',GROUP,'Generate seeded samples from eight noise families. Additive distributions are centered to avoid an unintended brightness shift.', 'g=f+n (additive); g=f+f n (speckle); Poisson models photon counts',SOURCE,
           [
               choice(
                   'model',
                   'Noise model',
                   'Gaussian',
                   ['Gaussian','Uniform','Exponential','Gamma','Rayleigh','Poisson','Speckle','Salt and pepper']
               ),
               choice('domain', 'Noise domain', 'grayscale', ['grayscale', 'RGB channels']),
               field('sigma','Noise standard deviation',2,1,100),
               field('amount','Impulse fraction',.05,.001,.5,.001),
               field('peak','Poisson peak photon count',30,1,255),
               field('seed','Random seed',42,0,9999)
           ])
def noise_models(image, params, reference):
    if params['domain'] == 'grayscale':
        image = gray(image)
    values = image.astype(float)
    rng = np.random.default_rng(params['seed'])
    sigma = params['sigma']
    model = params['model']
    if model == 'Gaussian':
        noise = gaussian_noise(image, params, rng)
    elif model == 'Uniform':
        noise = uniform_noise(image, params, rng)
    elif model == 'Exponential':
        noise = exponential_noise(image, params, rng)
    elif model == 'Gamma':
        noise = gamma_noise(image, params, rng)
    elif model == 'Rayleigh':
        noise = rayleigh_noise(image, params, rng)
    elif model == 'Poisson':
        noise = poisson_noise(image, params, rng)
    elif model == 'Speckle':
        noise = speckle_noise(image, params, rng)
    elif model == 'Salt and pepper':
        noise = salt_pepper_noise(image, params, rng)
    result = u8(values + noise)
    signal_power = float(np.mean(values ** 2))
    noise_power = float(np.mean(noise ** 2))
    return (result, {
        'unclipped_noise_mean': float(noise.mean()),
        'unclipped_noise_std': float(noise.std()),
        'snr_db': float(10 * np.log10(signal_power / noise_power)) if signal_power and noise_power else 'undefined',
        'note': 'Random seed makes this synthetic degradation repeatable. Noise statistics are measured before intensity clipping.'
    })
