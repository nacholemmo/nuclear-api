#!/bin/bash
# Start the Nuclear Physics API server
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
