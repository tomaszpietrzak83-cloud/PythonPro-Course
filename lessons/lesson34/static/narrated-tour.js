'use strict';
/* A narrated, frame-based tour. Playback advances on speech completion, not a clock. */
const NarratedTour = (() => {
  const escape = value => String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let script = [];
  let root=null,lesson=null,language='pl',host=null,voices=[],index=0,playing=false,serial=0,timer,utterance=null;
  let controller=null,runPromise=null,result=null,voiceListener=null,resizeObserver=null,positionFrame=null;
  let provider='elevenlabs',elevenConfig=null,configLoading=false,configError='',audio=null,audioAbort=null;
  const say=(pl,en)=>language==='pl'?pl:en;
  const text=value=>value[language==='pl'?0:1];
  const find=selector=>root?.querySelector(selector);
  const supported=()=> 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
  function html(lang) {
    const pl=lang==='pl';const label=(a,b)=>pl?a:b;
    return `<article class="page narrated-page" id="narrated-tour"><div class="tour-heading"><div><div class="eyebrow">${label('ZADANIE 07 · POKAZ Z LEKTOREM','TASK 07 · NARRATED TOUR')}</div><h2>${label('Prześledź broadcast z lektorem','Follow broadcast with narration')}</h2></div><span class="tour-badge">WebSocket · 12 ${label('klatek','frames')}</span></div><div class="tour-controls"><label>${label('Lektor','Narrator')}<select data-tour-provider aria-label="${label('Źródło lektora','Narrator source')}"><option value="elevenlabs">ElevenLabs · MP3</option><option value="browser">${label('Głos przeglądarki','Browser voice')}</option></select></label><label><span data-tour-voice-label>${label('Głos','Voice')}</span><select data-tour-voice aria-label="${label('Głos lektora','Narrator voice')}"></select></label><button data-tour-reload>${label('Odśwież głosy','Refresh voices')}</button><label>${label('Tempo','Rate')}<select data-tour-rate aria-label="${label('Tempo lektora','Narration rate')}"><option value="0.8">0.8×</option><option value="1" selected>1×</option><option value="1.2">1.2×</option><option value="1.5">1.5×</option></select></label><button class="primary" data-tour-play>▶ Play</button><button data-tour-focus>⛶ ${label('Skup pokaz / wróć','Focus tour / return')}</button><button data-tour-stop>■ ${label('Od początku','Restart')}</button></div><p class="tour-voice-info" data-tour-voices aria-live="polite"></p><p class="tour-eleven-config" data-tour-config aria-live="polite" hidden></p><div class="tour-navigation"><button data-tour-previous aria-label="${label('Poprzednia klatka','Previous frame')}">←</button><label>${label('Klatka','Frame')}<select data-tour-step aria-label="${label('Wybierz klatkę','Select frame')}"></select></label><button data-tour-next aria-label="${label('Następna klatka','Next frame')}">→</button><span data-tour-status role="status"></span></div><div class="tour-progress"><span data-tour-progress></span></div><div class="tour-stage"><div data-tour-scene></div><span class="tour-pointer" aria-hidden="true" hidden><svg viewBox="0 0 24 30" width="24" height="30"><path d="M2 2L21 17L12 18L9 27Z" fill="#edbd83" stroke="#17242c" stroke-width="2"/></svg></span></div><div class="tour-caption"><span data-tour-phase></span><h3 data-tour-title></h3><p data-tour-caption></p></div><small class="tour-footnote">${label('Najpierw wybierz głos, potem Play. Pauza zachowuje klatkę; wznowienie czyta ją od początku. Wyjście z zakładki zatrzymuje lektora.','Choose a voice, then Play. Pause keeps the frame; resume reads it from its beginning. Leaving the tab stops narration.')}</small></article>`;
  }
  function status(message){const el=find('[data-tour-status]');if(el)el.textContent=message;}
  function refreshVoices(){
    if(!root)return;
    if(provider==='elevenlabs'){elevenVoices();return;}
    find('[data-tour-config]').hidden=true;
    find('[data-tour-voice-label]').textContent=say('Głos przeglądarki','Browser voice');
    const select=find('[data-tour-voice]'),chosen=select.value||localStorage.getItem('l34-tour-voice');
    voices=supported()?window.speechSynthesis.getVoices():[];
    const locale=language==='pl'?'pl':'en';
    voices.sort((a,b)=>Number(!a.lang.toLowerCase().startsWith(locale))-Number(!b.lang.toLowerCase().startsWith(locale))||a.name.localeCompare(b.name));
    select.innerHTML=`<option value="">${say('Domyślny głos przeglądarki','Default browser voice')}</option>`+voices.map(v=>`<option value="${escape(v.voiceURI)}">${escape(v.name)} · ${escape(v.lang)}${v.localService?' · '+say('lokalny','local'):''}</option>`).join('');
    select.value=voices.some(v=>v.voiceURI===chosen)?chosen:(voices.find(v=>v.lang.toLowerCase().startsWith(locale))?.voiceURI||'');
    select.disabled=!supported()||playing;
    find('[data-tour-voices]').textContent=!supported()?say('Ta przeglądarka nie udostępnia lektora. Klatki i napisy możesz przeglądać ręcznie.','This browser has no speech synthesis. Browse frames and captions manually.'):voices.length?say(`Dostępne głosy: ${voices.length}. Głosy języka prezentacji są na początku listy.`,`Available voices: ${voices.length}. Presentation-language voices appear first.`):say('Przeglądarka nie podała jeszcze listy głosów. Możesz użyć domyślnego; lista uzupełni się po ich załadowaniu.','The browser has not supplied a voice list yet. You can use its default; the list updates when voices load.');
  }
  function controls(){
    if(!root)return;
    find('[data-tour-play]').textContent=playing?'Ⅱ '+say('Pauza','Pause'):'▶ '+(index===script.length-1?say('Odsłuchaj','Listen'):say('Odtwórz','Play'));
    find('[data-tour-play]').disabled=provider==='browser'?!supported():configLoading||(!elevenConfig?.configured&&!elevenConfig?.cached_available)||!find('[data-tour-voice]').value;
    find('[data-tour-voice]').disabled=playing||(provider==='browser'?!supported():configLoading);find('[data-tour-rate]').disabled=playing;
    find('[data-tour-provider]').disabled=playing;find('[data-tour-reload]').disabled=playing||configLoading;
    find('[data-tour-previous]').disabled=index===0;find('[data-tour-next]').disabled=index===script.length-1;
    find('[data-tour-step]').value=String(index);find('[data-tour-progress]').style.width=`${(index+1)/script.length*100}%`;
  }
  function cancelSpeech(){serial++;clearTimeout(timer);audioAbort?.abort();audioAbort=null;if(audio){audio.onended=null;audio.onerror=null;audio.pause();audio.removeAttribute('src');audio.load();audio=null;}if(utterance){utterance.onend=null;utterance.onerror=null;utterance=null;if(supported())window.speechSynthesis.cancel();}}
  function pause(){playing=false;cancelSpeech();controls();status(say('Pauza · wznowienie powtórzy klatkę','Paused · resume repeats the frame'));}
  function seek(next){pause();index=Math.max(0,Math.min(script.length-1,next));paint();status(say('Wybierz Play, aby odsłuchać klatkę','Choose Play to hear this frame'));}
  function point(){
    if(!root)return;
    const stage=find('.tour-stage'),cursor=find('.tour-pointer'),target=stage.querySelector('[data-tour-point]');
    cursor.hidden=!target;if(!target)return;
    const a=stage.getBoundingClientRect(),b=target.getBoundingClientRect();
    cursor.style.transform=`translate(${Math.max(4,b.left-a.left+5)}px,${Math.max(4,b.top-a.top+Math.min(12,b.height/2))}px)`;
  }
  function range(step){
    const lines=lesson.steps.source.split('\n');const start=lines.findIndex(line=>line.trim().startsWith(step.needle));
    if(start<0)throw new Error(say('Kod się zmienił. Zaktualizuj scenariusz lektora.','Source changed. Update the narration script.'));
    const delta=step.end?lines.slice(start).findIndex(line=>line.trim().startsWith(step.end)):0;
    if(delta<0)throw new Error(say('Nie znaleziono końca omawianego bloku.','Narrated block end was not found.'));
    return [start,start+delta];
  }
  function codeScene(step){
    const [start,end]=range(step);
    return `<div class="editor tour-editor"><div class="editor-head"><span>main.py</span><span>L${start+1}${end>start?'–'+(end+1):''}</span></div><div class="code">${lesson.steps.rows.map((row,i)=>`<div class="code-row guided-row ${i>=start&&i<=end?'is-current':''}" ${i===start?'data-tour-point':''}><span class="ln">${i+1}</span><span class="src">${row||' '}</span></div>`).join('')}</div></div>`;
  }
  function evidence(){
    const events=result?.events||[];
    const wires=events.filter(e=>e.ws_direction);
    if(result?.status!=='done'||!events.some(e=>e.label==='Scenario verified'&&e.value===true))throw new Error(say('Pokaz nie potwierdził wyniku. Zobacz dziennik w Obserwuj działanie.','Demo did not verify its result. See Observe execution logs.'));
    const outgoing=wires.filter(e=>e.ws_direction==='send');
    if(outgoing.length!==1)throw new Error(say('Nieoczekiwany przebieg: oczekiwano jednego wysłania.','Unexpected trace: expected one outgoing message.'));
    const body=outgoing[0].ws_body;
    const recipients=wires.filter(e=>e.ws_direction==='receive'&&e.ws_body===body);
    if(new Set(recipients.map(e=>e.ws_client)).size!==2)throw new Error(say('Nie potwierdzono odbioru przez dwóch klientów.','Delivery to two clients was not verified.'));
    return {wires,body,recipients};
  }
  function demoScene(step){
    if(!result)return `<div class="tour-wait"><strong>${say('Obserwuj działanie','Observe execution')}</strong><p>${say('Play uruchomi prawdziwy serwer i klientów. Narracja o wynikach zacznie się dopiero po ich otrzymaniu.','Play starts a real server and clients. Result narration begins only after receiving evidence.')}</p></div>`;
    const {wires,body,recipients}=evidence();
    const selected=e=>step.phase==='ready'?(e.ws_direction==='connect'||e.ws_body==='Ready'):step.phase==='send'?e.ws_direction==='send':e.ws_direction==='receive'&&e.ws_body===body;
    let first=true;
    return `<div class="tour-evidence"><div class="tour-evidence-head"><strong>${say('Obserwuj działanie · zapis prawdziwego pokazu','Observe execution · actual recorded run')}</strong><span>✓ ${say('Potwierdzony','Verified')} · ${recipients.length} ${say('odbiorców','recipients')}</span></div><div class="tour-messages">${wires.map(e=>{const active=selected(e),pointer=active&&first; if(pointer)first=false;return `<div class="tour-message ${active?'is-current':''}" ${pointer?'data-tour-point':''}><span>${escape(e.ws_client)}</span><b>${e.ws_direction==='connect'?say('Połączono','Connected'):e.ws_direction==='send'?say('Klient → serwer','Client → server'):say('Serwer → klient','Server → client')}</b><code>${escape(typeof e.ws_body==='string'?e.ws_body:JSON.stringify(e.ws_body))}</code></div>`;}).join('')}</div></div>`;
  }
  function paint(){
    if(!root)return;
    const step=script[index];controls();
    find('[data-tour-title]').textContent=text(step.title);find('[data-tour-caption]').textContent=step.kind==='demo'&&!result?say('Naciśnij Play, aby uruchomić pokaz. Na wyniki i ich omówienie poczekamy do zakończenia rzeczywistego wykonania.','Press Play to run the demo. We wait for actual execution to finish before showing and discussing results.'):text(step.text);
    find('[data-tour-phase]').textContent=`${index+1} / ${script.length} · ${step.kind==='code'?say('Zrozum kod','Understand code'):step.kind==='demo'?say('Obserwuj działanie','Observe execution'):step.kind==='intro'?say('Wstęp','Introduction'):say('Podsumowanie','Summary')}`;
    const scene=find('[data-tour-scene]');
    try{
      scene.innerHTML=step.kind==='code'?codeScene(step):step.kind==='demo'?demoScene(step):`<div class="tour-overview"><span class="tour-step-mark">${step.kind==='intro'?'01 → 02':'✓'}</span><h3 data-tour-point>${text(step.title)}</h3><div class="tour-flow"><span>Anna</span><span>→</span><strong>WebSocket<br>broadcast</strong><span>→</span><span>Anna + Jan</span></div><p>${step.kind==='intro'?say('Wstęp → kod → prawdziwy pokaz → wynik','Introduction → code → real demo → result'):say('prepare → add → async for → broadcast → finally','prepare → add → async for → broadcast → finally')}</p></div>`;
      const scroll=scene.querySelector('.code')||scene.querySelector('.tour-messages'),row=scene.querySelector('[data-tour-point]');
      if(scroll&&row)scroll.scrollTop=Math.max(0,scroll.scrollTop+row.getBoundingClientRect().top-scroll.getBoundingClientRect().top-55);
      cancelAnimationFrame(positionFrame);positionFrame=requestAnimationFrame(point);
    }catch(error){pause();status(error.message);}
  }
  function speak(){
    if(!root||!playing)return;
    cancelSpeech();const ticket=serial;
    utterance=new SpeechSynthesisUtterance(text(script[index].text));
    const voice=voices.find(v=>v.voiceURI===find('[data-tour-voice]').value);
    if(voice)utterance.voice=voice;
    utterance.lang=voice?.lang||(language==='pl'?'pl-PL':'en-US');utterance.rate=Number(find('[data-tour-rate]').value);
    utterance.onend=()=>{if(ticket!==serial)return;utterance=null;finished(ticket);};
    utterance.onerror=event=>{
      if(ticket!==serial)return;
      pause();status(say('Nie udało się odtworzyć głosu. Wybierz inny głos i naciśnij Play. Kod: ','Speech failed. Choose another voice and press Play. Code: ')+event.error);
    };
    status(say('Lektor mówi…','Narrating…'));
    window.speechSynthesis.resume();window.speechSynthesis.speak(utterance);
  }
  function finished(ticket){
    if(ticket!==serial||!playing||!root)return;
    if(index===script.length-1){playing=false;controls();status(say('Koniec pokazu','Tour complete'));return;}
    timer=setTimeout(()=>{if(ticket!==serial||!playing||!root)return;index++;paint();playFrame();},650);
  }
  function elevenVoices(){
    const select=find('[data-tour-voice]'),chosen=localStorage.getItem('l34-eleven-voice')||elevenConfig?.default_voice_id;
    find('[data-tour-voice-label]').textContent=say('Głos ElevenLabs','ElevenLabs voice');
    const options=[...(elevenConfig?.voices||[])].filter(v=>v.language?.toLowerCase().split('-')[0]===language);
    options.sort((a,b)=>Number(a.language!==language)-Number(b.language!==language)||a.name.localeCompare(b.name));
    select.innerHTML=options.length?options.map(v=>`<option value="${escape(v.id)}">${escape(v.name)}${v.language?' · '+say('głos źródłowy: ','source voice: ')+escape(v.language):''}</option>`).join(''):`<option value="">${say('Brak głosów dla tego języka','No voices for this language')}</option>`;
    select.value=options.some(v=>v.id===chosen)?chosen:(options.some(v=>v.id===elevenConfig?.default_voice_id)?elevenConfig.default_voice_id:(options[0]?.id||''));
    const info=find('[data-tour-config]');info.hidden=false;
    info.textContent=configLoading?say('Wczytuję głosy ElevenLabs…','Loading ElevenLabs voices…'):configError||(!elevenConfig?.configured&&!elevenConfig?.cached_available?say('Dodaj ELEVENLABS_API_KEY do lessons/lesson34/.env, zapisz plik i kliknij Odśwież głosy.','Add ELEVENLABS_API_KEY to lessons/lesson34/.env, save and click Refresh voices.'):say('ElevenLabs: pierwsze Play generuje MP3 bieżącej klatki, korzystając z limitu konta. Kolejne odtworzenia używają lokalnego pliku.','ElevenLabs: first Play generates this frame’s MP3 using your account allowance. Replays use the local file.'));
    find('[data-tour-voices]').textContent=options.length?say(`Dostępne głosy ElevenLabs: ${options.length}.`,`Available ElevenLabs voices: ${options.length}.`):'';
  }
  async function refreshEleven(){
    const mounted=root;if(!mounted)return;
    configLoading=true;configError='';refreshVoices();controls();
    try{
      if(!host.request)throw new Error(say('Brak połączenia z API lektora.','Narration API connection missing.'));
      const data=await host.request('/api/narration/config?refresh=1&language='+language);
      if(root!==mounted)return;
      elevenConfig=data;
    }catch(error){
      if(root!==mounted)return;
      elevenConfig=null;configError=error.message;
    }finally{if(root===mounted){configLoading=false;refreshVoices();controls();}}
  }
  async function speakEleven(){
    if(!root||!playing)return;
    cancelSpeech();const ticket=serial;audioAbort=new AbortController();
    status(say('Przygotowuję nagranie ElevenLabs…','Preparing ElevenLabs audio…'));
    try{
      const clip=await host.request('/api/narration/generate',{method:'POST',signal:audioAbort.signal,body:JSON.stringify({language,step:index,voice_id:find('[data-tour-voice]').value})});
      if(!root||!playing||ticket!==serial)return;
      if(!/^\/api\/narration\/audio\/[0-9a-f]{64}$/.test(clip.url))throw new Error(say('Nieprawidłowy adres nagrania.','Invalid audio URL.'));
      audio=new Audio(clip.url);audio.playbackRate=Number(find('[data-tour-rate]').value);audio.preservesPitch=true;
      audio.onended=()=>{if(ticket!==serial)return;audio=null;finished(ticket);};
      audio.onerror=()=>{if(ticket!==serial)return;pause();status(say('Nie można odtworzyć MP3. Spróbuj ponownie.','Cannot play MP3. Try again.'));};
      await audio.play();
      if(ticket===serial&&root)status(clip.cached?say('ElevenLabs · lokalne MP3','ElevenLabs · local MP3'):say('ElevenLabs · nowe nagranie zapisane','ElevenLabs · new recording saved'));
    }catch(error){
      if(!root||ticket!==serial||error.name==='AbortError')return;
      pause();status(error.name==='NotAllowedError'?say('Nagranie gotowe. Naciśnij Play jeszcze raz, aby przeglądarka odtworzyła dźwięk.','Audio is ready. Press Play again to allow playback.'):error.message);
    }
  }
  async function playFrame(){
    if(!root||!playing)return;
    const ticket=serial;
    if(script[index].kind==='demo'&&!result){
      status(say('Uruchamiam lokalnego Pythona. Czekam na prawdziwy wynik…','Starting local Python. Waiting for actual results…'));
      try{
        if(!runPromise){controller=new AbortController();runPromise=host.runDemo(controller.signal);}
        const pending=runPromise;
        const data=await pending;
        if(!root||runPromise!==pending)return;
        result=data;evidence();
        if(ticket!==serial||!playing)return;
        paint();
      }catch(error){
        if(!root||ticket!==serial||error.name==='AbortError')return;
        runPromise=null;result=null;pause();status(error.message);return;
      }
    }
    if(provider==='elevenlabs')await speakEleven();else speak();
  }
  function bind(data,lang,callbacks){
    destroy();root=document.querySelector('#narrated-tour');if(!root)return;
    lesson=data;language=lang;host=callbacks;provider=localStorage.getItem('l34-tour-provider')||'elevenlabs';elevenConfig=null;configError='';configLoading=false;index=0;result=null;runPromise=null;playing=false;
    find('[data-tour-step]').innerHTML=script.map((s,i)=>`<option value="${i}">${String(i+1).padStart(2,'0')} · ${escape(text(s.title))}</option>`).join('');
    find('[data-tour-step]').onchange=e=>seek(Number(e.target.value));
    find('[data-tour-previous]').onclick=()=>seek(index-1);find('[data-tour-next]').onclick=()=>seek(index+1);
    find('[data-tour-stop]').onclick=()=>{pause();controller?.abort();controller=null;runPromise=null;result=null;index=0;paint();status(say('Gotowe od początku','Ready from beginning'));};
    find('[data-tour-play]').onclick=()=>{if(playing){pause();return;}document.body.classList.add('tour-focused');playing=true;controls();playFrame();};
    find('[data-tour-focus]').onclick=()=>document.body.classList.toggle('tour-focused');
    find('[data-tour-provider]').value=provider;
    find('[data-tour-provider]').onchange=e=>{pause();provider=e.target.value;localStorage.setItem('l34-tour-provider',provider);if(provider==='elevenlabs')refreshEleven();else{refreshVoices();controls();}};
    find('[data-tour-reload]').onclick=()=>provider==='elevenlabs'?refreshEleven():refreshVoices();
    find('[data-tour-voice]').onchange=e=>{localStorage.setItem(provider==='elevenlabs'?'l34-eleven-voice':'l34-tour-voice',e.target.value);controls();};
    find('[data-tour-rate]').value=localStorage.getItem('l34-tour-rate')||'1';
    find('[data-tour-rate]').onchange=e=>localStorage.setItem('l34-tour-rate',e.target.value);
    if(supported()){voiceListener=refreshVoices;window.speechSynthesis.addEventListener('voiceschanged',voiceListener);}
    resizeObserver=new ResizeObserver(point);resizeObserver.observe(find('.tour-stage'));
    root.addEventListener('scroll',point,true);refreshVoices();paint();if(provider==='elevenlabs')refreshEleven();status(say('Wybierz głos i naciśnij Play','Choose a voice and press Play'));
  }
  function destroy(){
    document.body.classList.remove('tour-focused');
    playing=false;cancelSpeech();controller?.abort();controller=null;
    if(voiceListener&&supported())window.speechSynthesis.removeEventListener('voiceschanged',voiceListener);
    voiceListener=null;resizeObserver?.disconnect();resizeObserver=null;cancelAnimationFrame(positionFrame);root=null;result=null;runPromise=null;
  }
  return {html,bind,destroy,setScript:steps=>{script=steps;}};
})();
