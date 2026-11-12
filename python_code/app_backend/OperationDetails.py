"""Describe an operation and locate its Python implementation."""
import ast
import inspect
from pathlib import Path

from OperationRegistry import OPERATIONS


def describe(key):
    item = OPERATIONS[key]
    function = item['function']
    implementation = Path(inspect.getsourcefile(function)).resolve()
    code_root = Path(__file__).resolve().parent.parent
    lab_names = {
        'ImageNoise.py': 'GaussianNoise.py',
        'ImageRestoration.py': 'WienerFilter.py',
        'ImageMorphology.py': 'MorphologicalOpening.py',
        'LosslessImageCoding.py': 'HuffmanCoding.py',
        'ImageResize.py': 'ImageTransformComparison.py',
        'ImageCropping.py': 'ImageTransformComparison.py',
        'ImageRotation.py': 'ImageTransformComparison.py',
        'ImageFlip.py': 'ImageTransformComparison.py',
        'AverageFilter.py': 'SmoothingFilterComparison.py',
        'GaussianFilter.py': 'SmoothingFilterComparison.py',
        'MedianFilter.py': 'SmoothingFilterComparison.py',
        'BilateralFilter.py': 'SmoothingFilterComparison.py',
        'SobelEdgeDetection.py': 'EdgeDetectionComparison.py',
        'PrewittEdgeDetection.py': 'EdgeDetectionComparison.py',
        'RobertsEdgeDetection.py': 'EdgeDetectionComparison.py',
        'CannyEdgeDetection.py': 'EdgeDetectionComparison.py',
        'BinaryThreshold.py': 'ThresholdComparison.py',
        'AdaptiveThreshold.py': 'ThresholdComparison.py',
        'AdaptiveMeanThreshold.py': 'ThresholdComparison.py',
        'OtsuThreshold.py': 'ThresholdComparison.py',
        'WatershedSegmentation.py': 'SegmentationComparison.py',
        'RegionGrowing.py': 'SegmentationComparison.py',
        'KMeansSegmentation.py': 'SegmentationComparison.py'
    }
    lab_file = code_root / lab_names.get(implementation.name, implementation.name)
    code = lab_file.read_text(encoding='utf-8')
    names = {'cv2': 'OpenCV', 'numpy': 'NumPy', 'scipy': 'SciPy', 'matplotlib': 'Matplotlib'}
    libraries = set()
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [node.module or '']
        else:
            continue
        for module in modules:
            module_name = module.split('.')[0]
            if module_name in names:
                libraries.add(names[module_name])
    return {
        **{k: v for k, v in item.items() if k != 'function'},
        'code': code,
        'implementation_file': 'python_code/' + lab_file.relative_to(code_root).as_posix(),
        'module_libraries': sorted(libraries),
        'code_type': 'Standalone Python lab script (default example settings)'
    }
