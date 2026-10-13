"""Validate local Markdown links and portable source filenames."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
for path in (root / 'docs').rglob('*.md'):
    text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
    text = re.sub(r'`[^`]*`', '', text)
    if re.search(r'!\[\[', text):
        errors.append(f'{path.relative_to(root)}: unresolved Obsidian image')
    for target in re.findall(r'!?\[[^\]\n]*\]\(([^)\s]+)(?:\s+[^)]*)?\)', text):
        parts = urlsplit(target.strip('<>'))
        if parts.scheme or parts.netloc or not parts.path:
            continue
        dest = (path.parent / unquote(parts.path)).resolve()
        if not dest.exists():
            errors.append(f'{path.relative_to(root)}: missing {target}')
for folder in ('docs', 'scripts', 'experiments'):
    for path in (root / folder).rglob('*'):
        if not path.name.isascii() or ' ' in path.name:
            errors.append(f'Non-portable filename: {path.relative_to(root)}')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print('Markdown links and source filenames: OK')
