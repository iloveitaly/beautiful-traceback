import os
import sys
import threading

import pytest

from beautiful_traceback import exc_to_json
from beautiful_traceback import formatting


@pytest.fixture
def env_setup():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)

    test_paths = [
        project_root,
        "/home/user/venv/lib/python3.13/site-packages",
        "/opt/homebrew/Cellar/python/3.13.0/lib/python3.13",
    ]
    formatting.TEST_PATHS = test_paths
    formatting.PWD = project_root
    yield
    del formatting.TEST_PATHS[:]
    formatting.PWD = os.getcwd()


def test_simple_exception(env_setup):
    result = {}
    try:
        raise ValueError("test error message")
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(exc_info[1], exc_info[2])

    assert result["exception"] == "ValueError"
    assert result["message"] == "test error message"
    assert "frames" in result
    assert isinstance(result["frames"], list)
    assert len(result["frames"]) > 0

    frame = result["frames"][0]
    assert "module" in frame
    assert "alias" in frame
    assert "function" in frame
    assert "lineno" in frame

    assert frame["function"] == "test_simple_exception"
    assert isinstance(frame["lineno"], int)
    assert frame["alias"] == "<pwd>"
    assert "test_json_formatting.py" in frame["module"]


def test_exception_chain_with_cause(env_setup):
    result = {}
    try:
        try:
            raise KeyError("missing_key")
        except KeyError as e:
            raise ValueError("wrapper error") from e
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(exc_info[1], exc_info[2])

    assert result["exception"] == "ValueError"
    assert result["message"] == "wrapper error"
    assert "chain" in result
    assert len(result["chain"]) == 1

    chained = result["chain"][0]
    assert chained["exception"] == "KeyError"
    assert chained["message"] == "'missing_key'"
    assert chained["relationship"] == "caused_by"
    assert isinstance(chained["frames"], list)


def test_exception_chain_with_context(env_setup):
    result = {}
    try:
        try:
            raise KeyError("context_key")
        except KeyError:
            raise ValueError("new error")
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(exc_info[1], exc_info[2])

    assert result["exception"] == "ValueError"
    assert "chain" in result
    assert len(result["chain"]) == 1

    chained = result["chain"][0]
    assert chained["exception"] == "KeyError"
    assert chained["relationship"] == "context"


def test_local_stack_only_false(env_setup):
    def library_function():
        raise RuntimeError("library error")

    library_function.__module__ = "requests.sessions"

    result = {}
    try:
        library_function()
    except RuntimeError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(exc_info[1], exc_info[2], local_stack_only=False)

    assert len(result["frames"]) > 0


def test_local_stack_only_true(env_setup):
    result_local = {}
    result_all = {}
    try:
        raise RuntimeError("local error")
    except RuntimeError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result_all = exc_to_json(exc_info[1], exc_info[2], local_stack_only=False)
        result_local = exc_to_json(exc_info[1], exc_info[2], local_stack_only=True)

    for frame in result_local["frames"]:
        assert frame["alias"] == "<pwd>"

    assert len(result_local["frames"]) <= len(result_all["frames"])


def test_exclude_patterns(env_setup):
    result = {}
    try:
        raise ValueError("test")
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(
            exc_info[1],
            exc_info[2],
            exclude_patterns=[r"test_json_formatting\.py"],
        )

    assert result["frames"] == []


def test_exclude_patterns_chain(env_setup):
    result = {}
    try:
        try:
            raise KeyError("missing_key")
        except KeyError as e:
            raise ValueError("wrapper error") from e
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(
            exc_info[1],
            exc_info[2],
            exclude_patterns=[r"test_json_formatting\.py"],
        )

    assert result["frames"] == []
    assert "chain" in result
    assert result["chain"][0]["frames"] == []


def test_aliased_paths_not_full_paths(env_setup):
    result = {}
    try:
        raise ValueError("test")
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(exc_info[1], exc_info[2])

    for frame in result["frames"]:
        module = frame["module"]
        assert not module.startswith("/"), f"Expected relative path, got: {module}"
        assert frame["alias"], f"Expected alias to be set for: {module}"


def test_circular_exception_reference(env_setup):
    result = {}
    try:
        exc1 = ValueError("first")
        exc2 = RuntimeError("second")
        exc1.__cause__ = exc2
        exc2.__cause__ = exc1
        raise exc1
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(exc_info[1], exc_info[2])

    assert result["exception"] == "ValueError"
    assert "chain" in result


def test_exception_with_no_traceback(env_setup):
    exc = ValueError("no traceback")
    result = exc_to_json(exc, None)

    assert result["exception"] == "ValueError"
    assert result["message"] == "no traceback"
    assert result["frames"] == []


def test_frame_structure(env_setup):
    result = {}
    try:
        raise ValueError("test")
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(exc_info[1], exc_info[2])

    frame = result["frames"][0]

    assert set(frame.keys()) == {"module", "alias", "function", "lineno"}

    assert isinstance(frame["module"], str)
    assert isinstance(frame["alias"], str)
    assert isinstance(frame["function"], str)
    assert isinstance(frame["lineno"], int)


def test_multiple_alias_types(env_setup):
    result = {}
    try:
        raise ValueError("test")
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(exc_info[1], exc_info[2], local_stack_only=False)

    aliases_found = {frame["alias"] for frame in result["frames"]}
    assert "<pwd>" in aliases_found


def test_local_stack_only_filters_chain(env_setup):
    def site_function():
        raise KeyError("site error")

    site_function.__module__ = "requests.sessions"

    result = {}
    try:
        try:
            site_function()
        except KeyError as e:
            raise ValueError("wrapper") from e
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(exc_info[1], exc_info[2], local_stack_only=True)

    for frame in result["frames"]:
        assert frame["alias"] == "<pwd>"

    if "chain" in result:
        for chained_exc in result["chain"]:
            for frame in chained_exc["frames"]:
                assert frame["alias"] == "<pwd>"


def test_thread_metadata(env_setup):
    result = {}
    try:
        raise ValueError("test error in thread")
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None

        thread = threading.Thread(name="TestWorker", daemon=False)
        result = exc_to_json(exc_info[1], exc_info[2], thread=thread)

    assert result["exception"] == "ValueError"
    assert result["message"] == "test error in thread"
    assert "thread" in result
    assert result["thread"]["name"] == "TestWorker"
    assert result["thread"]["daemon"] is False


def test_thread_metadata_daemon(env_setup):
    result = {}
    try:
        raise RuntimeError("daemon thread error")
    except RuntimeError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None

        thread = threading.Thread(name="DaemonWorker", daemon=True)
        result = exc_to_json(exc_info[1], exc_info[2], thread=thread)

    assert result["exception"] == "RuntimeError"
    assert "thread" in result
    assert result["thread"]["name"] == "DaemonWorker"
    assert result["thread"]["daemon"] is True


def test_thread_metadata_none(env_setup):
    result = {}
    try:
        raise ValueError("no thread metadata")
    except ValueError:
        exc_info = sys.exc_info()
        assert exc_info[1] is not None
        result = exc_to_json(exc_info[1], exc_info[2], thread=None)

    assert result["exception"] == "ValueError"
    assert "thread" not in result
