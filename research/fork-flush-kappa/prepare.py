#!/usr/bin/env python3
"""Extract only a hash-pinned seed word; never unpack the full evidence archive."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import tarfile
from screen import ROOT, check_sources, require


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    pins = check_sources()
    require(not args.out.exists(), 'use a fresh output directory')
    with tarfile.open(ROOT / pins['seed_archive'], 'r:gz') as archive:
        data = archive.extractfile(pins['seed_member']).read()
    raw = gzip.decompress(data)
    require(hashlib.sha256(raw).hexdigest() == pins['word_content_sha256'], 'seed word mismatch')
    args.out.mkdir(parents=True)
    (args.out / 'WORD.json.gz').write_bytes(gzip.compress(raw, mtime=0))
    (args.out / 'INCUMBENT.json').write_text(json.dumps(dict(
        kappa=pins['kappa'], source_commit=pins['base_commit'],
        word_content_sha256=pins['word_content_sha256'],
        source='maintainer-reviewed committed evidence; this extraction is not a cold replay'), indent=2)+'\n')
    print(args.out / 'WORD.json.gz')


if __name__ == '__main__':
    main()
