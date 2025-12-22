@echo off
echo Building SWMM Extractor EXE...

REM Clean previous builds
rmdir /s /q build
rmdir /s /q dist
del *.spec

REM Run PyInstaller with Python 3.10
py -3.10 -m PyInstaller --noconsole --onefile --collect-all swmmtoolbox --name "SWMM_Extractor" main.py

echo.
if exist "dist\SWMM_Extractor.exe" (
    echo Build successful! EXE is in "dist\SWMM_Extractor.exe"
) else (
    echo Build failed!
    exit /b 1
)
