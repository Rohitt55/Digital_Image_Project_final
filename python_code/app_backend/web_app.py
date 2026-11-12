"""Local web interface for the supplied CSE 4245 image-processing labs."""
import base64
import io
import json
import warnings
from pathlib import Path

import cv2
import numpy as np
from flask import Flask, jsonify, render_template_string, request, send_file
from PIL import Image, ImageOps, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge

from OperationRegistry import OPERATIONS
from RunOperation import execute
from OperationDetails import describe
from ImageStatistics import statistics
import OperationLoader  # Registers the additional chapter algorithms.

PROJECT_ROOT = Path(__file__).resolve().parents[2]
app = Flask(__name__, static_folder=str(PROJECT_ROOT / 'static'), static_url_path='/static')
COURSE = json.loads((PROJECT_ROOT / 'data/course_topics.json').read_text(encoding='utf8'))
app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 12_000_000


# Page markup is kept here so the interface can be edited in this Python file.
INDEX_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f4f5f7">
  <title>PixelLab — Digital Image Processing</title>
  <link rel="icon" href="{{ url_for('static', filename='favicon.svg') }}" type="image/svg+xml">
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='usability.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='plain.css') }}">
  <script src="{{ url_for('static', filename='app.js') }}" defer></script>
</head>
<body>
  <aside class="sidebar">
    <a href="/" class="brand">PixelLab</a>
    <button id="mobile-menu" class="mobile-menu" aria-expanded="false" aria-controls="operation-list">Browse operations <span aria-hidden="true">☰</span></button>
    <p class="sidebar-caption">Operations</p>
    <label class="search"><span>⌕</span><input id="search" type="search" placeholder="Find an operation…" aria-label="Search operations"></label>
    <label class="chapter-selector">CHAPTER<select id="chapter-filter" aria-label="Filter operations by chapter"><option value="0">All chapters</option></select></label>
    <div class="nav-status"><span id="operation-count">Loading…</span><button id="clear-search" class="nav-clear" hidden>Clear filters</button></div>
    <nav id="operation-list" aria-label="Image processing operations"><p class="muted">Loading operations…</p></nav>
  </aside>
  <main>
    <section class="page-heading"><div><h1>Digital Image Processing Lab</h1><p class="subtitle">Upload an image, select an operation and view the output.</p></div><div class="heading-actions"><button class="button secondary" id="demo-button">Try a sample</button></div></section>
    <ol class="workflow" aria-label="Your experiment steps"><li id="step-upload" class="current"><span class="step-number">1</span><div><strong>Add an image</strong><small>Upload or use the sample</small></div></li><li id="step-run"><span class="step-number">2</span><div><strong>Choose & run</strong><small>Defaults are ready to use</small></div></li><li id="step-result"><span class="step-number">3</span><div><strong>Compare & save</strong><small>Image, plots and statistics</small></div></li></ol>
    <section class="upload-zone" id="drop-zone" aria-label="Image upload">
      <div><strong id="filename">Input image</strong><p id="upload-description">Choose or drop a PNG, JPG, WebP, BMP or TIFF file.</p><span id="upload-details" class="upload-details" hidden></span></div>
      <label class="button secondary file-label">Choose image<input id="image-upload" type="file" accept="image/*,.tif,.tiff,.bmp"></label>
    </section>
    <p id="notice" class="notice" role="status" aria-live="polite" hidden></p>
    <section class="quick-start" aria-label="Popular operations"><div><strong>Common operations</strong></div><div id="quick-operations" class="quick-operations"></div></section>
    <section class="control-panel" id="settings-panel">
      <div class="operation-info"><p class="eyebrow" id="operation-group">COLOR & INTENSITY</p><h2 id="operation-name">Grayscale</h2><p id="operation-explanation"></p><button class="text-button browse-all" id="browse-all">Browse all operations →</button></div>
      <form id="process-form"><div class="settings-toolbar"><span id="settings-caption">Operation settings</span><button type="button" class="text-button" id="reset-settings">Reset settings ↺</button></div><div id="parameters" class="parameters"></div><div id="reference-wrap" hidden><label class="parameter">Reference image<input type="file" id="reference-upload" accept="image/*,.tif,.tiff,.bmp"></label><span id="reference-name" class="muted"></span><p class="reference-help">This operation compares two images. Choose the second image here.</p></div><div class="run-row"><button type="submit" class="button primary" id="run-button" disabled>Run operation <span>→</span></button><button type="button" class="button secondary" id="download-button" disabled>↓ &nbsp; Download</button><button type="button" class="button secondary" id="download-encoded" hidden disabled>Download encoded file</button></div><p id="run-help" class="run-help" aria-live="polite">Add an image to get started.</p></form>
    </section>
    <div class="result-heading"><div><h2>Output</h2></div><span id="result-status" class="result-status">No result yet</span></div>
    <section class="studio-grid">
      <article class="image-card"><div class="card-heading"><h2><span class="card-dot"></span> Original image</h2><div class="image-tools"><span class="image-meta" id="original-meta">No image yet</span><button id="zoom-original" class="zoom-button" aria-label="Enlarge original image" disabled>⤢</button></div></div><div class="image-stage" id="original-stage"><img id="original-image" alt="Original uploaded image" hidden><div class="empty-state" id="original-empty"><span>▧</span><h3>Input preview</h3><p>No image uploaded.</p></div></div><div class="card-footer"><span>INPUT</span><button class="text-button" id="reset-button" disabled>Reset to uploaded image ↺</button></div></article>
      <article class="image-card result-card"><div class="card-heading"><h2><span class="card-dot green"></span> Processed image</h2><div class="image-tools"><span id="result-meta" class="image-meta">No result yet</span><button id="zoom-result" class="zoom-button" aria-label="Enlarge processed image" disabled>⤢</button></div></div><div class="image-stage" id="result-stage"><img id="result-image" alt="Processed output image" hidden><div class="empty-state" id="result-empty"><span>✳</span><h3>Processed output</h3><p>Run an operation to display its output.</p></div><div id="result-busy" class="processing-overlay" role="status" hidden><span class="spinner" aria-hidden="true"></span><strong>Processing your image…</strong><span>Generating output and plots</span></div></div><div class="card-footer"><span id="result-label">OUTPUT</span><button class="text-button" id="use-result" disabled>Use as next input →</button></div></article>
    </section>
    <section class="analysis-panel">
      <div class="tabs" role="tablist" aria-label="Experiment details"><button role="tab" id="tab-lab-output" aria-selected="true" aria-controls="lab-output" class="tab active" data-tab="lab-output">Lab output</button><button role="tab" id="tab-insights" aria-selected="false" aria-controls="insights" class="tab" data-tab="insights">Image insights</button><button role="tab" id="tab-algorithm" aria-selected="false" aria-controls="algorithm" class="tab" data-tab="algorithm">Algorithm & code</button><button role="tab" id="tab-history" aria-selected="false" aria-controls="history" class="tab" data-tab="history">Experiment history <span id="history-count">0</span></button></div>
      <div id="lab-output" class="tab-panel" role="tabpanel" aria-labelledby="tab-lab-output">
        <div class="lab-heading"><div><h3>Plots</h3><p id="lab-caption" class="muted">Run an operation to see its relevant plots and measurements.</p></div><button id="save-figure" class="button secondary" disabled>Save figure</button></div>
        <p id="lab-empty" class="lab-empty">Run an operation to see its Matplotlib figure and printed output here.</p>
        <a id="lab-figure-link" class="lab-figure-link" target="_blank" rel="noopener" aria-label="Open lab figure at full size" hidden><img id="lab-figure" class="lab-figure" alt="Operation-specific lab output" hidden></a>
        <a id="lab-layout-reference" class="source-line" target="_blank" rel="noopener" hidden></a>
        <div id="lab-tables" class="lab-tables" aria-label="Experiment result tables"></div>
        <details id="console-wrap" class="console-wrap" open hidden><summary>Terminal / printed output <span>Python</span></summary><pre id="lab-console" tabindex="0" aria-label="Python lab printed results"></pre></details>
      </div>
      <div id="insights" class="tab-panel" role="tabpanel" aria-labelledby="tab-insights" hidden><div class="stats-grid" id="stats"><div><span>DIMENSIONS</span><strong>—</strong></div><div><span>MEAN INTENSITY</span><strong>—</strong></div><div><span>RMS CONTRAST</span><strong>—</strong></div><div><span>PROCESSING TIME</span><strong>—</strong></div></div><div class="chart-heading"><h3>Intensity distribution</h3><div class="legend"><span class="before-key"></span>Original <span class="after-key"></span>Processed</div></div><canvas id="histogram-chart" height="180" aria-label="Grayscale histogram of original and processed images" role="img"></canvas><div class="chart-axis"><span>0 · Black</span><span>Grayscale pixel intensity</span><span>255 · White</span></div><div id="extra-details" class="extra-details"></div></div>
      <div id="algorithm" class="tab-panel" role="tabpanel" aria-labelledby="tab-algorithm" hidden><p class="muted">Understand the operation you are running.</p><div id="formula" class="formula"></div><p class="source-line">Course reference: <span id="source"></span></p><p class="source-line">Code type: <span id="code-type"></span><br>Module libraries: <span id="code-libraries"></span></p><details open><summary>Python implementation · <span id="implementation-file">python_code/ImageGrayscale.py</span></summary><pre><code id="python-code"></code></pre></details><p class="muted code-note">Shared helpers: gray() converts BGR to grayscale; normalize() maps values to 0–255. Parameters are validated by execute() before this function runs.</p></div>
      <div id="history" class="tab-panel" role="tabpanel" aria-labelledby="tab-history" hidden><p class="muted" id="history-empty">Your completed experiments will appear here during this session.</p><div id="history-list"></div></div>
    </section>
    <footer class="page-footer"><span>Developed by Rohiit Sarkar &middot; ID: 0802310405101055</span><span>PixelLab</span></footer>
  </main>
  <dialog id="image-viewer" class="image-viewer" aria-labelledby="viewer-title"><div class="viewer-heading"><h2 id="viewer-title">Image preview</h2><button id="close-viewer" class="button secondary" autofocus>Close ✕</button></div><img id="viewer-image" alt="Enlarged image preview"></dialog>
