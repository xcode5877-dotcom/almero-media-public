import subprocess, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = '/tmp/claude-0/-home-claude/9e664e83-b5f1-50bc-a8ba-f800783de781/scratchpad/'
OUT = sys.argv[1]
W, H, FPS, DUR = 1080, 1920, 30, 16.5
TEAL, DARK, MINT, HL, CREAM, TD, TS = '#066C71', '#034E54', '#3DDFD0', '#14C4B6', '#F2EEE2', '#00626B', '#448688'
ICON = Image.open('/home/claude/nmd-hub/brand/nowmarket/icon.png').convert('RGBA')
_fc = {}
def F(size, w='Black'):
    k = (size, w)
    if k not in _fc:
        f = ImageFont.truetype(D + 'fonts/Cairo.ttf', size); f.set_variation_by_name(w); _fc[k] = f
    return _fc[k]
def txt(d, xy, s, size, fill, w='Black', anchor='mm'):
    d.text(xy, s, font=F(size, w), fill=fill, anchor=anchor, direction='rtl', language='ar')
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def back(x):
    x = max(0, min(1, x)); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# gradient bg
bg = Image.new('RGB', (W, H), DARK)
g = Image.radial_gradient('L').resize((W * 2, H * 2)).crop((W // 2, H // 2, W // 2 + W, H // 2 + H))
bg = Image.composite(Image.new('RGB', (W, H), DARK), Image.new('RGB', (W, H), '#097E85'), g)
icon_s = ICON.resize((110, 110), Image.LANCZOS)

def paste_scaled(base, layer, cx, cy, s, alpha=1.0):
    if s <= 0.01: return
    l = layer.resize((max(1, int(layer.width * s)), max(1, int(layer.height * s))), Image.LANCZOS)
    if alpha < 1:
        a = l.split()[3].point(lambda v: int(v * alpha)); l.putalpha(a)
    base.alpha_composite(l, (int(cx - l.width / 2), int(cy - l.height / 2)))

def card(wd, ht, fill, radius=40):
    c = Image.new('RGBA', (wd + 40, ht + 40), (0, 0, 0, 0))
    sh = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((20, 28, wd + 20, ht + 28), radius, fill=(0, 0, 0, 90))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    ImageDraw.Draw(c).rounded_rectangle((20, 20, wd + 20, ht + 20), radius, fill=fill)
    return c

# hook cards
def price_card():
    c = card(400, 470, '#FFFFFF'); d = ImageDraw.Draw(c)
    txt(d, (220, 85), 'توصيل', 52, TS, 'Bold')
    txt(d, (220, 215), '15', 150, TD); txt(d, (220, 296), 'شيكل', 50, TD, 'ExtraBold')
    d.rounded_rectangle((70, 360, 370, 440), 40, fill=HL); txt(d, (220, 398), 'لباب البيت', 46, '#FFFFFF')
    return c
def trip_card():
    c = card(400, 470, '#0A5F64'); d = ImageDraw.Draw(c)
    txt(d, (220, 110), 'ولا…', 56, MINT, 'Bold')
    txt(d, (220, 240), 'المشوار', 88, '#FFFFFF')
    d.rounded_rectangle((70, 360, 370, 440), 40, outline=MINT, width=4); txt(d, (220, 398), 'على حسابك', 46, MINT)
    return c
PC, TC = price_card(), trip_card()

items = [('تلبس وتدوّر عالمفاتيح', 5), ('تسخّن السيارة بهالبرد', 5), ('تدوّر على موقف', 10), ('تستنى دورك بالمحل', 15), ('ترجع… والأكل برد', 5)]
T0, STEP = 3.2, 1.35
def item_row(s, m):
    r = Image.new('RGBA', (860, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(r)
    d.rounded_rectangle((0, 0, 860, 120), 30, fill='#FFFFFF')
    txt(d, (810, 60), s, 50, TD, 'ExtraBold', 'rm')
    d.rounded_rectangle((30, 25, 210, 95), 35, fill='#FBE3DE'); txt(d, (120, 58), f'{m} دقايق', 34, '#B4473A', 'Black')
    return r
ROWS = [item_row(*i) for i in items]

def end_card():
    e = Image.new('RGBA', (W, H), CREAM); d = ImageDraw.Draw(e)
    e.alpha_composite(ICON.resize((300, 300), Image.LANCZOS), (W // 2 - 150, 380))
    txt(d, (W / 2, 790), 'خليك بالبيت 😌'.replace(' 😌', ''), 70, TS, 'Bold')
    txt(d, (W / 2, 900), 'نزّل NOW Market', 104, TD)
    d.rounded_rectangle((W / 2 - 300, 1000, W / 2 + 300, 1120), 60, fill=TD); txt(d, (W / 2, 1058), 'الرابط بالبايو 👇'.replace(' 👇', ''), 60, '#FFFFFF')
    txt(d, (W / 2, 1230), 'توصيل 15 شيكل بدبورية', 56, TD, 'ExtraBold')
    txt(d, (W / 2, 1305), 'ومنوصّل كمان للقرى المجاورة', 44, TS, 'Bold')
    for i, s in enumerate(['App Store', 'Google Play']):
        x = W / 2 - 240 + i * 480
        d.rounded_rectangle((x - 200, 1400, x + 200, 1500), 24, fill='#111111'); d.text((x, 1450), s, font=F(46, 'Bold'), fill='#FFFFFF', anchor='mm')
    return e
END = end_card()

def scooter(d, x, y):
    d.rounded_rectangle((x - 70, y - 20, x + 60, y + 20), 18, fill='#FFFFFF')
    d.rounded_rectangle((x + 20, y - 75, x + 60, y - 15), 14, fill=MINT)
    d.ellipse((x - 85, y + 5, x - 35, y + 55), fill='#FFFFFF', outline=DARK, width=8)
    d.ellipse((x + 35, y + 5, x + 85, y + 55), fill='#FFFFFF', outline=DARK, width=8)
    d.line((x + 55, y - 15, x + 75, y - 80), fill='#FFFFFF', width=10)

def frame(t):
    im = bg.convert('RGBA'); d = ImageDraw.Draw(im)
    if t < 13.6:
        im.alpha_composite(icon_s, (W - 80 - 110, 250))
    if t < 3.2:
        # hook: cards pop from first frame
        a = back(t / 0.45); b = back((t - 0.35) / 0.45)
        txt(d, (W / 2, 520), 'برّا برد… وبدك أكل', 78, '#FFFFFF')
        txt(d, (W / 2, 620), 'شو بتختار؟', 64, MINT, 'ExtraBold')
        paste_scaled(im, PC, W * 0.73, 1030, 0.7 + 0.3 * a)
        paste_scaled(im, TC, W * 0.27, 1030, 0.7 + 0.3 * b)
        vs = ease((t - 0.8) / 0.3)
        if vs > 0:
            r = 48 * vs; d.ellipse((W / 2 - r, 1030 - r, W / 2 + r, 1030 + r), fill='#FFFFFF'); txt(d, (W / 2, 1025), 'ولا', int(36 * vs) + 1, TD)
        # pulse hint
        p = (math.sin(t * 6) + 1) / 2
        txt(d, (W / 2, 1450), 'خلّينا نحسب المشوار…', 56, (255, 255, 255, int(150 + 105 * p)), 'Bold')
    elif t < 11.2:
        lt = t - 3.2
        txt(d, (W / 2, 470), 'حساب المشوار 🧾'.replace(' 🧾', ''), 84, '#FFFFFF')
        n = sum(1 for i in range(len(items)) if t >= T0 + 0.4 + i * STEP)
        mins = sum(m for _, m in items[:n])
        # counter
        d.rounded_rectangle((W / 2 - 230, 560, W / 2 + 230, 680), 60, fill=HL)
        txt(d, (W / 2, 617), f'{mins} دقيقة', 66, '#FFFFFF')
        for i, r in enumerate(ROWS):
            st = T0 + 0.4 + i * STEP
            if t < st: continue
            k = ease((t - st) / 0.35); x = int(110 + (1 - k) * 900); y = 760 + i * 150
            im.alpha_composite(r, (x, y))
        if t > 10.0:
            k = back((t - 10.0) / 0.4)
            stamp = Image.new('RGBA', (900, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(stamp)
            sd.rounded_rectangle((10, 10, 890, 190), 30, outline='#E2574C', width=10)
            txt(sd, (450, 98), 'والأكل؟ بارد 🥶'.replace(' 🥶', ''), 84, '#E2574C')
            stamp = stamp.rotate(-6, expand=True, resample=Image.BICUBIC)
            paste_scaled(im, stamp, W / 2, 1600, 1.6 - 0.6 * k)
    elif t < 13.6:
        lt = t - 11.2
        k = back(lt / 0.5)
        txt(d, (W / 2, 560), 'ولا…', 90, MINT)
        paste_scaled(im, PC, W / 2, 1000, 0.5 + 0.7 * k)
        txt(d, (W / 2, 1380), 'والأكل بيوصلك سخن لعندك', 64, '#FFFFFF', 'ExtraBold')
        sx = -150 + (W + 300) * min(1, lt / 2.4)
        d.line((0, 1610, W, 1610), fill='#0A6A70', width=6)
        scooter(d, sx, 1540)
    else:
        lt = t - 13.6
        e = END.copy(); k = ease(lt / 0.4)
        if k < 1:
            mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).ellipse((W / 2 - 1300 * k, H / 2 - 1300 * k, W / 2 + 1300 * k, H / 2 + 1300 * k), fill=255)
            im.paste(e, (0, 0), mask)
        else:
            im = e
            d = ImageDraw.Draw(im)
            p = 1 + 0.03 * math.sin(lt * 5)
    return im.convert('RGB')

if len(sys.argv) > 2:
    for tt in sys.argv[2].split(','):
        frame(float(tt)).save(OUT.replace('.mp4', f'_f{tt}.jpg'), quality=85)
    sys.exit()
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', OUT], stdin=subprocess.PIPE)
for i in range(int(DUR * FPS)):
    p.stdin.write(frame(i / FPS).tobytes())
p.stdin.close(); p.wait()
