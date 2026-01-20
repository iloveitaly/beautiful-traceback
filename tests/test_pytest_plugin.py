"""
Tests for the beautiful_traceback pytest plugin.

These tests verify that the plugin correctly formats tracebacks
in pytest output when tests fail.
"""

import pytest
from beautiful_traceback import pytest_plugin, formatting


def test_plugin_hooks_exist():
    """Verify the plugin hooks are defined."""
    assert hasattr(pytest_plugin, "pytest_addoption")
    assert hasattr(pytest_plugin, "pytest_runtest_makereport")
    assert hasattr(pytest_plugin, "pytest_exception_interact")
    assert callable(pytest_plugin.pytest_addoption)
    assert callable(pytest_plugin.pytest_runtest_makereport)
    assert callable(pytest_plugin.pytest_exception_interact)


def test_get_option_helper():
    """Test the _get_option helper function."""
    from unittest.mock import Mock

    config = Mock()
    config.getoption.side_effect = Exception("Not found")
    config.getini.return_value = True

    result = pytest_plugin._get_option(config, "test_key")
    assert result is True
    config.getini.assert_called_once_with("test_key")


def test_get_option_from_getoption():
    """Test _get_option when getoption works."""
    from unittest.mock import Mock

    config = Mock()
    config.getoption.return_value = False

    result = pytest_plugin._get_option(config, "test_key")
    assert result is False
    config.getoption.assert_called_once_with("test_key")


def test_pytest_addoption():
    """Test that pytest_addoption registers the correct options."""
    from unittest.mock import Mock

    parser = Mock()
    pytest_plugin.pytest_addoption(parser)

    # Should be called twice (two options)
    assert parser.addini.call_count == 2

    # Check first call - enable_beautiful_traceback
    first_call = parser.addini.call_args_list[0]
    assert first_call[0][0] == "enable_beautiful_traceback"
    assert "beautiful traceback" in first_call[0][1].lower()
    assert first_call[1]["type"] == "bool"
    assert first_call[1]["default"] is True

    # Check second call - enable_beautiful_traceback_local_stack_only
    second_call = parser.addini.call_args_list[1]
    assert second_call[0][0] == "enable_beautiful_traceback_local_stack_only"
    assert "local" in second_call[0][1].lower()
    assert second_call[1]["type"] == "bool"
    assert second_call[1]["default"] is True


def test_exc_to_traceback_str_integration():
    """Test that exc_to_traceback_str works with real exceptions."""
    try:
        raise ValueError("Test error message")
    except ValueError as e:
        assert e.__traceback__ is not None
        tb_str = formatting.exc_to_traceback_str(
            e, e.__traceback__, color=False, local_stack_only=False
        )

        assert isinstance(tb_str, str)
        assert "ValueError" in tb_str
        assert "Test error message" in tb_str
        assert "test_exc_to_traceback_str_integration" in tb_str


def test_formatting_with_local_stack_only():
    """Test formatting with local_stack_only=True."""
    try:
        raise RuntimeError("Local stack test")
    except RuntimeError as e:
        assert e.__traceback__ is not None
        tb_str_all = formatting.exc_to_traceback_str(
            e, e.__traceback__, color=False, local_stack_only=False
        )
        tb_str_local = formatting.exc_to_traceback_str(
            e, e.__traceback__, color=False, local_stack_only=True
        )

        # Both should contain the error
        assert "RuntimeError" in tb_str_all
        assert "RuntimeError" in tb_str_local
        assert "Local stack test" in tb_str_all
        assert "Local stack test" in tb_str_local


def test_formatting_with_color():
    """Test that color formatting works."""
    try:
        raise TypeError("Color test")
    except TypeError as e:
        assert e.__traceback__ is not None
        tb_str_color = formatting.exc_to_traceback_str(
            e, e.__traceback__, color=True, local_stack_only=False
        )
        tb_str_no_color = formatting.exc_to_traceback_str(
            e, e.__traceback__, color=False, local_stack_only=False
        )

        # Both should work
        assert isinstance(tb_str_color, str)
        assert isinstance(tb_str_no_color, str)
        assert "TypeError" in tb_str_color
        assert "TypeError" in tb_str_no_color


def test_exception_message_override_for_assertions():
    """Test that assertion errors include verbose messages."""
    try:
        assert 1 == 2
    except AssertionError:
        excinfo = pytest.ExceptionInfo.from_current()
        message = pytest_plugin._get_exception_message_override(excinfo)

        tb_str = formatting.exc_to_traceback_str(
            excinfo.value,
            excinfo.tb,
            color=False,
            local_stack_only=False,
            exc_msg_override=message,
        )

        assert "assert 1 == 2" in tb_str


@pytest.mark.parametrize(
    ("exc_type", "message"),
    [
        (ValueError, "Test error message"),
        (KeyError, "missing key"),
        (TypeError, "bad type"),
        (AttributeError, "missing attribute"),
    ],
)
def test_exception_message_override_ignores_standard_message(exc_type, message):
    """Test that standard exception messages do not override."""
    try:
        raise exc_type(message)
    except exc_type:
        excinfo = pytest.ExceptionInfo.from_current()
        message_override = pytest_plugin._get_exception_message_override(excinfo)
        assert message_override is None


def test_chained_exceptions_in_formatting():
    """Test that chained exceptions are formatted correctly."""
    try:
        try:
            raise ValueError("Original error")
        except ValueError as e:
            raise RuntimeError("Wrapped error") from e
    except RuntimeError as e:
        assert e.__traceback__ is not None
        tb_str = formatting.exc_to_traceback_str(
            e, e.__traceback__, color=False, local_stack_only=False
        )

        # Should contain both exceptions
        assert "ValueError" in tb_str
        assert "Original error" in tb_str
        assert "RuntimeError" in tb_str
        assert "Wrapped error" in tb_str
        assert "direct cause" in tb_str


def test_nested_exceptions_in_formatting():
    """Test that nested exceptions (context) are formatted correctly."""
    try:
        try:
            raise ValueError("First error")
        except ValueError:
            raise RuntimeError("Second error")
    except RuntimeError as e:
        assert e.__traceback__ is not None
        tb_str = formatting.exc_to_traceback_str(
            e, e.__traceback__, color=False, local_stack_only=False
        )

        # Should contain both exceptions
        assert "ValueError" in tb_str
        assert "First error" in tb_str
        assert "RuntimeError" in tb_str
        assert "Second error" in tb_str


def test_plugin_registered_with_pytest(pytestconfig):
    """Test that the plugin is actually registered with pytest."""
    # This test will only work if the plugin entry point is configured
    plugin_names = [
        p.__name__ if hasattr(p, "__name__") else str(p)
        for p in pytestconfig.pluginmanager.get_plugins()
    ]

    # Check if our plugin module is loaded
    assert any("beautiful_traceback" in name for name in plugin_names)


def test_plugin_config_options_registered(pytestconfig):
    """Test that config options are registered when plugin loads."""
    # Try to access the ini options
    try:
        enable_bt = pytestconfig.getini("enable_beautiful_traceback")
        enable_local = pytestconfig.getini(
            "enable_beautiful_traceback_local_stack_only"
        )

        # Should be boolean values
        assert isinstance(enable_bt, bool)
        assert isinstance(enable_local, bool)
    except ValueError:
        pytest.skip("Plugin not fully registered - entry point may not be configured")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
