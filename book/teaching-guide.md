# Teaching, access, and reproducibility

## A 90-minute workshop

| Time | Activity | Evidence to leave with |
|---|---|---|
| 0–15 min | Lab 00: connect the decision, people, and data | A question and explicit value choices |
| 15–35 min | Demo gallery and Labs 02/04 | A map comparison with units, denominator, and fixed scale |
| 35–55 min | Choose Lab 05, 06, or 08 | A query, a held-out evaluation, or a paired scenario comparison |
| 55–75 min | Labs 07/09 | A dissent-aware decision record and privacy release boundary |
| 75–90 min | Explain findings to another group | Assumptions, unresolved questions, and a stopping rule |

For a longer course, run each 30–45-minute lesson with a discussion and one exercise. The source-to-lesson guide supports a seminar on the evolution from public-health informatics to geospatial intelligence.

## Run and save

1. Open JupyterLite, choose a notebook, and wait for its Python kernel to become ready.
2. Run cells in order. Package installation is in the first code cell and may take time on first use.
3. Keep `rewiring.py`, `data/`, and `assets/` beside the notebooks. They are included in the site.
4. Download edited notebooks and desired files from `exports/` before closing or clearing browser data.

JupyterLite stores edits in browser-local storage. A site update does not necessarily replace an already edited local copy. Download your work first, then rename/remove the old local copy or use a fresh browser profile to obtain updated content. Private browsing and storage clearing can discard work.

The book retains executed outputs for reading without a kernel. The JupyterLite deployment starts from clean-output notebook copies, keeping initial downloads smaller. Outputs generated during your session remain local unless you export or explicitly send them to a service.

## Accessibility and cognition

The demo offers keyboard-selectable map cells, a cell dropdown, labeled controls, a data table, explicit play/pause, and no autoplay. Animation is accompanied by small multiples and aligned time series. 3D views have 2D alternatives. Color maps are sequential for magnitude and diverging for signed differences; comparisons share limits.

The original silent video has on-frame labels and a written description. The external GeoLibre video has a linked written tutorial. Do not rely on motion, color, or perspective as the only way to communicate a result.

## Troubleshooting

| Symptom | What to do |
|---|---|
| First cell is still busy | Allow package/runtime downloads to finish; check connectivity and browser console/network restrictions. |
| A package fails to install | Restart the kernel and run the first cell again. Use the documented pins for xarray/Zarr. Check whether a managed network blocks PyPI or jsDelivr. |
| An import cannot find `rewiring` | Restore the shared module beside the notebook; run from the notebook directory. |
| A 3D or Leaflet output is blank | Use the static 2D figure or demo table; WebGL or an external JavaScript CDN may be blocked. |
| GeoLibre/video will not embed | Open the supplied direct link. External embedding policies may change. |
| AI panel has no response | No model provider is preconfigured. Use the template chat in Lab 07 or configure an approved provider. |
| STAC request fails | Leave `LIVE_STAC=False` to use the bundled metadata snapshot. |
| An encrypted export cannot be decrypted later | The lesson key was deliberately ephemeral and unexported. Do not use this exercise as a storage service. |

## Reproducibility and validation

The generator uses a fixed seed. Model checks verify reproducibility, population conservation, synchronous transitions, rate denominators, GeoJSON geometry, and the explicit synthetic-input contract. Every notebook is executed before the site is built, and execution errors fail CI. Lab 09 tests tamper and wrong-key rejection. Browser runtime and JavaScript demos also need smoke testing when dependencies change.

These checks establish specific software properties. They do not establish epidemiologic validity, clinical safety, anonymity, causal identification, or policy effectiveness. See each lesson's model/data contract before reusing its methods.
