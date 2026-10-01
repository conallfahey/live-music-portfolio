from pathlib import Path
from PIL import Image, ImageOps, ImageCms
from concurrent.futures import ThreadPoolExecutor
import json, io

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'dist' / 'photos.json').read_text(encoding='utf-8'))
# Preserve image IDs, captions and gallery order when source files are renamed.
files = {photo['id']: root.parent / 'Photos' / photo['original'] for photo in manifest}
order = [photo['id'] for photo in manifest]
labels = {photo['id']: photo['label'] for photo in manifest}

def convert(i):
    p = files[i]
    with Image.open(p) as source:
        im = ImageOps.exif_transpose(source).convert('RGB')
        profile = source.info.get('icc_profile')
        if profile:
            try:
                im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(profile)), ImageCms.createProfile('sRGB'), outputMode='RGB')
            except (ValueError, OSError):
                pass
        w,h = im.size
        variants = []
        for size in [640,1280,2400]:
            copy = im.copy()
            copy.thumbnail((size,round(size*h/w)),Image.Resampling.LANCZOS)
            name = f'photo-{i:02d}-{size}.webp'
            copy.save(root/'dist'/'images'/name,'WEBP',quality=90 if size<2400 else 93,method=6)
            variants.append({'src':'images/'+name,'width':copy.width})
        return {'id':i,'width':w,'height':h,'label':labels.get(i,'Live music — Conall Fahey'),'variants':variants,'original':p.name}

with ThreadPoolExecutor(max_workers=4) as pool:
    photos=list(pool.map(convert,order))
(root/'dist'/'photos.json').write_text(json.dumps(photos),encoding='utf-8')
print(f'Converted {len(photos)} photographs; WebP total: {sum(p.stat().st_size for p in (root/"dist"/"images").glob("*.webp"))/1024/1024:.1f} MB')
