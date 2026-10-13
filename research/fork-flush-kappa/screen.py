#!/usr/bin/env python3
"""Frozen local-word screen. A projected kappa is NOT an admitted construction."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from fractions import Fraction

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACKAGE = ROOT / 'research/gauge44-frames-x'


def require(value, message):
    if not value:
        raise ValueError(message)


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def check_sources():
    pins = json.loads((HERE / 'PINS.json').read_text())
    for name, expected in pins['sha256'].items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected,
                'changed evaluator input: ' + name)
    return pins


def profile_delta(current, old, new):
    result = {int(k): v for k, v in current.items()}
    for sign, profile in ((-1, old), (1, new)):
        for rank, count in profile.items():
            require(type(count) is int and count >= 0, 'invalid count')
            r = int(rank)
            require(r > 0, 'invalid rank')
            result[r] = result.get(r, 0) + sign * 72 * count
    require(all(v >= 0 for v in result.values()), 'negative projected count')
    require(sum(r * n for r, n in result.items()) == 520704, 'changed global rank mass')
    return {str(r): n for r, n in sorted(result.items()) if n}


def run(word, output):
    require(not sys.flags.optimize, 'assertions must remain enabled')
    pins = check_sources()
    require(not output.exists(), 'use a fresh output directory')
    output.mkdir(parents=True)
    # Snapshot the actual submission, not a path that the search may overwrite.
    raw = gzip.decompress(word.read_bytes())
    candidate = output / 'WORD.json.gz'
    candidate.write_bytes(gzip.compress(raw, mtime=0))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    for key in ('WITNESS_DISCOVER', 'WITNESS_RECORD', 'XPARAM', 'EXTRAH', 'PAIRING_RANKS', 'DIAG', 'HYBBUDGET', 'PR635_CODE'):
        env.pop(key, None)

    def command(label, args):
        with (output / (label + '.log')).open('w') as log:
            subprocess.run([sys.executable, '-B', *map(str, args)], cwd=ROOT,
                           env=env, stdout=log, stderr=subprocess.STDOUT, check=True,
                           timeout=600)

    command('local', [PACKAGE / 'independent/audit_local.py', '--main', ROOT,
                      '--word', candidate, '--output', output / 'LOCAL.json'])
    local = json.loads((output / 'LOCAL.json').read_text())
    baseline = pins['local']
    for field in ('v', 'h', 'R', 'entering', 'lowends', 'coldends', 'width_inventory'):
        require(local[field] == baseline[field], 'outside fixed-interface screen: ' + field)
    projected = profile_delta(pins['global_profile'], baseline['local_profile'], local['local_profile'])
    write(output / 'PROFILE.json', projected)
    command('price', [PACKAGE / 'independent/price_profile.py', '--main', ROOT,
                      '--profile', output / 'PROFILE.json', '--output', output / 'PRICE.json'])
    price = json.loads((output / 'PRICE.json').read_text())
    kappa = price['prices']['native']['outer_with_bit']['kappa']
    result = dict(status='LOCAL_PASS_PROJECTED_ONLY', word_content_sha256=hashlib.sha256(raw).hexdigest(),
                  projected_kappa=kappa, baseline_kappa=pins['kappa'],
                  projected_improvement=Fraction(kappa) > Fraction(pins['kappa']),
                  verified_incumbent_kappa=pins['kappa'], full_admission=False,
                  local_profile=local['local_profile'], global_profile=projected,
                  scope='Exact local scalar/frame checks and conditional all72 profile pricing only. Native phases, physical ownership, full invoice, hosted precision and cold composition must be rebuilt independently before claiming a new kappa.')
    write(output / 'SCREEN.json', result)
    print(json.dumps(result, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--word', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    run(args.word.resolve(), args.out.resolve())


if __name__ == '__main__':
    main()
