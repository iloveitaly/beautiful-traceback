"""Pytest plugin that preserves rewritten assertion details in tracebacks.

Pytest rewrites assert statements at import time for test modules (and any
modules registered via pytest.register_assert_rewrite). The rewritten asserts
raise AssertionError instances that include rich explanation text and left/right
diffs inside pytest's repr objects, not on the exception itself. This plugin
extracts those repr details and appends them to beautiful_traceback output.
"""

import os
from typing import Generator

import pytest
from pytest import Config
from pytest_plugin_utils.config import (
    get_pytest_option,
    register_pytest_options,
    set_pytest_option,
)

from . import config
from . import formatting
from .pytest_assertion import get_exception_message_override
from .pytest_assertion import get_pytest_assertion_details

# __package__ is str | None (None when run as a top-level script), so we narrow it here
assert __package__ is not None
_namespace: str = __package__

set_pytest_option(
    _namespace,
    "enable_beautiful_traceback",
    default=config.env_bool("ENABLED", True),
    type_hint=bool,
    available="all",
    help="Enable the beautiful traceback plugin",
)
set_pytest_option(
    _namespace,
    "enable_beautiful_traceback_local_stack_only",
    default=config.env_bool("LOCAL_STACK_ONLY", True),
    type_hint=bool,
    available="all",
    help="Show only local code (filter out library/framework internals)",
)
set_pytest_option(
    _namespace,
    "beautiful_traceback_exclude_patterns",
    default=[],
    type_hint=list[str],
    available="all",
    help="Exclude traceback frames that match regex patterns",
)
set_pytest_option(
    _namespace,
    "beautiful_traceback_show_aliases",
    default=config.env_bool("SHOW_ALIASES", True),
    type_hint=bool,
    available="all",
    help="Show the 'Aliases for entries in sys.path' section",
)


def _opt_bool(config: Config, key: str) -> bool:
    val = get_pytest_option(_namespace, config, key, type_hint=bool)
    assert isinstance(val, bool)
    return val


def _opt_str_list(config: Config, key: str) -> list[str]:
    val = get_pytest_option(_namespace, config, key, type_hint=list[str])
    assert isinstance(val, list)
    return val


def _format_traceback(excinfo: pytest.ExceptionInfo, config: Config) -> str:
    """Format a traceback with beautiful_traceback styling and pytest details."""
    message_override = get_exception_message_override(excinfo)
    assertion_details = get_pytest_assertion_details(excinfo)

    formatted_traceback = formatting.exc_to_traceback_str(
        excinfo.value,
        excinfo.tb,
        color=True,
        local_stack_only=_opt_bool(
            config, "enable_beautiful_traceback_local_stack_only"
        ),
        exc_msg_override=message_override,
        exclude_patterns=_opt_str_list(config, "beautiful_traceback_exclude_patterns"),
        show_aliases=_opt_bool(config, "beautiful_traceback_show_aliases"),
    )

    if assertion_details:
        formatted_traceback += os.linesep + assertion_details + os.linesep

    return formatted_traceback


def pytest_addoption(parser) -> None:
    register_pytest_options(_namespace, parser)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call) -> Generator[None, None, None]:
    """Format test execution tracebacks with beautiful_traceback.

    This hook runs during the test execution phase and replaces pytest's
    default traceback formatting with beautiful_traceback's output.
    """
    outcome = yield  # type: ignore[misc]
    report = outcome.get_result()  # type: ignore[attr-defined]

    if _opt_bool(item.config, "enable_beautiful_traceback") and report.failed:
        report.longrepr = _format_traceback(call.excinfo, item.config)


def pytest_exception_interact(node, call, report) -> None:
    """Format collection-phase tracebacks with beautiful_traceback.

    This hook runs during collection (e.g., import errors, fixture errors)
    and ensures those errors also use beautiful_traceback formatting.
    """
    if _opt_bool(node.config, "enable_beautiful_traceback") and report.failed:
        report.longrepr = _format_traceback(call.excinfo, node.config)
