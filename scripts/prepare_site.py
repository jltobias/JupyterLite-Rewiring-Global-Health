"""Stage demos and lean notebook copies after the book build."""
from pathlib import Path
import shutil
import nbformat
ROOT=Path(__file__).resolve().parents[1]
output=ROOT/'_build/html'
if not (output/'index.html').exists():
    raise SystemExit('Build the Jupyter Book before staging the site.')
shutil.copytree(ROOT/'demos',output/'demos',dirs_exist_ok=True)
contents=ROOT/'_build/lite-contents';contents.mkdir(parents=True,exist_ok=True)
for path in (ROOT/'notebooks').glob('*.ipynb'):
    notebook=nbformat.read(path,as_version=4)
    for cell in notebook.cells:
        if cell.cell_type=='code':
            cell.outputs=[];cell.execution_count=None
    notebook.metadata.pop('widgets',None)
    nbformat.write(notebook,contents/path.name)
shutil.copy2(ROOT/'notebooks/rewiring.py',contents/'rewiring.py')
for folder in ['assets','data','wheels']:
    shutil.copytree(ROOT/'notebooks'/folder,contents/folder,dirs_exist_ok=True)
(output/'.nojekyll').touch()
print('Staged demos and ten clean-output JupyterLite notebooks.')
