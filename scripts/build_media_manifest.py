#!/usr/bin/env python3
"""Build the Motion Gallery and Residences manifest from local files."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
VIDEO_EXTS = {'.mp4', '.webm'}
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.avif'}

def files(folder, extensions):
    return sorted((p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in extensions), key=lambda p: p.name.casefold()) if folder.is_dir() else []

def rel(path):
    return path.relative_to(ROOT).as_posix()

def read_info(folder):
    path = folder / 'info.json'
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError) as e:
        print(f'Warning: could not read {path}: {e}')
        return {}

motion = []
video_dir = ASSETS / 'motion-gallery'
for video in files(video_dir, VIDEO_EXTS):
    poster = next((p for p in files(video_dir, IMAGE_EXTS) if p.stem.casefold() == video.stem.casefold()), None)
    motion.append({'src': rel(video), 'title': video.stem.replace('_', ' ').replace('-', ' '), 'description': '', **({'poster': rel(poster)} if poster else {})})

residences = []
res_dir = ASSETS / 'residences'
if res_dir.is_dir():
    for folder in sorted((p for p in res_dir.iterdir() if p.is_dir()), key=lambda p: p.name.casefold()):
        info = read_info(folder)
        for photo in files(folder, IMAGE_EXTS):
            residences.append({'image': rel(photo), 'title': str(info.get('title') or folder.name.replace('-', ' ')), 'description': str(info.get('description') or '')})
    for photo in files(res_dir, IMAGE_EXTS):
        residences.append({'image': rel(photo), 'title': photo.stem.replace('-', ' '), 'description': ''})

output = ASSETS / 'media-manifest.json'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps({'motion': motion, 'residences': residences}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Media manifest built: {len(motion)} videos, {len(residences)} residence photos')
