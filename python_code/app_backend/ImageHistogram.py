from OperationRegistry import operation


@operation(
    'histogram',
    'Histogram & contrast analysis',
    'Histograms',
    'Inspect grayscale frequency, cumulative distribution and contrast statistics.',
    'p(r) = count(r) / N; CDF(r) = sum p(0…r)',
    'ImageHistogram.py'
)
def histogram(image, params, reference):
    return image.copy()
