"""JSON exception formatting for production logging.

This module provides exc_to_json() which converts exceptions to structured
dictionaries suitable for JSON logging in production environments.
"""

import types
import typing as typ

import beautiful_traceback.common as com
import beautiful_traceback.formatting as fmt


def _row_to_json_frame(row: fmt.Row) -> dict[str, typ.Any]:
    """Convert a Row to a JSON-serializable frame dict."""
    return {
        "module": row.short_module,
        "alias": row.alias,
        "function": row.call,
        "lineno": int(row.lineno),
    }


def _format_traceback_json(
    rows: list[fmt.Row],
    exc_name: str,
    exc_msg: str,
    local_stack_only: bool,
) -> dict[str, typ.Any]:
    """Convert rows to a JSON-serializable traceback dict."""
    if local_stack_only:
        filtered_rows = [row for row in rows if row.alias == "<pwd>"]
    else:
        filtered_rows = rows

    frames = [_row_to_json_frame(row) for row in filtered_rows]

    return {
        "exception": exc_name,
        "message": exc_msg,
        "frames": frames,
    }


def exc_to_json(
    exc_value: BaseException,
    traceback: types.TracebackType | None,
    local_stack_only: bool = False,
) -> dict[str, typ.Any]:
    """Convert an exception to a JSON-serializable dictionary.

    This function is designed for production JSON logging. It always uses
    aliased paths (e.g., <pwd>/app.py, <site>/requests/sessions.py) and
    respects the local_stack_only flag to filter library frames.

    Args:
        exc_value: The exception instance
        traceback: The traceback object (can be None)
        local_stack_only: If True, only include frames from <pwd> (current directory)

    Returns:
        A dictionary with exception details and stack frames, including any
        chained exceptions. Structure:
        {
            "exception": "ExceptionName",
            "message": "exception message",
            "frames": [
                {
                    "module": "app.py",
                    "alias": "<pwd>",
                    "function": "function_name",
                    "lineno": 42
                },
                ...
            ],
            "chain": [  # optional, if exception has __cause__ or __context__
                {
                    "exception": "CauseName",
                    "message": "cause message",
                    "relationship": "caused_by",  # or "context"
                    "frames": [...]
                }
            ]
        }

    Example:
        >>> import sys
        >>> try:
        ...     raise ValueError("test error")
        ... except ValueError:
        ...     exc_info = sys.exc_info()
        ...     result = exc_to_json(exc_info[1], exc_info[2])
        ...     print(result["exception"])
        ValueError
    """
    tracebacks = _exc_to_traceback_list(exc_value, traceback)

    if not tracebacks:
        return {
            "exception": type(exc_value).__name__,
            "message": str(exc_value),
            "frames": [],
        }

    main_tb = tracebacks[0]
    entries = list(main_tb.entries)

    if not entries:
        result = {
            "exception": main_tb.exc_name,
            "message": main_tb.exc_msg,
            "frames": [],
        }
    else:
        ctx = fmt._init_entries_context(entries, term_width=fmt.DEFAULT_COLUMNS)
        result = _format_traceback_json(
            ctx.rows,
            main_tb.exc_name,
            main_tb.exc_msg,
            local_stack_only,
        )

    if len(tracebacks) > 1:
        chain = []
        for tb in tracebacks[1:]:
            entries = list(tb.entries)
            if not entries:
                chain_item = {
                    "exception": tb.exc_name,
                    "message": tb.exc_msg,
                    "relationship": "caused_by" if tb.is_caused else "context",
                    "frames": [],
                }
            else:
                ctx = fmt._init_entries_context(entries, term_width=fmt.DEFAULT_COLUMNS)
                chain_item = _format_traceback_json(
                    ctx.rows,
                    tb.exc_name,
                    tb.exc_msg,
                    local_stack_only,
                )
                chain_item["relationship"] = "caused_by" if tb.is_caused else "context"
            chain.append(chain_item)

        result["chain"] = chain

    return result


def _exc_to_traceback_list(
    exc_value: BaseException,
    traceback: types.TracebackType | None,
) -> list[com.Traceback]:
    """Convert exception with chaining to a list of Traceback objects.

    Handles __cause__ and __context__ chains, detecting circular references.
    """
    tracebacks: list[com.Traceback] = []
    seen_exceptions: set[int] = set()

    current_exc = exc_value
    current_tb = traceback
    is_caused = False
    is_context = False

    while current_exc is not None:
        exc_id = id(current_exc)

        if exc_id in seen_exceptions:
            break

        seen_exceptions.add(exc_id)

        entries = fmt._traceback_to_entries(current_tb) if current_tb else []

        tb_obj = com.Traceback(
            exc_name=type(current_exc).__name__,
            exc_msg=str(current_exc),
            entries=entries,
            is_caused=is_caused,
            is_context=is_context,
        )
        tracebacks.append(tb_obj)

        next_exc = None
        next_tb = None

        if current_exc.__cause__ is not None:
            next_exc = current_exc.__cause__
            next_tb = next_exc.__traceback__
            is_caused = True
            is_context = False
        elif current_exc.__context__ is not None and not current_exc.__suppress_context__:
            next_exc = current_exc.__context__
            next_tb = next_exc.__traceback__
            is_caused = False
            is_context = True

        current_exc = next_exc
        current_tb = next_tb

    return tracebacks
