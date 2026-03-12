#!/bin/sh
. .venv/bin/activate
uvicorn app:app --reload
