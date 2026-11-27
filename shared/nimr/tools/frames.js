const {chromium}=require('playwright');
const [,,file,dur,out]=process.argv;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/'+file);await p.evaluate(()=>document.fonts.ready);
require('fs').mkdirSync(out,{recursive:true});
const N=Math.round(+dur*30);
for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/30);await p.screenshot({path:`${out}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:90});}
await b.close();})();
