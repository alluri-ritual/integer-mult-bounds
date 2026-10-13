#!/usr/bin/env bash
# The delivery branch carries only research files on the user's existing fork.
# Reconstruct the pinned research base separately, without changing workflows.
set -euo pipefail
destination="${1:-/tmp/integer-mult-kappa}"
base=f567884aeb8851b6e794af1184119a3bfbe1e631
git fetch https://github.com/CrocSwap/integer-mult-bounds.git "$base"
git worktree add --detach "$destination" "$base"
git archive HEAD research/fork-flush-kappa | tar -x -C "$destination"
cd "$destination"
bash research/fork-flush-kappa/bootstrap.sh
