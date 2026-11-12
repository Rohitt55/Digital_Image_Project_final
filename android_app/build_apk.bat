@echo off
setlocal
cd /d "%~dp0\.."
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" "android_app\build_apk.py"
) else (
    py -3 "android_app\build_apk.py"
)
if errorlevel 1 (
    echo APK build failed. Read the error above.
    pause
    exit /b 1
)
echo APK saved in output\android\PixelLab-offline.apk
pause
