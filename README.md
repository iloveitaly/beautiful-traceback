# Beautiful Traceback

> **Note:** This is a fork of the [pretty-traceback](https://github.com/mbarkhau/pretty-traceback) repo with simplified development and improvements for better integration with FastAPI, structured logging, IPython, pytest, and more.

Human readable stacktraces for Python.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)
[![Python Versions](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Overview

Beautiful Traceback groups together what belongs together, adds coloring and alignment. All of this makes it easier for you to see patterns and filter out the signal from the noise. This tabular format is best viewed in a wide terminal.

In other words, get this 😍

```
Aliases for entries in sys.path:
    <pwd>: /Users/mike/Projects/python/beautiful-traceback/
Traceback (most recent call last):
    <pwd> examples/simple.py:77  <module>           main()
    <pwd> examples/simple.py:72  main               results = process_batch(batches)
    <pwd> examples/simple.py:48  process_batch      avg = calculate_average(batch)
    <pwd> examples/simple.py:35  calculate_average  raise ValueError("Cannot calculate average of empty list")
ValueError: Cannot calculate average of empty list
```

Instead of this 🤮

```
Traceback (most recent call last):
  File "test/test_formatting.py", line 199, in <module>
    main()
  File "test/test_formatting.py", line 190, in main
    run_pingpong()
  File "test/test_formatting.py", line 161, in run_pingpong
    sched3.run()
  File "/home/mbarkhau/miniconda3/envs/beautiful-traceback_py38/lib/python3.8/sched.py", line 151, in run
    action(*argument, **kwargs)
  File "/home/mbarkhau/miniconda3/envs/beautiful-traceback_py38/lib/python3.8/sched.py", line 151, in run
    action(*argument, **kwargs)
  File "/home/mbarkhau/miniconda3/envs/beautiful-traceback_py38/lib/python3.8/sched.py", line 151, in run
    action(*argument, **kwargs)
  File "test/test_formatting.py", line 151, in _ping
    _pong(depth + 1)
  File "test/test_formatting.py", line 129, in _pong
    _ping(depth + 1)
  File "test/test_formatting.py", line 136, in _ping
    sp.check_output(["command_that", "doesnt", "exist"])
  File "/home/mbarkhau/miniconda3/envs/beautiful-traceback_py38/lib/python3.8/subprocess.py", line 411, in check_output
    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
  File "/home/mbarkhau/miniconda3/envs/beautiful-traceback_py38/lib/python3.8/subprocess.py", line 489, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/home/mbarkhau/miniconda3/envs/beautiful-traceback_py38/lib/python3.8/subprocess.py", line 854, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/home/mbarkhau/miniconda3/envs/beautiful-traceback_py38/lib/python3.8/subprocess.py", line 1702, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'command_that'
```

If your terminal is wide enough, the long paths are preserved for better navigation.

## Installation

### Using uv (recommended)

```bash
uv add beautiful-traceback
```

### Using pip

```bash
pip install beautiful-traceback
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

## Examples

Check out the [examples](examples/) directory for more usage examples:

```bash
# Quick single-exception example
uv run examples/simple.py

# Interactive demo with multiple exception types
uv run examples/demo.py
```

## Options

Beautiful Traceback supports several configuration options:

```python
beautiful_traceback.install(
    color=True,                            # Enable colored output
    only_tty=True,                         # Only activate for TTY output
    only_hook_if_default_excepthook=True,  # Only install if default hook
    local_stack_only=False,                # Filter to show only local code
    envvar='ENABLE_BEAUTIFUL_TRACEBACK'    # Optional environment variable
)
```

## Alternatives

Beautiful Traceback is heavily inspired by the backtrace module by [nir0s](https://github.com/nir0s/backtrace) but there are many others (sorted by github stars):

- https://github.com/qix-/better-exceptions
- https://github.com/cknd/stackprinter
- https://github.com/onelivesleft/PrettyErrors
- https://github.com/skorokithakis/tbvaccine
- https://github.com/aroberge/friendly-traceback
- https://github.com/HallerPatrick/frosch
- https://github.com/nir0s/backtrace
- https://github.com/staticshock/colored-traceback.py
- https://github.com/chillaranand/ptb
- https://github.com/laurb9/rich-traceback
- https://github.com/willmcgugan/rich#tracebacks

## License

MIT License - see [LICENSE.md](LICENSE.md) for details.
