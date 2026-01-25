import os
from typing import Any, Generator

from . import formatting
import pytest

from pytest import Config


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


def _get_exception_message_override(excinfo: pytest.ExceptionInfo) -> str | None:
    """Return pytest's verbose exception message when rewriting adds detail.

    The plugin overrides pytest's longrepr rendering, which skips the
    ExceptionInfo repr where pytest stores rewritten assertion diffs. Without
    this, AssertionError messages collapse to str(exc) and omit left/right
    details. Pulling reprcrash.message preserves that verbose message when
    pytest provides one.
    """
    try:
        repr_info = excinfo.getrepr(style="long")
    except Exception:
        return None

    reprcrash = getattr(repr_info, "reprcrash", None)
    if reprcrash is None:
        return None

    message = getattr(reprcrash, "message", None)
    if not message:
        return None

    exc_name = type(excinfo.value).__name__
    prefix = f"{exc_name}: "
    if message.startswith(prefix):
        message = message.removeprefix(prefix)

    if not message or message == exc_name:
        return None

    exc_message = str(excinfo.value)
    if message == exc_message:
        return None

    return message


def _get_pytest_assertion_details(excinfo: pytest.ExceptionInfo) -> str | None:
    """Return the pytest assertion diff lines for AssertionError."""
    if not isinstance(excinfo.value, AssertionError):
        return None

    try:
        # pytest stores assertion diffs on its own repr object, not the exception.
        # Reference: https://github.com/pytest-dev/pytest/blob/main/src/_pytest/_code/code.py
        repr_info = excinfo.getrepr(style="long")
    except Exception:
        return None

    # Get the full formatted traceback text. pytest doesn't expose longreprtext
    # as a public attribute, but some versions may have it. Fall back to str()
    # which calls the repr object's __str__() method.
    longreprtext = getattr(repr_info, "longreprtext", None)
    if not longreprtext:
        longreprtext = str(repr_info)

    if not longreprtext:
        return None

    # Keep only the assertion diff lines for concise appending.
    lines = []
    for line in longreprtext.splitlines():
        # Keep pytest's assertion diff lines and the failing expression.
        stripped = line.lstrip()
        if stripped.startswith("E"):
            lines.append(stripped)
            continue

        # Include the source line marker when present.
        if stripped.startswith(">"):
            lines.append(stripped)

    if not lines:
        return None

    return os.linesep.join(lines)


def _format_traceback(excinfo: pytest.ExceptionInfo, config: Config) -> str:
    """Format a traceback with beautiful_traceback styling and pytest assertion details."""
    message_override = _get_exception_message_override(excinfo)
    assertion_details = _get_pytest_assertion_details(excinfo)

    formatted_traceback = formatting.exc_to_traceback_str(
        excinfo.value,
        excinfo.tb,
        color=True,
        local_stack_only=_get_option(
            config, "enable_beautiful_traceback_local_stack_only"
        ),
        exc_msg_override=message_override,
    )

    if assertion_details:
        formatted_traceback += (
            os.linesep
            + "PYTEST ASSERTION"
            + os.linesep
            + assertion_details
            + os.linesep
        )

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
