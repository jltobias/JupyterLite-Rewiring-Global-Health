# References

## Four supplied presentations

1. Tobias, J. L. (2013, November 6). *Rewiring to meet the challenges of “Wicked Problems” within global and domestic Public Health*. Spatial Plexus. Supplied as `Tobias_Spatial_Plexus_Presentation_2013_w_appendix.pdf`, 31 pages.
2. Tobias, J. L. (2026, July 10). *JupyterLite: Geospatial Data Science and Global Health*. Supplied as `Jim-Tobias-Peraton-JupyterLite-Geospatial-Data-Science-and-Global-Health-7102026.pdf`, 47 pages.
3. Tobias, J. L., Tolentino, H., Wuhib, T., Moonan, P., & Oeltmann, J. (2026, August 27). *Digital Twins: Botswana Kopanyo TB Study (2012–2016) for Gaborone TB simulation*. Supplied as `Gaborone-Digital-Twin-TB_Agent-Based-Modeling-8272026.pdf`, 22 pages. Names follow the title-slide contributor list; this repository does not assert a separate peer-reviewed publication.
4. Tolentino, H., Tobias, J. L., Wuhib, T., & Mishra, V. (2026, September 21). *Map Encryption Democratized with JupyterLite*. Supplied as `Map_Encryption_JupyterLite_9212026.pdf`, 36 pages.

These PDFs were reviewed as source material but are not redistributed here. See the [source-to-lesson guide](book/source-presentations.md) for specific page references. Internal systems mentioned in slides are not presented as public resources.

## Decision-making, ethics, and world models

- Zuckerman, E. (2013). *Rewire: Digital Cosmopolitans in the Age of Connection*. W. W. Norton. [Author's book page](https://ethanzuckerman.com/books/rewire/) and [user-supplied Goodreads record](https://www.goodreads.com/en/book/show/16233761-rewire). The narrative uses attributed paraphrases rather than treating wording in the supplied splash graphic as a verified direct quotation.
- de Bono, E. (1985). *Six Thinking Hats*. The computational role-review exercise is an adaptation; purple synthesis is not one of the original six hats.
- World Health Organization. (2021). *Ethics and governance of artificial intelligence for health*. ISBN 978-92-4-002920-0. [Official publication](https://www.who.int/publications/i/item/9789240029200).
- Ha, D., & Schmidhuber, J. (2018). *World Models*. [Author-hosted paper and interactive explanation](https://worldmodels.github.io/), [arXiv:1803.10122](https://arxiv.org/abs/1803.10122). Used for the distinction between representation, transition, and control; no claim that the small teaching models implement its architecture.

## Implementation and data documentation

- [JupyterLite](https://jupyterlite.readthedocs.io/en/stable/), [Pyodide](https://pyodide.org/en/stable/), and [Jupyter Book](https://jupyterbook.org/stable/).
- [JupyterLite AI](https://github.com/jupyterlite/ai), including [key handling](https://jupyterlite-ai.readthedocs.io/en/latest/api-keys/) and [custom providers](https://jupyterlite-ai.readthedocs.io/en/latest/custom-providers/).
- [GeoLibre tutorials](https://geolibre.app/tutorials/), [sharing/embedding](https://geolibre.app/tutorials/sharing-embedding/), and [creator-hosted videos](https://geolibre.app/tutorials/videos/).
- [STAC Sentinel-2 tutorial](https://stacspec.org/en/tutorials/access-sentinel-2-data-aws/), [Earth Search source and documentation](https://github.com/Element84/earth-search), [C3S Atlas](https://atlas.climate.copernicus.eu/), and [Climate Data Store](https://cds.climate.copernicus.eu/).
- [Zarr 2.18.7](https://zarr.readthedocs.io/en/v2.18.7/), [xarray Zarr I/O](https://docs.xarray.dev/en/stable/user-guide/io.html#zarr), [SQLite](https://sqlite.org/), and [DuckDB-Wasm](https://duckdb.org/docs/stable/clients/wasm/overview).
- [Folium](https://python-visualization.github.io/folium/latest/), [Plotly](https://plotly.com/python/), [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/), and [Matplotlib animation](https://matplotlib.org/stable/api/animation_api.html).
- [cryptography AES-GCM](https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESGCM).

Links and selected package compatibility were reviewed on 2026-10-04. Live services can evolve; the bundled synthetic examples and catalog snapshot provide a reproducible baseline.

## Rewiring and innovation
- Zuckerman, E. (2013). *Rewire: Digital Cosmopolitans in the Age of Connection*. W. W. Norton.
- Johnson, S. (2006). *The Ghost Map: The Story of London's Most Terrifying Epidemic—and How It Changed Science, Cities, and the Modern World*.
- Johnson, S. (2010). *Where Good Ideas Come From: The Natural History of Innovation*.
- Tobias, J. L. (2013). *Rewiring to meet the challenges of “Wicked Problems” within global and domestic Public Health*. Spatial Plexus.

## Browser scientific computing
- Pérez, F., & Granger, B. E. (2007). IPython: A System for Interactive Scientific Computing. DOI: 10.1109/MCSE.2007.53.
- Kluyver, T. et al. (2016). Jupyter Notebooks – a publishing format for reproducible computational workflows.
- Haas, A. et al. (2017). Bringing the Web up to Speed with WebAssembly. DOI: 10.1145/3062341.3062363.
- JupyterLite documentation: https://jupyterlite.readthedocs.io/
- Pyodide documentation: https://pyodide.org/

## Geospatial / GeoAI
- Wu, Q. / Open Geospatial Solutions. *GeoLibre*. [Official project](https://geolibre.app/) and [source](https://github.com/opengeos/GeoLibre). Cite the version used. A DOI shown in the supplied presentation could not be resolved during this build; the maintained project links are used here.
- Wu, Q. / Open Geospatial Solutions. *GeoAI*. [Source and current citation guidance](https://github.com/opengeos/geoai). Cite the release and citation metadata supplied by the project.
- STAC specification: https://stacspec.org/
- Zarr: https://zarr.dev/

## Digital twins / global health
See the repository notebooks and the Botswana Kopanyo TB literature cited in the associated digital-twin presentation for disease- and setting-specific evidence. Do not treat synthetic notebook parameters as epidemiologic estimates.
