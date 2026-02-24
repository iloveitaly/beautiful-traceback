"""Pytest plugin that preserves rewritten assertion details in tracebacks.

Pytest rewrites assert statements at import time for test modules (and any
modules registered via pytest.register_assert_rewrite). The rewritten asserts
raise AssertionError instances that include rich explanation text and left/right
diffs inside pytest's repr objects, not on the exception itself. This plugin
extracts those repr details and appends them to beautiful_traceback output.
"""

import os
from typing import Any, Generator

import pytest
from pytest import Config

from . import formatting
from .pytest_assertion import get_exception_message_override
from .pytest_assertion import get_pytest_assertion_details


def _get_option(config: Config, key: str) -> Any:
    val = None

    # will throw an exception if option is not set
    try:
        val = config.getoption(key)
    except Exception:
        pass

    if val is None:
        val = config.getini(key)

    return val


def _format_traceback(excinfo: pytest.ExceptionInfo, config: Config) -> str:
    """Format a traceback with beautiful_traceback styling and pytest details."""
    message_override = get_exception_message_override(excinfo)
    assertion_details = get_pytest_assertion_details(excinfo)
    exclude_patterns = _get_option(config, "beautiful_traceback_exclude_patterns")

    formatted_traceback = formatting.exc_to_traceback_str(
        excinfo.value,
        excinfo.tb,
        color=True,
        local_stack_only=_get_option(
            config, "enable_beautiful_traceback_local_stack_only"
        ),
        exc_msg_override=message_override,
        exclude_patterns=exclude_patterns,
        show_aliases=_get_option(config, "beautiful_traceback_show_aliases"),
    )

    if assertion_details:
        formatted_traceback += os.linesep + assertion_details + os.linesep

    return formatted_traceback


def pytest_addoption(parser) -> None:
    parser.addini(
        "enable_beautiful_traceback",
        "Enable the beautiful traceback plugin",
        type="bool",
        default=True,
    )

    parser.addini(
        "enable_beautiful_traceback_local_stack_only",
        "Show only local code (filter out library/framework internals)",
        type="bool",
        default=True,
    )

    parser.addini(
        "beautiful_traceback_exclude_patterns",
        "Exclude traceback frames that match regex patterns",
        type="linelist",
        default=[],
    )

    parser.addini(
        "beautiful_traceback_show_aliases",
        "Show the 'Aliases for entries in sys.path' section",
        type="bool",
        default=True,
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call) -> Generator[None, None, None]:
    """Format test execution tracebacks with beautiful_traceback.

    This hook runs during the test execution phase and replaces pytest's
    default traceback formatting with beautiful_traceback's output.
    """
    outcome = yield  # type: ignore[misc]
    report = outcome.get_result()  # type: ignore[attr-defined]

    if _get_option(item.config, "enable_beautiful_traceback") and report.failed:
        report.longrepr = _format_traceback(call.excinfo, item.config)


def pytest_exception_interact(node, call, report) -> None:
    """Format collection-phase tracebacks with beautiful_traceback.

    This hook runs during collection (e.g., import errors, fixture errors)
    and ensures those errors also use beautiful_traceback formatting.
    """
    if _get_option(node.config, "enable_beautiful_traceback") and report.failed:
        report.longrepr = _format_traceback(call.excinfo, node.config)
