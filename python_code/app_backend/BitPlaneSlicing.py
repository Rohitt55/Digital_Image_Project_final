from OperationRegistry import operation, field, choice
from ConvertToGray import gray


SOURCE = 'Chap2 Image Enhancement.pdf'

@operation('bit_planes', 'Bit-plane slicing', 'Color & intensity', 'Inspect one bit of each grayscale pixel or reconstruct the highest selected bits.', 'Plane b = ((r >> b) & 1) × 255', SOURCE,
           [
               choice('mode','Display','single plane',['single plane','reconstruct high bits']),
               field('bit','Bit / lowest retained bit',7,0,7)
           ])
def bit_planes(image, params, reference):
    values = gray(image)
    bit = params['bit']

    if params['mode'] == 'single plane':
        # Move the selected bit to position zero and isolate it.
        plane = (values >> bit) & 1
        result = plane * 255
    else:
        # Remove the lower bits, then restore the remaining positions.
        high_bits = values >> bit
        result = high_bits << bit
    return result
