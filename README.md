# ExtractTimeseries
Extract timeseries data from SWMM out files.

## Deployable GitHub Pages app
A browser-only front-end (Pyodide) lives in `index.html` and `assets/`. It runs entirely client-side, so you can host it on GitHub Pages without a backend.

### Run locally
```bash
python -m http.server 8000
# then open http://localhost:8000
```

### Deploy to GitHub Pages
1. Commit the static assets (`index.html`, `assets/`, `web_support.py`, `core.py`).
2. Push to a branch configured for Pages (e.g., `gh-pages`).
3. In repository settings, set Pages source to that branch (root directory).
4. Visit the published URL to use the extractor directly in the browser.
