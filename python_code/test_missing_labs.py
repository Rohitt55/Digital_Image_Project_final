"""Known-value checks for the Lab 1 and Lab 2 additions."""
import base64
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'app_backend'))

import unittest
import cv2
import numpy as np

import OperationLoader
from OperationRegistry import OPERATIONS
from RunOperation import execute
from RGBToHSI import hsi_components


class MissingLabTests(unittest.TestCase):
    def setUp(self):
        self.image = np.random.default_rng(4).integers(0, 256, (32, 48, 3), dtype=np.uint8)

    def test_statistics_include_population_variance_and_contrast(self):
        image = np.array([[[0, 2, 4]]], dtype=np.uint8)
        _, info = execute('image_measurements', image, {})
        self.assertEqual(info['mean'], 2)
        self.assertAlmostEqual(info['variance'], 8 / 3)
        self.assertAlmostEqual(info['standard_deviation'], np.sqrt(8 / 3))
        self.assertEqual(info['simple_contrast'], 4)
        self.assertEqual(info['michelson_contrast'], 1)
        _, info = execute('image_measurements', np.zeros((2, 2, 3), np.uint8), {})
        self.assertEqual(info['michelson_contrast'], 0)

    def test_pdf_index_palette_and_connectivity(self):
        result, info = execute('indexed_image', self.image, {})
        np.testing.assert_array_equal(result[0, 1], [0, 0, 255])
        np.testing.assert_array_equal(result[0, 3], [0, 255, 0])
        np.testing.assert_array_equal(result[1, 1], [255, 0, 0])
        _, info = execute('pixel_connectivity', self.image, {})
        self.assertEqual((info['node_count'], info['edge_count']), (9, 12))
        _, info = execute('pixel_connectivity', self.image, {'connectivity': '8'})
        self.assertEqual(info['edge_count'], 20)

    def test_knn_preserves_samples_and_pdf_center_is_25(self):
        result, info = execute('knn_interpolation', self.image, {})
        self.assertAlmostEqual(info['center_value'], 25)
        np.testing.assert_array_equal(result[[0, 0, 2, 2], [0, 2, 0, 2]], [10, 20, 30, 40])
        _, info = execute('knn_interpolation', self.image, {'neighbors': 9})
        self.assertEqual(info['effective_neighbors'], 4)

    def test_ycrcb_known_rgb_pixel(self):
        image = np.array([[[200, 150, 100]]], dtype=np.uint8)
        result, info = execute('color_spaces', image, {'space': 'YCrCb'})
        np.testing.assert_allclose(info['center_pixel'], [141, 99, 161], atol=1)
        self.assertEqual(result.shape, (1, 1))
        self.assertEqual(info['channel_order'], ['Y', 'Cr', 'Cb'])

    def test_hsi_primary_colors_achromatic_pixels_and_round_trip(self):
        image = np.array([[[0, 0, 255], [0, 255, 0], [255, 0, 0], [0, 0, 0], [128, 128, 128]]], dtype=np.uint8)
        H, S, I = hsi_components(image)
        np.testing.assert_allclose(H[0], [0, 120, 240, 0, 0], atol=1e-10)
        np.testing.assert_allclose(S[0], [1, 1, 1, 0, 0])
        np.testing.assert_allclose(I[0, :3], [1 / 3] * 3)
        result, info = execute('hsi_to_rgb', self.image, {})
        np.testing.assert_array_equal(result, self.image)
        self.assertEqual(info['reconstruction_mse'], 0)
        for hue, bgr in [(0, [0, 0, 255]), (120, [0, 255, 0]), (240, [255, 0, 0]), (360, [0, 0, 255])]:
            with self.subTest(hue=hue):
                result, info = execute('hsi_to_rgb', image, {'input': 'Numeric HSI', 'hue': hue, 'saturation': 1, 'intensity': 1 / 3})
                np.testing.assert_array_equal(result[0, 0], bgr)
        result, info = execute('hsi_to_rgb', image, {'input': 'Numeric HSI', 'hue': 60, 'saturation': 0.7, 'intensity': 0.8})
        self.assertGreater(info['clipped_channel_values'], 0)

    def test_adaptive_mean_threshold(self):
        image = np.zeros((3, 3, 3), dtype=np.uint8)
        image[1, 1] = 100
        result, _ = execute('adaptive_mean', image, {'kernel': 3, 'constant': 0})
        expected = np.zeros((3, 3), dtype=np.uint8)
        expected[1, 1] = 255
        np.testing.assert_array_equal(result, expected)

    def test_region_growing_is_four_connected_and_accepts_edge_seeds(self):
        gray = np.array([[10, 100, 10], [100, 10, 100], [10, 100, 10]], dtype=np.uint8)
        image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        result, info = execute('region_growing', image, {'seed_x': 0, 'seed_y': 0, 'tolerance': 0})
        self.assertEqual(info['region_pixels'], 1)
        self.assertEqual(result[0, 0], 255)
        _, info = execute('region_growing', image, {'seed_x': 100, 'seed_y': 100, 'tolerance': 0})
        self.assertEqual(info['seed_xy'], [2, 2])

    def test_watershed_and_kmeans_segment_known_objects(self):
        image = np.full((64, 96, 3), 255, dtype=np.uint8)
        cv2.circle(image, (24, 32), 12, (0, 0, 0), -1)
        cv2.circle(image, (72, 32), 12, (0, 0, 0), -1)
        result, info = execute('watershed', image, {})
        self.assertEqual(info['foreground_markers'], 2)
        self.assertGreater(info['boundary_pixels'], 0)
        self.assertTrue(np.any(np.all(result == [0, 0, 255], axis=2)))
        image = np.zeros((12, 16, 3), dtype=np.uint8)
        image[:, 8:] = [40, 100, 220]
        result, info = execute('kmeans', image, {'clusters': 2})
        np.testing.assert_array_equal(result, image)
        self.assertEqual(len(info['centers_rgb']), 2)
        with self.assertRaises(ValueError):
            execute('kmeans', image[:1, :1], {'clusters': 2})

    def test_histogram_matching_changes_distribution(self):
        source = np.full((3, 4, 3), 20, np.uint8)
        reference = np.full((7, 2, 3), 180, np.uint8)
        result, info = execute('histogram_matching', source, {}, reference)
        self.assertTrue(np.all(result == 180))
        self.assertGreater(info['cdf_distance_before'], 0)
        self.assertEqual(info['cdf_distance_after'], 0)
        with self.assertRaises(ValueError):
            execute('histogram_matching', source, {})

    def test_exact_pdf_matrices_and_equalization_mapping(self):
        result, info = execute('lab_histogram_matrix', self.image, {})
        self.assertEqual(result.shape, (5, 5))
        self.assertEqual(info['histogram'], [2, 5, 3, 4, 5, 2, 4])
        basic, info = execute('lab_basic_equalization', self.image, {})
        self.assertEqual((info['total_pixels'], info['cdf_min']), (64, 1))
        self.assertEqual((info['mapping'][52], info['mapping'][55]), (4, 16))
        normalized, info = execute('lab_normalized_equalization', self.image, {})
        self.assertEqual((info['mapping'][52], info['mapping'][55]), (0, 12))
        self.assertEqual(normalized[0, 0], 0)
        binary, info = execute('binary_matrix', self.image, {})
        self.assertEqual(info['foreground_pixels'], 7)
        self.assertEqual(set(np.unique(binary)), {0, 255})

    def test_png_export_decodes_to_exact_input_pixels(self):
        result, info = execute('image_read_save', self.image, {})
        data = base64.b64decode(info['artifact']['data'].split(',')[1])
        decoded = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
        np.testing.assert_array_equal(decoded, self.image)
        self.assertEqual(len(data), info['png_bytes'])


if __name__ == '__main__':
    unittest.main()
