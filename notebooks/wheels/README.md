# Browser wheel: asciitree 0.3.3

`asciitree-0.3.3-py3-none-any.whl` is built without source changes from the
[PyPI asciitree 0.3.3 distribution](https://pypi.org/project/asciitree/0.3.3/).
Zarr 2 needs this pure-Python dependency, but its upstream PyPI release provides
only a source archive. Micropip cannot build source archives in the browser.

Rebuild with `python -m pip wheel --no-deps --wheel-dir notebooks/wheels asciitree==0.3.3`.
The wheel contains the full MIT license, copyright (c) 2015 Marc Brinkmann,
at `asciitree-0.3.3.dist-info/licenses/LICENSE`.

The notebook installs the wheel from the browser filesystem with an `emfs:` URI,
then installs xarray/Zarr and their remaining dependencies normally.
