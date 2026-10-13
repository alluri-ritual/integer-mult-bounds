#!/usr/bin/env bash
# Codex cloud setup, run from the repository root. No credentials required.
set -euo pipefail
python3 -m venv /tmp/kappa-venv
/tmp/kappa-venv/bin/python -m pip install numpy scipy sympy
if ! printf '#include <boost/multiprecision/cpp_int.hpp>\nint main(){}\n' | g++ -x c++ - -o /tmp/kappa-boost-check; then
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends g++ libboost-dev
fi
/tmp/kappa-venv/bin/python -B research/fork-flush-kappa/prepare.py --out /tmp/kappa-seed
echo 'Use /tmp/kappa-venv/bin/python for all verification commands.'
