import sys
from PIL import Image, ImageDraw, ImageFont
D='/tmp/claude-0/-home-claude/9e664e83-b5f1-50bc-a8ba-f800783de781/scratchpad/'
W,H=1080,1920
def F(s,w='Black'):
    f=ImageFont.truetype(D+'fonts/Cairo.ttf',s); f.set_variation_by_name(w); return f
def t(d,xy,s,sz,fill,w='Black'): d.text(xy,s,font=F(sz,w),fill=fill,anchor='mm',direction='rtl',language='ar')
DARK,MID,MINT,HL,CREAM,TD='#034E54','#097E85','#3DDFD0','#14C4B6','#F2EEE2','#00626B'
icon=Image.open('/home/claude/nmd-hub/brand/nowmarket/icon.png').convert('RGBA')
g=Image.radial_gradient('L').resize((W*2,H*2)).crop((W//2,H//2,W//2+W,H//2+H))
def base(): 
    im=Image.composite(Image.new('RGB',(W,H),DARK),Image.new('RGB',(W,H),MID),g).convert('RGBA'); im.alpha_composite(icon.resize((120,120)),(W-200,250)); return im
def save(im,n): im.convert('RGB').save(D+n,quality=90)
# 28/11 teaser collab
im=base(); d=ImageDraw.Draw(im)
t(d,(W/2,640),'الليلة 7:00',110,MINT); t(d,(W/2,800),'ريل جديد مع قشطوطة',82,'#FFFFFF')
d.rounded_rectangle((140,950,940,1250),50,fill='#FFFFFF'); t(d,(W/2,1050),'المدير سأل:',64,'#448688','Bold'); t(d,(W/2,1150),'مين بدّه يوصّل كل هالطلبات؟',58,TD)
t(d,(W/2,1420),'فعّل الإشعارات وما تفوّته',54,'#FFFFFF','Bold'); save(im,'story_2811.jpg')
# 29/11 question
im=base(); d=ImageDraw.Draw(im)
t(d,(W/2,600),'سؤال الأحد 👇'.replace(' 👇',''),70,MINT,'ExtraBold'); t(d,(W/2,740),'شو بدك الليلة؟',120,'#FFFFFF')
for i,(a,b) in enumerate([('حلو','إشي للسهرة'),('مالح','عشا مرتّب'),('خفيف','عالماشي')]):
    y=920+i*200; d.rounded_rectangle((140,y,940,y+160),40,fill='#FFFFFF'); t(d,(760,y+80),a,66,TD); t(d,(400,y+80),b,44,'#448688','Bold')
t(d,(W/2,1600),'ابعتلنا جوابك بالرسايل',56,'#FFFFFF','Bold'); save(im,'story_2911.jpg')
# 30/11 teaser reel
im=base(); d=ImageDraw.Draw(im)
t(d,(W/2,640),'الليلة 7:00',110,MINT); t(d,(W/2,800),'حسبنا المشوار…',90,'#FFFFFF')
d.rounded_rectangle((240,930,840,1310),50,fill='#FFFFFF'); t(d,(W/2,1060),'كم دقيقة',70,'#448688','Bold'); t(d,(W/2,1180),'بيروحوا عليك؟',80,TD)
t(d,(W/2,1460),'خمّن واكتبلنا بالرسايل',56,'#FFFFFF','Bold'); save(im,'story_3011.jpg')
# 1/12
im=Image.new('RGBA',(W,H),CREAM); d=ImageDraw.Draw(im); im.alpha_composite(icon.resize((260,260)),(W//2-130,420))
t(d,(W/2,860),'أول يوم بكانون',76,'#448688','Bold'); t(d,(W/2,990),'برد؟ خليك بالبيت',104,TD)
d.rounded_rectangle((W/2-320,1130,W/2+320,1250),60,fill=TD); t(d,(W/2,1188),'نزّل NOW Market',62,'#FFFFFF')
t(d,(W/2,1340),'الرابط بالبايو',56,TD,'ExtraBold'); t(d,(W/2,1430),'توصيل 15 شيكل بدبورية · ومنوصّل كمان للقرى المجاورة',38,'#448688','Bold'); save(im,'story_0112.jpg')
