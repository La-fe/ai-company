#!/usr/bin/env bash
# Usage: git-safe-commit.sh <company_dir> <message> [tag_name] [tag_message]
# Performs a safe git commit: checks for changes before committing, optionally tags.

set -euo pipefail

COMPANY_DIR="${1:?Usage: git-safe-commit.sh <company_dir> <message> [tag_name] [tag_message]}"
MESSAGE="${2:?Usage: git-safe-commit.sh <company_dir> <message> [tag_name] [tag_message]}"
TAG_NAME="${3:-}"
TAG_MESSAGE="${4:-$MESSAGE}"

cd "$COMPANY_DIR"

if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "ERROR: $COMPANY_DIR is not a git repository"
  exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "$MESSAGE"
  echo "COMMITTED: $MESSAGE"
else
  echo "NO_CHANGES: nothing to commit"
fi

if [ -n "$TAG_NAME" ]; then
  git tag -f "$TAG_NAME" -m "$TAG_MESSAGE"
  echo "TAGGED: $TAG_NAME"
fi
