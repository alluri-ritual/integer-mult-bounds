#!/usr/bin/env python3
"""Real malformed-word controls against the unchanged independent checker."""
import copy
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from screen import HERE, ROOT, check_sources, profile_delta


def main():
    pins = check_sources()
    with tempfile.TemporaryDirectory(prefix='fork-flush-controls-') as directory:
        work = Path(directory)
        subprocess.run([sys.executable, '-B', str(HERE/'prepare.py'), '--out', str(work/'seed')], check=True)
        word = json.loads(gzip.decompress((work/'seed/WORD.json.gz').read_bytes()))
        cases = {}
        claim = copy.deepcopy(word)
        claim['report']['local_profile']['1'] -= 1
        cases['forged_cheaper_profile'] = claim
        scalar = copy.deepcopy(word)
        gate = next(g for g in scalar['B'] if g[0] == 'add')
        gate[3] += gate[4]
        cases['wrong_scalar_map'] = scalar
        frame = copy.deepcopy(word)
        gate = next(g for g in frame['B'] if g[-1])
        gate[-1] = []
        cases['illegal_frame_chain'] = frame
        for name, value in cases.items():
            path = work/(name+'.json.gz')
            path.write_bytes(gzip.compress(json.dumps(value).encode(), mtime=0))
            with (work/(name+'.log')).open('w') as log:
                result = subprocess.run([sys.executable, '-B', str(HERE/'screen.py'),
                    '--word', str(path), '--out', str(work/name)], stdout=log, stderr=subprocess.STDOUT, timeout=120)
            if result.returncode == 0 or (work/name/'SCREEN.json').exists():
                raise RuntimeError('accepted malformed candidate: '+name)
            if not (work/name/'local.log').exists():
                raise RuntimeError('control did not reach independent checker: '+name)
            print('REJECTED', name)
        wrong = dict(pins['local']['local_profile'])
        wrong['1'] -= 1
        try:
            profile_delta(pins['global_profile'], pins['local']['local_profile'], wrong)
        except ValueError as error:
            if str(error) != 'changed global rank mass':
                raise
        else:
            raise RuntimeError('accepted rank-mass loss')
        print('REJECTED changed global rank mass')
    print('PASS four failure controls; run the unmodified seed screen separately as a positive control')


if __name__ == '__main__':
    main()
