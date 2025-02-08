from __future__ import annotations\\\n\\nimport sys\nimport os\nfrom pathlib import Path\nimport click\nimport shutil\n\nimport rich\n\n\ndef assert_uv_available():\n    if shutil.which("uv") is None:\n        rich.print("Error: 'uv' command not found.", file=sys.stderr)\n        rich.print("Please install 'uv' to run `juv`.", file=sys.stderr)\n        rich.print(\"For more information, visit: https://github.com/astral-sh/uv\", file=sys.stderr)\n        sys.exit(1)\n\n@click.group()\ndef cli():\n    """A wrapper around uv to launch ephemeral Jupyter notebooks."""\n    pass\n\n\n@cli.command()\ndef version() -> None:\n    """Display juv's version."""\n    from ._version import __version__\n    print(f"juv {__version__}")\n\n@cli.command()\ndef info():\n    """Display juv and uv versions."""\n    from ._version import __version__\n    import subprocess\n    print(f"juv {__version__}")\n    uv_version = subprocess.run(["uv", "version"], capture_output=True, text=True)\n    print(uv_version.stdout)\n\n@cli.command()\n@click.argument("file", type=click.Path(exists=False), required=False)\n@click.option("--python", type=click.STRING, required=False)\ndef init(file: str | None, python: str | None, with_args: tuple[str, ...] = ()) -> None:\n    """Initialize a new notebook."""\n    from ._init import init\n    init(path=Path(file) if file else None, python=python, with_args=with_args)\n\n@cli.command()\n@click.argument("file", type=click.Path(exists=True), required=True)\n@click.option("--requirements", "-r", type=click.Path(exists=True), required=False)\n@click.argument("packages", nargs=-1)\ndef add(file: str, requirements: str | None, packages: tuple[str, ...]) -> None:\n    """Add dependencies to the notebook."""\n    from ._add import add\n    add(path=Path(file), packages=packages, requirements=requirements)\n    rich.print(f"Updated `[cyan]${Path(file).resolve().absolute()}[/cyan]`")\n\n@cli.command()\n@click.argument("file", type=click.Path(exists=True), required=True)\n@click.option("--jupyter", required=False, help="The Jupyter frontend to use. [env: JUV_JUPYTER=]")\n@click.option("--with", "with_args", type=click.STRING, multiple=True)\n@click.option("--python", type=click.STRING, required=False)\ndef run(file: str, jupyter: str | None, with_args: tuple[str, ...], python: str | None) -> None:\n    """Launch a notebook or script."""\n    from ._run import run\n    run(path=Path(file), jupyter=jupyter, python=python, with_args=with_args)\n\n\ndef upgrade_legacy_jupyter_command(args: list[str]) -> None:\n    """Check legacy lab/notebook/nbclassic command usage and upgrade to 'run' with deprecation notice."""\n    for i, arg in enumerate(args):\n        if i == 0:\n            continue\n        if (arg.startswith(('lab', 'notebook', 'nbclassic')) and not args[i - 1].startswith('--') and not arg.startswith('--')):\n            rich.print(\"[bold]Warning:[/bold] The command '{arg}' is deprecated. Please use 'run' with `--jupyter={arg}` or set JUV_JUPYTER={arg}\")\n            os.environ['JUV_JUPYTER'] = arg\n            args[i] = 'run'\n\n\ndef main():\n    upgrade_legacy_jupyter_command(sys.argv)\n    cli()\n