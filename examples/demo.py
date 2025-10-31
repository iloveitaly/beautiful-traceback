#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "colorama>=0.4.6",
# ]
# ///
"""
Beautiful Traceback Demo

Run this script to see beautiful-traceback in action!
It will show several different types of exceptions with
formatted, colored output.

Usage:
    uv run examples/demo.py
    # or
    python examples/demo.py

Note: This script assumes beautiful-traceback is installed in the
current project or available in the Python path.
"""

import sys

# Add parent directory to path to import beautiful_traceback during development
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import beautiful_traceback

# Install the beautiful exception hook
beautiful_traceback.install()


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def demo_simple_exception():
    """Demonstrate a simple exception with a call stack."""
    print_section("1. Simple Exception (ZeroDivisionError)")
    
    def level_3():
        result = 42 / 0
        return result
    
    def level_2(x):
        value = level_3()
        return x + value
    
    def level_1():
        data = {"name": "example", "count": 10}
        result = level_2(data["count"])
        return result
    
    level_1()


def demo_chained_exception():
    """Demonstrate chained exceptions."""
    print_section("2. Chained Exception (with 'from')")
    
    def fetch_data(key):
        data = {"user": "alice", "age": 30}
        if key not in data:
            raise KeyError(f"Key '{key}' not found")
        return data[key]
    
    def process_user():
        try:
            email = fetch_data("email")
            return email.upper()
        except KeyError as e:
            raise ValueError("Failed to process user data") from e
    
    process_user()


def demo_nested_exception():
    """Demonstrate nested exceptions with context."""
    print_section("3. Nested Exception (with context)")
    
    def parse_config(config_str):
        import json
        return json.loads(config_str)
    
    def load_settings():
        invalid_json = '{"name": "test", "value": 123'  # Missing closing brace
        try:
            settings = parse_config(invalid_json)
            return settings
        except:
            # This will show both exceptions
            raise RuntimeError("Configuration loading failed")
    
    load_settings()


def demo_attribute_error():
    """Demonstrate AttributeError."""
    print_section("4. Attribute Error")
    
    class User:
        def __init__(self, name):
            self.name = name
    
    user = User("Alice")
    # This will fail - no 'email' attribute
    email = user.email
    return email


def demo_type_error():
    """Demonstrate TypeError."""
    print_section("5. Type Error")
    
    def calculate(x, y, z):
        return (x + y) * z
    
    # Wrong number of arguments
    result = calculate(10, 20)
    return result


def demo_index_error():
    """Demonstrate IndexError."""
    print_section("6. Index Error")
    
    items = ["apple", "banana", "cherry"]
    print(f"Items: {items}")
    
    # This will fail
    item = items[10]
    return item


def main():
    """Run all demos."""
    print("\n" + "🌈" * 30)
    print("  BEAUTIFUL TRACEBACK DEMO")
    print("🌈" * 30)
    print("\nThis demo will show 6 different types of exceptions")
    print("formatted with beautiful-traceback.\n")
    print("Press Ctrl+C to exit at any time.\n")
    
    demos = [
        demo_simple_exception,
        demo_chained_exception,
        demo_nested_exception,
        demo_attribute_error,
        demo_type_error,
        demo_index_error,
    ]
    
    for i, demo in enumerate(demos, 1):
        try:
            demo()
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            sys.exit(0)
        except Exception:
            # The beautiful exception will be shown
            if i < len(demos):
                input("\n\nPress Enter to continue to the next example...")
            else:
                print("\n\n" + "=" * 60)
                print("  Demo Complete!")
                print("=" * 60)
                print("\nThank you for trying beautiful-traceback! 🎉\n")


if __name__ == "__main__":
    main()
