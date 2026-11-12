"""Choose plots and measurements that explain the selected experiment."""
import base64
import io
import os
from pathlib import Path
import tempfile
import threading

import cv2
import numpy as np

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'pixellab-matplotlib'))
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from ConvertToGray import gray
from ConvertToUint8 import u8
from LimitImageSize import bounded
from OperationRegistry import OPERATIONS
from RunOperation import validated_params
from AdditionalLabOutput import additional_panels
from PdfLabLayouts import pdf_panels, mapping_tables, layout_reference
from PdfLabConsole import pdf_console

_plot_lock = threading.Lock()


def image_panel(title, image):
    return {'kind': 'image', 'title': title, 'image': image}


def histogram_panel(title, values):
    return {'kind': 'histogram', 'title': title, 'values': np.bincount(gray(values).ravel(), minlength=256)}


def cdf_panel(title, values):
    hist = np.bincount(gray(values).ravel(), minlength=256)
    return {'kind': 'cdf', 'title': title, 'values': np.cumsum(hist / hist.sum())}


def output_panels(key, original, result, params, details, reference=None):
    """Use real inputs, selected parameters and the actual result in every panel."""
    extra = pdf_panels(key, original, result, params, details, reference)
    if extra is not None:
        return extra
    extra = additional_panels(key, original, result, params, details, reference)
    if extra is not None:
        return extra
    source = gray(original)
    if key == 'histogram':
        return [image_panel('Grayscale input', source), histogram_panel('Intensity histogram', source), cdf_panel('Cumulative probability', source)]
    if key in ('equalize_basic', 'equalize'):
        return [image_panel('Original grayscale', source), histogram_panel('Original histogram', source), cdf_panel('Original CDF', source),
                image_panel('Equalized image', result), histogram_panel('Equalized histogram', result), cdf_panel('Equalized CDF', result)]
    if key in ('stretch', 'clahe'):
        before = original if key == 'stretch' else source
        return [image_panel('Original', before), image_panel('Enhanced image', result),
                histogram_panel('Original histogram', before), histogram_panel('Enhanced histogram', result)]
    if key == 'pixel_matrix':
        return [image_panel('Grayscale input', source), image_panel('Sampled pixel values', result)]
    if key == 'resize':
        h, w = original.shape[:2]
        rh, rw = result.shape[:2]
        return [image_panel(f'Original: {w} x {h}', original), image_panel(f'Resized: {rw} x {rh}', result)]
    if key == 'crop':
        marked = original.copy()
        h, w = original.shape[:2]
        x = int(w * params['x'] / 100)
        y = int(h * params['y'] / 100)
        right = min(w, max(x + 1, int(w * (params['x'] + params['width']) / 100)))
        bottom = min(h, max(y + 1, int(h * (params['y'] + params['height']) / 100)))
        cv2.rectangle(marked, (x, y), (right - 1, bottom - 1), (0, 0, 255), max(1, min(h, w) // 200))
        return [image_panel('Selected crop region', marked), image_panel('Cropped image', result)]
    if key == 'matching':
        target = cv2.resize(gray(reference), (source.shape[1], source.shape[0]))
        return [image_panel('Source grayscale', source), image_panel('Aligned reference', target), image_panel('Absolute pixel difference', result)]
    if key == 'morphology':
        _, binary = cv2.threshold(source, params['threshold'], 255, cv2.THRESH_BINARY)
        return [image_panel('Binary input', binary), image_panel(params['method'].capitalize(), result)]
    if key in ('threshold', 'otsu', 'adaptive'):
        return [image_panel('Grayscale input', source), image_panel(OPERATIONS[key]['name'], result)]
    if key in ('sobel', 'prewitt', 'roberts', 'canny', 'laplacian'):
        title = 'Sharpened image' if key == 'laplacian' and params['mode'] == 'sharpen' else 'Edge response'
        return [image_panel('Grayscale input', source), image_panel(title, result)]
    if key == 'fft':
        return [image_panel('Grayscale input', source), image_panel('Centered log DFT magnitude', result)]
    if key == 'idft':
        error = np.abs(source.astype(float) - result.astype(float))
        return [image_panel('Grayscale input', source), image_panel('IDFT reconstruction', result), image_panel('Absolute error (0 to 255)', error)]
    if key == 'dct':
        values = gray(bounded(original, 1024))
        if params['mode'] == 'spectrum':
            return [image_panel('Grayscale input', values), image_panel(f"Log DCT magnitude: {params['dimensions']}", result)]
        from ForwardCosineTransform import forward_dct
        coefficients = forward_dct(values.astype(float), params['dimensions'])
        rows = values.shape[0] if params['dimensions'] == '1D rows' else max(1, round(values.shape[0] * params['retain'] / 100))
        cols = max(1, round(values.shape[1] * params['retain'] / 100))
        retained = np.zeros_like(coefficients)
        retained[:rows, :cols] = coefficients[:rows, :cols]
        spectrum = cv2.normalize(np.log1p(np.abs(retained)), None, 0, 255, cv2.NORM_MINMAX)
        return [image_panel('Grayscale input', values), image_panel('Retained DCT magnitude', spectrum), image_panel('IDCT reconstruction', result)]
    if key == 'frequency_filter':
        h, w = source.shape
        yy, xx = np.ogrid[:h, :w]
        radius = min(h, w) * params['radius'] / 100
        mask = (xx - w // 2) ** 2 + (yy - h // 2) ** 2 <= radius ** 2
        if params['mode'] == 'high-pass':
            mask = ~mask
        return [image_panel('Grayscale input', source), image_panel('Frequency mask', mask.astype(np.uint8) * 255), image_panel(params['mode'] + ' result', result)]
    if key == 'noise_models':
        difference = gray(result).astype(float) - source.astype(float)
        counts, edges = np.histogram(difference, bins=61, range=(-255, 255))
        return [image_panel('Original', original), image_panel(params['model'] + ' noise', result),
                {'kind': 'noise', 'title': 'Applied grayscale noise', 'values': counts, 'x': (edges[1:] + edges[:-1]) / 2}]
    if key == 'inverse_wiener':
        from BlurKernel import psf
        from BlurTransferFunction import otf
        values = gray(bounded(original, 1024)).astype(float)
        if params['input_mode'] == 'uploaded degraded image':
            return [image_panel('Uploaded degraded input', values), image_panel(params['method'] + ' restoration', result)]
        transfer = otf(psf(params['kernel'], params['blur']), values.shape)
        blurred = np.fft.ifft2(np.fft.fft2(values) * transfer).real
        observed = blurred + np.random.default_rng(42).normal(0, params['noise'], values.shape)
        return [image_panel('Original grayscale', values), image_panel('Blurred + noisy observation', u8(observed)), image_panel(params['method'] + ' restoration', result)]
    if key in ('compression', 'lossless_coding'):
        if key == 'compression':
            before = original
            sizes = [details['raw_pixel_bytes'], details['jpeg_bytes']]
            labels = ['Raw pixels', 'JPEG file']
            title = 'Decoded JPEG'
        else:
            before = gray(bounded(original, int(params['size'])))
            sizes = [details['raw_grayscale_bytes'], details['coded_payload_bytes'], details['exported_file_bytes']]
            labels = ['Raw grayscale', 'Coded payload', 'Exported JSON']
            title = params['codec'] + ' decoded image'
        return [image_panel('Encoding input', before), image_panel(title, result),
                {'kind': 'sizes', 'title': 'Storage size (bytes)', 'values': sizes, 'labels': labels}]
    labels = {
        'grayscale': 'Grayscale image', 'negative': 'Negative image', 'contrast': 'Brightness / contrast result',
        'gamma': 'Gamma-corrected image', 'quantization': 'Quantized image', 'color_channel': params.get('channel', 'Selected channel'),
        'rotate': 'Rotated image', 'flip': 'Flipped image', 'mean': 'Average-filtered image', 'gaussian': 'Gaussian-filtered image',
        'median': 'Median-filtered image', 'bilateral': 'Bilateral-filtered image', 'sharpen': 'Sharpened image',
        'log_transform': params.get('mode', 'log') + ' transform', 'bit_planes': 'Bit-plane result'
    }
    before = source if key == 'bit_planes' or key == 'quantization' and params['domain'] == 'grayscale' else original
    return [image_panel('Input image', before), image_panel(labels[key], result)]


def draw_panel(axis, panel):
    kind = panel['kind']
    axis.set_title(panel['title'], fontsize=11)
    if kind == 'image':
        image = panel['image']
        small = bounded(image, 960)
        if small.ndim == 3 and not panel.get('encoded_rgb'):
            small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        maximum = panel.get('vmax', 255)
        shown = axis.imshow(small, cmap=panel.get('cmap', 'gray'), vmin=0, vmax=maximum, interpolation='nearest')
        if panel.get('colorbar'):
            axis.figure.colorbar(shown, ax=axis, shrink=0.75)
        if panel.get('axes'):
            axis.set_xlabel('Column')
            axis.set_ylabel('Row')
            if panel.get('matrix_ticks'):
                axis.set_xticks(range(image.shape[1]))
                axis.set_yticks(range(image.shape[0]))
        else:
            axis.axis('off')
        index_labels = panel.get('index_labels')
        if index_labels is not None:
            for y in range(index_labels.shape[0]):
                for x in range(index_labels.shape[1]):
                    axis.text(x, y, str(index_labels[y, x]), ha='center', va='center', color='white', fontsize=11, fontweight='bold')
        if image.ndim == 2 and max(image.shape) <= 16 and panel.get('annotate', True):
            for y in range(image.shape[0]):
                for x in range(image.shape[1]):
                    value = int(image[y, x])
                    axis.text(x, y, str(value), ha='center', va='center', fontsize=7,
                              color='black' if value > maximum / 2 else 'white')
    elif kind == 'table':
        axis.axis('off')
        table = axis.table(cellText=panel['rows'], colLabels=['Measurement', 'Value'], loc='center', cellLoc='left')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.6)
    elif kind == 'graph':
        pixels = panel['pixels']
        for first, second in panel['edges']:
            y1, x1 = first
            y2, x2 = second
            axis.plot([x1, x2], [-y1, -y2], color='gray')
        for y in range(pixels.shape[0]):
            for x in range(pixels.shape[1]):
                axis.scatter(x, -y, s=800, color='lightblue', edgecolors='black', zorder=3)
                label = f'({y},{x})' if panel.get('coordinate_labels') else str(pixels[y, x])
                axis.text(x, -y, label, ha='center', va='center', zorder=4, fontsize=9)
        axis.set_aspect('equal')
        axis.margins(0.25)
        axis.axis('off')
    elif kind == 'sizes':
        bars = axis.bar(panel['labels'], panel['values'], color='#277454')
        axis.bar_label(bars, fontsize=8, padding=3)
        axis.set_ylabel('Bytes')
        axis.margins(y=0.2)
    else:
        values = panel['values']
        if kind == 'cdf':
            axis.plot(np.arange(256), values, color='#277454')
            axis.set_ylabel(panel.get('ylabel', 'Cumulative probability'))
            if panel.get('probability', True):
                axis.set_ylim(0, 1.02)
        else:
            x = panel.get('x', np.arange(len(values)))
            width = x[1] - x[0] if len(x) > 1 else 1
            axis.bar(x, values, width=width, color='#526ba3')
            axis.set_ylabel('Pixel count')
        axis.set_xlabel('Intensity change' if kind == 'noise' else 'Pixel intensity')
        axis.grid(axis='y', alpha=0.2)
        axis.set_axisbelow(True)


def console_output(key, original, result, before, after, params, details, reference=None):
    example = pdf_console(key, original, result, params, details, reference)
    if example is not None:
        return example
    lines = [f">>> Operation: {OPERATIONS[key]['name']}", f'Parameters: {params}', '']
    if key in ('resize', 'crop', 'rotate', 'flip'):
        lines += [f"Input size: {before['width']} x {before['height']}", f"Output size: {after['width']} x {after['height']}"]
    elif key == 'pixel_matrix':
        lines += [f'Processed grayscale pixel matrix (actual {result.shape[0]} x {result.shape[1]}):',
                  np.array2string(result, max_line_width=100, threshold=256)]
    elif key in ('histogram', 'equalize_basic', 'equalize', 'stretch', 'clahe'):
        stats = [('Input', before)] if key == 'histogram' else [('Input', before), ('Output', after)]
        for label, item in stats:
            lines += [f'{label} intensity range: {item["min"]} to {item["max"]}',
                      f'{label} RMS contrast: {item["rms_contrast"]}',
                      f'{label} histogram:', np.array2string(np.array(item['histogram']), max_line_width=100, threshold=256)]
            if key in ('histogram', 'equalize_basic', 'equalize'):
                lines += [f'{label} CDF:', np.array2string(np.array(item['cdf']), precision=4, max_line_width=100, threshold=256)]
    elif key in ('threshold', 'otsu', 'adaptive', 'morphology'):
        white = int(np.count_nonzero(result))
        lines += [f'Foreground pixels: {white}', f'Background pixels: {result.size - white}']
    elif key in ('sobel', 'prewitt', 'roberts', 'canny') or key == 'laplacian' and params['mode'] == 'edge magnitude':
        lines += [f'Nonzero edge-response pixels: {np.count_nonzero(result)}']
    elif key == 'bit_planes':
        lines += [f"Selected bit: {params['bit']}", f'Nonzero output pixels: {np.count_nonzero(result)}']
    elif key in ('contrast', 'gamma', 'log_transform', 'sharpen', 'laplacian'):
        lines += [f"Input mean intensity: {before['mean']}", f"Output mean intensity: {after['mean']}",
                  f"Input RMS contrast: {before['rms_contrast']}", f"Output RMS contrast: {after['rms_contrast']}"]
    elif key in ('fft', 'dct', 'frequency_filter', 'idft'):
        values = gray(bounded(original, 1024)) if key == 'dct' else gray(original)
        lines += [f'Transform input: {values.shape[1]} x {values.shape[0]}',
                  'Spectrum / mask panels are display maps; reconstruction error is reported when available.']
    elif key in ('grayscale', 'color_channel', 'quantization'):
        lines += [f"Output channels: {after['channels']}", f"Output intensity range: {after['min']} to {after['max']}"]
    excluded = {'pixel_matrix', 'download', 'artifact'}
    if key in ('lab_basic_equalization', 'lab_normalized_equalization'):
        lines += ['Original 8 x 8 matrix:', np.array2string(np.array(details['original_matrix'])),
                  'Equalized 8 x 8 matrix:', np.array2string(result),
                  'Intensity  Frequency  Cumulative count  Mapped intensity']
        for value in details['intensities']:
            lines.append(f"{value:9} {details['histogram'][value]:10} {details['cumulative_counts'][value]:17} {details['mapping'][value]:17}")
        excluded.update(('original_matrix', 'equalized_matrix', 'histogram', 'cumulative_counts', 'mapping', 'intensities'))
    if key in ('lab_histogram_matrix', 'pixel_connectivity'):
        lines += ['PDF/sample pixel matrix:', np.array2string(result)]
    for name, value in details.items():
        if name not in excluded:
            lines.append(f'{name}: {value}')
    lines += ['', 'Process finished successfully.']
    return '\n'.join(lines)


def make_output(original, result, before, after, key, params, details, reference=None):
    settings = validated_params(key, params)
    panels = output_panels(key, original, result, settings, details, reference)
    columns = 4 if key == 'quantization' else 2 if len(panels) == 4 else min(len(panels), 3)
    rows = (len(panels) + columns - 1) // columns
    with _plot_lock:
        figure = Figure(figsize=(5 * columns, 4.5 * rows), dpi=140, facecolor='white')
        axes = figure.subplots(rows, columns, squeeze=False).ravel()
        figure.suptitle(OPERATIONS[key]['name'], fontsize=14)
        for axis, panel in zip(axes, panels):
            draw_panel(axis, panel)
        for axis in axes[len(panels):]:
            axis.axis('off')
        figure.tight_layout(rect=(0, 0, 1, 0.94), h_pad=2, w_pad=2)
        buffer = io.BytesIO()
        FigureCanvasAgg(figure).print_png(buffer)
        figure.clear()
    titles = [panel['title'] for panel in panels]
    return {
        'figure': 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii'),
        'console': console_output(key, original, result, before, after, settings, details, reference),
        'panels': titles,
        'caption': ' · '.join(titles),
        'tables': mapping_tables(key, original, result, details),
        'layout_reference': layout_reference(key)
    }
