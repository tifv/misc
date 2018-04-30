#!/usr/bin/env python3.6

import sys
from pathlib import Path
import subprocess

LABEL = 'MemAvailable:'

meminfo = Path('/proc/meminfo').read_text().split('\n')
for line in meminfo:
    if line.startswith(LABEL):
        assert line.endswith(' kB'), line
        available = int(line[len(LABEL):-3])
        break
else:
    print('\n'.join(meminfo), file=sys.stderr)
    raise ValueError()

print(available)
if available < 2 * 2**20:
    subprocess.run(['justmessage', 'Low memory!'])
