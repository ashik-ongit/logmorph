#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -q -r requirements.txt
python -m app.seed >/dev/null
uvicorn app.main:app --reload --port 8000
