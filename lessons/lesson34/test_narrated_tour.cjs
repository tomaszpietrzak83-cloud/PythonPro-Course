/* Deterministic speech/lifecycle checks; no browser, sound or npm packages needed.
 * Run: node --test lessons/lesson34/test_narrated_tour.cjs
 */
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'static/narrated-tour.js'),'utf8');
const python=fs.readFileSync(path.join(__dirname,'examples/task07/main.py'),'utf8');

function harness({supported=true,initialVoices=[],provider='browser',request}={}){
  const elements=new Map(),timers=new Map(),listeners=new Map(),storage=new Map(),spoken=[];
  storage.set('l34-tour-provider',provider);
  const media=[];
  class AudioStub{constructor(url){this.url=url;this.paused=false;media.push(this);}play(){return Promise.resolve();}pause(){this.paused=true;}removeAttribute(){}load(){}}
  let timerId=0,voices=initialVoices,cancels=0;
  function element(selector){
    if(!elements.has(selector))elements.set(selector,{value:selector==='[data-tour-rate]'?'1':'',style:{},textContent:'',innerHTML:'',disabled:false,hidden:false,querySelector:()=>null,addEventListener:()=>{}});
    return elements.get(selector);
  }
  const root={querySelector:element,addEventListener:()=>{}};
  const synth={getVoices:()=>[...voices],speak:u=>spoken.push(u),cancel:()=>{cancels++;},resume:()=>{},addEventListener:(name,fn)=>listeners.set(name,fn),removeEventListener:(name,fn)=>{if(listeners.get(name)===fn)listeners.delete(name);}};
  class Utterance{constructor(text){this.text=text;}}
  const context=vm.createContext({
    window:supported?{speechSynthesis:synth,SpeechSynthesisUtterance:Utterance}:{},
    SpeechSynthesisUtterance:Utterance,document:{querySelector:()=>root,body:{classList:{add(){},remove(){},toggle(){}}}},
    localStorage:{getItem:key=>storage.get(key)||null,setItem:(key,v)=>storage.set(key,v)},
    setTimeout:fn=>{const id=++timerId;timers.set(id,fn);return id;},clearTimeout:id=>timers.delete(id),
    requestAnimationFrame:()=>1,cancelAnimationFrame:()=>{},ResizeObserver:class{observe(){}disconnect(){}},
    AbortController,DOMException,console,Audio:AudioStub,
  });
  vm.runInContext(source+'\nthis.tour=NarratedTour;',context);
  context.tour.setScript(JSON.parse(fs.readFileSync(path.join(__dirname,'static/narrated-script.json'),'utf8')));
  const lesson={steps:{source:python,rows:python.trimEnd().split('\n')}};
  let calls=0,signal;
  let resolveRun;
  const pending=new Promise(resolve=>{resolveRun=resolve;});
  context.tour.bind(lesson,'pl',{request,runDemo:s=>{calls++;signal=s;return pending;}});
  return {
    tour:context.tour,el:element,spoken,listeners,media,
    get calls(){return calls;},get signal(){return signal;},get cancels(){return cancels;},
    voices:items=>{voices=items;listeners.get('voiceschanged')?.();},
    click:selector=>element(selector).onclick(),
    seek:index=>element('[data-tour-step]').onchange({target:{value:String(index)}}),
    fire:()=>{const current=[...timers.values()];timers.clear();for(const fn of current)fn();},
    resolveRun,
  };
}
function verifiedRun(){return {status:'done',events:[
  {ws_direction:'receive',ws_client:'Anna',ws_body:'Ready'},
  {ws_direction:'receive',ws_client:'Jan',ws_body:'Ready'},
  {ws_direction:'send',ws_client:'Anna',ws_body:'Hello room'},
  {ws_direction:'receive',ws_client:'Anna',ws_body:'Hello room'},
  {ws_direction:'receive',ws_client:'Jan',ws_body:'Hello room'},
  {label:'Scenario verified',value:true},
]};}
const flush=()=>new Promise(resolve=>setImmediate(resolve));

