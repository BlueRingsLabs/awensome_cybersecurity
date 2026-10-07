#!/usr/bin/env bash
# Commit and push whatever the pipeline has produced so far.
#
#   commit-progress.sh "<label>"
#
# Called after ingestion and after every enrichment chunk, so a cancelled or
# timed-out job never loses finished work. The library is only committed if it
# passes `cyberkb check`; a push rejected because the branch moved meanwhile is
# rebased onto the new tip and retried (the pipeline only touches library/,
# catalogs and docs/audit/, so a conflict means a human edited the same file and
# must stop the job loudly rather than be resolved by a script).
set -euo pipefail

label="${1:?usage: commit-progress.sh <label>}"
branch="${GITHUB_REF_NAME:?GITHUB_REF_NAME is not set}"

if ! uv run cyberkb check > /dev/null; then
  echo "::error::cyberkb check failed after ${label}; refusing to commit an invalid library."
  uv run cyberkb check || true
  exit 1
fi

git add -A
if git diff --cached --quiet; then
  echo "Nothing to commit after ${label}."
  exit 0
fi
git commit -q -m "chore(library): ingest, enrich and regenerate catalogs (${label}) [skip ci]"

for attempt in 1 2 3; do
  if git push -q origin "HEAD:${branch}"; then
    echo "Committed and pushed progress after ${label}."
    exit 0
  fi
  echo "::warning::push rejected (attempt ${attempt}); rebasing onto origin/${branch}."
  git pull -q --rebase origin "${branch}"
done
echo "::error::could not push progress after ${label}."
exit 1
