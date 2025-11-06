# Readable Python Stack Traces

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)
[![Python Versions](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

When you're debugging a production issue at 2am, the last thing you need is hunting through walls of text trying to find the actual error. Beautiful Traceback transforms Python's default exception output into something you can actually read—colored, formatted, and organized in a tabular layout that groups related information together.

This is a fork of [pretty-traceback](https://github.com/mbarkhau/pretty-traceback) with cleaner development setup and better integration for FastAPI, [structlog](https://github.com/iloveitaly/structlog-config), IPython, and pytest. I use it in [python-starter-template](https://github.com/iloveitaly/python-starter-template) to make debugging production issues less painful.

![Comparison of standard Python traceback vs Beautiful Traceback](comparison.webp)

The tabular format works best in a wide terminal where you can see the full context at a glance.

## Installation

```bash
# Using uv (recommended)
uv add beautiful-traceback

# Using pip
pip install beautiful-traceback
```

Want to try it first? Clone and run an example:

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

Important: don't put this in `__init__.py` or any module others might import. Your users might not appreciate you messing with their traceback formatting.

If you really need to enable it in shared code, use the `envvar` gate:

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

Want beautiful tracebacks in every Python project without touching any code? Use a `.pth` file. Python executes import statements in `.pth` files at interpreter startup.

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
