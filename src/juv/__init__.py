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


def upgrade_legacy_jupyter_command(args: list[str]) -> None:
    """Check legacy lab/notebook/nbclassic command usage and upgrade to 'run' with deprecation notice."
    for i, arg in enumerate(args):
        if i == 0:  # Skip the first argument which is the script name
            continue
        if arg.startswith(('lab', 'notebook', 'nbclassic')) and not args[i - 1].startswith('--') and not arg.startswith('--'):
            rich.print(
                f'\[bold]Warning:[/bold] The command \'{arg}\' is deprecated. ',  # Corrected the escape sequence for bold text
                f'Please use \'run\' with `--jupyter={arg}` or set JUV_JUPYTER={arg}',
            )
            os.environ['JUV_JUPYTER'] = arg
            args[i] = 'run'


def main():
    upgrade_legacy_jupyter_command(sys.argv)
    cli()