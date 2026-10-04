# Architecture

The project uses a **browser-first / secure-handoff** architecture. JupyterLite supplies a low-friction learning runtime; cloud-native geospatial formats reduce unnecessary downloads; sensitive or computationally heavy work is handed off to approved full runtimes.

## Browser-first lane

Use public or synthetic data, COG/GeoJSON/Zarr/STAC resources, Pyodide-compatible Python, browser maps, charts, and deterministic teaching agents.

## Secure / heavy-compute lane

Use protected compute for sensitive health data, long-lived credentials, GPU inference, large calibration runs, or regulated workflows. The browser notebook can export a request, configuration, or derived non-sensitive artifact without exposing protected source data.