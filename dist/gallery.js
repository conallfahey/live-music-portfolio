const gallery = document.querySelector('.gallery');
const dialog = document.querySelector('.lightbox');
const viewer = dialog.querySelector('.viewer-image');
let photos = [], active = 0, lastFocus;
const number = n => String(n + 1).padStart(2, '0');

function layout() {
  const width = gallery.clientWidth;
  const gap = parseFloat(getComputedStyle(gallery).getPropertyValue('--gap'));
  const columns = matchMedia('(max-width: 700px)').matches ? 1 : width < 1000 ? 2 : 3;
  const columnWidth = (width - gap * (columns - 1)) / columns;
  const bottoms = Array(columns).fill(0);
  photos.forEach(photo => {
    const column = bottoms.indexOf(Math.min(...bottoms));
    const height = columnWidth * photo.height / photo.width;
    const button = photo.button;
    button.style.width = `${columnWidth}px`;
    button.style.height = `${height}px`;
    button.style.left = `${column * (columnWidth + gap)}px`;
    button.style.top = `${bottoms[column]}px`;
    button.querySelector('img').sizes = `${Math.ceil(columnWidth)}px`;
    if (button.parentElement !== gallery) gallery.append(button);
    bottoms[column] += height + gap;
  });
  gallery.style.height = `${Math.max(...bottoms) - gap}px`;
}

function show(index) {
  active = (index+photos.length)%photos.length;
  const photo = photos[active];
  viewer.src = photo.variants[2].src;
  viewer.alt = photo.label;
  dialog.querySelector('.viewer-count').textContent = `${number(active)} / ${photos.length}`;
  dialog.querySelector('.viewer-label').textContent = photo.label;
  if (!dialog.open) { lastFocus = document.activeElement; dialog.showModal(); document.body.style.overflow='hidden'; }
  [active-1,active+1].forEach(i=>{const preload=new Image();preload.src=photos[(i+photos.length)%photos.length].variants[2].src;});
}
dialog.querySelector('.close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('close',()=>{document.body.style.overflow='';lastFocus?.focus({preventScroll:true});});
dialog.querySelector('.previous').addEventListener('click',()=>show(active-1));
dialog.querySelector('.next').addEventListener('click',()=>show(active+1));
document.addEventListener('keydown',e=>{if(!dialog.open)return;if(e.key==='ArrowLeft'){e.preventDefault();show(active-1);}if(e.key==='ArrowRight'){e.preventDefault();show(active+1);}});
let touchX;
viewer.addEventListener('touchstart',e=>touchX=e.changedTouches[0].clientX,{passive:true});
viewer.addEventListener('touchend',e=>{const delta=e.changedTouches[0].clientX-touchX;if(Math.abs(delta)>50)show(active+(delta<0?1:-1));},{passive:true});
document.querySelector('#year').textContent = new Date().getFullYear();
fetch('photos.json').then(r=>{if(!r.ok)throw new Error('Collection unavailable');return r.json();}).then(data=>{
  photos=data;
  photos.forEach((photo,i)=>{
    const button=document.createElement('button');button.className='photo';button.setAttribute('aria-label',`View photograph ${number(i)}: ${photo.label}`);
    const img=new Image();img.alt=photo.label;img.width=photo.width;img.height=photo.height;img.loading=i<3?'eager':'lazy';img.decoding='async';if(i===0)img.fetchPriority='high';
    img.addEventListener('load',()=>img.classList.add('loaded'));img.addEventListener('error',()=>{img.classList.add('loaded');button.style.background='#242721';});
    img.srcset=photo.variants.map(v=>`${v.src} ${v.width}w`).join(', ');img.src=photo.variants[1].src;
    const meta=document.createElement('span');meta.className='photo-meta';const label=document.createElement('span');label.textContent=photo.label;const count=document.createElement('span');count.className='photo-number';count.textContent=number(i);meta.append(label,count);button.append(img,meta);button.addEventListener('click',()=>show(i));photo.button=button;
  });
  layout();new ResizeObserver(()=>requestAnimationFrame(layout)).observe(gallery);
}).catch(()=>{gallery.innerHTML='<p class="no-script">The collection couldn’t load. Please refresh to try again.</p>';});
