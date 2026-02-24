import os

_PREFIX = "BEAUTIFUL_TRACEBACK_"
_TRUTHY = frozenset({"1", "true", "yes", "on"})
_FALSY = frozenset({"0", "false", "no", "off"})


def env_bool(name: str, default: bool) -> bool:
    val = os.environ.get(_PREFIX + name, "").strip().lower()
    if val in _TRUTHY:
        return True
    if val in _FALSY:
        return False
    return default
