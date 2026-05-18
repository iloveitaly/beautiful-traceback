"""Test beautiful-traceback."""

import beautiful_traceback


def test_import() -> None:
    """Test that the  can be imported."""
    assert isinstance(beautiful_traceback.__name__, str)


def test_version() -> None:
    """Test that the version is available."""
    assert isinstance(beautiful_traceback.__version__, str)
