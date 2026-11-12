"""Validate parameters and run the selected lab operation."""
import math
import time

from OperationRegistry import OPERATIONS


def validated_params(key, params):
    spec = OPERATIONS[key]
    clean = {}
    for item in spec['fields']:
        value = params.get(item['key'], item['default'])
        if item['type'] == 'select':
            if value not in item['options']:
                raise ValueError('Invalid ' + item['label'] + '.')
        elif item['type'] == 'text':
            if not isinstance(value, str) or len(value) > 512:
                raise ValueError(item['label'] + ' must be text of at most 512 characters.')
        else:
            try:
                value = float(value)
            except (TypeError, ValueError) as exc:
                raise ValueError(item['label'] + ' must be a number.') from exc
            if not math.isfinite(value) or not item['min'] <= value <= item['max']:
                raise ValueError(f"{item['label']} must be between {item['min']} and {item['max']}.")
            if item['step'] == 1:
                if not value.is_integer():
                    raise ValueError(item['label'] + ' must be a whole number.')
                value = int(value)
        clean[item['key']] = value
    if 'kernel' in clean and clean['kernel'] % 2 == 0:
        raise ValueError('Kernel size must be an odd number (3, 5, 7, ...).')
    return clean


def execute(key, image, params, reference=None):
    spec = OPERATIONS[key]
    clean = validated_params(key, params)
    start = time.perf_counter()
    output = spec['function'](image, clean, reference)
    result, extra = output if isinstance(output, tuple) else (output, {})
    extra['processing_ms'] = round((time.perf_counter() - start) * 1000, 2)
    return (result, extra)
