# Data sources, provenance, and attribution

## Bundled asset register

Updated 2026-10-04. **No patient, household, Kopanyo study, or operational surveillance data are included.** References to a real region provide geographic context only.

The small `notebooks/wheels/asciitree-0.3.3-py3-none-any.whl` is a software dependency, not a dataset. It is built from the upstream PyPI source distribution without source changes; its MIT license and provenance are documented beside the wheel and in the third-party notices.

| Asset | Origin, transformation, and status | Units / coverage | License and attribution |
|---|---|---|---|
| `notebooks/rewiring.py:city()` | Original deterministic generator, NumPy seed 2026. Fictional population, terrain, access, heat, rainfall, and events. | 8×8 grid; 24 monthly steps; longitude 25.85–26.05, latitude −24.75–−24.55; coordinates WGS84. No measured conditions. | Code MIT; generated data CC BY 4.0, Tobias (2026), this repository. |
| `demos/data/cube.json` | Generated from `city()` by `scripts/build_assets.py`; numeric values rounded to four decimal places. | Temperature °C, rainfall mm/month, events/month, events per 1,000 synthetic people/month. Population held fixed. | Original synthetic data, CC BY 4.0. |
| `demos/data/heat-grid.geojson` | Original fictional grid polygons and month-1 heat, generated from the same cube. | WGS84 longitude/latitude; closed polygon rings; `data_status=synthetic`. | CC BY 4.0. No OSM or administrative boundary data used. |
| `notebooks/data/stac-snapshot.json` | Real item metadata fetched from [Element 84 Earth Search](https://earth-search.aws.element84.com/v1), Sentinel-2 L2A, on 2026-10-04. Three items in January 2025; source query retained in JSON. | Item IDs, timestamps, cloud metadata, asset links, projection/band metadata. Not climate or health observations. | Attribute Element 84 Earth Search and Copernicus Sentinel-2. Provider/item license links are preserved. No imagery bytes are redistributed or relicensed. |
| Notebook figures and animation | Original plots calculated from the synthetic data; no third-party basemap tiles. | Each caption specifies quantity, time, scale, and limitations. | CC BY 4.0. |
| `notebooks/assets/*.svg` | Original explanatory vector diagrams; scripts generate the new diagrams. The existing convergence diagram is retained. | Decision loop, discovery, layer contracts, cube/query relationship, world model, hats, and privacy. | CC BY 4.0. Hats concepts credited to Edward de Bono; purple synthesis is a project extension. |
| `demos/assets/climate-story.mp4` and poster | Original silent 12-second visualization, Matplotlib + FFmpeg; generated with `build_assets.py --video`. | 24 monthly synthetic event-rate maps; fixed map scale; population-weighted citywide time series. | CC BY 4.0. On-frame labels and a text description accompany the video. |
| `assets/rewiring-global-health.png` | Splash graphic supplied by James L. Tobias and retained unchanged at his request. | Composite project artwork; not a source of analytical data or a verified verbatim literary quotation. | Supplied project artwork; third-party elements, names, and quotations retain their respective rights. |
| Export files produced in lessons | Locally generated decision records, GeoJSON, model card, or encrypted synthetic payload. The encryption key is not saved. | Synthetic exercise only. Exports are not committed or used as source data. | Original generated content CC BY 4.0. |

The synthetic heat/event association is a programmed illustration. The access proxy assumes straight-line walking at 4 km/h with five minutes of overhead; it is not network routing. Latitudinal distance uses 111.32 km/degree and longitude applies the local cosine correction. Rates use explicit population denominators. The simulation is uncalibrated and has no disease-specific parameter provenance because its numbers are invented for teaching.

## External media and services actually linked

- [GeoLibre Web](https://web.geolibre.app/) and its [tutorials](https://geolibre.app/tutorials/), Qiusheng Wu / Open Geospatial Solutions. External service; no project is uploaded automatically.
- [GeoLibre 1.0 video](https://www.youtube.com/watch?v=87Cm0QagtxI), linked from the creator's [video index](https://geolibre.app/tutorials/videos/). Embedded through YouTube's privacy-enhanced domain; not downloaded, edited, or redistributed. Creator/platform terms apply. Written tutorial is the text alternative.
- [Copernicus Interactive Climate Atlas](https://atlas.climate.copernicus.eu/) and [CDS](https://cds.climate.copernicus.eu/). Learners select products and record provenance themselves; **no C3S dataset is bundled**.
- JavaScript libraries: Leaflet/Folium, Plotly, and MapLibre. Some views load code from CDNs; the custom 2D SVG explorer and its data table have no external library dependency.

## Optional data ecosystems, not bundled observations

The live notebooks are designed to run with **synthetic or public examples** unless otherwise stated. When a notebook is adapted to a new dataset, add the exact product, version, retrieval date, spatial/temporal resolution, units, transformations, license, and required attribution.

## Core public data ecosystems

| Source | Role | Attribution / caution |
|---|---|---|
| Copernicus Climate Data Store / C3S | climate observations, reanalysis, indicators, projections | Cite the exact dataset/product and follow its license/terms: https://cds.climate.copernicus.eu/ |
| Copernicus Interactive Climate Atlas | visual climate exploration | https://atlas.climate.copernicus.eu/ |
| Copernicus Data Space Ecosystem | Sentinel and related EO discovery/access | https://dataspace.copernicus.eu/ |
| STAC | metadata/catalog standard | Cite STAC plus the underlying data product: https://stacspec.org/ |
| OpenStreetMap | roads, places, buildings, context | © OpenStreetMap contributors; https://www.openstreetmap.org/copyright |
| WorldPop | gridded population | Cite the exact WorldPop product and its DOI/license: https://www.worldpop.org/ |
| WHO | health indicators, facilities, guidance | Cite the exact WHO dataset/publication: https://www.who.int/data |
| World Bank | development indicators and geospatial resources | Cite the exact dataset: https://data.worldbank.org/ |
| USGS | earthquakes, elevation, land products | Cite the exact USGS product: https://www.usgs.gov/ |
| NASA Earthdata / GIBS | Earth observation and imagery services | Cite the underlying NASA science product/instrument: https://www.earthdata.nasa.gov/ |
| Overture Maps Foundation | open map data | Follow dataset-specific attribution/license: https://overturemaps.org/ |

## Cloud-native formats and services

- Cloud Optimized GeoTIFF (COG): https://www.cogeo.org/
- Zarr: https://zarr.dev/
- GeoParquet: https://geoparquet.org/
- PMTiles: https://protomaps.com/docs/pmtiles
- H3: https://h3geo.org/
- DuckDB-Wasm: https://duckdb.org/docs/stable/clients/wasm/overview

## Sensitive health data

Patient-level, household-level, rare-event, movement, and exact-location data require additional governance. A public GitHub repository is not an appropriate default location for protected or operational sensitive health data. Prefer synthetic/de-identified examples for teaching, and use approved secure environments for operational data.

## Provenance checklist

For every externally sourced layer record: producer; product/dataset name; version; temporal range; retrieval date; CRS; spatial resolution; units; processing level; license; URL/DOI; transformation steps; and privacy classification.
