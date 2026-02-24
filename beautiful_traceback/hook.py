import inspect
import logging
import os
import sys
import threading
import types
import typing as typ

import colorama

from beautiful_traceback import config
from beautiful_traceback import formatting

log = logging.getLogger(__name__)


def _source_location(func: typ.Callable) -> str:
    try:
        file = inspect.getfile(func)
        _, line = inspect.getsourcelines(func)
        return f"{file}:{line}"
    except (TypeError, OSError):
        return repr(func)


def _format_thread_header(thread: threading.Thread, color: bool) -> str:
    daemon_suffix = " (daemon)" if thread.daemon else ""
    text = f"Exception in thread {thread.name}{daemon_suffix}:\n"

    if not color:
        return text

    return colorama.Fore.RED + colorama.Style.BRIGHT + text + colorama.Style.RESET_ALL


def init_excepthook(
    color: bool,
    local_stack_only: bool,
    exclude_patterns: typ.Sequence[str],
    show_aliases: bool = True,
) -> typ.Callable:
    def excepthook(
        exc_type: typ.Type[BaseException],
        exc_value: BaseException,
        traceback: types.TracebackType,
        thread: threading.Thread | None = None,
    ) -> None:
        tb_str = (
            formatting.exc_to_traceback_str(
                exc_value,
                traceback,
                color,
                local_stack_only,
                exclude_patterns=exclude_patterns,
                show_aliases=show_aliases,
            )
            + "\n"
        )

        if thread is not None:
            tb_str = _format_thread_header(thread, color) + tb_str

        sys.stderr.write(tb_str)

    return excepthook


def install(
    color: bool = True,
    only_tty: bool = True,
    only_hook_if_default_excepthook: bool = True,
    local_stack_only: bool | None = None,
    exclude_patterns: typ.Sequence[str] = (),
    show_aliases: bool | None = None,
) -> None:
    """Hook the current excepthook to the beautiful_traceback.

    If you set `only_tty=False`, beautiful_traceback will always
    be active even when stdout is piped or redirected.

    Color output respects the NO_COLOR environment variable
    (https://no-color.org/). If NO_COLOR is set (regardless of
    its value), color output will be disabled.
    """
    if not config.env_bool("ENABLED", True):
        return

    if local_stack_only is None:
        local_stack_only = config.env_bool("LOCAL_STACK_ONLY", False)

    if show_aliases is None:
        show_aliases = config.env_bool("SHOW_ALIASES", True)

    if "NO_COLOR" in os.environ:
        color = False

    # avoid installing when not running in a tty
    isatty = getattr(sys.stderr, "isatty", lambda: False)()
    if only_tty and not isatty:
        return

    if not isatty:
        color = False

    is_default_sys_hook = sys.excepthook == sys.__excepthook__
    if only_hook_if_default_excepthook and not is_default_sys_hook:
        return

    if not is_default_sys_hook:
        log.info(
            "overriding non-default sys.excepthook: %s",
            _source_location(sys.excepthook),
        )

    is_default_thread_hook = threading.excepthook == threading.__excepthook__
    if not is_default_thread_hook:
        log.info(
            "overriding non-default threading.excepthook: %s",
            _source_location(threading.excepthook),
        )

    excepthook = init_excepthook(
        color=color,
        local_stack_only=local_stack_only,
        exclude_patterns=exclude_patterns,
        show_aliases=show_aliases,
    )
    sys.excepthook = excepthook

    def thread_excepthook(args):
        excepthook(
            args.exc_type, args.exc_value, args.exc_traceback, thread=args.thread
        )

    threading.excepthook = thread_excepthook


def uninstall() -> None:
    """Restore the default excepthook."""
    sys.excepthook = sys.__excepthook__
    threading.excepthook = threading.__excepthook__
