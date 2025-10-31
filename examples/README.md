# Beautiful Traceback Examples

This directory contains example scripts demonstrating how to use beautiful-traceback.

## Running the Examples

All examples are standalone scripts using [uv](https://github.com/astral-sh/uv)'s inline script metadata. You can run them directly:

```bash
# Quick single-exception example
uv run examples/simple.py

# Interactive demo with multiple exception types
uv run examples/demo.py

# Traditional examples (require project to be installed)
python examples/basic_example.py
python examples/chained_exceptions.py
python examples/logging_example.py
```

## Examples

### `simple.py` ⭐ Start Here!
A quick, standalone example showing a single exception with beautiful formatting. Perfect for getting started.

```bash
uv run examples/simple.py
```

### `demo.py` 🎨 Interactive Demo
An interactive demo that shows 6 different types of exceptions:
1. Simple exception with call stack
2. Chained exception (using `raise ... from`)
3. Nested exception with context
4. AttributeError
5. TypeError
6. IndexError

```bash
uv run examples/demo.py
```

Press Enter between examples to see each one.

### `basic_example.py`
Shows basic installation and a simple multi-level call stack with a `ZeroDivisionError`.

### `chained_exceptions.py`
Demonstrates how beautiful-traceback handles exception chaining (both `raise ... from` and exception context).

### `logging_example.py`
Shows how to use `LoggingFormatter` to get beautiful tracebacks in your Python logging output.

## Features Demonstrated

- ✅ Colored, formatted output
- ✅ Path aliasing (shortens long paths)
- ✅ Call stack visualization
- ✅ Exception chaining support
- ✅ Integration with Python logging
- ✅ IPython/Jupyter support (via `_extension.py`)
- ✅ Pytest plugin support

## Installation

For your own projects:

```python
import beautiful_traceback

# Install globally for all exceptions
beautiful_traceback.install()

# Or use with logging
import logging
handler = logging.StreamHandler()
handler.setFormatter(beautiful_traceback.LoggingFormatter())
logger.addHandler(handler)
```

## Tips

- Use `beautiful_traceback.install(color=False)` to disable colors
- Use `beautiful_traceback.install(only_tty=True)` to only enable for TTY
- Use `beautiful_traceback.install(local_stack_only=True)` to only show your code (filter out library code)
