"""Start the web app; standalone lab scripts are beside this file."""
from pathlib import Path
import runpy
import sys

backend = Path(__file__).resolve().parent / 'app_backend'
sys.path.insert(0, str(backend))

if __name__ == '__main__':
    runpy.run_path(str(backend / 'web_app.py'), run_name='__main__')
else:
    app_module = runpy.run_path(str(backend / 'web_app.py'))
    app = app_module['app']
    COURSE = app_module['COURSE']
