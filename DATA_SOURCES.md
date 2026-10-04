# Data sources, provenance, and attribution

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