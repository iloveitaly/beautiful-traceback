from .hook import install
from .hook import uninstall
from .formatting import LoggingFormatter
from .formatting import LoggingFormatterMixin

from ._extension import load_ipython_extension  # noqa: F401

__version__ = "0.1.0"


# retain typo for backward compatibility
LoggingFormaterMixin = LoggingFormatterMixin


__all__ = [
    "install",
    "uninstall",
    "__version__",
    "LoggingFormatter",
    "LoggingFormatterMixin",
    "LoggingFormaterMixin",
]
