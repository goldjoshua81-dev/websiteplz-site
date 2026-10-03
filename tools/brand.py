"""WebsitePlz brand assets: logo.svg (outlined wordmark), logo-light.svg, favicon.svg,
favicon.ico, apple-touch-icon.png, img/icon-512.png. Run: python3 tools/brand.py
Needs fontTools + the Bricolage Grotesque font (OFL) at G below; output is committed."""
import os,subprocess,io
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G='/usr/share/fonts/truetype/sand-box/google/Bricolage Grotesque/BricolageGrotesque-VariableFont_opsz,wdth,wght.ttf'
INK='#0B1B2E';CORAL='#D1361A';CORAL_L='#FF8A6B'
def text_path(text,size,x,y,track=0):
    f=instancer.instantiateVariableFont(TTFont(G),{'wght':800,'opsz':48,'wdth':100})
    gs=f.getGlyphSet();cm=f.getBestCmap();s=size/f['head'].unitsPerEm
    out=[];cx=x
    for ch in text:
        pen=SVGPathPen(gs,ntos=lambda v:("%.2f"%v).rstrip("0").rstrip("."))
        g=cm[ord(ch)];gs[g].draw(TransformPen(pen,(s,0,0,-s,cx,y)));out.append((ch,pen.getCommands()));cx+=gs[g].width*s+track
    return out,cx-x-track
def icon(p='w'):
    return (f'<defs><linearGradient id="{p}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1D3A63"/><stop offset="1" stop-color="{INK}"/></linearGradient></defs>'
     f'<rect width="48" height="48" rx="13" fill="url(#{p}g)"/>'
     '<rect x="8.5" y="11" width="25" height="20" rx="4" fill="none" stroke="#fff" stroke-width="2.6"/>'
     '<path d="M8.5 17h25" stroke="#fff" stroke-width="2.6"/><circle cx="12.6" cy="14" r="1" fill="#fff"/><circle cx="15.8" cy="14" r="1" fill="#fff"/>'
     f'<circle cx="32.5" cy="31.5" r="10" fill="{CORAL}" stroke="{INK}" stroke-width="2.5"/>'
     '<path d="M29.2 27.6h2l.9 2.3-1.2.8a6 6 0 0 0 3.4 3.4l.8-1.2 2.3.9v2a1.1 1.1 0 0 1-1.2 1.1 9 9 0 0 1-8.1-8.1 1.1 1.1 0 0 1 1.1-1.2z" fill="#fff"/>')
def logo(light=False):
    parts,w=text_path('WebsitePlz',27,58,33.5,-.3)
    c1='#FFFFFF' if light else INK; c2=CORAL_L if light else CORAL
    d1=''.join(d for ch,d in parts[:7]); d2=''.join(d for ch,d in parts[7:])
    W=int(58+w+3)
    return W,(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 48" width="{W}" height="48">{icon("L" if light else "D")}'
              f'<path d="{d1}" fill="{c1}"/><path d="{d2}" fill="{c2}"/></svg>')
def png(svg,size,out):
    open('/tmp/_w.html','w').write(f'<html><body style="margin:0;background:transparent">{svg.replace("<svg ",f"<svg width=\"{size}\" height=\"{size}\" ",1)}</body></html>')
    subprocess.run(['google-chrome','--headless=new','--no-sandbox','--disable-gpu','--hide-scrollbars','--default-background-color=00000000',f'--window-size={size},{size}',f'--screenshot={out}','file:///tmp/_w.html'],capture_output=True,timeout=40)
if __name__=='__main__':
    W,l=logo();open(f'{ROOT}/img/logo.svg','w').write(l)
    _,ll=logo(True);open(f'{ROOT}/img/logo-light.svg','w').write(ll)
    fav=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">{icon("f")}</svg>'
    open(f'{ROOT}/favicon.svg','w').write(fav)
    png(fav,180,f'{ROOT}/apple-touch-icon.png'); png(fav,512,f'{ROOT}/img/icon-512.png'); png(fav,256,'/tmp/_ico.png')
    from PIL import Image
    Image.open('/tmp/_ico.png').save(f'{ROOT}/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
    print('logo width',W)
