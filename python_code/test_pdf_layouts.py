"""Check the sample grids, mapping tables and measured image interpolation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'app_backend'))

import unittest
import numpy as np

import OperationLoader
from RunOperation import execute, validated_params
from LabOutput import output_panels, make_output
from ImageStatistics import statistics
from KNNImageInterpolation import image_scores


class PdfLayoutTests(unittest.TestCase):
    def setUp(self):
        self.image = np.random.default_rng(21).integers(0, 256, (32, 48, 3), dtype=np.uint8)

    def panels(self, key, params=None):
        params = validated_params(key, params or {})
        result, details = execute(key, self.image, params)
        return result, output_panels(key, self.image, result, params, details)

    def test_comparison_grids_keep_actual_selected_output(self):
        for key, params, index, count in [('resize', {'width': 17, 'height': 11}, 2, 6),
                                          ('mean', {'kernel': 3}, 1, 5),
                                          ('threshold', {'threshold': 70}, 1, 6),
                                          ('flip', {'axis': 'both'}, 6, 7),
                                          ('sobel', {}, 1, 5)]:
            with self.subTest(operation=key):
                result, panels = self.panels(key, params)
                self.assertEqual(len(panels), count)
                np.testing.assert_array_equal(panels[index]['image'], result)

    def test_sampling_and_bit_depth_comparisons(self):
        result, panels = self.panels('sampling')
        self.assertEqual([p['image'].shape[:2] for p in panels], [(32, 48), (32, 32), (64, 64), (1024, 1024)])
        result, panels = self.panels('quantization', {'bits': '3'})
        self.assertEqual(len(panels), 8)
        np.testing.assert_array_equal(panels[5]['image'], result)
        for bit, panel in zip(range(8, 0, -1), panels):
            self.assertLessEqual(len(np.unique(panel['image'])), 2 ** bit)

    def test_normalized_mapping_table_uses_exact_pdf_data(self):
        result, details = execute('lab_normalized_equalization', self.image, {})
        output = make_output(self.image, result, statistics(self.image), statistics(result), 'lab_normalized_equalization', {}, details)
        rows = {row[0]: row for row in output['tables'][0]['rows']}
        self.assertEqual(rows[52], [52, 1, 1, 0.015625, 0])
        self.assertEqual(rows[55], [55, 3, 4, 0.0625, 12])
        self.assertEqual(len(output['panels']), 5)

    def test_threshold_and_segmentation_sample_order(self):
        _, panels = self.panels('adaptive_mean')
        self.assertEqual(len(panels), 6)
        self.assertEqual(panels[0]['title'], 'Original Image')
        self.assertIn('Mean', panels[3]['title'])
        self.assertIn('Otsu', panels[5]['title'])
        _, panels = self.panels('watershed')
        self.assertEqual([p['title'] for p in panels], ['Original Image', 'Binary Image', 'Watershed Segmentation', 'Region Growing', 'K-Means Segmentation (K=3)', 'Distance Transform'])

    def test_knn_image_reconstruction_and_scores(self):
        constant = np.full((17, 23, 3), [30, 90, 150], dtype=np.uint8)
        for k in [1, 4, 9]:
            result, details = execute('knn_interpolation', constant, {'input': 'Uploaded 8x8 image', 'output_side': 32, 'neighbors': k})
            self.assertEqual(result.shape, (32, 32, 3))
            np.testing.assert_array_equal(result, np.full_like(result, [30, 90, 150]))
            self.assertEqual(details['knn_scores']['mse'], 0)
            self.assertEqual(details['knn_scores']['ssim'], 1)
            self.assertEqual(details['knn_scores']['psnr_db'], 'infinity')
        scores = image_scores(self.image, self.image)
        self.assertEqual(scores['mse'], 0)
        self.assertAlmostEqual(scores['ssim'], 1)

    def test_single_sample_figures_are_not_padded_with_unrelated_panels(self):
        for key, kind in [('binary_matrix', 'image'), ('indexed_image', 'image'), ('pixel_connectivity', 'graph')]:
            _, panels = self.panels(key)
            self.assertEqual(len(panels), 1)
            self.assertEqual(panels[0]['kind'], kind)

    def test_sample_reference_links_and_mapping_table_api(self):
        import io
        import cv2
        from web_app import app
        image_bytes = cv2.imencode('.png', self.image)[1].tobytes()
        with app.test_client() as client:
            response = client.post('/api/process', data={'operation': 'lab_normalized_equalization', 'lab_output': 'true',
                                                       'image': (io.BytesIO(image_bytes), 'sample.png')})
            self.assertEqual(response.status_code, 200)
            lab = response.get_json()['lab']
            self.assertEqual(lab['layout_reference']['source'], 'DIP-Lab2.pdf')
            self.assertIn(16, lab['layout_reference']['pages'])
            self.assertEqual(lab['tables'][0]['rows'][0][0], 52)
            self.assertNotIn('Lab 2:', response.get_json()['operation'])
            for number in [1, 2]:
                with client.get(f'/api/lab/source/{number}') as source:
                    self.assertEqual(source.status_code, 200)
                    self.assertTrue(source.data.startswith(b'%PDF'))
            self.assertEqual(client.get('/api/lab/source/3').status_code, 404)
            self.assertIn(b'id="lab-tables"', client.get('/').data)


if __name__ == '__main__':
    unittest.main()
