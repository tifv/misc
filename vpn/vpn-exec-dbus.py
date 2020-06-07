#!/usr/bin/python3

import re
import os
import sys
import subprocess
import tempfile

DBUS_ADDRESS = os.environ['DBUS_SESSION_BUS_ADDRESS']

if DBUS_ADDRESS.startswith('unix:abstract='):
    match = re.fullmatch(
        'unix:abstract=(/tmp/dbus-[0-9a-zA-Z]+),guid=[0-9a-f]+',
        DBUS_ADDRESS )
    if match is None:
        print("Could not parse D-Bus session address", file=sys.stderr)
        os.execvp('vpn-exec', sys.argv[1:])
    else:
        address = match.group(1)
        with tempfile.TemporaryDirectory() as tmpdir:
            proxy = tmpdir + '/dbus-proxy'
            socat_proc = subprocess.Popen(
                [ 'socat',
                    f'UNIX-LISTEN:{proxy},fork',
                    f'ABSTRACT-CONNECT:{address}' ],
            )
            os.environ['DBUS_SESSION_BUS_ADDRESS'] = 'unix:path=' + proxy
            vpn_proc = None
            try:
                vpn_proc = subprocess.run(['vpn-exec'] + sys.argv[1:])
            finally:
                socat_proc.terminate()
                socat_proc.wait()
            if vpn_proc is not None:
                exit(vpn_proc.returncode)


