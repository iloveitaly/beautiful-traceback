from typing import Any


def load_ipython_extension(ip: Any) -> None:  # pragma: no cover
    # prevent circular import
    from beautiful_traceback import install

    install()


def unload_ipython_extension(ip: Any) -> None:  # pragma: no cover
    from beautiful_traceback import uninstall

    uninstall()
