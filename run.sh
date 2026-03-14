#!/bin/bash

# Ensure virtual environment exists and activate it.
if [ -f ".venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    . .venv/bin/activate
else
    echo "Virtual environment not found. Run 'python3 -m venv .venv' first." >&2
    exit 1
fi

# Launch the FastAPI server. Using exec replaces the shell process with uvicorn.
exec uvicorn app:app --reload
