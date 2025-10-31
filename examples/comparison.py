#!/usr/bin/env python3
"""
Comparison example showing standard Python traceback vs beautiful-traceback.

This script demonstrates the same error twice:
1. First with standard Python traceback
2. Then with beautiful-traceback formatting
"""


def level_3():
    """Deepest level - this is where the error happens."""
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


def show_standard_traceback():
    """Show the standard Python traceback."""
    print("=" * 60)
    print("STANDARD PYTHON TRACEBACK")
    print("=" * 60)
    print()

    try:
        level_1()
    except Exception:
        import traceback

        traceback.print_exc()


def show_beautiful_traceback():
    """Show the beautiful-traceback version."""
    print()
    print()
    print("=" * 60)
    print("WITH BEAUTIFUL-TRACEBACK")
    print("=" * 60)
    print()

    import beautiful_traceback

    beautiful_traceback.install()

    level_1()


if __name__ == "__main__":
    print("\nComparison: Standard vs Beautiful Traceback")
    print()

    # Show standard traceback first
    show_standard_traceback()

    # Show beautiful traceback
    show_beautiful_traceback()
