#!/bin/bash
set -euo pipefail
CV_ROOT="$(cd -- "$(dirname -- "$0")" && pwd)"
cd "$CV_ROOT"
CV_PYTHON="${CV_PYTHON:-python3}"
"$CV_PYTHON" -c 'import sys; assert sys.version_info >= (3,11), "Python 3.11 or newer is required"'
"$CV_PYTHON" -m venv .venv-cv
.venv-cv/bin/python -m pip install -r scripts/requirements-cv.txt
CV_HOOKS=$(git config --get core.hooksPath || true)
if [[ -n "$CV_HOOKS" && "$CV_HOOKS" != '.githooks' ]]; then
  echo "Existing hooks at $CV_HOOKS. Integrate the CV hook there before changing this setting." >&2
  exit 1
fi
if [[ -z "$CV_HOOKS" && -x .git/hooks/pre-commit ]]; then
  echo 'An existing pre-commit hook needs to be combined with .githooks/pre-commit.' >&2
  exit 1
fi
git config core.hooksPath .githooks
echo 'CV generation is enabled for local commits. Push normally to publish.'
