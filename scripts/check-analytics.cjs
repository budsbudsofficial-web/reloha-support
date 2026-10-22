const vm = require('node:vm');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const code = fs.readFileSync('assets/analytics.js','utf8');
function run({path='/reloha-support/guide/watering-when/',phone=false,narrow=false,search='',frame=false,entry=null}={}) {
  const tags=[],events={};
  const window={dataLayer:[],matchMedia:()=>({matches:narrow}),sessionStorage:{getItem:()=>entry&&JSON.stringify(entry),removeItem:()=>{}}};
  window.self=window;window.top=frame?{}:window;
  const context={window,document:{head:{appendChild:x=>tags.push(x)},createElement:()=>({}),addEventListener:(e,f)=>events[e]=f},location:{pathname:path,search,href:'https://budsbudsofficial-web.github.io'+path},navigator:{userAgent:phone?'iPhone':'Desktop'},URL,URLSearchParams,Date};
  vm.runInNewContext(code,context);vm.runInNewContext(code,context);
  return {window,tags,events};
}
let r=run();assert.equal(r.tags.length,1);assert.equal(r.window.dataLayer.filter(x=>x[0]==='config').length,1);
for(const opts of [{frame:true},{path:'/reloha-support/',phone:true},{path:'/reloha-support/',narrow:true}]) assert.equal(run(opts).tags.length,0);
assert.equal(run({path:'/reloha-support/',phone:true,narrow:true,search:'?desktop=1'}).tags.length,1);
assert.equal(run({path:'/reloha-support/mobile/',phone:true,narrow:true}).tags.length,1);
let link={href:'https://apps.apple.com/jp/app/reloha/id6813563330?utm_source=test',closest:()=>({})};
r.events.click({target:{closest:()=>link}});
assert.equal(r.window.dataLayer.filter(x=>x[0]==='event'&&x[1]==='app_store_click').length,1);
link.href='https://example.com/id6813563330';r.events.click({target:{closest:()=>link}});
assert.equal(r.window.dataLayer.filter(x=>x[0]==='event').length,1);
console.log('Analytics checks passed: initialization, redirects, iframe exclusion, App Store filtering.');

r=run({path:'/reloha-support/mobile/',entry:{value:'https://www.google.com/',time:Date.now()}});assert.equal(r.window.dataLayer.find(x=>x[0]==='config')[2].page_referrer,'https://www.google.com/');
r=run({path:'/reloha-support/mobile/',entry:{value:'https://www.google.com/',time:Date.now()-120000}});assert.equal(r.window.dataLayer.find(x=>x[0]==='config')[2].page_referrer,undefined);
console.log('Mobile original-referrer and expiry checks passed.');
