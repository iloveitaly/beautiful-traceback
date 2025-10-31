# Beautiful Traceback

> **Note:** This is a fork of the [pretty-traceback](https://github.com/mbarkhau/pretty-traceback) repo with simplified development and improvements for better integration with FastAPI, [structlog](https://github.com/iloveitaly/structlog-config), IPython, pytest, and more. This project is used in [python-starter-template](https://github.com/iloveitaly/python-starter-template) to provide better debugging experience in production environments.

Human readable stacktraces for Python.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)
[![Python Versions](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Quick Start

The fastest way to see it in action:

```bash
# Clone and run an example
git clone https://github.com/iloveitaly/beautiful-traceback
cd beautiful-traceback
uv run examples/simple.py
```

## Overview

Beautiful Traceback groups together what belongs together, adds coloring and alignment. All of this makes it easier for you to see patterns and filter out the signal from the noise. This tabular format is best viewed in a wide terminal.

![Comparison of standard Python traceback vs Beautiful Traceback](comparison.webp)

## Installation

### From PyPI (when published)

```bash
# Using uv (recommended)
uv add beautiful-traceback

# Using pip
pip install beautiful-traceback
```

### Development Installation

To install from source:

```bash
git clone https://github.com/iloveitaly/beautiful-traceback
cd beautiful-traceback
uv sync
```

Run examples:
```bash
uv run examples/simple.py
```

Run tests:
```bash
uv run pytest
```

## Usage

Add the following to your `__main__.py` or the equivalent module which is your entry point.

```python
try:
    import beautiful_traceback
    beautiful_traceback.install()
except ImportError:
    pass    # no need to fail because of missing dev dependency
```

Please do not add this code e.g. to your `__init__.py` or any other module that your users may import. They may not want you to mess with how their tracebacks are printed.

If you do feel the overwhelming desire to import the `beautiful_traceback` in code that others might import, consider using the `envvar` argument, which will cause the install function to effectively be a noop unless you set `ENABLE_BEAUTIFUL_TRACEBACK=1`.

```python
try:
    import beautiful_traceback
    beautiful_traceback.install(envvar='ENABLE_BEAUTIFUL_TRACEBACK')
except ImportError:
    pass    # no need to fail because of missing dev dependency
```

Note, that the hook is only installed if the existing hook is the default. Any existing hooks that were installed before the call of `beautiful_traceback.install` will be left in place.

## LoggingFormatter

A `logging.Formatter` subclass is also available (e.g. for integration with Flask, FastAPI, etc).

```python
import os
from flask.logging import default_handler

try:
    if os.getenv('FLASK_DEBUG') == "1":
        import beautiful_traceback
        default_handler.setFormatter(beautiful_traceback.LoggingFormatter())
except ImportError:
    pass    # no need to fail because of missing dev dependency
```

## IPython and Jupyter Integration

Beautiful Traceback works seamlessly in IPython and Jupyter notebooks:

```python
# Load the extension
%load_ext beautiful_traceback

# Unload if needed
%unload_ext beautiful_traceback
```

The extension automatically installs beautiful tracebacks for your interactive session.

## Pytest Integration

Beautiful Traceback includes a pytest plugin that automatically enhances test failure output.

### Automatic Activation

The plugin activates automatically when `beautiful-traceback` is installed. No configuration needed!

### Configuration Options

Customize the plugin in your `pytest.ini` or `pyproject.toml`:

```toml
[tool.pytest.ini_options]
enable_beautiful_traceback = true                    # Enable/disable the plugin
enable_beautiful_traceback_local_stack_only = true   # Show only local code (filter libraries)
```

Or in `pytest.ini`:

```ini
[pytest]
enable_beautiful_traceback = true
enable_beautiful_traceback_local_stack_only = true
```

## Examples

Check out the [examples/](examples/) directory for detailed usage examples including basic usage, exception chaining, logging integration, and more.

```bash
# Quick single-exception example
uv run examples/simple.py

# Interactive demo with multiple exception types
uv run examples/demo.py
```

## Configuration

### Installation Options

Beautiful Traceback supports several configuration options:

```python
beautiful_traceback.install(
    color=True,                            # Enable colored output
    only_tty=True,                         # Only activate for TTY output
    only_hook_if_default_excepthook=True,  # Only install if default hook
    local_stack_only=False,                # Filter to show only local code
    envvar='ENABLE_BEAUTIFUL_TRACEBACK'    # Optional environment variable gate
)
```

### Environment Variables

- **`NO_COLOR`** - Disables colored output when set (respects [no-color.org](https://no-color.org) standard)
- **`ENABLE_BEAUTIFUL_TRACEBACK`** - Controls activation when using the `envvar` parameter (set to `1` to enable)

### LoggingFormatterMixin

For more advanced logging integration, you can use `LoggingFormatterMixin` as a base class:

```python
import logging
import beautiful_traceback

class MyFormatter(beautiful_traceback.LoggingFormatterMixin, logging.Formatter):
    def __init__(self):
        super().__init__(fmt='%(levelname)s: %(message)s')
```

This gives you full control over the log format while adding beautiful traceback support.

## Global Installation via PTH File

You can enable beautiful-traceback across all Python projects without modifying any source code by using a `.pth` file. Python automatically executes import statements in `.pth` files during interpreter startup, making this perfect for development environments.

Add this function to your `.zshrc` or `.bashrc`:

```bash
# Create a file to automatically import beautiful-traceback on startup
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

After sourcing your shell config, run `python-inject-beautiful-traceback` to enable beautiful tracebacks globally for that Python environment.

## Alternatives

Beautiful Traceback is heavily inspired by the backtrace module by [nir0s](https://github.com/nir0s/backtrace) but there are many others (sorted by github stars):

- https://github.com/qix-/better-exceptions
- https://github.com/cknd/stackprinter
- https://github.com/onelivesleft/PrettyErrors
- https://github.com/skorokithakis/tbvaccine
- https://github.com/aroberge/friendly-traceback
- https://github.com/HallerPatrick/frosch
- https://github.com/nir0s/backtrace
- https://github.com/mbarkhau/pretty-traceback
- https://github.com/staticshock/colored-traceback.py
- https://github.com/chillaranand/ptb
- https://github.com/laurb9/rich-traceback
- https://github.com/willmcgugan/rich#tracebacks

## License

MIT License - see [LICENSE.md](LICENSE.md) for details.
