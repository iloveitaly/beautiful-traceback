# This file is part of the beautiful-traceback project
# https://github.com/iloveitaly/beautiful-traceback
#
# Copyright (c) 2020-2024 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

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


def main():
    import logging
    logging.basicConfig(level="INFO")
    logger = logging.getLogger(__name__)
    logger.info("Beautiful Traceback installed!")
