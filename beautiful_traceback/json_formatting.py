"""JSON exception formatting for production logging.

This module provides exc_to_json() which converts exceptions to structured
dictionaries suitable for JSON logging in production environments.
"""

import threading
import types
import typing as typ

from beautiful_traceback.common import ExceptionTraceback
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
    exc_info: tuple[type[BaseException], BaseException, types.TracebackType | None]
    | BaseException,
    traceback: types.TracebackType | None = None,
    local_stack_only: bool = False,
    exclude_patterns: typ.Sequence[str] = (),
    thread: threading.Thread | None = None,
) -> dict[str, typ.Any]:
    """Convert an exception to a JSON-serializable dictionary for structured logging.

    Args:
        exc_info: Either a (exc_type, exc_value, traceback) tuple as returned by
            sys.exc_info(), or the exception instance directly (in which case
            traceback must be passed as the second argument).
        traceback: The traceback object. Only used when exc_info is a BaseException instance.
        local_stack_only: Only include frames from <pwd>, filtering out library frames.
        exclude_patterns: Regex patterns matched against frame paths to drop frames.
        thread: If provided, adds {"thread": {"name": ..., "daemon": ...}} to output.

    Returns:
        Dict with keys: "exception", "message", "frames". Optional keys:
        - "notes": list of strings added via exc.add_note() (Python 3.11+)
        - "syntax_error": dict of SyntaxError attributes (filename, lineno, offset, etc.)
        - "chain": list of chained exception dicts, each with a "relationship" key
          ("caused_by" for __cause__, "context" for __context__)
        - "thread": thread metadata when thread parameter is provided
    """
    if isinstance(exc_info, tuple):
        _exc_type, exc_value, traceback = exc_info
    else:
        exc_value = exc_info
    tracebacks = _exc_to_traceback_list(exc_value, traceback)

    if not tracebacks:
        result = {
            "exception": type(exc_value).__name__,
            "message": str(exc_value),
            "frames": [],
        }
        result.update(_exc_metadata(exc_value))
        if thread is not None:
            result["thread"] = {
                "name": thread.name,
                "daemon": thread.daemon,
            }
        return result

    main_tb, main_exc = tracebacks[0]
    entries = list(main_tb.stack_frames)

    if not entries:
        result = {
            "exception": main_tb.exc_name,
            "message": main_tb.exc_msg,
            "frames": [],
        }
    else:
        ctx = fmt._init_entries_context(
            entries,
            term_width=fmt.DEFAULT_COLUMNS,
            exclude_patterns=exclude_patterns,
        )
        result = _format_traceback_json(
            ctx.rows,
            main_tb.exc_name,
            main_tb.exc_msg,
            local_stack_only,
        )

    result.update(_exc_metadata(main_exc))

    if len(tracebacks) > 1:
        chain = []
        for tb, chain_exc in tracebacks[1:]:
            entries = list(tb.stack_frames)
            if not entries:
                chain_item = {
                    "exception": tb.exc_name,
                    "message": tb.exc_msg,
                    "relationship": "caused_by" if tb.is_caused else "context",
                    "frames": [],
                }
            else:
                ctx = fmt._init_entries_context(
                    entries,
                    term_width=fmt.DEFAULT_COLUMNS,
                    exclude_patterns=exclude_patterns,
                )
                chain_item = _format_traceback_json(
                    ctx.rows,
                    tb.exc_name,
                    tb.exc_msg,
                    local_stack_only,
                )
                chain_item["relationship"] = "caused_by" if tb.is_caused else "context"
            chain_item.update(_exc_metadata(chain_exc))
            chain.append(chain_item)

        result["chain"] = chain

    if thread is not None:
        result["thread"] = {
            "name": thread.name,
            "daemon": thread.daemon,
        }

    return result


def _exc_metadata(exc: BaseException) -> dict[str, typ.Any]:
    meta: dict[str, typ.Any] = {}

    notes = getattr(exc, "__notes__", None)
    if notes:
        meta["notes"] = notes

    if isinstance(exc, SyntaxError):
        meta["syntax_error"] = {
            "filename": exc.filename,
            "lineno": exc.lineno,
            "offset": exc.offset,
            "text": exc.text,
            "end_lineno": exc.end_lineno,
            "end_offset": exc.end_offset,
            "msg": exc.msg,
        }

    return meta


def _exc_to_traceback_list(
    exc_value: BaseException,
    traceback: types.TracebackType | None,
) -> list[tuple[ExceptionTraceback, BaseException]]:
    """Convert exception with chaining to a list of (Traceback, exc) pairs.

    Handles __cause__ and __context__ chains, detecting circular references.
    """
    tracebacks: list[tuple[ExceptionTraceback, BaseException]] = []
    seen_exceptions: set[int] = set()

    current_exc: BaseException | None = exc_value
    current_tb = traceback
    is_caused = False
    is_context = False

    while current_exc is not None:
        exc_id = id(current_exc)

        if exc_id in seen_exceptions:
            break

        seen_exceptions.add(exc_id)

        entries = fmt._traceback_to_entries(current_tb) if current_tb else []

        tb_obj = ExceptionTraceback(
            exc_name=type(current_exc).__name__,
            exc_msg=str(current_exc),
            stack_frames=entries,
            is_caused=is_caused,
            is_context=is_context,
        )
        tracebacks.append((tb_obj, current_exc))

        next_exc: BaseException | None = None
        next_tb = None

        if current_exc.__cause__ is not None:
            next_exc = current_exc.__cause__
            next_tb = next_exc.__traceback__
            is_caused = True
            is_context = False
        elif (
            current_exc.__context__ is not None and not current_exc.__suppress_context__
        ):
            next_exc = current_exc.__context__
            next_tb = next_exc.__traceback__
            is_caused = False
            is_context = True

        current_exc = next_exc
        current_tb = next_tb

    return tracebacks
