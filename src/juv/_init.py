from __future__ import annotations

from pathlib import Path
import tempfile
import subprocess
import typing
import sys

import rich

from ._nbconvert import new_notebook, code_cell, write_ipynb


def new_notebook_with_inline_metadata(dir: Path, python: str | None = None) -> dict:
    """Create a new notebook with inline metadata.

    Parameters
    ----------
    dir : pathlib.Path
        A directory for uv to run `uv init` in. This is used so that we can
        defer the selection of Python (if not specified) to uv.
    python : str, optional
        A version of the Python interpreter. Provided as `--python` to uv if specified.

    Returns
    -------
    dict
        A new notebook with a single code cell containing the contents of the
        script generated by `uv init`.
    """
    with tempfile.NamedTemporaryFile(
        mode="w+",
        suffix=".py",
        delete=True,
        dir=dir,
    ) as f:
        cmd = ["uv", "init", "--quiet"]
        if python:
            cmd.extend(["--python", python])
        cmd.extend(["--script", f.name])

        subprocess.run(cmd)
        f.seek(0)
        contents = f.read().strip()
        notebook = new_notebook(cells=[code_cell(contents, hidden=True)])

    return notebook


def get_first_non_conflicting_untitled_ipynb(dir: Path) -> Path:
    if not (dir / "Untitled.ipynb").exists():
        return dir / "Untitled.ipynb"

    for i in range(1, 100):
        if not (dir / f"Untitled{i}.ipynb").exists():
            return dir / f"Untitled{i}.ipynb"

    raise ValueError("Could not find an available UntitledX.ipynb")


def init(
    path: Path | None,
    python: str | None,
    packages: typing.Sequence[str] = [],
) -> None:
    """Initialize a new notebook."""
    if not path:
        path = get_first_non_conflicting_untitled_ipynb(Path.cwd())

    if not path.suffix == ".ipynb":
        rich.print("File must have a `[cyan].ipynb[/cyan]` extension.", file=sys.stderr)
        sys.exit(1)

    notebook = new_notebook_with_inline_metadata(path.parent, python)
    write_ipynb(notebook, path)

    if len(packages) > 0:
        from ._add import add

        add(path=path, packages=packages, requirements=None)

    rich.print(f"Initialized notebook at `[cyan]{path.resolve().absolute()}[/cyan]`")
