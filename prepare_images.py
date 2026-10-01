from pathlib import Path
from PIL import Image, ImageOps, ImageCms
from concurrent.futures import ThreadPoolExecutor
import json, io

root = Path(__file__).resolve().parent
files = sorted((root.parent / 'Photos').glob('*'))
order = [6,12,36,1,7,10,20,5,21,3,4,11,24,13,14,15,9,0,19,22,23,16,17,18,25,26,27,28,29,30,31,32,2,33,34,35,8]
labels = {6:'Droptines · Lincoln Hall, Chicago',12:'Denzel Curry · Riviera Theatre',36:'Tazu · Red Rocks',7:'Sam Blacky · Radius, Chicago',10:'Chance the Rapper',5:'Daniel Allan',3:'Gotti · PRYSM',4:'Gotti · PRYSM',11:'Claude VonStroke · Chicago',13:'Fly Nari',32:'Radius, Chicago',35:'Supertaste · Electric Forest'}

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
