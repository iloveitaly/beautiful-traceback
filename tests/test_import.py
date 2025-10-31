"""Test beautiful-traceback."""

import beautiful_traceback


def test_import() -> None:
    """Test that the  can be imported."""
    assert isinstance(beautiful_traceback.__name__, str)