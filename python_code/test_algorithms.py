import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'app_backend'))

import base64
import io
import json
import unittest

import cv2
import numpy as np

from web_app import app, COURSE
from OperationRegistry import OPERATIONS
from RunOperation import execute
from ConvertToGray import gray
from RunLengthCoding import rle_encode, rle_decode
from HuffmanCoding import huffman_encode, huffman_decode
from ArithmeticCoding import arithmetic_encode, arithmetic_decode
from LZWCoding import lzw_encode, lzw_decode


class ChapterTests(unittest.TestCase):

    def setUp(self):
        self.image = np.random.default_rng(42).integers(0, 256, (48, 64, 3), dtype=np.uint8)

    def test_all_selectable_algorithm_variants(self):
        for key, spec in OPERATIONS.items():
            for field in spec['fields']:
                if field['type'] != 'select':
                    continue
                for option in field['options']:
                    with self.subTest(operation=key, field=field['key'], value=option):
                        result, details = execute(key, self.image, {field['key']: option}, self.image)
                        self.assertEqual(result.dtype, np.uint8)
                        self.assertIn(result.ndim, [2, 3])
                        self.assertGreater(result.size, 0)
                        json.dumps(details, allow_nan=False)

    def test_course_topics_have_valid_source_and_presets(self):
        self.assertEqual(len(COURSE['chapters']), 8)
        self.assertEqual(len(COURSE['topics']), 86)
        for chapter in COURSE['chapters']:
            topics = [topic for topic in COURSE['topics'] if topic['chapter'] == chapter['id']]
            self.assertEqual(chapter['topic_count'], len(topics))
        for topic in COURSE['topics']:
            self.assertTrue(topic['lesson'])
            self.assertTrue(topic['pages'])
            for item in topic['operations']:
                with self.subTest(topic=topic['topic'], operation=item['id']):
                    self.assertIn(item['id'], OPERATIONS)
                    output, _ = execute(item['id'], self.image, item['params'], self.image)
                    self.assertGreater(output.size, 0)
        with app.test_client() as client:
            self.assertEqual(len(client.get('/api/course').get_json()['topics']), len(COURSE['topics']))
            with client.get('/api/course/source/1') as pdf:
                self.assertEqual(pdf.status_code, 200)
                self.assertTrue(pdf.data.startswith(b'%PDF'))
            self.assertEqual(client.get('/api/course/source/99').status_code, 404)

    def test_lossless_coders_decode_difficult_sequences(self):
        sequences = [
            [0],
            [255] * 100,
            list(range(256)),
            [0, 255] * 100,
            np.random.default_rng(4).integers(0, 256, 1024).tolist()
        ]
        for sequence in sequences:
            for name in ['RLE', 'Huffman', 'Arithmetic', 'LZW']:
                with self.subTest(codec=name, length=len(sequence)):
                    if name == 'RLE':
                        payload, _ = rle_encode(sequence)
                        decoded = rle_decode(payload)
                    elif name == 'Huffman':
                        payload, metadata = huffman_encode(sequence)
                        decoded = huffman_decode(payload, metadata)
                    elif name == 'Arithmetic':
                        payload, metadata = arithmetic_encode(sequence)
                        decoded = arithmetic_decode(payload, metadata)
                    else:
                        payload, _ = lzw_encode(sequence)
                        decoded = lzw_decode(payload)
                    self.assertEqual(decoded, sequence)

    def test_exported_arithmetic_file_is_independently_decodable(self):
        with app.test_client() as client:
            response = client.post('/api/process', data={
                'operation': 'lossless_coding',
                'params': json.dumps({'codec': 'Arithmetic'}),
                'image': (io.BytesIO(cv2.imencode('.png', self.image)[1].tobytes()), 'input.png')
            })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        document = json.loads(base64.b64decode(data['artifact']['data'].split(',')[1]))
        decoded = np.array(
            arithmetic_decode(base64.b64decode(document['payload_base64']), document['metadata']),
            np.uint8
        ).reshape(document['shape'])
        np.testing.assert_array_equal(decoded, gray(self.image))
        self.assertTrue(data['details']['lossless_round_trip'])
        self.assertEqual(
            len(base64.b64decode(data['artifact']['data'].split(',')[1])),
            data['details']['exported_file_bytes']
        )

    def test_dct_reconstruction(self):
        for dimensions in ['2D', '1D rows']:
            with self.subTest(dimensions=dimensions):
                output, details = execute('dct', self.image, {
                    'mode': 'reconstruction', 'retain': 100, 'dimensions': dimensions
                })
                np.testing.assert_array_equal(output, gray(self.image))
                self.assertLess(details['reconstruction_mse'], 1e-15)

    def test_morphology_mathematical_properties(self):
        binary = np.where(gray(self.image) > 127, 255, 0).astype(np.uint8)
        opening, _ = execute('morphology', self.image, {'method': 'opening'})
        closing, _ = execute('morphology', self.image, {'method': 'closing'})
        self.assertTrue(np.all(opening <= binary))
        self.assertTrue(np.all(closing >= binary))
        opening_twice, _ = execute('morphology', opening, {'method': 'opening'})
        closing_twice, _ = execute('morphology', closing, {'method': 'closing'})
        np.testing.assert_array_equal(opening, opening_twice)
        np.testing.assert_array_equal(closing, closing_twice)


if __name__=='__main__': unittest.main()
