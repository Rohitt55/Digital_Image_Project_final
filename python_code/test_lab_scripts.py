"""Run every standalone lab with its supplied sample image."""
import contextlib
import io
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


class StandaloneLabTests(unittest.TestCase):
    def test_all_lab_scripts_produce_images_and_plots(self):
        root = Path(__file__).resolve().parent
        scripts = sorted(path for path in root.glob('*.py')
                         if path.name not in ('web_app.py', 'mobile_server.py') and not path.name.startswith('test_'))
        self.assertEqual(len(scripts), 83)
        for path in scripts:
            with self.subTest(script=path.name):
                try:
                    with patch.object(plt, 'show') as show:
                        with contextlib.redirect_stdout(io.StringIO()):
                            values = runpy.run_path(str(path))
                        show.assert_called_once()
                    result = values['result']
                    self.assertEqual(result.dtype, np.uint8)
                    self.assertIn(result.ndim, (2, 3))
                    self.assertGreater(result.size, 0)
                    self.assertTrue(plt.get_fignums())
                    titles = [axis.get_title() for number in plt.get_fignums()
                              for axis in plt.figure(number).axes]
                    expected = {
                        'ImageHistogram.py': ['Grayscale Image', 'Image Histogram'],
                        'ImagePixelMatrix.py': ['Original Grayscale Image', '8 x 8 Digital Image with Pixel Values'],
                        'ImageMatching.py': ['Source Image', 'Source Histogram', 'Reference Image', 'Reference Histogram'],
                        'WienerFilter.py': ['Original grayscale', 'Blurred + noisy observation', 'Wiener Filter restoration'],
                        'InverseCosineTransform.py': ['Grayscale input', 'Retained DCT magnitude', 'IDCT reconstruction']
                    }
                    if path.name in expected:
                        self.assertEqual(titles, expected[path.name])
                    if path.name == 'ImageResize.py':
                        self.assertEqual(len(titles), 2)
                        self.assertTrue(titles[0].startswith('Original: '))
                        self.assertEqual(titles[1], 'Resized: 400 x 300')
                    for number in plt.get_fignums():
                        figure = plt.figure(number)
                        figure.canvas.draw()
                    if 'decoded' in values:
                        np.testing.assert_array_equal(result, values['small'])
                finally:
                    plt.close('all')


if __name__ == '__main__':
    unittest.main()
