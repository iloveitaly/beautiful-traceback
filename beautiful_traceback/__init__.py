from .hook import install
from .hook import uninstall
from .formatting import LoggingFormatter
from .formatting import LoggingFormatterMixin
from .json_formatting import exc_to_json

from ._extension import load_ipython_extension  # noqa: F401

__version__ = "0.2.0"


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
