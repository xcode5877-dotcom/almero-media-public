# python3 music.py out.wav duration "hit1,hit2,..." seed
import sys, numpy as np, wave
out, dur, hits, seed = sys.argv[1], float(sys.argv[2]), [float(x) for x in sys.argv[3].split(',') if x], int(sys.argv[4])
sr = 44100; n = int(sr*dur); t = np.arange(n)/sr
rng = np.random.default_rng(seed)
bpm = 104; beat = 60/bpm
def note(f): return 440*2**((f-69)/12)
# progression (C major-ish, warm): C - G - Am - F, 2 beats each... 1 bar each
prog = [[60,64,67,72],[55,62,67,71],[57,60,64,69],[53,60,65,69]]
mix = np.zeros(n)
bar = beat*4
# pad
for i in range(int(dur/bar)+1):
    ch = prog[i % 4]; s = int(i*bar*sr); e = min(n, int((i+1)*bar*sr)+int(.3*sr))
    if s >= n: break
    tt = np.arange(e-s)/sr; env = np.minimum(1, tt/.25)*np.exp(-tt*.25)
    for m in ch[:3]:
        f = note(m-12)
        mix[s:e] += .05*env*(np.sin(2*np.pi*f*tt)+.3*np.sin(2*np.pi*2*f*tt+.2)+.15*np.sin(2*np.pi*3.01*f*tt))
# pluck arpeggio 8ths
step = beat/2; k = 0
while k*step < dur:
    s = int(k*step*sr); ch = prog[int(k*step/bar) % 4]; m = ch[[0,1,2,3,2,1,2,3][k % 8]]+12
    f = note(m); L = int(.6*sr); e = min(n, s+L); tt = np.arange(e-s)/sr
    env = np.exp(-tt*7)
    mix[s:e] += .07*env*(np.sin(2*np.pi*f*tt)+.4*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*12))
    k += 1
# soft kick on beats + clap on 2/4 after first 2 s
k = 0
while k*beat < dur:
    s = int(k*beat*sr)
    if k*beat >= 1.15:
        L = int(.25*sr); e = min(n, s+L); tt = np.arange(e-s)/sr
        f = 50+60*np.exp(-tt*30); mix[s:e] += .22*np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tt*14)
        if k % 2 == 1:
            L2 = int(.18*sr); e2 = min(n, s+L2); tt2 = np.arange(e2-s)/sr
            mix[s:e2] += .06*rng.standard_normal(e2-s)*np.exp(-tt2*25)
    # shaker 16ths
    for q in (0.25, 0.75):
        s2 = int((k+q)*beat*sr); L = int(.05*sr)
        if s2+L < n and (k+q)*beat > 1.15: mix[s2:s2+L] += .015*rng.standard_normal(L)*np.exp(-np.arange(L)/sr*80)
    k += 1
# whoosh + chime at hits
for h in hits:
    s = int(max(0, h-.35)*sr); L = int(.45*sr); e = min(n, s+L)
    if e > s:
        nz = rng.standard_normal(e-s); tt = np.arange(e-s)/sr
        env = np.sin(np.pi*tt/.45)**2
        # crude lowpass sweep
        y = np.zeros_like(nz); a = 0.0
        for i in range(len(nz)):
            c = .02+.25*(i/len(nz)); a += c*(nz[i]-a); y[i] = a
        mix[s:e] += .25*env*y
    s = int(h*sr); L = int(1.2*sr); e = min(n, s+L); tt = np.arange(e-s)/sr
    for f in (note(84), note(91)):
        mix[s:e] += .05*np.sin(2*np.pi*f*tt)*np.exp(-tt*4)
# fades
fi = int(.05*sr); fo = int(1.2*sr)
mix[:fi] *= np.linspace(0, 1, fi); mix[-fo:] *= np.linspace(1, 0, fo)
mix = np.tanh(mix*1.4)/1.1
st = np.stack([mix, mix], 1)
st = (st/np.max(np.abs(st))*.9*32767).astype(np.int16)
w = wave.open(out, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(st.tobytes()); w.close()
print('ok', out)