</body>
</html>
"""


def read_image(upload):
    if upload is None or not upload.filename:
        raise ValueError('Please upload an image first.')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(upload.stream) as image:
                if image.width * image.height > 12000000:
                    raise ValueError('Please use an image with at most 12 million pixels.')
                rgb = np.asarray(ImageOps.exif_transpose(image).convert('RGB'))
        return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise ValueError('Cannot read this image. Try PNG, JPG, BMP, WebP or TIFF.') from exc


def encode(image, extension='.png', options=None):
    ok, data = cv2.imencode(extension, image, options or [])
    if not ok:
        raise ValueError('Could not encode the processed image.')
    mime = 'image/jpeg' if extension == '.jpg' else 'image/png'
    return 'data:' + mime + ';base64,' + base64.b64encode(data).decode('ascii')


@app.get('/')
def index():
    return render_template_string(INDEX_HTML)


@app.get('/api/operations')
def operations():
    groups = [
        'Fundamentals',
        'Color & intensity',
        'Histograms',
        'Geometry',
        'Filters & restoration',
        'Edges & segmentation',
        'Morphology',
        'Transforms & comparison',
        'Compression'
    ]
    keys = sorted(
        OPERATIONS,
        key=lambda key: groups.index(OPERATIONS[key]['group']) if OPERATIONS[key]['group'] in groups else len(groups)
    )
    result = []
    fallback = {
        'Fundamentals': 1,
        'Color & intensity': 3,
        'Histograms': 2,
        'Geometry': 4,
        'Filters & restoration': 6,
        'Edges & segmentation': 5,
        'Morphology': 8,
        'Transforms & comparison': 4,
        'Compression': 7
    }
    for key in keys:
        item = describe(key)
        if request.args.get('include_code') == 'false':
            item.pop('code', None)
        chapters = set()
        for topic in COURSE['topics']:
            for op in topic['operations']:
                if op['id'] == key:
                    chapters.add(topic['chapter'])
                    break
        item['chapters'] = sorted(chapters or {fallback.get(item['group'], 1)})
        result.append(item)
    return jsonify(result)


@app.get('/api/operations/<key>')
def operation_example(key):
    if key not in OPERATIONS:
        return jsonify(error='Unknown operation.'), 404
    return jsonify(describe(key))


@app.get('/api/course')
def course():
    return jsonify(COURSE)


@app.get('/api/chapters')
def chapters():
    result = []
    for item in COURSE['chapters']:
        result.append({'id': item['id'], 'title': item['title']})
    return jsonify(result)


@app.get('/api/course/source/<int:chapter>')
def course_source(chapter):
    entry = None
    for item in COURSE['chapters']:
        if item['id'] == chapter:
            entry = item
            break
    if entry is None:
        return (jsonify(error='Unknown chapter.'), 404)
    path = PROJECT_ROOT / 'pdfs' / entry['source']
    if not path.is_file():
        return (jsonify(error='The original chapter PDF is missing from the pdfs folder.'), 404)
    return send_file(path, mimetype='application/pdf')


@app.get('/api/health')
def health():
    return jsonify(status='ok', operations=len(OPERATIONS), course_topics=len(COURSE['topics']))


@app.get('/api/lab/source/<int:lab>')
def lab_source(lab):
    if lab not in (1, 2):
        return jsonify(error='Unknown lab source.'), 404
    path = PROJECT_ROOT / 'pdfs' / f'DIP-Lab{lab}.pdf'
    if not path.is_file():
        return jsonify(error='The source PDF is missing.'), 404
    return send_file(path, mimetype='application/pdf')


@app.get('/api/demo')
def demo():
    """A repeatable test scene with color, edges, texture and uneven lighting."""
    y, x = np.mgrid[:480, :720]
    image = np.zeros((480, 720, 3), np.uint8)
    image[:, :, 0] = (40 + x * 0.16 + y * 0.1).astype(np.uint8)
    image[:, :, 1] = (60 + x * 0.12).astype(np.uint8)
    image[:, :, 2] = (95 + y * 0.18).astype(np.uint8)
    cv2.rectangle(image, (80, 95), (295, 345), (100, 190, 225), -1)
    cv2.circle(image, (490, 235), 125, (180, 205, 85), -1)
    for i in range(8):
        cv2.line(image, (90 + i * 25, 110), (90 + i * 25, 330), (45, 65, 85), 3)
    cv2.putText(image, 'DIP LAB', (230, 435), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (240, 245, 250), 3)
    return jsonify(image=encode(image), statistics=statistics(image))


@app.post('/api/process')
def process():
    try:
        operation = request.form.get('operation', '')
        if operation not in OPERATIONS:
            raise ValueError('Choose a valid processing operation.')
        params = json.loads(request.form.get('params', '{}'))
        if not isinstance(params, dict):
            raise ValueError('Parameters must be a JSON object.')
        image = read_image(request.files.get('image'))
        reference = None
        reference_upload = request.files.get('reference')
        if reference_upload:
            reference = read_image(reference_upload)
        if (OPERATIONS[operation]['requires_reference'] or operation == 'matching') and reference is None:
            raise ValueError('Upload a reference image for this operation.')
        result, details = execute(operation, image, params, reference)
        if operation == 'compression':
            output = details.pop('download')
        else:
            output = encode(result)
        artifact = details.pop('artifact', None)
        before, after = (statistics(image), statistics(result))
        lab = None
        if request.form.get('lab_output') == 'true':
            from LabOutput import make_output
            lab = make_output(image, result, before, after, operation, params, details, reference)
        return jsonify(
            original=None if request.form.get('include_original') == 'false' else encode(image),
            result=output,
            before=before,
            after=after,
            details=details,
            lab=lab,
            artifact=artifact,
            operation=describe(operation)['name']
        )
    except (ValueError, TypeError, OverflowError, json.JSONDecodeError) as exc:
        return (jsonify(error=str(exc)), 400)
    except cv2.error:
        return (
            jsonify(error='These settings cannot be applied to this image. Try a larger image or smaller kernel.'),
            400
        )


@app.errorhandler(RequestEntityTooLarge)
def too_large(error):
    return (jsonify(error='Upload is too large. The total request limit is 24 MB.'), 413)


if __name__ == '__main__':
    import argparse
    import threading
    import time
    import urllib.error
    import urllib.request
    import webbrowser

    parser = argparse.ArgumentParser(description='Start the local PixelLab backend.')
    parser.add_argument('--open-browser', action='store_true', help='Open the app after the backend is ready.')
    args = parser.parse_args()

    def open_when_ready():
        for _ in range(60):
            try:
                with urllib.request.urlopen('http://127.0.0.1:5000/api/health', timeout=1) as response:
                    if json.load(response).get('status') == 'ok':
                        webbrowser.open('http://127.0.0.1:5000')
                        return
            except (urllib.error.URLError, OSError, ValueError):
                pass
            time.sleep(0.25)
        print('Backend is not ready. Check the error above before refreshing your browser.', flush=True)

    if args.open_browser:
        threading.Thread(target=open_when_ready, daemon=True).start()
    app.run(host='127.0.0.1', port=5000, debug=False)
