#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "colorama>=0.4.6",
# ]
# ///
"""
Beautiful Traceback - Quick Example

A simple, standalone example showing beautiful-traceback in action.

Usage:
    uv run examples/simple.py

Note: This script assumes beautiful-traceback is installed in the
current project or available in the Python path.
"""

import sys
from pathlib import Path

# Add parent directory to path to import beautiful_traceback during development
sys.path.insert(0, str(Path(__file__).parent.parent))

import beautiful_traceback

# Install the beautiful exception hook
beautiful_traceback.install()


def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    
    total = sum(numbers)
    count = len(numbers)
    return total / count


def process_batch(batches):
    """Process multiple batches of numbers."""
    results = []
    
    for i, batch in enumerate(batches):
        print(f"Processing batch {i + 1}...")
        avg = calculate_average(batch)
        results.append(avg)
        print(f"  Average: {avg}")
    
    return results


def main():
    """Run the example."""
    print("=" * 60)
    print("  Beautiful Traceback - Simple Example")
    print("=" * 60)
    print()
    print("Processing some data that will cause an error...")
    print()
    
    # This will work fine
    batches = [
        [10, 20, 30],
        [5, 15, 25, 35],
        [],  # This will cause an error!
        [100, 200],
    ]
    
    results = process_batch(batches)
    print(f"\nResults: {results}")


if __name__ == "__main__":
    main()
