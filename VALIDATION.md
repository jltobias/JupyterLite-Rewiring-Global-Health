# Validation record

Reviewed 2026-10-04. These checks establish software behavior for the teaching examples; they do not validate real health outcomes or certify privacy or security for an operational deployment.

| Check | Result |
|---|---|
| Ten notebooks, 121 cells / 58 code cells | All code cells executed without errors in native Python 3.13. |
| Browser numerical runtime | All ten lessons executed in Chromium using Pyodide 314.0.6. Nine passed on the first browser run; the Zarr lesson passed after bundling the missing pure-Python asciitree wheel. |
| Actual JupyterLite interface | Lab 05 completed all six code cells using Run All Cells; kernel returned to Idle with no traceback. Confirms notebook filesystem, local wheel, Zarr, SQL, and output integration. |
| Model/data invariants | Deterministic generation, unique cell/time rows, rate denominators, GeoJSON coordinates/ring closure, population conservation, synchronous transitions, and synthetic-input contract passed. |
| Cryptography | AES-GCM round trip passed; modified ciphertext and a wrong key were rejected. No key is printed or exported. |
| Demo interaction | Cell selection, linked month/series, six-map matrix, orbitable cube, play/pause, GeoJSON download, mobile overflow check, and WebGL scene passed. |
| Visual review | Notebook figure contact sheets, SVG diagrams, desktop/mobile demos, 3D scene, and book home reviewed. Map ticks and diagram spacing adjusted after inspection. |
| Publishing build | Jupyter Book strict build and JupyterLite build passed locally. GitHub Actions repeats native execution and the build before deployment. |

## Reproduce

```bash
python -m pip install -r requirements-labs.txt
python scripts/check_models.py
python scripts/execute_notebooks.py
jupyter book build --html --strict
python scripts/prepare_site.py
jupyter lite build --contents _build/lite-contents --output-dir _build/html/lite
```

For browser checks, install Playwright and its Chromium runtime, serve the repository root on `127.0.0.1:8765`, then run `python scripts/check_browser.py --runtime`. Use `--notebook 05` to target the Zarr lesson after changing that dependency chain. The harness is not shipped in the published learning site. QA screenshots and runtime logs are written under ignored `_build/qa/`.

Initial package downloads, external CDN availability, WebGL, browser storage policies, and provider configuration can affect the experience. The static figures and data tables provide alternatives to external JavaScript views. JupyterLite AI is installed, but no authenticated live model endpoint was configured or tested; the template chat and request-contract lesson run without one.
