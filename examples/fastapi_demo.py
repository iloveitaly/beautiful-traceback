#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "fastapi",
#     "uvicorn",
#     "beautiful_traceback"
# ]
# ///
"""FastAPI demo showing exc_to_json for JSON logging.

Note: This demo requires beautiful-traceback to be installed locally.
Run from the project root with the project installed:
    python examples/fastapi_demo.py

Or install the project first:
    pip install -e .
    uv run examples/fastapi_demo.py

Or with uvicorn:
    uvicorn examples.fastapi_demo:app --reload

Then visit:
- http://localhost:8000/ - root endpoint
- http://localhost:8000/error - raises a simple error
- http://localhost:8000/chained-error - raises a chained error
- http://localhost:8000/users/999 - raises a not found error
- http://localhost:8000/local-only-error - compare full vs local-only tracebacks
"""

import logging
import sys

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from beautiful_traceback import exc_to_json


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)
log = logging.getLogger(__name__)

app = FastAPI(title="Beautiful Traceback JSON Demo")


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    """Global exception handler that logs exceptions as JSON."""
    exc_info = sys.exc_info()
    json_traceback = exc_to_json(exc_info[1], exc_info[2], local_stack_only=False)

    log.error("unhandled exception", extra={"traceback": json_traceback})

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "traceback": json_traceback,
        },
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Visit /error, /chained-error, or /users/999 to see error handling"
    }


@app.get("/error")
async def simple_error():
    """Endpoint that raises a simple error."""
    data = {"key": "value"}
    return data["missing_key"]


def fetch_user_from_db(user_id: int):
    """Simulate fetching user from database."""
    users = {1: "Alice", 2: "Bob", 3: "Charlie"}
    return users[user_id]


def process_user(user_id: int):
    """Process user data."""
    try:
        user = fetch_user_from_db(user_id)
        return user
    except KeyError as e:
        raise ValueError(f"User {user_id} not found in database") from e


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Endpoint that raises a chained error for missing users."""
    user = process_user(user_id)
    return {"user_id": user_id, "name": user}


@app.get("/chained-error")
async def chained_error():
    """Endpoint demonstrating exception chaining."""
    return await get_user(999)


@app.get("/local-only-error")
async def local_only_error():
    """Endpoint that shows local_stack_only filtering."""
    try:
        data = {"key": "value"}
        return data["missing_key"]
    except Exception:
        exc_info = sys.exc_info()
        json_traceback_full = exc_to_json(
            exc_info[1], exc_info[2], local_stack_only=False
        )
        json_traceback_local = exc_to_json(
            exc_info[1], exc_info[2], local_stack_only=True
        )

        return {
            "full_traceback": json_traceback_full,
            "local_only_traceback": json_traceback_local,
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
