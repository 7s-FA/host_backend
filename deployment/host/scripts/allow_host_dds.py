#!/usr/bin/env python3
"""Run on an AMR with sudo: allow one host in its existing domain-40 DDS filter."""
import argparse
import ipaddress
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time


def updated_allow(text, address):
    pattern = re.compile(r'^ALLOW="([0-9a-fA-F.:/ ]*)"\s*$', re.MULTILINE)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise ValueError('Expected one literal ALLOW="..." setting; no changes made')
    match = matches[0]
    entries = match[1].split()
    for entry in entries:
        ipaddress.ip_network(entry, strict=False)
    if address not in entries:
        entries.append(address)
    return text[:match.start()] + 'ALLOW="' + ' '.join(entries) + '"\n' + text[match.end():]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('host_ip', type=ipaddress.IPv4Address)
    args = parser.parse_args()
    if os.geteuid() != 0:
        parser.error('sudo is required on the robot')
    address = str(args.host_ip)
    script = Path('/usr/local/sbin/dds-allow.sh')
    source = script.read_text()
    settings = Path('/etc/default/dds-allow') if '. /etc/default/dds-allow' in source else script
    before = settings.read_text()
    after = updated_allow(before, address)
    subprocess.run(['sh', '-n', str(script)], check=True)
    rules = subprocess.check_output(['iptables', '-S', 'INPUT'], text=True)
    if '--dport 17400:17649 -j DDS_ALLOW' not in rules:
        raise RuntimeError('Expected domain-40 DDS filter was not found; no changes made')
    subprocess.run(['iptables', '-S', 'DDS_ALLOW'], check=True, stdout=subprocess.DEVNULL)
    rule = ['DDS_ALLOW', '-s', address + '/32', '-j', 'RETURN']
    exists = subprocess.run(['iptables', '-C', *rule], capture_output=True).returncode == 0
    backup = None
    if before != after:
        backup = settings.with_name(settings.name + '.before-host-' + time.strftime('%Y%m%d-%H%M%S'))
        shutil.copy2(settings, backup)
        fd, temporary = tempfile.mkstemp(dir=settings.parent, prefix='.dds-host-')
        try:
            with os.fdopen(fd, 'w') as stream:
                stream.write(after)
            shutil.copystat(settings, temporary)
            os.replace(temporary, settings)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    try:
        if not exists:
            # Insert before DROP; retain all existing peers and other firewall rules.
            subprocess.run(['iptables', '-I', 'DDS_ALLOW', '1', *rule[1:]], check=True)
        subprocess.run(['iptables', '-C', *rule], check=True)
    except Exception:
        if backup:
            shutil.copy2(backup, settings)
        raise
    print(f'DDS host allowed: {address}/32 (UDP 17400-17649 only)')
    print(f'Persistent settings: {settings}')
    if backup:
        print(f'Backup: {backup}')
    print('Existing allow list retained. No robot service restart or motion command.')


if __name__ == '__main__':
    main()
