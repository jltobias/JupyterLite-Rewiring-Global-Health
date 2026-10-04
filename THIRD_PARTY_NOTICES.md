# Third-party notices and acknowledgements

## Scope and asset-level credits

Original code in this repository is MIT; original text, synthetic data, diagrams, charts, and the generated silent video are CC BY 4.0. The [asset register](DATA_SOURCES.md) identifies what is generated, supplied, fetched, or externally embedded. Those licenses do not relicense a dependency, supplied composite artwork element, external video, source PDF, or underlying satellite asset.

- **Supplied splash graphic:** James L. Tobias, `assets/rewiring-global-health.png`, retained unchanged. Embedded third-party elements and quotations keep their own rights. No analytical claim is inferred from the artwork.
- **Supplied presentations:** Tobias and collaborators, 2013 and 2026; cited by title, date, and PDF page in the book. Not redistributed.
- **Six Thinking Hats:** conceptual credit to Edward de Bono. The newly drawn SVG is original. The user-supplied global-health image inspired the framing but is not copied into this repository. Purple synthesis is a project extension.
- **GeoLibre video:** Qiusheng Wu / Open Geospatial Solutions, *GeoLibre 1.0: A Free, Open-Source Cloud-Native GIS That Runs Anywhere*. [Creator index](https://geolibre.app/tutorials/videos/), [YouTube video](https://www.youtube.com/watch?v=87Cm0QagtxI). External embed/link only; creator and platform terms apply.
- **Satellite metadata:** Element 84 Earth Search and Copernicus Sentinel-2, source links/license links retained in the JSON snapshot. Source imagery is not copied.
- **Related teaching work:** PHI-Case-Studies; James L. Tobias's related JupyterLite projects; `dzole0311/zarr-sql-views` as the conceptual antecedent named by the related Zarr teaching atlas. No upstream implementation code from those case-study projects is copied into the new lessons. Their licenses remain applicable when following or adapting their repositories.

## Browser and numerical dependencies

**Redistributed pure-Python wheel:** `notebooks/wheels/asciitree-0.3.3-py3-none-any.whl`, built without source changes from the PyPI source distribution. MIT, copyright (c) 2015 Marc Brinkmann. The complete upstream license is included inside the wheel. See its adjacent README for provenance and rebuild command.

Build tools package their own third-party assets and license metadata. Consult the version-specific upstream license when redistributing or altering a dependency. Primary license references include:

| Project | License / official reference |
|---|---|
| JupyterLite, jupyterlite-ai, ipywidgets | BSD-family project licenses; [JupyterLite](https://github.com/jupyterlite/jupyterlite/blob/main/LICENSE), [JupyterLite AI](https://github.com/jupyterlite/ai/blob/main/LICENSE). |
| Jupyter Book / MyST | See the version-specific [MyST license](https://github.com/jupyter-book/mystmd/blob/main/LICENSE) and installed distributions. |
| Pyodide | Mozilla Public License 2.0; [license](https://github.com/pyodide/pyodide/blob/main/LICENSE) |
| NumPy, pandas | BSD-family licenses, with additional dependency notices in the NumPy distribution. |
| xarray | Apache-2.0; [source](https://github.com/pydata/xarray). |
| Folium, Zarr | MIT; [Folium source](https://github.com/python-visualization/folium), [Zarr source](https://github.com/zarr-developers/zarr-python). |
| Matplotlib | Matplotlib license, based on PSF; [license](https://matplotlib.org/stable/project/license.html). |
| Plotly.js / Plotly Python | MIT; [Plotly.js license](https://github.com/plotly/plotly.js/blob/master/LICENSE). |
| MapLibre GL JS | BSD-3-Clause; [license](https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt). |
| Leaflet | BSD-2-Clause; [license](https://github.com/Leaflet/Leaflet/blob/main/LICENSE). |
| SQLite | Public domain; [copyright statement](https://sqlite.org/copyright.html). |
| cryptography | Apache-2.0 or BSD-3-Clause; [license](https://github.com/pyca/cryptography/blob/main/LICENSE). |

FFmpeg is used only as a local video-encoding tool; its executable is not redistributed in this repository. The custom 2D demo is original SVG/JavaScript. Folium, Plotly, and MapLibre visual outputs may fetch JavaScript from external CDNs. The demo does not request OSM or other basemap tiles; any basemap subsequently selected in GeoLibre requires its own visible attribution.

This repository combines or references software, standards, data services, and publications maintained by others. Those works retain their original licenses and terms.

## Core software

- **JupyterLite / Project Jupyter** — https://jupyterlite.readthedocs.io/ and https://github.com/jupyterlite/jupyterlite
- **Pyodide** — https://pyodide.org/
- **Jupyter Book / MyST** — https://jupyterbook.org/
- **GeoLibre** — Qiusheng Wu / Open Geospatial Solutions; source https://github.com/opengeos/GeoLibre and documentation https://geolibre.app/
- **GeoAI** — Qiusheng Wu / Open Geospatial Solutions; source and current citation guidance https://github.com/opengeos/geoai
- **NumPy, pandas, Matplotlib, xarray, Zarr** — retain their respective project licenses.
- **STAC** — https://stacspec.org/
- **DuckDB / DuckDB-Wasm** — https://duckdb.org/

## Conceptual and scholarly influences

- Zuckerman, E. (2013). *Rewire: Digital Cosmopolitans in the Age of Connection*. W. W. Norton.
- Johnson, S. (2006). *The Ghost Map*.
- Johnson, S. (2010). *Where Good Ideas Come From*.
- Tobias, J. L. (2013). *Rewiring to meet the challenges of “Wicked Problems” within global and domestic Public Health*. Spatial Plexus.
- Pérez, F., & Granger, B. E. (2007). “IPython: A System for Interactive Scientific Computing.” DOI 10.1109/MCSE.2007.53.
- Kluyver, T. et al. (2016). “Jupyter Notebooks – a publishing format for reproducible computational workflows.”
- Haas, A. et al. (2017). “Bringing the Web up to Speed with WebAssembly.” DOI 10.1145/3062341.3062363.

## Basemaps and external viewers

When GeoLibre or another map displays OpenStreetMap-derived basemaps, preserve visible **© OpenStreetMap contributors** attribution.

## No implied endorsement

Reference to a third-party project, service, organization, agency, or product does not imply endorsement of this repository by that party.
