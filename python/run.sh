#!/bin/sh
exec uv run --no-project --python '>=3.10' python "$(dirname "$0")/bf.py" "$1"