test('voices may arrive late; selected voice and rate are passed to speech',()=>{
  const h=harness();
  assert.match(h.el('[data-tour-voices]').textContent,/nie podała jeszcze/);
  h.voices([{voiceURI:'polish',name:'Paulina',lang:'pl-PL',localService:true},{voiceURI:'english',name:'English',lang:'en-GB',localService:true}]);
  assert.match(h.el('[data-tour-voice]').innerHTML,/Paulina/);
  h.el('[data-tour-voice]').value='polish';h.el('[data-tour-rate]').value='1.2';
  h.click('[data-tour-play]');
  assert.equal(h.spoken[0].voice.voiceURI,'polish');assert.equal(h.spoken[0].rate,1.2);
  h.spoken[0].onend();h.fire();
  assert.equal(h.el('[data-tour-step]').value,'1');
  assert.match(h.el('[data-tour-scene]').innerHTML,/create_app/);
  h.tour.destroy();
});

test('pause blocks stale end callbacks; every source range resolves',()=>{
  const h=harness();h.click('[data-tour-play]');const stale=h.spoken[0].onend;
  h.click('[data-tour-play]');stale();h.fire();
  assert.equal(h.el('[data-tour-step]').value,'0');
  for(let i=1;i<=7;i++){h.seek(i);assert.match(h.el('[data-tour-scene]').innerHTML,/guided-row/);assert.doesNotMatch(h.el('[data-tour-status]').textContent,/Kod się zmienił/);}
  h.tour.destroy();
});

test('result narration waits for verified Python evidence and reuses one run',async()=>{
  const h=harness();h.seek(8);h.click('[data-tour-play]');
  assert.equal(h.calls,1);assert.equal(h.spoken.length,0);
  h.click('[data-tour-play]');h.click('[data-tour-play]');assert.equal(h.calls,1);
  h.resolveRun(verifiedRun());await flush();
  assert.equal(h.spoken.length,1);assert.match(h.el('[data-tour-scene]').innerHTML,/Hello room/);
  h.spoken[0].onend();h.fire();await flush();
  assert.equal(h.el('[data-tour-step]').value,'9');assert.equal(h.calls,1);
  h.tour.destroy();
});

test('leaving aborts owned run and removes voice listener',async()=>{
  const h=harness();h.seek(8);h.click('[data-tour-play]');
  h.tour.destroy();assert.equal(h.signal.aborted,true);assert.equal(h.listeners.size,0);
  h.resolveRun(verifiedRun());await flush();assert.equal(h.spoken.length,0);
});

test('failed evidence never gets a success narration',async()=>{
  const h=harness();h.seek(8);h.click('[data-tour-play]');
  h.resolveRun({status:'error',events:[]});await flush();
  assert.equal(h.spoken.length,0);assert.match(h.el('[data-tour-status]').textContent,/nie potwierdził/);
  h.tour.destroy();
});

test('missing speech support keeps manual frames and disables Play',()=>{
  const h=harness({supported:false});assert.equal(h.el('[data-tour-play]').disabled,true);
  h.seek(3);assert.match(h.el('[data-tour-scene]').innerHTML,/prepare/);h.tour.destroy();
});


test('ElevenLabs plays local MP3 and advances only after the audio ends',async()=>{
  const requests=[];
  const h=harness({provider:'elevenlabs',request:async(url,options)=>{
    requests.push({url,options});
    if(url.includes('/config'))return {configured:true,voices:[{id:'voice_test',name:'Polski głos',language:'pl'}]};
    return {url:'/api/narration/audio/'+'a'.repeat(64),cached:true};
  }});
  await flush();assert.equal(h.el('[data-tour-play]').disabled,false);
  h.click('[data-tour-play]');await flush();
  assert.equal(h.spoken.length,0);assert.equal(h.media.length,1);
  assert.equal(h.el('[data-tour-step]').value,'0');
  const payload=JSON.parse(requests[1].options.body);
  assert.deepEqual(payload,{language:'pl',step:0,voice_id:'voice_test'});
  h.media[0].onended();h.fire();await flush();
  assert.equal(h.el('[data-tour-step]').value,'1');assert.equal(h.media.length,2);
  h.tour.destroy();assert.equal(h.media[1].paused,true);
});

test('missing ElevenLabs key disables Play and explains local setup',async()=>{
  const h=harness({provider:'elevenlabs',request:async()=>({configured:false,voices:[],cached_available:false})});
  await flush();assert.equal(h.el('[data-tour-play]').disabled,true);
  assert.match(h.el('[data-tour-config]').textContent,/ELEVENLABS_API_KEY/);
  h.tour.destroy();
});
