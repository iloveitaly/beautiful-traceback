import os
import typing as typ

_PREFIX = "BEAUTIFUL_TRACEBACK_"
_TRUTHY = frozenset({"1", "true", "yes", "on"})
_FALSY = frozenset({"0", "false", "no", "off"})

_config: dict[str, typ.Any] = {}


def env_bool(name: str, default: bool) -> bool:
    val = os.environ.get(_PREFIX + name, "").strip().lower()
    if val in _TRUTHY:
        return True
    if val in _FALSY:
        return False
    return default


def configure(
    local_stack_only: bool | None = None,
    exclude_patterns: typ.Sequence[str] | None = None,
) -> None:
    """Set global defaults for exc_to_json().

    Per-call arguments always override these defaults.
    """
    if local_stack_only is not None:
        _config["local_stack_only"] = local_stack_only
    if exclude_patterns is not None:
        _config["exclude_patterns"] = exclude_patterns


def get_default(key: str, fallback: typ.Any) -> typ.Any:
    return _config.get(key, fallback)
