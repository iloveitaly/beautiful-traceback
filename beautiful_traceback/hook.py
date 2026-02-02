import os
import sys
import types
import typing as typ

from beautiful_traceback import formatting


def init_excepthook(
    color: bool,
    local_stack_only: bool,
    exclude_patterns: typ.Sequence[str],
) -> typ.Callable:
    def excepthook(
        exc_type: typ.Type[BaseException],
        exc_value: BaseException,
        traceback: types.TracebackType,
    ) -> None:
        tb_str = (
            formatting.exc_to_traceback_str(
                exc_value,
                traceback,
                color,
                local_stack_only,
                exclude_patterns=exclude_patterns,
            )
            + "\n"
        )

        sys.stderr.write(tb_str)

    return excepthook


def install(
    envvar: typ.Optional[str] = None,
    color: bool = True,
    only_tty: bool = True,
    only_hook_if_default_excepthook: bool = True,
    local_stack_only: bool = False,
    exclude_patterns: typ.Sequence[str] = (),
) -> None:
    """Hook the current excepthook to the beautiful_traceback.

    If you set `only_tty=False`, beautiful_traceback will always
    be active even when stdout is piped or redirected.

    Color output respects the NO_COLOR environment variable
    (https://no-color.org/). If NO_COLOR is set (regardless of
    its value), color output will be disabled.
    """
    if envvar and os.environ.get(envvar, "0") == "0":
        return

    if "NO_COLOR" in os.environ:
        color = False

    # avoid installing when not running in a tty
    isatty = getattr(sys.stderr, "isatty", lambda: False)()
    if only_tty and not isatty:
        return

    if not isatty:
        color = False

    is_default_exepthook = sys.excepthook == sys.__excepthook__
    if only_hook_if_default_excepthook and not is_default_exepthook:
        return

    sys.excepthook = init_excepthook(
        color=color,
        local_stack_only=local_stack_only,
        exclude_patterns=exclude_patterns,
    )


def uninstall() -> None:
    """Restore the default excepthook."""
    sys.excepthook = sys.__excepthook__
