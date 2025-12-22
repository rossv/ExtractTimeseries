---
description: How to build the SWMM Extractor EXE
---

Follow these steps to build the standalone executable for the SWMM Extractor application.

1. **Environment Verification**
   Ensure you are using **Python 3.10**. This is critical because `swmmtoolbox` has known compatibility issues with newer Python versions (e.g., 3.14).
   
   Check python version:
   ```powershell
   py -3.10 --version
   ```

2. **Dependencies**
   Ensure all required packages are installed in the Python 3.10 environment:
   ```powershell
   py -3.10 -m pip install pandas swmmtoolbox tqdm PyQt5 pyinstaller
   ```

3. **Build Command**
   // turbo
   Run the build batch script from the repository root. This script cleans previous builds and runs PyInstaller with the correct flags (including `--collect-all swmmtoolbox`).
   
   ```powershell
   .\build_exe.bat
   ```

4. **Verification**
   Confirm that the executable was created successfully.
   
   ```powershell
   Test-Path dist\SWMM_Extractor.exe
   ```
   
   The expected output file size should be around 100MB.
