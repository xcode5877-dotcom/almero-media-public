const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const P=(t,a,b)=>clamp((t-a)/(b-a));
const eo=x=>1-Math.pow(1-x,3);
const eb=x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const $=s=>document.querySelector(s);
const $$=s=>[...document.querySelectorAll(s)];
function css(el,o){if(typeof el==='string')el=$(el);if(!el)return;Object.assign(el.style,o)}
// pop in at a..a+d, out at b..b+d (b optional)
function pop(el,t,a,d=.35,b=null,dy=40){let x=eb(P(t,a,a+d));let o=P(t,a,a+d*.6);if(b!==null){const q=P(t,b,b+d*.7);o*=1-q;x=x*(1-q)}
 css(el,{opacity:o,transform:`translateY(${(1-clamp(x,0,1.2))*dy}px) scale(${.85+.15*clamp(x,0,1.2)})`})}
