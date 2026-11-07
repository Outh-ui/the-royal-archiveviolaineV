# THE ROYAL ARCHIVE — Dynamic Galleries

This project preserves the original website and its existing images. New images can be uploaded to specific folders without editing HTML.

## Uploading images

Upload **new** pictures to the appropriate folder (do not delete existing images):

- Character galleries: `assets/gallery-uploads/characters/<name>/`
- Moments albums: `assets/gallery-uploads/moments/<album>/`

Character folder names: `vincent, violaine, simon, evelyn, thea, lowen, charlotte, nilan, brennan, sylvia, vince, rosalinda, malvira`.

Moments folders:
- `couple` — Violaine & Vincent
- `evelyn-simon` — Evelyn & Simon
- `family` — Violaine & Vincent's family
- `other` — Other moments

Each new image will appear in its character gallery or Moments album **after the manifest is regenerated**. Do not upload images into `assets/images/` for this workflow; that folder holds the original archive.

## Cloudflare Pages (GitHub integration)

1. Create a **private** GitHub repository and upload the **contents** of this ZIP, not the ZIP itself.
2. In Cloudflare Pages, connect the GitHub repository.
3. Framework preset: **None**.
4. **Build command:** `python3 scripts/build_gallery_manifest.py`
5. **Build output directory:** `.`
6. Deploy. On each GitHub push, Cloudflare runs the build command and creates an updated image index.

The checked-in `assets/gallery-manifest.json` initially has empty galleries for *new uploads*. Existing images are still in the original website and will continue to appear. New photos will be indexed during the Cloudflare build. A local `file://` preview may not load the manifest due to browser restrictions; the existing archive still works locally, and dynamic uploads work when served over HTTP(S).

## Important

- Use unique filenames for each image; no fixed photo count is required.
- Upload photos directly to the correct folder. Keep the original archive files.
- Public site visitors can view and download images even when the GitHub repository is private.
- No password is required to access the deployed website.
- `robots.txt` asks search engines not to index the site; this is **not** access control.
