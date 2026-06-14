#!/bin/sh
# Install devnull's tracked git hooks into .git/hooks.
# Re-run after cloning. Safe to run repeatedly.
set -e
repo_root=$(git rev-parse --show-toplevel)
src="$repo_root/scripts/hooks"
dst="$repo_root/.git/hooks"
for hook in "$src"/*; do
  name=$(basename "$hook")
  if [ -e "$dst/$name" ] && ! cmp -s "$hook" "$dst/$name"; then
    echo "WARNING: $dst/$name exists and differs; backing up to $dst/$name.bak"
    cp "$dst/$name" "$dst/$name.bak"
  fi
  cp "$hook" "$dst/$name"
  chmod +x "$dst/$name"
  echo "installed: $dst/$name"
done
