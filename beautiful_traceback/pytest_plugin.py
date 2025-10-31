from . import formatting
import pytest

from pytest import Config


def _get_option(config: Config, key: str):
    val = None

    # will throw an exception if option is not set
    try:
        val = config.getoption(key)
    except Exception:
        pass

    if val is None:
        val = config.getini(key)

    return val


def pytest_addoption(parser):
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
def pytest_runtest_makereport(item, call):
    """
    Pytest stack traces are challenging to work with by default. This plugin allows beautiful_traceback to be used instead.

    This little piece of code was hard-won:

    https://grok.com/share/bGVnYWN5_951be3b1-6811-4fda-b220-c1dd72dedc31
    """
    outcome = yield
    report = outcome.get_result()  # Get the generated TestReport object

    # Check if the report is for the 'call' phase (test execution) and if it failed
    if _get_option(item.config, "enable_beautiful_traceback") and report.failed:
        value = call.excinfo.value
        tb = call.excinfo.tb

        formatted_traceback = formatting.exc_to_traceback_str(
            value,
            tb,
            color=True,
            local_stack_only=_get_option(
                item.config, "enable_beautiful_traceback_local_stack_only"
            ),
        )
        report.longrepr = formatted_traceback


def pytest_exception_interact(node, call, report):
    """
    This can run during collection, not just test execution.

    So, if there's an import or other pre-run error in pytest, this will apply the correct formatting.
    """
    if report.failed:
        value = call.excinfo.value
        tb = call.excinfo.tb
        formatted_traceback = formatting.exc_to_traceback_str(
            value,
            tb,
            color=True,
            local_stack_only=_get_option(
                node.config, "enable_beautiful_traceback_local_stack_only"
            ),
        )
        report.longrepr = formatted_traceback
