"""Almero21 story generator. Usage: python3 make_stories.py <spec.json> <src_dir> <out_dir>
spec: [{"id":"s01","clip":"video_x.mp4","start":1.0,"dur":6,"text":"...","card":false}]
Needs: google-chrome + playwright (python), ffmpeg."""
import asyncio, json, os, sys, subprocess
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); F='file://'+HERE+'/fonts/'
CSS=f"""@font-face{{font-family:H;font-weight:900;src:url({F}heebo-hebrew-900-normal.woff2)}}
@font-face{{font-family:H;font-weight:900;src:url({F}heebo-latin-900-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
@font-face{{font-family:H;font-weight:500;src:url({F}heebo-hebrew-500-normal.woff2)}}
@font-face{{font-family:H;font-weight:500;src:url({F}heebo-latin-500-normal.woff2);unicode-range:U+0000-00FF,U+2000-206F}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;background:transparent;direction:rtl}}
.brand{{position:absolute;top:300px;left:0;right:0;text-align:center;font:900 44px H;letter-spacing:.35em;color:#fff;text-shadow:0 3px 14px rgba(0,0,0,.6);direction:ltr}}
.t{{position:absolute;top:1180px;left:0;right:0;text-align:center}}
.t span{{display:inline-block;background:#fff;color:#0b0b0b;font:900 78px/1.15 H;padding:16px 44px;transform:rotate(-2deg);box-shadow:0 10px 30px rgba(0,0,0,.35);max-width:900px}}
.cta{{position:absolute;top:1430px;left:0;right:0;text-align:center}} .cta b{{display:inline-block;font:500 44px H;color:#fff;background:rgba(10,10,10,.72);padding:12px 34px;border-radius:40px}}
.card{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#fff;background:rgba(8,8,8,.62)}}
.card .big{{font:900 96px/1.15 H;padding:0 60px}} .card .sm{{font:500 52px/1.6 H;color:#eee;margin-top:40px}}
"""
def html(s):
    if s.get('card'):
        return f"<div class=card><div class=big>{s['text']}</div><div class=sm>{s.get('sub','לקביעת תור · הלינק בביו')}</div></div><div class=brand>ALMERO21</div>"
    return f"<div class=brand>ALMERO21</div><div class=t><span>{s['text']}</span></div><div class=cta><b>לקביעת תור · הלינק בביו</b></div>"
async def overlays(spec,out):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        for s in spec:
            fn=f"{out}/{s['id']}_ov.html"; open(fn,'w').write(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{html(s)}</body></html>")
            await pg.goto('file://'+fn); await pg.wait_for_timeout(500); await pg.evaluate('document.fonts.ready')
            await pg.screenshot(path=f"{out}/{s['id']}_ov.png",omit_background=True); os.remove(fn)
        await b.close()
def main():
    spec=json.load(open(sys.argv[1])); src=sys.argv[2]; out=os.path.abspath(sys.argv[3]); os.makedirs(out,exist_ok=True)
    asyncio.run(overlays(spec,out))
    for s in spec:
        vf="scale=1080:1920,setsar=1,fps=30,eq=contrast=1.06:saturation=1.05"
        if s.get('card'): vf+=",boxblur=12:2"
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(s['start']),'-t',str(s['dur']),'-i',f"{src}/{s['clip']}",'-i',f"{out}/{s['id']}_ov.png",
          '-filter_complex',f"[0:v]{vf}[a];[a][1:v]overlay=0:0,format=yuv420p,fade=t=in:st=0:d=0.3[v]",'-map','[v]','-an',
          '-c:v','libx264','-preset','veryfast','-crf','21','-movflags','+faststart',f"{out}/{s['id']}.mp4"],check=True)
        os.remove(f"{out}/{s['id']}_ov.png")
main()
