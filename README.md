# Readable Python Stack Traces

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)
[![Python Versions](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Beautiful Traceback transforms Python's default exception output into a readable tabular format with colors and better organization. Instead of hunting through walls of text, you get module names, function calls, line numbers, and code context grouped together in columns.

> [!NOTE]
> This is a fork of [pretty-traceback](https://github.com/mbarkhau/pretty-traceback) with cleaner development setup and better integration for FastAPI, [structlog](https://github.com/iloveitaly/structlog-config), IPython, and pytest. Used in [python-starter-template](https://github.com/iloveitaly/python-starter-template).

![Comparison of standard Python traceback vs Beautiful Traceback](comparison.webp)

The tabular format works best in a wide terminal where you can see the full context at a glance.

## Installation

```bash
# Using uv (recommended)
uv add beautiful-traceback

# Using pip
pip install beautiful-traceback
```

To run an example:

```bash
git clone https://github.com/iloveitaly/beautiful-traceback
cd beautiful-traceback
uv run examples/simple.py
```

## Usage

Drop this into your `__main__.py` or entry point:

```python
try:
    import beautiful_traceback
    beautiful_traceback.install()
except ImportError:
    pass
```

Don't add this to `__init__.py` or any module that others might import—it modifies global exception handling.

To enable it conditionally in shared code, use the `envvar` parameter:

```python
try:
    import beautiful_traceback
    beautiful_traceback.install(envvar='ENABLE_BEAUTIFUL_TRACEBACK')
except ImportError:
    pass
```

Now it only activates when `ENABLE_BEAUTIFUL_TRACEBACK=1` is set. The hook respects any existing custom excepthooks—it only installs if you're using Python's default.

## Features

- Tabular layout groups module names, function calls, line numbers, and code context together
- Color-coded output makes different elements easy to distinguish (respects NO_COLOR standard)
- Local stack filtering to hide library internals and focus on your code
- Automatic pytest integration—just install and your test failures become readable
- IPython and Jupyter notebook support via `%load_ext beautiful_traceback`
- Logging integration for FastAPI, Flask, and other frameworks
- Smart TTY detection—only activates in terminals, not in CI logs or piped output
- Zero dependencies except colorama

## Framework Integration

### Logging (Flask, FastAPI, etc.)

Use `LoggingFormatter` to integrate with any framework using Python's logging:

```python
import os
from flask.logging import default_handler

try:
    if os.getenv('FLASK_DEBUG') == "1":
        import beautiful_traceback
        default_handler.setFormatter(beautiful_traceback.LoggingFormatter())
except ImportError:
    pass
```

### IPython and Jupyter

Works in notebooks and IPython REPL:

```python
%load_ext beautiful_traceback
%unload_ext beautiful_traceback  # if you need to turn it off
```

### Pytest

The pytest plugin activates automatically when beautiful-traceback is installed. Configure it in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
enable_beautiful_traceback = true
enable_beautiful_traceback_local_stack_only = true  # hide library internals
```

Or `pytest.ini`:

```ini
[pytest]
enable_beautiful_traceback = true
enable_beautiful_traceback_local_stack_only = true
```

## Configuration

Customize the install call:

```python
beautiful_traceback.install(
    color=True,                            # colored output
    only_tty=True,                         # only activate in terminals
    only_hook_if_default_excepthook=True,  # respect existing hooks
    local_stack_only=False,                # hide library frames
    envvar='ENABLE_BEAUTIFUL_TRACEBACK'    # environment variable gate
)
```

Environment variables:

- `NO_COLOR` - Disables colors ([no-color.org](https://no-color.org) standard)
- `ENABLE_BEAUTIFUL_TRACEBACK` - Set to `1` to enable when using `envvar` parameter

For custom logging formatters, use `LoggingFormatterMixin`:

```python
import logging
import beautiful_traceback

class MyFormatter(beautiful_traceback.LoggingFormatterMixin, logging.Formatter):
    def __init__(self):
        super().__init__(fmt='%(levelname)s: %(message)s')
```

## Global Setup via PTH File

To enable beautiful tracebacks globally across all Python projects, use a `.pth` file. Python executes import statements in `.pth` files at interpreter startup.

Add this to `.zshrc` or `.bashrc`:

```bash
python-inject-beautiful-traceback() {
  local site_packages=$(python -c "import site; print(site.getsitepackages()[0])")
  local pth_file=$site_packages/beautiful_traceback_injection.pth
  local py_file=$site_packages/_beautiful_traceback_injection.py

  cat <<'EOF' >"$py_file"
def run_startup_script():
  try:
    import beautiful_traceback
    beautiful_traceback.install()
  except ImportError:
    pass

run_startup_script()
EOF

  echo "import _beautiful_traceback_injection" >"$pth_file"
  echo "Beautiful traceback injection created: $pth_file"
}
```

Source your shell config, then run `python-inject-beautiful-traceback`.

## Alternatives

Heavily inspired by [backtrace](https://github.com/nir0s/backtrace). Other similar tools:

- [better-exceptions](https://github.com/qix-/better-exceptions)
- [stackprinter](https://github.com/cknd/stackprinter)
- [PrettyErrors](https://github.com/onelivesleft/PrettyErrors)
- [tbvaccine](https://github.com/skorokithakis/tbvaccine)
- [friendly-traceback](https://github.com/aroberge/friendly-traceback)
- [frosch](https://github.com/HallerPatrick/frosch)
- [pretty-traceback](https://github.com/mbarkhau/pretty-traceback)
- [rich tracebacks](https://github.com/willmcgugan/rich#tracebacks)
- [colored-traceback.py](https://github.com/staticshock/colored-traceback.py)
- [ptb](https://github.com/chillaranand/ptb)
- [rich-traceback](https://github.com/laurb9/rich-traceback)

[MIT License](LICENSE.md)
