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

### `comparison.py`
Side-by-side comparison showing the same exception with standard Python traceback vs beautiful-traceback formatting.

### `json_demo.py` 📊 JSON Formatting
Demonstrates `exc_to_json()` for converting exceptions to structured JSON:
- Simple exceptions
- Exception chains
- Using `local_stack_only` flag

```bash
uv run examples/json_demo.py
```

Perfect for production logging with structured loggers like structlog.

### `fastapi_demo.py` 🚀 FastAPI Integration
Shows how to use `exc_to_json()` in a FastAPI application for JSON logging.

**Prerequisites:**
```bash
pip install fastapi uvicorn
```

**Run:**
```bash
# Direct execution
python examples/fastapi_demo.py

# Or with uvicorn for auto-reload
uvicorn examples.fastapi_demo:app --reload
```

**Endpoints:**
- `GET /` - Root endpoint with instructions
- `GET /error` - Raises a simple KeyError
- `GET /chained-error` - Raises a chained exception
- `GET /users/{user_id}` - Returns user or raises error if not found
- `GET /local-only-error` - Compare full vs local-only tracebacks

The demo includes a global exception handler that catches all exceptions, converts them to JSON using `exc_to_json()`, and returns structured error responses.

## Features Demonstrated

- ✅ Colored, formatted output
- ✅ Path aliasing (shortens long paths)
- ✅ Call stack visualization
- ✅ Exception chaining support
- ✅ Integration with Python logging
- ✅ JSON formatting for production logging
- ✅ FastAPI integration
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

# Or use JSON formatting for production
import sys
from beautiful_traceback import exc_to_json

try:
    # your code
    pass
except Exception:
    exc_info = sys.exc_info()
    json_tb = exc_to_json(exc_info[1], exc_info[2], local_stack_only=True)
    # Pass json_tb to your structured logger
```

## Tips

- Use `beautiful_traceback.install(color=False)` to disable colors
- Use `beautiful_traceback.install(only_tty=True)` to only enable for TTY
- Use `beautiful_traceback.install(local_stack_only=True)` to only show your code (filter out library code)
