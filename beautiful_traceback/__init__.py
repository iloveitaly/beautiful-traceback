from ._extension import load_ipython_extension
from .config import configure, get_config
from .formatting import LoggingFormatter, LoggingFormatterMixin
from .hook import install, uninstall
from .json_formatting import exc_to_json
from .version import __version__

# retain typo for backward compatibility
LoggingFormaterMixin = LoggingFormatterMixin

__all__ = (
    "LoggingFormaterMixin",
    "LoggingFormatter",
    "LoggingFormatterMixin",
    "__version__",
    "configure",
    "exc_to_json",
    "get_config",
    "install",
    "load_ipython_extension",
    "uninstall",
)
