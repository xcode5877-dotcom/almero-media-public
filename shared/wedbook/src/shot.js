const {chromium}=require('playwright');const S=process.argv[2];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(let i=1;i<=5;i++){await p.goto('file://'+S+'/carousel.html?s='+i);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(200);await p.screenshot({path:S+'/out/car_'+i+'.jpg',type:'jpeg',quality:92});}
await b.close();})();
