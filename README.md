# Conall Fahey - Live Music Photo Portfolio

A contemporary photography portfolio featuring 37 live music photographs, an equal-width masonry gallery, a single-column mobile layout, and an accessible full-screen viewer.

## Website

https://conallfahey.github.io/live-music-portfolio/

## Edit and preview

The complete static website lives in `dist/`. Edit `index.html`, `style.css`, or `gallery.js`; update image captions and ordering in `photos.json`.

Run a local preview from the repository root:

```sh
python -m http.server 4173 --directory dist
```

Open http://localhost:4173. No package installation or build is required.

## Publishing

Push to `main` to publish through the GitHub Pages workflow in `.github/workflows/pages.yml`. The workflow uploads only the `dist/` directory.

## Photographs

Each photograph has 640, 1280, and 2400 pixel WebP variants. The gallery uses responsive image selection and native lazy loading; the viewer loads the largest variant. Original proportions are preserved.

`prepare_images.py` regenerates the assets using Pillow from a sibling `Photos/` directory. Original photographs are retained locally and are not included in this repository.

© Conall Fahey. All photographs reserved. Publication of this repository does not grant permission to reuse the photographs.
