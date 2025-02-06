import pytest
from pathlib import Path
from unittest.mock import patch
import pathlib
import re
import os
from inline_snapshot import snapshot

import jupytext
from nbformat.v4.nbbase import new_code_cell, new_notebook

from click.testing import CliRunner, Result

from juv import cli, assert_uv_available
from juv._nbconvert import write_ipynb
from juv._pep723 import parse_inline_script_metadata
from juv._run import to_notebook, prepare_uvx_args, Runtime, Pep723Meta


def invoke(args: list[str], uv_python: str = "3.13") -> Result:
    return CliRunner().invoke(
        cli,
        args,
        env={**os.environ, "UV_PYTHON": uv_python},
    )


@pytest.fixture
def sample_script() -> str:
    return """
# /// script
# dependencies = ["numpy", "pandas"]
# requires-python = ">=3.8"
# ///

import numpy as np
import pandas as pd

print('Hello, world!')
"""


@pytest.fixture
def sample_notebook() -> dict:
    return {
        "cells": [
            {
                "cell_type": "code",
                "source": "# /// script\n# dependencies = [\"pandas\"]\n# ///\n\nimport pandas as pd\nprint('Hello, pandas!')",
            }
        ],
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def test_parse_pep723_meta(sample_script: str) -> None:
    meta = parse_inline_script_metadata(sample_script)
    assert meta == snapshot("""\ndependencies = ["numpy", "pandas"]\nrequires-python = ">=3.8"\n""")


def test_parse_pep723_meta_no_meta() -> None:
    script_without_meta = "print('Hello, world!')"
    assert parse_inline_script_metadata(script_without_meta) is None


def filter_ids(output: str) -> str:
    return re.sub(r"\"id\": \"[a-zA-Z0-9-]+\"", "\"id\": '<ID>'", output)


def test_to_notebook_script(tmp_path: pathlib.Path):
    script = tmp_path / "script.py"
    script.write_text("""# /// script
# dependencies = ["numpy"]
# requires-python = ">=3.8"
# ///


import numpy as np

# %%\nprint('Hello, numpy!')\narr = np.array([1, 2, 3])"""")

    meta, nb = to_notebook(script)
    output = jupytext.writes(nb, fmt="ipynb")
    output = filter_ids(output)

    assert (meta, output) == snapshot((
        """\ndependencies = ["numpy"]\nrequires-python = ">=3.8"\n""",
        """{\n "cells": [\n  {\n   "cell_type": "code",\n   "execution_count": null,\n   "id": '<ID>',\n   "metadata": {\n    "jupyter": {\n     "source_hidden": true\n    }\n   },\n   "outputs": [],\n   "source": [\n    '# /// script\n',\n    '# dependencies = [\