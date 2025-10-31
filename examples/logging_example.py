#!/usr/bin/env python3
"""
Example demonstrating beautiful-traceback with Python logging.

Shows how to use LoggingFormatter to get beautiful tracebacks
in your log output.
"""

import logging
import beautiful_traceback

# Create a logger with beautiful formatting
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(beautiful_traceback.LoggingFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def divide_numbers(a, b):
    """Divide two numbers."""
    return a / b


def calculate_average(numbers):
    """Calculate average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")

    total = sum(numbers)
    count = len(numbers)

    # This will fail if count is 0
    return divide_numbers(total, count)


def process_data():
    """Process some data - will log errors beautifully."""
    logger.info("Starting data processing")

    try:
        # This will succeed
        result1 = calculate_average([1, 2, 3, 4, 5])
        logger.info(f"First average: {result1}")

        # This will fail
        result2 = calculate_average([])
        logger.info(f"Second average: {result2}")

    except Exception:
        logger.exception("Error during data processing")
        raise


if __name__ == "__main__":
    print("Beautiful Traceback - Logging Example")
    print("=" * 45)
    print("\nThis will show beautiful tracebacks in log output...\n")

    process_data()
