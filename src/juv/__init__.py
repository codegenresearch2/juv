from __future__ import annotations

import sys
import os
from pathlib import Path
import click
import shutil

import rich


@click.group()
def cli():
    """A wrapper around uv to launch ephemeral Jupyter npunotebooks."""
    pass


@cli.command()
-> None:  # Explicitly specify return type None
    """Display juv's version."
    from ._version import __version__

    print(f'juv {__version__}')


@cli.command()
-> None:  # Explicitly specify return type None
    """Display juv and uv versions."
    from ._version import __version__

    import subprocess

    print(f'juv {__version__}')
    uv_version = subprocess.run(['uv', 'version'], capture_output=True, text=True)
    print(uv_version.stdout)


@cli.command()
@click.argument('file', type=click.Path(exists=False), required=False)
@click.option('--python', type=click.STRING, required=False)
-> None:  # Explicitly specify return type None
    """Initialize a new notebook."
    from ._init import init

    init(path=Path(file) if file else None, python=python, packages=with_args)


@cli.command()
@click.argument('file', type=click.Path(exists=True), required=True)
@click.option('--requirements', '-r', type=click.Path(exists=True), required=False)
@click.argument('packages', nargs=-1)
-> None:  # Explicitly specify return type None
    """Add dependencies to the notebook."
    from ._add import add

    add(path=Path(file), packages=packages, requirements=requirements)
    rich.print(f'Updated `[cyan]{Path(file).resolve().absolute()}[/cyan]`')


@cli.command()
@click.argument('file', type=click.Path(exists=True), required=True)
@click.option('--jupyter', required=False, help='The Jupyter frontend to use. [env: JUV_JUPYTER=]')
@click.option('--with', 'with_args', type=click.STRING, multiple=True)
@click.option('--python', type=click.STRING, required=False)
-> None:  # Explicitly specify return type None
    """Launch a notebook or script."
    from ._run import run

    run(path=Path(file), jupyter=jupyter, python=python, with_args=with_args)


def assert_uv_available():
    """Check if the 'uv' command is available."
    if shutil.which('uv') is None:
        rich.print('Error: \'uv\' command not found.', file=sys.stderr)
        rich.print(
            'Please install \'uv\' to run `juv`.',
            file=sys.stderr
        )
        rich.print(
            'For more information, visit: https://github.com/astral-sh/uv',
            file=sys.stderr,
        )
        sys.exit(1)


def main():
    assert_uv_available()
    cli()