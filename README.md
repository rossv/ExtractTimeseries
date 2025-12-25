# ExtractTimeseries

PyQt5 desktop tool for extracting time series data from SWMM `.out` files with the help of `swmmtoolbox`.

## Repository layout
- `main.py` starts the PyQt5 application with the dark theme and window icon.
- `gui.py` defines the `ExtractorWindow` interface, menus, theme helper, and ties UI actions to the extraction logic.
- `logic.py` contains the data parsing, filtering, and export helpers used by the GUI and tests.
- `help_ui.py` provides the in-app help/about dialog content.
- `assets/extract_timeseries.ico` supplies the application icon used by both the runtime and the PyInstaller build (`SWMM_Extractor.spec`).
- `tests/` exercises the export helpers.

## Run the desktop app
```bash
pip install -r requirements.txt
python main.py
```

## Deployable GitHub Pages app
This repository does not ship a browser-only build; the shipped interface is the PyQt5 desktop app. If you want a static download page on GitHub Pages, publish artifacts from the existing desktop bundle instead of pointing at non-existent `index.html` files.

### Build distributable artifacts
```bash
pip install -r requirements.txt
pyinstaller SWMM_Extractor.spec
# artifacts land in dist/SWMM_Extractor/
```

### Publish on GitHub Pages
1. Copy the contents of `dist/SWMM_Extractor/` (and a simple `index.html` describing the download) into a `docs/` folder or a dedicated `gh-pages` branch.
2. Commit and push the static files.
3. In repository settings (**Pages**), set the source to the `/docs` folder on `main` (or to the `gh-pages` branch) and save.
4. Visit the Pages URL to confirm the downloadable artifacts are available.
