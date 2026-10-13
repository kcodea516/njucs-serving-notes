"""Validate the shared Markdown vault and its MkDocs entry point."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import os
import re
import sys

root = Path(__file__).resolve().parents[1]
vault = root / 'vault'
docs = root / 'docs'
errors = []
if not docs.is_symlink() or docs.resolve() != vault.resolve():
    errors.append('docs must be a relative symlink to vault')
elif os.path.isabs(os.readlink(docs)):
    errors.append('docs symlink must remain portable across checkouts')
for path in vault.rglob('*'):
    relative = path.relative_to(vault)
    if any(part.startswith('.') for part in relative.parts):
        continue
    if not path.name.isascii() or ' ' in path.name:
        errors.append(f'Non-portable filename: {relative}')
    if not path.is_file():
        continue
    if path.suffix.lower() not in {'.md', '.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif'}:
        errors.append(f'Non-document file in vault: {relative}')
    if path.suffix != '.md':
        continue
    text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
    text = re.sub(r'`[^`]*`', '', text)
    if re.search(r'!\[\[', text):
        errors.append(f'{relative}: unresolved Obsidian image')
    for target in re.findall(r'!?\[[^\]\n]*\]\(([^)\s]+)(?:\s+[^)]*)?\)', text):
        parts = urlsplit(target.strip('<>'))
        if parts.scheme or parts.netloc or not parts.path:
            continue
        dest = (path.parent / unquote(parts.path)).resolve()
        if not dest.exists():
            errors.append(f'{relative}: missing {target}')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print('Shared vault, document-only contents, and Markdown links: OK')
