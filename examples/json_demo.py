#!/usr/bin/env -S uv run --script

"""Demo of exc_to_json for JSON logging."""

import json
import sys

from beautiful_traceback import exc_to_json


def process_user_data(user_id):
    """Simulate processing user data."""
    users = {"alice": 1, "bob": 2}
    return users[user_id]


def handle_request(user_id):
    """Simulate handling a request."""
    try:
        result = process_user_data(user_id)
        return result
    except KeyError as e:
        raise ValueError(f"User '{user_id}' not found") from e


def main():
    print("=== Simple Exception ===")
    try:
        raise ValueError("Something went wrong")
    except ValueError:
        exc_info = sys.exc_info()
        result = exc_to_json(exc_info[1], exc_info[2])
        print(json.dumps(result, indent=2))

    print("\n=== Exception Chain ===")
    try:
        handle_request("charlie")
    except ValueError:
        exc_info = sys.exc_info()
        result = exc_to_json(exc_info[1], exc_info[2])
        print(json.dumps(result, indent=2))

    print("\n=== With local_stack_only=True ===")
    try:
        handle_request("charlie")
    except ValueError:
        exc_info = sys.exc_info()
        result = exc_to_json(exc_info[1], exc_info[2], local_stack_only=True)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
