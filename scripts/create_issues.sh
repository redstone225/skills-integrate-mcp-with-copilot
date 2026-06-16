#!/usr/bin/env bash
set -euo pipefail

# Create GitHub issues from markdown files in ./issues
# Requires: GitHub CLI (`gh`) installed and authenticated with permission to create issues.

ROOT_DIR=$(dirname "$0")/..
ISSUES_DIR="$ROOT_DIR/issues"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not found. Install GitHub CLI and authenticate (gh auth login)." >&2
  exit 1
fi

for file in "$ISSUES_DIR"/[0-9][0-9]-*.md; do
  [ -e "$file" ] || continue
  title=$(sed -n '1s/^# //p' "$file" | sed -n '1p')
  body=$(sed '1d' "$file")

  echo "Creating issue: $title"
  gh issue create --title "$title" --body "$body"
done

echo "All issue drafts processed."
