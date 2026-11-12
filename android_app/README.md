# PixelLab offline Android app

Install `../output/android/PixelLab-offline.apk`, then open PixelLab. No computer, server, Wi-Fi, mobile data, login or first-run download is required. The APK bundles Python, OpenCV, NumPy, SciPy, Matplotlib, Pillow, all 59 operations, the sample image and Python examples. Photo/reference selection, PDF-style figures and tables, zoom, result chaining and saving work on the device. The app requests no Internet permission.

Open the sidebar with the fixed ☰ menu or Browse operations button. It contains all eight chapters, chapter-specific operation counts, search, Clear filters and a scrollable operation list with the current selection highlighted. Choosing an operation closes the drawer and shows its settings in the workspace. Back, the close button or tapping outside dismisses the sidebar. The filter area scrolls separately so the operation list remains usable on smaller screens and while the keyboard is open. Chapter membership follows `data/course_topics.json`; operations without an explicit topic use the same group-to-chapter mapping as the desktop app. Navigation keeps the chosen image.

Requires Android 7.0/API 24 or later and a 64-bit ARM phone (arm64-v8a); the universal APK also includes x86_64 for emulators. Images are limited to 12 million pixels and 23 MB total input. Large scientific operations can take longer on a phone. Version 2.2 uses the existing development signing key and version code 4, so it can update earlier PixelLab installations.

## Build

Use JDK 17, Android SDK/platform 36, Gradle 8.13, Chaquopy 17.2.0 and Python 3.10 as the build interpreter. Install Gradle under `.android-build/tools/gradle-8.13` and Python under `.android-build/python/cpython-3.10.22-windows-x86_64-none`, or adjust the build interpreter path in app/build.gradle. Run `android_app/build_apk.bat` or `.venv/Scripts/python.exe android_app/build_apk.py`. Build dependencies are downloaded during development; they are bundled into the APK and are not downloaded by the installed app.

The build script stages the current lab sources from `python_code/` plus the local adapter from `engine/offline.py`. Java calls the bundled Python module directly through Chaquopy. No Flask process, local HTTP server or network request is used. Keep `keystore/debug.keystore` for compatible updates.

`build_apk.py --device-test` creates a separate APK with test instrumentation, which checks every operation, bundled examples, known pixels, PDF mapping, photo loading, native result rendering and file saving. Do not distribute the instrumented APK.

Verified on the isolated Android 36 x86_64 emulator with Wi-Fi and mobile data disabled: 272 integration checks passed, covering all 59 operations, every chapter filter, combined chapter/search filtering, no-match handling, clearing filters, sidebar open/close, operation selection and keeping the selected image. The delivered APK was also checked visually, including selecting a feature and dismissing the drawer using Android Back. APK signature verification passed and no Internet permission is requested. The earlier desktop Python suite passed all 47 tests. ARM64 libraries are bundled; a physical ARM phone was not available for testing.
