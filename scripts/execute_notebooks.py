"""Validate and execute every notebook, failing on errors; retain readable outputs."""
import argparse
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--only',default='*.ipynb')
    parser.add_argument('--check',action='store_true',help='Check stored outputs and schema without executing')
    args=parser.parse_args()
    for path in sorted((ROOT/'notebooks').glob(args.only)):
        notebook=nbformat.read(path,as_version=4)
        nbformat.validate(notebook)
        if not args.check:
            print('Executing',path.name,flush=True)
            NotebookClient(notebook,timeout=180,kernel_name='python3',
                           resources={'metadata':{'path':str(ROOT/'notebooks')}}).execute()
            nbformat.write(notebook,path)
        code=[c for c in notebook.cells if c.cell_type=='code']
        assert all(c.execution_count is not None for c in code),f'Unexecuted cell: {path}'
        assert not any(o.output_type=='error' for c in code for o in c.outputs),f'Error output: {path}'
        print(f'PASS {path.name}: {len(notebook.cells)} cells, {len(code)} executed',flush=True)

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
