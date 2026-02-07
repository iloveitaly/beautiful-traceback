"""Tests for threading.excepthook support."""

import io
import sys
import threading

import beautiful_traceback


def test_threading_excepthook_installed():
    """Test that threading.excepthook is installed."""
    original_hook = threading.excepthook

    beautiful_traceback.install(only_tty=False)

    assert threading.excepthook != original_hook

    beautiful_traceback.uninstall()
    assert threading.excepthook == threading.__excepthook__


def test_threading_excepthook_formats_exception():
    """Test that threading.excepthook properly formats exceptions."""
    beautiful_traceback.install(only_tty=False, color=False)

    captured_output = io.StringIO()
    original_stderr = sys.stderr

    try:
        sys.stderr = captured_output

        def crasher():
            raise ValueError("Thread error message")

        t = threading.Thread(target=crasher, name="TestWorker")
        t.start()
        t.join()

        output = captured_output.getvalue()

        assert "Exception in thread TestWorker:" in output
        assert "ValueError: Thread error message" in output
        assert "crasher" in output

    finally:
        sys.stderr = original_stderr
        beautiful_traceback.uninstall()


def test_threading_excepthook_daemon_suffix():
    """Test that daemon threads show (daemon) suffix."""
    beautiful_traceback.install(only_tty=False, color=False)

    captured_output = io.StringIO()
    original_stderr = sys.stderr

    try:
        sys.stderr = captured_output

        def crasher():
            raise RuntimeError("Daemon error")

        t = threading.Thread(target=crasher, name="DaemonWorker", daemon=True)
        t.start()
        t.join()

        output = captured_output.getvalue()

        assert "Exception in thread DaemonWorker (daemon):" in output
        assert "RuntimeError: Daemon error" in output

    finally:
        sys.stderr = original_stderr
        beautiful_traceback.uninstall()


def test_threading_excepthook_uninstall():
    """Test that uninstall restores original threading.excepthook."""
    original_hook = threading.excepthook

    beautiful_traceback.install(only_tty=False)
    assert threading.excepthook != original_hook

    beautiful_traceback.uninstall()
    assert threading.excepthook == original_hook
