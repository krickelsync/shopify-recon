#!/usr/bin/env bash
# auto-sync.sh — Auto-commit + push the shopify-recon toolkit to GitHub.
#
# Runs non-interactively. Stages tracked tool changes, commits with a
# timestamped message (or a message passed as $1), and pushes to origin/main.
# Safe to run from cron: if there are no changes, it exits quietly (0).
#
# AUTH: relies on git credential store (~/.git-credentials) being populated
# once via setup-github-auth.sh. No token is ever printed or committed.
#
# Usage:
#   ./auto-sync.sh                 # auto timestamped commit message
#   ./auto-sync.sh "fix: blah"     # custom commit message

set -euo pipefail

REPO_DIR="/home/ubuntu/tools"
cd "$REPO_DIR"

# Only operate inside the git repo
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repo: $REPO_DIR" >&2
  exit 1
fi

# Stage everything that isn't gitignored (clone artifacts/secrets are excluded
# by .gitignore already).
git add -A

# Nothing to commit? exit quietly so cron stays silent.
if git diff --cached --quiet; then
  echo "auto-sync: no changes to commit"
  exit 0
fi

# Build commit message
MSG="${1:-}"
if [ -z "$MSG" ]; then
  CHANGED=$(git diff --cached --name-only | tr '\n' ' ')
  MSG="chore: auto-sync $(date -u +%Y-%m-%dT%H:%MZ) — ${CHANGED}"
fi

git commit -m "$MSG"

# Push. If auth isn't set up, this fails loudly so the problem is visible.
if git push origin main; then
  echo "auto-sync: pushed to origin/main"
else
  echo "auto-sync: PUSH FAILED — run setup-github-auth.sh once to store a token" >&2
  exit 2
fi
