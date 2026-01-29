"""Helpers for extracting pytest's rewritten assertion details."""

import os

import pytest


def get_exception_message_override(excinfo: pytest.ExceptionInfo) -> str | None:
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


def get_pytest_assertion_details(excinfo: pytest.ExceptionInfo) -> str | None:
    """Return pytest's rewritten assertion lines for AssertionError.

    Pytest only provides left/right diffs when a module is rewritten during
    import. For helper modules, call pytest.register_assert_rewrite before
    importing them, otherwise the assertion message is plain and there are no
    diff lines to extract.
    """
    if not isinstance(excinfo.value, AssertionError):
        return None

    try:
        # pytest stores assertion diffs on its own repr object, not the exception.
        # Reference: https://github.com/pytest-dev/pytest/blob/main/src/_pytest/_code/code.py
        repr_info = excinfo.getrepr(style="long")
    except Exception:
        return None

    reprtraceback = getattr(repr_info, "reprtraceback", None)
    if reprtraceback is None:
        chain = getattr(repr_info, "chain", None)
        if chain:
            reprtraceback = chain[-1][0]

    if reprtraceback is None:
        return None

    reprentries = getattr(reprtraceback, "reprentries", None)
    if not reprentries:
        return None

    last_entry = reprentries[-1]
    entry_lines = getattr(last_entry, "lines", None)
    if not entry_lines:
        return None

    lines = []
    for line in entry_lines:
        stripped = line.lstrip()
        if stripped.startswith("E"):
            lines.append(stripped)
            continue

        if stripped.startswith(">"):
            lines.append(stripped)

    if not lines:
        return None

    return os.linesep.join(lines)
