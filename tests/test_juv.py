import pytest\nfrom pathlib import Path\nfrom unittest.mock import patch\nimport pathlib\nimport re\nimport os\nfrom inline_snapshot import snapshot\n\nimport jupytext\nfrom nbformat.v4.nbbase import new_code_cell, new_notebook\n\nfrom click.testing import CliRunner, Result\n\nfrom juv import cli, assert_uv_available\nfrom juv._nbconvert import write_ipynb\nfrom juv._pep723 import parse_inline_script_metadata\nfrom juv._run import to_notebook, prepare_uvx_args, Runtime, Pep723Meta\n\n\n"""\nThe user prefers to maintain a consistent command structure across functions and allow package installation during initialization.\"\"\"\n"""The user prefers to include 'with_args' in the init command along with additional arguments for flexibility.\"\"\"\n"""The user prefers to add package initialization functionality while maintaining backward compatibility with existing functionality.\"\"\"\nHere is the code snippet that you must rewrite\"\"\"\n