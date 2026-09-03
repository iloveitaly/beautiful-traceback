"""Test beautiful-traceback."""

import subprocess
import sys
from importlib.resources import files
from pathlib import Path

import beautiful_traceback

CONSUMER_REEXPORTS = Path(__file__).parent / "typing" / "consumer_reexports.py"


def test_import() -> None:
    """Test that the  can be imported."""
    assert isinstance(beautiful_traceback.__name__, str)


def test_version() -> None:
    """Test that the version is available."""
    assert isinstance(beautiful_traceback.__version__, str)


def test_py_typed_marker() -> None:
    """PEP 561 marker so type checkers treat the installed package as typed."""
    assert files("beautiful_traceback").joinpath("py.typed").is_file()


def test_package_root_reexports_pass_mypy_strict() -> None:
    """Strict mypy rejects implicit re-exports; __all__ must declare the public API."""
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", str(CONSUMER_REEXPORTS)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
