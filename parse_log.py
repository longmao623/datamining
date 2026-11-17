import re
from collections import Counter
from datetime import datetime
import pandas as pd

# Parse access.log
pattern = r'(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+|-) "([^"]*)" "([^"]*)"'

records = []
with open(r'C:\Users\dbw\.openclaw\workspace\大作业\大作业\access.log', 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        m = re.match(pattern, line)
        if m:
            records.append({
                'ip': m.group(1),
                'timestamp': m.group(2),
                'method': m.group(3),
                'path': m.group(4),
                'protocol': m.group(5),
                'status': int(m.group(6)),
                'size': 0 if m.group(7) == '-' else int(m.group(7)),
                'referer': m.group(8),
                'ua': m.group(9)
            })

print(f'Total parsed: {len(records)}')

# Quick stats
statuses = Counter(r['status'] for r in records)
print('Status codes:', dict(statuses))

methods = Counter(r['method'] for r in records)
print('Methods:', dict(methods))

# Top IPs
ips = Counter(r['ip'] for r in records)
print('Top 10 IPs:', ips.most_common(10))

# Some suspicious patterns
suspicious_keywords = ['passwd', 'nmap', 'sql', 'union', 'select', 'eval', 'exec', '../', '..%2f', 'etc', 'config', 'admin', 'login', 'phpmyadmin']
suspicious = [r for r in records if r['status'] in [403, 404] or any(k in r['path'].lower() for k in suspicious_keywords)]
print(f'Suspicious requests: {len(suspicious)}')
print('Sample suspicious:')
for r in suspicious[:10]:
    print(f"  {r['ip']} {r['method']} {r['path']} -> {r['status']} ({r['ua'][:60]})")
