import base64
import json


def artifact(method, shape, payload, metadata):
    document = {
        'format': 'PixelLab teaching codec v1',
        'method': method,
        'shape': list(shape),
        'metadata': metadata,
        'payload_base64': base64.b64encode(payload).decode('ascii')
    }
    encoded = json.dumps(document, separators=(',', ':')).encode('utf8')
    return ({
        'name': f"PixelLab-{method.lower().replace(' ', '-')}.json",
        'mime': 'application/json',
        'data': 'data:application/json;base64,' + base64.b64encode(encoded).decode('ascii')
    }, len(encoded))
