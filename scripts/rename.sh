#!/bin/bash
# Rename the project everywhere: display name, distribution name and import name.
#   scripts/rename.sh "New Name" new-dist new_import
# The display name alone lives in src/outcome_evals/_meta.py (NAME); change only that line for a display-only rename.
set -euo pipefail
NEW_NAME="$1"; NEW_DIST="$2"; NEW_IMPORT="$3"
git ls-files -z | xargs -0 grep -lI -e "Outcome Evals" -e "outcome-evals" -e "outcome_evals" | while read -r f; do
  sed -i.bak -e "s/Outcome Evals/${NEW_NAME}/g" -e "s/outcome-evals/${NEW_DIST}/g" -e "s/outcome_evals/${NEW_IMPORT}/g" "$f" && rm "$f.bak"
done
git mv src/outcome_evals "src/${NEW_IMPORT}"
echo "Renamed. Question ids keep their 'oe-' prefix so published ids stay stable."
