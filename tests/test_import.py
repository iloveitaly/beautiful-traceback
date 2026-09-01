"""Test beautiful-traceback."""

from importlib.resources import files

import beautiful_traceback


def test_import() -> None:
    """Test that the  can be imported."""
    assert isinstance(beautiful_traceback.__name__, str)


def test_version() -> None:
    """Test that the version is available."""
    assert isinstance(beautiful_traceback.__version__, str)


def test_py_typed_marker() -> None:
    """PEP 561 marker so type checkers treat the installed package as typed."""
    assert files("beautiful_traceback").joinpath("py.typed").is_file()
