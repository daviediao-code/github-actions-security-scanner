#!/usr/bin/env python3
"""Lightweight secret scanner for GitHub Actions."""
import os
import re
import sys
from pathlib import Path

# Patterns to scan for
SECRET_PATTERNS = {
    'AWS Access Key': r'AKIA[0-9A-Z]{16}',
    'GitHub Token': r'gh[pousr]_[0-9a-zA-Z]{36}',
    'Private Key': r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----',
    'Generic API Key': r'(api[_-]?key|apikey)[=: ]+[\'"][a-zA-Z0-9]{20,}[\'"]',
    'Slack Token': r'xox[baprs]-[0-9a-zA-Z-]+',
    'Google API Key': r'AIza[0-9A-Za-z\-_]{35}',
    'JWT Token': r'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}',
}

def scan_file(filepath, patterns):
    """Scan a single file for secrets."""
    findings = []
    try:
        content = filepath.read_text(errors='ignore')
        for name, pattern in patterns.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                findings.append({
                    'file': str(filepath),
                    'line': content[:match.start()].count('\n') + 1,
                    'type': name,
                    'match': match.group()[:20] + '...'  # Truncate
                })
    except (PermissionError, OSError):
        pass
    return findings

def scan_directory(directory, patterns, exclude=None):
    """Scan directory for secrets."""
    exclude = exclude or ['.git', 'node_modules', '__pycache__', 'vendor']
    all_findings = []
    
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude]
        
        for file in files:
            filepath = Path(root) / file
            # Skip binary files
            if filepath.suffix in ['.png', '.jpg', '.gif', '.ico', '.pdf']:
                continue
            findings = scan_file(filepath, patterns)
            all_findings.extend(findings)
    
    return all_findings

def main():
    """Main entry point."""
    scan_dir = os.getenv('SCAN_DIR', '.')
    patterns = SECRET_PATTERNS
    
    print(f"🔍 Scanning {scan_dir} for secrets...")
    findings = scan_directory(scan_dir, patterns)
    
    if findings:
        print(f"\n⚠️  Found {len(findings)} potential secrets:\n")
        for f in findings:
            print(f"  [{f['type']}] {f['file']}:{f['line']}")
        sys.exit(1)
    else:
        print("\n✅ No secrets detected.")
        sys.exit(0)

if __name__ == '__main__':
    main()
