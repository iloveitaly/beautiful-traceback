"""Common data structures and constants for beautiful-traceback.

This module provides an Internal Representation (IR) used to normalize Python's
complex exception graph into a simplified, flat format suitable for both
text and JSON rendering.

These structures:
1. Prevent circular imports between formatting modules.
2. Bundle exceptions with their specific traceback entries.
3. Flatten recursive exception chains (__cause__, __context__) into linear lists.
"""

import typing as typ


class StackFrameEntry(typ.NamedTuple):
    """A normalized stack frame.

    Attributes:
        module: The path to the source file.
        call: The name of the function or scope.
        lineno: The line number as a string.
        src_ctx: The source code line content.
    """

    module: str
    call: str
    lineno: str
    src_ctx: str


StackFrameEntryList = typ.List[StackFrameEntry]


class ExceptionTraceback(typ.NamedTuple):
    """A normalized representation of a single exception and its stack.

    This bundles the exception metadata with its specific traceback entries,
    and explicitly marks its relationship to other exceptions in a chain.

    Attributes:
        exc_name: The class name of the exception.
        exc_msg: The string representation of the exception.
        stack_frames: A list of stack frames.
        is_caused: True if this exception was the direct cause (__cause__).
        is_context: True if this exception occurred during handling (__context__).
    """

    exc_name: str
    exc_msg: str
    stack_frames: StackFrameEntryList

    is_caused: bool
    is_context: bool


ExceptionTracebackList = typ.List[ExceptionTraceback]

# Standard headers used across different renderers
ALIASES_HEAD = "Aliases for entries in sys.path:"
"Header shown before the list of path aliases."

TRACEBACK_HEAD = "Traceback (most recent call last):"
"Standard Python header for a traceback."

CAUSE_HEAD = "The above exception was the direct cause of the following exception:"
"Header shown when an exception has an explicit __cause__."

CONTEXT_HEAD = "During handling of the above exception, another exception occurred:"
"Header shown when an exception has an implicit __context__."
