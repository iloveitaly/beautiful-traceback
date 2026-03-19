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


def test_configure_sets_show_aliases():
    configure(show_aliases=True)
    assert bt_config._config["show_aliases"] is True


def test_configure_sets_both():
    configure(local_stack_only=False, exclude_patterns=["pat"])
    assert bt_config._config["local_stack_only"] is False
    assert bt_config._config["exclude_patterns"] == ["pat"]


def test_configure_sets_all_values():
    configure(local_stack_only=False, exclude_patterns=["pat"], show_aliases=True)
    assert bt_config._config["local_stack_only"] is False
    assert bt_config._config["exclude_patterns"] == ["pat"]
    assert bt_config._config["show_aliases"] is True


def test_configure_none_args_do_not_overwrite():
    configure(local_stack_only=True)
    configure(local_stack_only=None)
    assert bt_config._config["local_stack_only"] is True


def test_configure_none_show_aliases_does_not_overwrite():
    configure(show_aliases=True)
    configure(show_aliases=None)
    assert bt_config._config["show_aliases"] is True


def test_configure_overwrites_previous_value():
    configure(local_stack_only=True)
    configure(local_stack_only=False)
    assert bt_config._config["local_stack_only"] is False


def test_configure_overwrites_show_aliases_value():
    configure(show_aliases=True)
    configure(show_aliases=False)
    assert bt_config._config["show_aliases"] is False


def test_get_default_returns_configured_value():
    configure(local_stack_only=True)
    assert bt_config.get_default("local_stack_only", False) is True


def test_get_default_returns_configured_show_aliases_value():
    configure(show_aliases=True)
    assert bt_config.get_default("show_aliases", False) is True


def test_get_default_returns_fallback_when_not_configured():
    assert bt_config.get_default("local_stack_only", False) is False
    assert bt_config.get_default("exclude_patterns", ()) == ()
    assert bt_config.get_default("show_aliases", False) is False


def test_configure_no_args_does_not_mutate_config():
    configure()
    assert bt_config._config == {}


def test_get_config_returns_copy():
    configure(local_stack_only=True, exclude_patterns=["a"], show_aliases=True)
    config_copy = bt_config.get_config()
    assert config_copy["local_stack_only"] is True
    assert config_copy["exclude_patterns"] == ["a"]
    assert config_copy["show_aliases"] is True

    # Mutate the copy
    config_copy["local_stack_only"] = False

    # Ensure original is unchanged
    assert bt_config._config["local_stack_only"] is True


def test_install_persists_show_aliases_config():
    import beautiful_traceback

    beautiful_traceback.install(only_tty=False, show_aliases=True)

    try:
        assert bt_config.get_default("show_aliases", False) is True
    finally:
        beautiful_traceback.uninstall()


def test_get_config_is_exposed():
    import beautiful_traceback

    assert hasattr(beautiful_traceback, "get_config")
    assert beautiful_traceback.get_config is bt_config.get_config
