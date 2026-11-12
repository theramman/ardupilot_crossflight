#!/usr/bin/env python3
"""Read-only validation of the RadioLink CrossFlight pin/timer mapping."""
import argparse
import re
from pathlib import Path

EXPECTED = {1: 'TIMA_9', 2: 'TIMA_4', 3: 'TIMA_1', 4: 'TIMA_1',
            5: 'TIMA_1', 6: 'TIMA_1', 7: 'TIMA_4', 8: 'TIMA_4',
            9: 'TIMA_4', 10: 'TIMA_9'}


def parse(text):
    mapping = {}
    for line in text.splitlines():
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        match = re.search(r'\b(TIMA_\d+)\b\s+PWM\((\d+)\)', line)
        if match:
            timer, output = match.group(1), int(match.group(2))
            if output in mapping:
                raise ValueError(f'Duplicate PWM output {output}')
            mapping[output] = timer
    return mapping


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('hwdef', type=Path)
    args = ap.parse_args()
    mapping = parse(args.hwdef.read_text())
    print('CrossFlight PWM output timer assignments:')
    for timer in sorted(set(mapping.values())):
        print(f'  {timer}: {", ".join(str(k) for k in sorted(mapping) if mapping[k] == timer)}')
    if mapping != EXPECTED:
        print('WARNING: mapping differs from audited RadioLink Copter-4.3.7 definition')
        print('Observed:', mapping)
        raise SystemExit(1)
    print('PASS: matches audited CrossFlight PWM mapping (not a DShot capability test)')


if __name__ == '__main__':
    main()
