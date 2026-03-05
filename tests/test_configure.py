import pytest

import beautiful_traceback.config as bt_config
from beautiful_traceback import configure


@pytest.fixture(autouse=True)
def clean_config():
    yield
    bt_config._config.clear()


def test_configure_sets_local_stack_only():
    configure(local_stack_only=True)
    assert bt_config._config["local_stack_only"] is True


def test_configure_sets_exclude_patterns():
    configure(exclude_patterns=["pattern_a", "pattern_b"])
    assert bt_config._config["exclude_patterns"] == ["pattern_a", "pattern_b"]


def test_configure_sets_both():
    configure(local_stack_only=False, exclude_patterns=["pat"])
    assert bt_config._config["local_stack_only"] is False
    assert bt_config._config["exclude_patterns"] == ["pat"]


def test_configure_none_args_do_not_overwrite():
    configure(local_stack_only=True)
    configure(local_stack_only=None)
    assert bt_config._config["local_stack_only"] is True


def test_configure_overwrites_previous_value():
    configure(local_stack_only=True)
    configure(local_stack_only=False)
    assert bt_config._config["local_stack_only"] is False


def test_get_default_returns_configured_value():
    configure(local_stack_only=True)
    assert bt_config.get_default("local_stack_only", False) is True


def test_get_default_returns_fallback_when_not_configured():
    assert bt_config.get_default("local_stack_only", False) is False
    assert bt_config.get_default("exclude_patterns", ()) == ()


def test_configure_no_args_does_not_mutate_config():
    configure()
    assert bt_config._config == {}
