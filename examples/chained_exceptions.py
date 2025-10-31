#!/usr/bin/env python3
"""
Example demonstrating beautiful-traceback with chained exceptions.

Shows how beautiful-traceback handles exception chains
(using 'raise ... from ...' and exception context).
"""

import beautiful_traceback

# Install the beautiful exception hook
beautiful_traceback.install()


def fetch_data(key):
    """Simulate fetching data that might fail."""
    data = {"user": "alice", "age": 30}

    if key not in data:
        raise KeyError(f"Key '{key}' not found in data")

    return data[key]


def process_user():
    """Process user data - demonstrates exception chaining."""
    try:
        # Try to fetch a non-existent key
        email = fetch_data("email")
        return email.upper()
    except KeyError as e:
        # Chain the exception with additional context
        raise ValueError("Failed to process user data") from e


def run_workflow():
    """Main workflow that will fail."""
    print("Starting workflow...")
    result = process_user()
    print(f"Result: {result}")


if __name__ == "__main__":
    print("Beautiful Traceback - Chained Exceptions Example")
    print("=" * 50)
    print("\nThis will show a chained exception traceback...\n")

    run_workflow()
