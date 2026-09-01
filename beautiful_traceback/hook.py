import inspect
import logging
import os
import sys
import threading
import types
import typing as typ

import colorama

from beautiful_traceback import config, formatting

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
    show_aliases: bool = False,
) -> typ.Callable:
    def excepthook(
        exc_type: type[BaseException],
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
    exclude_patterns: typ.Sequence[str] | None = None,
    show_aliases: bool | None = None,
) -> None:
    """Hook sys.excepthook and threading.excepthook to print beautiful tracebacks.

    Use this at a process entrypoint (script, CLI, app startup) so uncaught
    exceptions dump a formatted traceback to stderr. Skip it in production if
    another library (e.g. structlog-config) already installs an exception hook
    for structured logging.

    For process-wide frame filters used by `exc_to_json` and pytest, call
    `configure` instead — or in addition. `configure` does not install a hook.

    If you set `only_tty=False`, beautiful_traceback will always
    be active even when stdout is piped or redirected.

    Color output respects the NO_COLOR environment variable
    (https://no-color.org/). If NO_COLOR is set (regardless of
    its value), color output will be disabled.

    Args:
        color: Enable ANSI-colored output. Forced off when stderr is not a TTY
            or when `NO_COLOR` is set (https://no-color.org/).
        only_tty: Only install the hook when stderr is a TTY. Pass `False` to
            activate even when output is piped or redirected. Helpful to set
            to `False` when running in a Docker container.
        only_hook_if_default_excepthook: Only replace `sys.excepthook` when it
            is still Python's default. Pass `False` to override an existing
            hook (rich, typer, etc).
        local_stack_only: Only include frames from `<pwd>`, filtering out
            library frames. `None` uses `configure` /
            `BEAUTIFUL_TRACEBACK_LOCAL_STACK_ONLY`. Written into the global
            config when not `None`.
        exclude_patterns: Regex patterns matched against frame paths to drop
            frames. `None` uses `configure` defaults. Written into the
            global config when not `None`.
        show_aliases: Show the sys.path aliases section. `None` uses
            `configure` / `BEAUTIFUL_TRACEBACK_SHOW_ALIASES` (default:
            false). Written into the global config when not `None`.
    """
    if not config.env_bool("ENABLED", True):
        return

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

    # configure settings passed to install globally to they stick around
    if (
        local_stack_only is not None
        or exclude_patterns is not None
        or show_aliases is not None
    ):
        config.configure(
            local_stack_only=local_stack_only,
            exclude_patterns=exclude_patterns,
            show_aliases=show_aliases,
        )

    resolved_local_stack_only = config.get_default(
        "local_stack_only", config.env_bool("LOCAL_STACK_ONLY", False)
    )
    resolved_exclude_patterns = config.get_default("exclude_patterns", ())
    resolved_show_aliases = (
        show_aliases
        if show_aliases is not None
        else config.get_default("show_aliases", config.env_bool("SHOW_ALIASES", False))
    )

    excepthook = init_excepthook(
        color=color,
        local_stack_only=resolved_local_stack_only,
        exclude_patterns=resolved_exclude_patterns,
        show_aliases=resolved_show_aliases,
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
