#!/usr/bin/env python3
"""
Basic example demonstrating beautiful-traceback.

This script shows how to install beautiful-traceback and see
formatted exceptions with colors and improved readability.
"""

import beautiful_traceback

# Install the beautiful exception hook
beautiful_traceback.install()


def level_3():
    """Deepest level - this is where the error happens."""
    # This will cause a ZeroDivisionError
    result = 42 / 0
    return result


def level_2(x):
    """Middle level - calls level_3."""
    value = level_3()
    return x + value


def level_1():
    """Top level - calls level_2."""
    data = {"name": "example", "count": 10}
    result = level_2(data["count"])
    return result


if __name__ == "__main__":
    print("Beautiful Traceback Example")
    print("=" * 40)
    print("\nAbout to trigger an exception...\n")
    
    # This will trigger a beautiful traceback
    level_1()
