from ._extension import load_ipython_extension  # noqa: F401
from .formatting import LoggingFormatter, LoggingFormatterMixin
from .hook import install, uninstall
from .json_formatting import exc_to_json

# retain typo for backward compatibility
LoggingFormaterMixin = LoggingFormatterMixin


__all__ = [
    "install",
    "uninstall",
    "__version__",
    "LoggingFormatter",
    "LoggingFormatterMixin",
    "LoggingFormaterMixin",
    "exc_to_json",
]
