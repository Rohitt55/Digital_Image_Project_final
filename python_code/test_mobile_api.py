"""Compatibility checks for the native Android client's compact API requests."""
import base64
import io
from pathlib import Path
import sys
import socket
sys.path.insert(0, str(Path(__file__).resolve().parent / 'app_backend'))

import unittest
import cv2
import numpy as np
from web_app import app


class MobileApiTests(unittest.TestCase):
    def test_mobile_launcher_skips_an_occupied_port(self):
        from mobile_server import available_port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as occupied:
            occupied.bind(('127.0.0.1', 0))
            port = occupied.getsockname()[1]
            if port > 65519:
                self.skipTest('No room above this ephemeral port for the search window.')
            self.assertNotEqual(available_port('127.0.0.1', port), port)

    def test_compact_catalog_preserves_operations_and_settings(self):
        with app.test_client() as client:
            full = client.get('/api/operations').get_json()
            compact = client.get('/api/operations?include_code=false').get_json()
            self.assertEqual(len(full), len(compact))
            for normal, mobile in zip(full, compact):
                self.assertNotIn('code', mobile)
                self.assertEqual(normal['id'], mobile['id'])
                self.assertEqual(normal['fields'], mobile['fields'])
            example = client.get('/api/operations/resize')
            self.assertEqual(example.status_code, 200)
            self.assertIn('cv2.imread', example.get_json()['code'])
            self.assertEqual(client.get('/api/operations/unknown').status_code, 404)

    def test_mobile_result_omits_duplicate_original_only_when_requested(self):
        image = np.full((8, 10, 3), 50, dtype=np.uint8)
        encoded = cv2.imencode('.png', image)[1].tobytes()
        with app.test_client() as client:
            response = client.post('/api/process', data={
                'operation': 'negative', 'include_original': 'false', 'lab_output': 'true',
                'image': (io.BytesIO(encoded), 'input.png')
            })
            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertIsNone(result['original'])
            raw = base64.b64decode(result['result'].split(',')[1])
            pixels = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
            self.assertTrue(np.all(pixels == 205))
            self.assertTrue(result['lab']['figure'].startswith('data:image/png;base64,'))
            response = client.post('/api/process', data={'operation': 'negative', 'image': (io.BytesIO(encoded), 'input.png')})
            self.assertIsNotNone(response.get_json()['original'])


if __name__ == '__main__':
    unittest.main()
