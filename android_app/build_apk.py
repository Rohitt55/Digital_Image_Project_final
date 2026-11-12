"""Stage the lab sources and build the self-contained, offline Android APK."""
from pathlib import Path
import argparse
import hashlib
import os
import shutil
import subprocess

PROJECT = Path(__file__).resolve().parent
ROOT = PROJECT.parent

def build(device_test=False):
    target = PROJECT / 'app/src/main/python/pixellab_engine'
    target.mkdir(parents=True, exist_ok=True)
    (target / '__init__.py').write_text('')
    shutil.copy2(PROJECT / 'engine/offline.py', target / 'offline.py')
    code = target / 'python_code'
    if code.exists():
        assert code.resolve().is_relative_to((PROJECT / 'app/src/main/python').resolve())
        for staged in code.rglob('*.py'):
            if not (ROOT / 'python_code' / staged.relative_to(code)).is_file():
                staged.unlink()
    shutil.copytree(ROOT / 'python_code', code,
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__', 'test*', 'web_app.py', 'mobile_server.py'))
    (target / 'images').mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'images/sample.png', target / 'images/sample.png')
    (target / 'data').mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'data/course_topics.json', target / 'data/course_topics.json')
    env = os.environ.copy()
    env.pop('DEBUG', None)
    user = Path.home()
    sdk = Path(env.get('ANDROID_HOME', user / 'AppData/Local/Android/Sdk'))
    (PROJECT / 'local.properties').write_text('sdk.dir=' + sdk.as_posix() + '\n')
    if 'JAVA_HOME' not in env:
        jdks = list((user / '.gradle/jdks').glob('*17*'))
        if not jdks:
            raise RuntimeError('Install JDK 17 or set JAVA_HOME.')
        env['JAVA_HOME'] = str(jdks[0])
    env['GRADLE_USER_HOME'] = str(ROOT / '.android-build/gradle-home')
    gradle = ROOT / '.android-build/tools/gradle-8.13/bin/gradle.bat'
    if not gradle.exists():
        raise RuntimeError('Install Gradle 8.13 at .android-build/tools/gradle-8.13 or open the project in Android Studio.')
    args = [str(gradle), '-p', str(PROJECT), '--no-daemon', 'assembleDebug', '--console', 'plain']
    if device_test:
        args.append('-PdeviceTest')
    subprocess.run(args, env=env, check=True)
    output = ROOT / 'output/android'
    output.mkdir(parents=True, exist_ok=True)
    apk = output / ('PixelLab-device-test.apk' if device_test else 'PixelLab-offline.apk')
    shutil.copy2(PROJECT / 'app/build/outputs/apk/debug/app-debug.apk', apk)
    if not device_test:
        shutil.copy2(apk, output / 'PixelLab-debug.apk')
        (output / 'PixelLab-debug.apk.idsig').unlink(missing_ok=True)
    digest = hashlib.sha256(apk.read_bytes()).hexdigest()
    apk.with_suffix('.apk.sha256').write_text(digest + '  ' + apk.name + '\n')
    if not device_test:
        (output / 'PixelLab-debug.apk.sha256').write_text(digest + '  PixelLab-debug.apk\n')
    print(f'Built {apk} ({apk.stat().st_size / 1024**2:.1f} MB)')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--device-test', action='store_true')
    build(parser.parse_args().device_test)
