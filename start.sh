#!/bin/bash
# Start the Nuclear Physics API server
set -a && source .env && set +a
uv run uvicorn main:app \
    --host "${API_HOST:-0.0.0.0}" \
    --port "${API_PORT:-8000}" \
    $([ "${API_RELOAD:-true}" = "true" ] && echo "--reload")
