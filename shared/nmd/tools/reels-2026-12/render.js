// usage: node render.js page.html out.mp4 DURATION [fps] [--still t1,t2 outprefix]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const [html, out, durS, fpsS] = process.argv.slice(2);
  const still = process.argv.indexOf('--still');
  const dur = parseFloat(durS), fps = parseInt(fpsS || '30');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.evaluate(() => {
    document.getAnimations().forEach(a => a.pause());
    window.setT = (t) => {
      document.querySelectorAll('.scene').forEach(sc => {
        const s = +sc.dataset.s, e = +sc.dataset.e;
        const on = t >= s && t < e;
        sc.style.display = on ? 'block' : 'none';
        if (on) sc.getAnimations({ subtree: true }).forEach(a => { a.pause(); a.currentTime = (t - s) * 1000; });
      });
      document.querySelectorAll('.glob').forEach(g => g.getAnimations({ subtree: true }).forEach(a => { a.pause(); a.currentTime = t * 1000; }));
      if (window.onT) window.onT(t);
    };
  });
  if (still > 0) {
    const ts = process.argv[still + 1].split(',').map(Number), pre = process.argv[still + 2];
    for (const t of ts) { await p.evaluate(t => setT(t), t); await p.screenshot({ path: `${pre}_${t}.png` }); }
    await b.close(); return;
  }
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'ignore', 'inherit'] });
  const n = Math.round(dur * fps);
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => setT(t), i / fps);
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
})();
