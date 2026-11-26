// node render.js <html> <out.mp4> [stillsAt=comma list of seconds]
const {chromium}=require('playwright');const {spawn}=require('child_process');const path=require('path');
const [,,html,out,stills]=process.argv;const FPS=30;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(html));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const dur=await p.evaluate(()=>window.DUR);
if(stills){for(const s of stills.split(',')){await p.evaluate(t=>render(t),+s);await p.screenshot({path:out.replace('.mp4',`_f${s}.jpg`),type:'jpeg',quality:85});}await b.close();return;}
const ff=spawn('ffmpeg',['-loglevel','error','-y','-f','image2pipe','-framerate',''+FPS,'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out],{stdio:['pipe','inherit','inherit']});
const N=Math.round(dur*FPS);
for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/FPS);const buf=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('done',N);})();
