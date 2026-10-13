#!/usr/bin/env python3
"""Isolate inherited files, or independently rescreen and retain the best word."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import shutil
from screen import run, require, write


def fork(leader, output, count):
    require(2 <= count <= 4, 'choose 2 to 4 branches')
    require(not output.exists(), 'fresh round directory required')
    require(not output.resolve().is_relative_to(leader.resolve()), 'round must be outside leader')
    require((leader / 'WORD.json.gz').is_file(), 'leader must contain WORD.json.gz')
    output.mkdir(parents=True)
    for i in range(count):
        shutil.copytree(leader, output / ('branch-' + str(i)), symlinks=False)
    write(output / 'ROUND.json', dict(leader=str(leader.resolve()), branches=count,
          context_requirement='Start a NEW researcher with empty conversation for each branch. This file-copy tool does not launch agents or clear contexts.'))


def select(incumbent, candidates, output):
    require(not output.exists(), 'fresh selection directory required')
    for path in [incumbent, *candidates]:
        require(not output.resolve().is_relative_to(path.resolve()), 'selection must be outside candidates')
    output.mkdir(parents=True)
    rows = []
    best = None
    winner = incumbent
    for i, path in enumerate([incumbent, *candidates]):
        try:
            result = run(path / 'WORD.json.gz', output / ('check-' + str(i)))
            value = Fraction(result['projected_kappa'])
            rows.append(dict(path=str(path), result=result))
            # Incumbent wins ties. A broken branch never replaces it.
            if best is None or value > best:
                best, winner = value, path
        except Exception as error:
            if i == 0:
                raise RuntimeError('incumbent failed; stop selection') from error
            rows.append(dict(path=str(path), rejected=str(error)))
    shutil.copytree(winner, output / 'leader')
    write(output / 'SELECTION.json', dict(winner=str(winner), projected_kappa=str(best),
          full_admission=False, evaluations=rows,
          scope='Selection for further research by local checks and projected pricing, not a certified frontier promotion.'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    branch = commands.add_parser('fork')
    branch.add_argument('--leader', type=Path, required=True)
    branch.add_argument('--out', type=Path, required=True)
    branch.add_argument('--branches', type=int, default=3)
    choose = commands.add_parser('select')
    choose.add_argument('--incumbent', type=Path, required=True)
    choose.add_argument('--candidate', type=Path, action='append', default=[])
    choose.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'fork':
        fork(args.leader, args.out, args.branches)
    else:
        select(args.incumbent, args.candidate, args.out)


if __name__ == '__main__':
    main()
