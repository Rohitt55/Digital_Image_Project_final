"""Device-local adapter for the existing lab operations; never starts a web server."""
import base64
import io
import json
import os
from pathlib import Path
import sys


def initialize(cache_dir):
    os.environ['MPLCONFIGDIR'] = str(Path(cache_dir) / 'matplotlib')
    os.environ['MPLBACKEND'] = 'Agg'
    sys.path.insert(0, str(Path(__file__).parent / 'python_code' / 'app_backend'))
    import OperationLoader  # registers all bundled operations


def encode(image):
    import cv2
    ok, data = cv2.imencode('.png', image)
    if not ok:
        raise ValueError('Cannot encode the processed image.')
    return 'data:image/png;base64,' + base64.b64encode(data).decode('ascii')


def get_json(path):
    from OperationRegistry import OPERATIONS
    from OperationDetails import describe
    if path == '/api/health':
        value = dict(status='ok', offline=True, operations=len(OPERATIONS))
    elif path == '/api/chapters':
        course = json.loads((Path(__file__).parent / 'data/course_topics.json').read_text(encoding='utf8'))
        value = [dict(id=item['id'], title=item['title']) for item in course['chapters']]
    elif path.startswith('/api/operations/'):
        value = describe(path.rsplit('/', 1)[-1])
    elif path.startswith('/api/operations'):
        course = json.loads((Path(__file__).parent / 'data/course_topics.json').read_text(encoding='utf8'))
        memberships = {}
        for topic in course['topics']:
            for operation in topic['operations']:
                memberships.setdefault(operation['id'], set()).add(topic['chapter'])
        fallback = {'Fundamentals': 1, 'Color & intensity': 3, 'Histograms': 2,
                    'Geometry': 4, 'Filters & restoration': 6, 'Edges & segmentation': 5,
                    'Morphology': 8, 'Transforms & comparison': 4, 'Compression': 7}
        value = [describe(key) for key in OPERATIONS]
        for item in value:
            item['chapters'] = sorted(memberships.get(item['id']) or {fallback.get(item['group'], 1)})
        if 'include_code=false' in path:
            for item in value:
                item.pop('code', None)
    elif path == '/api/demo':
        import cv2
        from ImageStatistics import statistics
        image = cv2.imread(str(Path(__file__).parent / 'images' / 'sample.png'))
        value = dict(image=encode(image), statistics=statistics(image))
    else:
        raise ValueError('Unknown local request.')
    return json.dumps(value)


def read_image(data):
    import cv2
    import numpy as np
    from PIL import Image, ImageOps
    with Image.open(io.BytesIO(base64.b64decode(data))) as source:
        if source.width * source.height > 12_000_000:
            raise ValueError('Please use an image with at most 12 million pixels.')
        rgb = np.asarray(ImageOps.exif_transpose(source).convert('RGB'))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def process_json(operation, params_json, image_b64, reference_b64=''):
    import cv2
    from OperationRegistry import OPERATIONS
    from OperationDetails import describe
    from RunOperation import execute
    from ImageStatistics import statistics
    from LabOutput import make_output
    try:
        if operation not in OPERATIONS:
            raise ValueError('Choose a valid processing operation.')
        params = json.loads(params_json)
        if not isinstance(params, dict):
            raise ValueError('Parameters must be a JSON object.')
        image = read_image(image_b64)
        reference = read_image(reference_b64) if reference_b64 else None
        if (OPERATIONS[operation]['requires_reference'] or operation == 'matching') and reference is None:
            raise ValueError('Choose a reference image for this operation.')
        result, details = execute(operation, image, params, reference)
        output = details.pop('download') if operation == 'compression' else encode(result)
        artifact = details.pop('artifact', None)
        before, after = statistics(image), statistics(result)
        lab = make_output(image, result, before, after, operation, params, details, reference)
        return json.dumps(dict(original=None, result=output, before=before, after=after,
                               details=details, lab=lab, artifact=artifact, operation=describe(operation)['name']))
    except cv2.error:
        return json.dumps(dict(error='These settings cannot be applied. Try a larger image or smaller kernel.'))
    except (ValueError, TypeError, OverflowError, OSError) as exc:
        return json.dumps(dict(error=str(exc)))
