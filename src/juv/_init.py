from __future__ import annotations\\\\\n\\\nfrom pathlib import Path\\\nimport tempfile\\\nimport subprocess\\\nimport sys\\\n\\\nimport rich\\\n\\\nfrom ._nbconvert import new_notebook, code_cell, write_ipynb\\\n\\\ndef new_notebook_with_inline_metadata(dir: Path, python: str | None = None) -> dict:\\\n    """Create a new notebook with inline metadata.\\n\\n    Parameters\\\n    ----------\\\n    dir : pathlib.Path\\\n        A directory for uv to run `uv init` in. This is used so that we can\\\n        defer the selection of Python (if not specified) to uv.\\n    python : str, optional\\\n        A version of the Python interpreter. Provided as `--python` to uv if specified.\\n\\n    Returns\\\n    -------\\\\\\n    dict\\\n        A new notebook with a single code cell containing the contents of the\\\n        script generated by `uv init`.\\"""\\\n    with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=True, dir=dir) as f:\\\n        cmd = ['uv', 'init', '--quiet']\\\n        if python:\\\n            cmd.extend(['--python', python])\\\\\n        cmd.extend(['--script', f.name])\\\\\n\\\n        subprocess.run(cmd, check=True)\\\\\n        f.seek(0)\\\\\n        contents = f.read().strip()\\\n        notebook = new_notebook(cells=[code_cell(contents, hidden=True)])\\\\\n\\\n    return notebook\\\\n\\\ndef get_first_non_conflicting_untitled_ipynb(dir: Path) -> Path:\\\n    if not (dir / 'Untitled.ipynb').exists():\\\n        return dir / 'Untitled.ipynb'\\\n\\\n    for i in range(1, 100):\\\n        if not (dir / f'Untitled{i}.ipynb').exists():\\\n            return dir / f'Untitled{i}.ipynb'\\\n\\\n    raise ValueError('Could not find an available UntitledX.ipynb')\\\\\n\\\ndef init(path: Path | None, python: str | None, packages: typing.Sequence[str] = ()) -> None:\\\n    """Initialize a new notebook.\\n    """\\\n    if not path:\\\n        path = get_first_non_conflicting_untitled_ipynb(Path.cwd())\\\\\n\\\n    if not path.suffix == '.ipynb':\\\n        rich.print('File must have a `[cyan].ipynb[/cyan]` extension.', file=sys.stderr)\\\\\n        sys.exit(1)\\\\\n\\\n    notebook = new_notebook_with_inline_metadata(path.parent, python)\\\\\n    write_ipynb(notebook, path)\\\\\n\\\n    rich.print(f'Initialized notebook at `[cyan]{path.resolve().absolute()}[/cyan]`')