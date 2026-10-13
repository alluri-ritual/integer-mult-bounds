# Fork-and-flush kappa research pilot

Prepared for Alluri with substantial OpenAI Codex assistance. Apache-2.0.
This is research infrastructure, not a new exponent result or runtime claim.
The protected reviewed incumbent is **1661634653669567/10^18**, from Jeremy
Kothe / JointXF's #799 composed with #589 and the credited supplier chain in
`CONTRIBUTORS.md`. Base commit: `f567884aeb8851b6e794af1184119a3bfbe1e631`.

## Method and limits

Inspired by Cai et al., [Fork-and-Flush](https://arxiv.org/html/2610.07447v1):
periodically branch the retained workspace into independent fresh conversations,
evaluate the branches, keep the best, and continue it alone before branching
again. Carry files and experimental evidence, not the parent's chat transcript.
Preserve the best evaluated artifact separately from ongoing edits.

Our bounded pilot adapts this method: three branches, three rounds, and a
conditional profile score for exploration. This is not a reproduction of the
paper's benchmark or its four-branch compute schedule. A local screen cannot
certify the global construction. Only full cold admission can improve the
verified incumbent. The paper provides no promised gain on this problem.

## Portable setup

The `research/fork-flush-cloud-port` delivery branch intentionally carries only
these research files on the user's older fork baseline. Before running anything
there, use `bash research/fork-flush-kappa/start-cloud.sh`. It checks out the
pinned upstream base into `/tmp/integer-mult-kappa`, overlays this package and
bootstraps dependencies. Continue in that reconstructed checkout. This avoids
publishing unrelated upstream workflow changes through the user's OAuth token.

On a Linux Codex cloud environment with Python 3.11+, git, g++, and sudo:

```sh
bash research/fork-flush-kappa/bootstrap.sh
/tmp/kappa-venv/bin/python -B research/fork-flush-kappa/screen.py \
  --word /tmp/kappa-seed/WORD.json.gz --out /tmp/kappa-seed-screen
/tmp/kappa-venv/bin/python -B scripts/verify_frontier799.py \
  --work /tmp/kappa-baseline-cold
```

The archive seed is hash checked and extracted by member name; extracting it is
not a cold replay. The last command rebuilds the selected result. NumPy, SciPy,
SymPy and Boost match the dependencies in the repository's frontier799 CI.
The bootstrap installs current packages; record actual versions in cloud results.

## Search tools

`prepare.py` creates the protected seed. `screen.py` snapshots a proposed word,
calls unchanged independent exact scalar/frame checks, verifies its interface
and width inventory, and projects its local profile change across 72 calls.
Unchanged rational moment engines and 47 outer inequalities price that projected
profile. It explicitly returns `full_admission: false`; neither JSON claims nor
cheap operation counts promote a certified result. `PINS.json` binds the source
inputs; review/pin this package's Git commit separately. These are research
integrity checks, not an adversarial sandbox.

```sh
python3 -B research/fork-flush-kappa/round.py fork \
  --leader /tmp/kappa-seed --out /tmp/kappa-round0 --branches 3
# Launch independent researchers with empty chat contexts, one per directory.
# They keep their best candidate at branch-N/WORD.json.gz.
python3 -B research/fork-flush-kappa/round.py select \
  --incumbent /tmp/kappa-seed \
  --candidate /tmp/kappa-round0/branch-0 \
  --candidate /tmp/kappa-round0/branch-1 \
  --candidate /tmp/kappa-round0/branch-2 --out /tmp/kappa-selection0
```

Selection reruns the screen; it never trusts branch-supplied scores. It retains
the old leader on ties and rejects failed candidates. A promising profile still
needs native/phase, ownership, invoice, hosted-precision, two-supplier and outer
checks. A change outside the fixed-interface screen needs a separately reviewed
evaluator extension; do not weaken the frozen checker to make it pass.

Follow `CLOUD-TASK.txt` for the agent-driven schedule. The scripts do not start
agents themselves. Cloud best-of-N alone is not periodic fork-and-flush.
Run `python3 -B research/fork-flush-kappa/test_screen.py` for failure controls.

## Prior work to avoid repeating

Our preceding bounded heuristic tried single commuting-gate relocations within
a 32-gate window on #741 and #799, with retained, minimal and coordinate frame
variants: no gain. This is a scoped negative result, not an optimality theorem.
Read #795, #775, #799 and #815 before proposing fixed-owner, paired-read or
fixed-order frame searches. Check their current exact heads and the maintainer
ledger; overlapping work may have advanced after this package was pinned.

This pilot should change the construction or search neighborhood, not rename
the merged #799 gain. Preserve source authorship and failed experiments. A
useful negative result may be reported, but no speculative frontier PR should
be opened. Keep `upstream/`, the selected record and existing evaluators intact.
