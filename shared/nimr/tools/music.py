import numpy as np, sys, wave
sr=44100
def note(f,d,amp=.2,kind='pad'):
    t=np.arange(int(sr*d))/sr
    if kind=='pad':
        s=sum(np.sin(2*np.pi*f*m*t+0.3*np.sin(2*np.pi*0.2*t))/m**1.6 for m in (1,2,3,4))
        env=np.minimum(1,t/0.8)*np.minimum(1,(d-t)/0.8)
    elif kind=='pl':
        s=sum(np.sin(2*np.pi*f*m*t)/m**2 for m in (1,2,3,5))
        env=np.exp(-t*3.2)*np.minimum(1,t/0.005)
    else: # kick-ish pulse
        s=np.sin(2*np.pi*(55+60*np.exp(-t*30))*t); env=np.exp(-t*9)
    return amp*s*env
def mtof(m): return 440*2**((m-69)/12)
def build(prog,dur,bpm,seed,out):
    rng=np.random.default_rng(seed)
    L=int(sr*dur); mix=np.zeros(L+sr*12)
    bar=4*60/bpm; t=0; i=0
    while t<dur:
        ch=prog[i%len(prog)]; p=int(t*sr)
        for m in ch: x=note(mtof(m),bar*1.05,.06); mix[p:p+len(x)]+=x
        x=note(mtof(ch[0]-12),bar,.08); mix[p:p+len(x)]+=x
        beat=60/bpm
        for k in range(8):
            q=p+int(k*beat/2*sr); m=ch[rng.integers(len(ch))]+12*(k%3==0)
            x=note(mtof(m+12),1.2,.05,'pl'); mix[q:q+len(x)]+=x
        if t>3:
            for k in range(4):
                q=p+int(k*beat*sr); x=note(0,.4,.18,'k'); mix[q:q+len(x)]+=x
        t+=bar; i+=1
    mix=mix[:L]; fade=int(sr*2.5); mix[-fade:]*=np.linspace(1,0,fade)
    # simple reverb
    for dly,g in ((0.11,.3),(0.23,.2),(0.37,.12)):
        d=int(dly*sr); mix[d:]+=g*mix[:-d]
    mix/=np.abs(mix).max()*1.1
    st=np.stack([mix,np.roll(mix,300)],1)
    w=wave.open(out,'wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((st*32767).astype(np.int16).tobytes());w.close()
# R16: A minor-ish, 92bpm ; R17: D minor, 84bpm
build([[57,60,64],[53,57,60],[48,52,55],[55,59,62]],37,92,1,'m16.wav')
build([[50,53,57],[46,50,53],[53,57,60],[48,52,55]],38,84,2,'m17.wav')
