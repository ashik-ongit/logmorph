#!/usr/bin/env bash
rm -f "$(cd "$(dirname "$0")/.." && pwd)/data/security.db"
echo "Local runtime database removed."
