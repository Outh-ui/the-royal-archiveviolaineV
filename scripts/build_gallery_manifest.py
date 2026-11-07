#!/usr/bin/env python3
"""Build a gallery index from images uploaded to designated folders."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'assets' / 'gallery-uploads'
CHARACTERS = ['vincent', 'violaine', 'simon', 'evelyn', 'thea', 'lowen', 'charlotte', 'nilan', 'brennan', 'sylvia', 'vince', 'rosalinda', 'malvira', 'aria', 'ronan', 'lucas-sylvester', 'ira', 'ryan', 'exathrion-edward', 'nicholas-vaithrion', 'oliver', 'harlan']
MOMENTS = ['couple', 'evelyn-simon', 'family', 'other', 'nilan-aria']
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}
def images(folder):
    if not folder.exists(): return []
    return [f.relative_to(ROOT).as_posix() for f in sorted(folder.iterdir(), key=lambda f: f.name.casefold()) if f.is_file() and f.suffix.lower() in EXTENSIONS]
SPECIAL = ('card', 'cover', 'profile', 'dossier-card')
def special(folder, stem):
    if not folder.exists(): return None
    matches = [f for f in folder.iterdir() if f.is_file() and f.stem.lower() == stem and f.suffix.lower() in EXTENSIONS]
    return sorted(matches, key=lambda f: f.name.casefold())[0].relative_to(ROOT).as_posix() if matches else None

# Include every image file in Moments, even if its bytes match another file.
# Each distinct path is a separate gallery entry.
def all_moments(folder):
    return images(BASE / 'moments' / folder)

manifest = {
    'characters': {k: images(BASE/'characters'/k) for k in CHARACTERS},
    'moments': {k: all_moments(k) for k in MOMENTS},
    'displayImages': {k: {name: path for name in SPECIAL if (path := special(BASE/'characters'/k, name))} for k in CHARACTERS},
    'bookCovers': {str(i): path for i in range(1, 5) if (path := special(ROOT/'assets'/'book-covers', f'volume-{i}'))},
}
(ROOT/'assets'/'gallery-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('Gallery manifest built:', sum(map(len,manifest['characters'].values())), 'character photos,', sum(map(len,manifest['moments'].values())), 'moment photos')
