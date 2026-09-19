#!/bin/bash
# Double-click in Finder, or run ./generate-cv.command [generator options].
set -euo pipefail
CV_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
if [[ ! -x "$CV_ROOT/.venv-cv/bin/python" ]]; then
  echo "First install Python 3.11 or newer, then run these commands in the website folder:"
  echo "  python3 -m venv .venv-cv"
  echo "  .venv-cv/bin/python -m pip install -r scripts/requirements-cv.txt"
  exit 1
fi
exec "$CV_ROOT/.venv-cv/bin/python" "$CV_ROOT/scripts/generate_cv.py" "$@"
