#!/usr/bin/env python3
"""
Threading example demonstrating beautiful-traceback with background threads.

This script shows how beautiful-traceback catches and formats exceptions
that occur in background threads, including both regular and daemon threads.
It also demonstrates JSON output for thread exceptions in production logging.
"""

import json
import sys
import threading
import time

import beautiful_traceback
from beautiful_traceback import exc_to_json

# Install the beautiful exception hook
# Note: only_tty=False allows it to work even when output is redirected
beautiful_traceback.install(only_tty=False)


def worker_task():
    """A worker thread that crashes after some work."""
    print(f"  [{threading.current_thread().name}] Starting work...")
    time.sleep(0.1)
    print(f"  [{threading.current_thread().name}] Processing data...")

    # This will cause a ValueError in the worker thread
    raise ValueError("Failed to process data in worker thread!")


def daemon_task():
    """A daemon thread that crashes."""
    print(f"  [{threading.current_thread().name}] Daemon starting...")
    time.sleep(0.1)

    # This will cause a RuntimeError in the daemon thread
    raise RuntimeError("Daemon thread encountered an error!")


def database_connection():
    """Simulates a database connection error in a thread."""
    print(f"  [{threading.current_thread().name}] Connecting to database...")
    time.sleep(0.05)

    # Simulate a connection error
    raise ConnectionError("Database connection refused on port 5432")


def json_logging_task():
    """Demonstrates JSON logging with thread metadata."""
    print(f"  [{threading.current_thread().name}] Starting API processing...")
    time.sleep(0.05)

    try:
        # Simulate an error during API processing
        raise ValueError("Invalid API response: missing 'data' field")
    except ValueError:
        # Capture exception info for JSON logging
        exc_info = sys.exc_info()

        if exc_info[1] is not None:
            # Convert to JSON with thread metadata
            json_output = exc_to_json(
                exc_info[1],
                exc_info[2],
                thread=threading.current_thread(),
                local_stack_only=True,
            )

            # In production, you'd send this to your structured logger
            print("\n  JSON output for structured logging:")
            print("  " + "-" * 46)
            print(json.dumps(json_output, indent=2))

        # Re-raise to show the beautiful terminal output too
        raise


if __name__ == "__main__":
    print("Beautiful Traceback - Threading Example")
    print("=" * 50)

    # Example 1: Regular worker thread
    print("\n1. Regular worker thread exception:")
    print("-" * 50)
    worker = threading.Thread(target=worker_task, name="Worker-1")
    worker.start()
    worker.join()

    # Example 2: Daemon thread
    print("\n2. Daemon thread exception:")
    print("-" * 50)
    daemon = threading.Thread(target=daemon_task, name="BackgroundService", daemon=True)
    daemon.start()
    daemon.join()

    # Example 3: Named thread with specific error
    print("\n3. Database connection thread:")
    print("-" * 50)
    db_thread = threading.Thread(target=database_connection, name="DB-Connection-Pool-1")
    db_thread.start()
    db_thread.join()

    # Example 4: JSON logging with thread metadata
    print("\n4. JSON logging with thread metadata:")
    print("-" * 50)
    print("  (Useful for production structured logging)")
    json_thread = threading.Thread(target=json_logging_task, name="API-Worker-3", daemon=True)
    json_thread.start()
    json_thread.join()

    print("\n" + "=" * 50)
    print("All thread exceptions have been displayed!")
    print("\nNotice how:")
    print("  - Thread names are shown in the exception header")
    print("  - Daemon threads are marked with '(daemon)'")
    print("  - Stack traces use beautiful formatting with aliases")
    print("  - JSON output includes thread metadata (name, daemon status)")
