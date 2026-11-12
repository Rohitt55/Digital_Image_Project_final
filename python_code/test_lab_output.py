"""Check that plots explain the chosen operation and use its real values."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'app_backend'))

import unittest

import cv2
import numpy as np

import OperationLoader
from LabOutput import output_panels, make_output
from OperationRegistry import OPERATIONS
from RunOperation import execute, validated_params
from ImageStatistics import statistics


class LabOutputTests(unittest.TestCase):
    def setUp(self):
        self.image = np.random.default_rng(10).integers(0, 256, (32, 48, 3), dtype=np.uint8)
        self.reference = 255 - self.image

    def panels(self, key, params=None):
        params = validated_params(key, params or {})
        result, details = execute(key, self.image, params, self.reference)
        return output_panels(key, self.image, result, params, details, self.reference)

    def test_every_selectable_variant_has_relevant_valid_panels(self):
        for key, spec in OPERATIONS.items():
            variants = [{}]
            for field in spec['fields']:
                if field['type'] == 'select':
                    variants.extend({field['key']: value} for value in field['options'])
            for params in variants:
                with self.subTest(operation=key, params=params):
                    panels = self.panels(key, params)
                    self.assertGreaterEqual(len(panels), 1)
                    for panel in panels:
                        self.assertTrue(panel['title'])
                        if panel['kind'] == 'image':
                            self.assertGreater(panel['image'].size, 0)
                            self.assertTrue(np.isfinite(panel['image']).all())
                    if key not in ('histogram', 'equalize_basic', 'equalize', 'lab_basic_equalization', 'lab_normalized_equalization'):
                        self.assertNotIn('cdf', [panel['kind'] for panel in panels])
                    if key not in ('histogram', 'equalize_basic', 'equalize', 'stretch', 'clahe', 'matching', 'image_measurements', 'histogram_matching', 'lab_histogram_matrix', 'lab_basic_equalization', 'lab_normalized_equalization'):
                        self.assertNotIn('histogram', [panel['kind'] for panel in panels])

    def test_histogram_and_equalization_show_actual_distributions(self):
        panels = self.panels('histogram')
        values = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        expected = np.bincount(values.ravel(), minlength=256)
        np.testing.assert_array_equal(panels[1]['values'], expected)
        self.assertEqual(len(panels), 2)
        equalized = self.panels('equalize')
        self.assertEqual(len(equalized), 5)
        np.testing.assert_array_equal(equalized[2]['values'], np.cumsum(expected))

    def test_matching_uses_uploaded_reference(self):
        panels = self.panels('matching')
        target = cv2.cvtColor(self.reference, cv2.COLOR_BGR2GRAY)
        np.testing.assert_array_equal(panels[2]['image'], target)
        np.testing.assert_array_equal(panels[3]['values'], np.bincount(target.ravel(), minlength=256))

    def test_restoration_only_shows_ground_truth_in_demo_mode(self):
        self.assertEqual(len(self.panels('inverse_wiener')), 3)
        panels = self.panels('inverse_wiener', {'input_mode': 'uploaded degraded image'})
        self.assertEqual(len(panels), 2)
        self.assertEqual(panels[0]['title'], 'Uploaded degraded input')

    def test_frequency_mask_and_compression_sizes_are_real(self):
        low = self.panels('frequency_filter')[1]['image']
        high = self.panels('frequency_filter', {'mode': 'high-pass'})[1]['image']
        np.testing.assert_array_equal(low + high, np.full(low.shape, 255, dtype=np.uint8))
        panels = self.panels('compression')
        self.assertEqual(panels[2]['values'][0], self.image.nbytes)
        expected_bytes = cv2.imencode('.jpg', self.image, [cv2.IMWRITE_JPEG_QUALITY, 80])[1].size
        self.assertEqual(panels[2]['values'][1], expected_bytes)

    def test_layouts_render_and_console_excludes_unrelated_data(self):
        for key in ['resize', 'histogram', 'equalize', 'dct', 'inverse_wiener', 'noise_models', 'compression', 'matching']:
            with self.subTest(operation=key):
                result, details = execute(key, self.image, {}, self.reference)
                output = make_output(self.image, result, statistics(self.image), statistics(result), key, {}, details, self.reference)
                self.assertTrue(output['figure'].startswith('data:image/png;base64,'))
                self.assertTrue(output['caption'])
                if key == 'resize':
                    self.assertIn('Input size: 48 x 32', output['console'])
                    self.assertIn('Output size: 400 x 300', output['console'])
                    self.assertNotIn('CDF', output['console'])
                    self.assertNotIn('pixel matrix', output['console'])

    def test_numeric_string_parameters_match_execution(self):
        params = {'kernel': '3', 'threshold': '100'}
        result, details = execute('morphology', self.image, params)
        output = make_output(self.image, result, statistics(self.image), statistics(result), 'morphology', params, details)
        self.assertIn('Opening', output['panels'])


if __name__ == '__main__':
    unittest.main()
