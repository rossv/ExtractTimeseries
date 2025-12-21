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
1. Commit and push to the `main` branch; this triggers the GitHub Actions Pages publish workflow, which outputs the static site to the `gh-pages` branch.
2. In repository settings (Pages), set the source to the `gh-pages` branch and the root (`/`) directory.
3. Monitor workflow runs in the **Actions** tab (look for the Pages publish workflow) to confirm deployments succeed before checking the live site.
