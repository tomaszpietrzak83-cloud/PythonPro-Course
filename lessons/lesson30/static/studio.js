'use strict';
const $ = (s, root = document) => root.querySelector(s);
const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let language = localStorage.getItem('l30-language') || 'pl';
let continuous = localStorage.getItem('l30-mode') === 'continuous';
let large = localStorage.getItem('l30-large') === '1';
let lessons = [], current = null, section = 0, pageIndex = 0;
let codeCache = new Map(), histories = {}, selectedRuns = {}, activeRun = null;
let replay = {}, replayTimer = null, resourceState = null;
let controls = {};
const words = (pl, en) => language === 'pl' ? pl : en;
const t = item => item[language];
const names = () => [words('Treść zadania','Assignment'),words('Wstęp','Introduction'), words('Obserwuj działanie','Observe execution'), words('Zrozum kod','Understand code'), words('Cały kod','Full code'), words('Pytania','Questions')];
function toast(text) { const el = $('#toast'); el.textContent = text; el.hidden = false; setTimeout(() => el.hidden = true, 6000); }
async function api(url, options = {}) {
  const csrf = document.cookie.split('; ').find(v => v.startsWith('csrftoken='))?.split('=')[1];
  const response = await fetch(url, {cache:'no-store',...options, headers: {'Content-Type':'application/json', 'X-CSRFToken':csrf || '', ...(options.headers || {})}});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data;
}
function preferences() {
  document.documentElement.lang = language;
  document.documentElement.style.setProperty('--font', large ? '23px' : '20px');
  document.body.classList.toggle('continuous', continuous);
  document.body.classList.toggle('slide-task',!!current&&!continuous);
  document.body.classList.toggle('large-text',large);
  document.querySelectorAll('[data-lang]').forEach(b => b.classList.toggle('active', b.dataset.lang === language));
  $('#mode').textContent = continuous ? words('Tryb ciągły','Continuous') : words('Slajdy','Slides');
  $('#drawer-title').textContent = words('Wybierz eksperyment','Choose an experiment');
  $('#task-list').innerHTML = lessons.map(l => `<button data-task="${l.number}" class="${current?.number === l.number ? 'active' : ''}">${String(l.number).padStart(2,'0')} · ${esc(t(l.title))}</button>`).join('');
}
function catalog() {
  current = null; preferences();
  $('#main').innerHTML = `<div class="catalog-hero"><div><div class="eyebrow">${words('LEKCJA 30 · LABORATORIUM WSPÓŁBIEŻNOŚCI','LESSON 30 · CONCURRENCY LAB')}</div><h1>${words('Zobacz, jak kod<br>działa razem.','See how code<br>works together.')}</h1><p>${words('Wątki, procesy i GIL — od pierwszego uruchomienia do zrozumienia mechanizmu. Wybierz eksperyment, przewidź wynik i sprawdź go na żywo.','Threads, processes and the GIL — from the first run to understanding the mechanism. Choose an experiment, predict the result and test it live.')}</p></div><div class="orbital" aria-hidden="true"><span>thread → process → result</span></div></div>
  <div class="catalog-intro"><div><div class="eyebrow">${words('20 OSOBNYCH CELÓW NAUKI','20 DISTINCT LEARNING GOALS')}</div><p>${words('Gotowe dane. Rzeczywiste wykonanie. Kod objaśniony krok po kroku.','Prepared inputs. Real execution. Code explained step by step.')}</p></div><button id="open-guide">${words('Jak prezentować?','How to present?')}</button></div>
  <div class="catalog-grid">${lessons.map(l => `<button class="tile" data-task="${l.number}"><span class="num">${String(l.number).padStart(2,'0')} / ${l.number < 9 ? words('PODSTAWY','FOUNDATIONS') : words('PRAKTYKA','PRACTICE')}</span><strong>${esc(t(l.title))}</strong><span class="arrow">↗</span></button>`).join('')}</div>
  <div class="callout">${words('Domyślnie kod działa w lokalnym Pythonie. Docker jest opcjonalnym środowiskiem dla przykładów, z limitem 2 CPU i 2 GB RAM. Przed jego wyborem uruchom Docker Desktop i zbuduj obraz zgodnie z README.','By default code runs in local Python. Docker is an optional example environment limited to 2 CPUs and 2 GB RAM. Start Docker Desktop and build the image as described in README before selecting it.')}</div>`;
  $('#open-guide').onclick = () => {
    $('#resources-body').innerHTML = `<p>${words('1. Przeczytaj wstęp i przewidź wynik. 2. Uruchom gotowy wariant. 3. Wskaż różnicę na osi czasu lub w wynikach. 4. Przejdź od bloku do instrukcji kodu. 5. Odpowiedz na pytanie własnymi słowami.','1. Read the introduction and predict the result. 2. Run the prepared variant. 3. Point to a difference in the timeline or results. 4. Move from blocks to code statements. 5. Answer the question in your own words.')}</p><p>${words('Strzałki ← → zmieniają slajdy. ⛶ otwiera pełny ekran. A+ powiększa tekst. Zwykły pokaz nie wymaga wpisywania danych.','Arrow keys ← → change slides. ⛶ opens fullscreen. A+ enlarges text. A normal demonstration requires no typing.')}</p><p>${words('Oś czasu pochodzi ze zdarzeń Pythona, nie z odgadywanych statusów. Odtwarzanie pozwala wrócić do zapisanego przebiegu; nie zatrzymuje pracującego programu.','The timeline comes from Python events, not inferred statuses. Replay revisits a recording; it does not pause the running program.')}</p>`;
    $('#resource-dialog').showModal();
  };
}
function explanationPages() {
  const pages = [];
  for (const step of current.steps.steps) {
    if (step.details.length === 0) {
      pages.push({...step, kind:step.start===step.end ? 'line' : 'block'});
      continue;
    }
    pages.push({...step, kind:'block'});
    for (const detail of step.details) pages.push({...detail, id:step.id, kind:'line'});
  }
  return pages;
}
function countPages(s = section) { return s === 0 ? current.assignment.pages[language].length : s === 3 ? explanationPages().length : 1; }
function assignmentHTML(index) {
  const assignment = current.assignment;
  const inline = value => esc(value).replace(/`([^`]+)`/g,'<code>$1</code>');
  const blocks = assignment.pages[language][index];
  const content = blocks.map(block => {
    if(block.kind==='code')return `<pre class="assignment-code"><code>${esc(block.text)}</code></pre>`;
    if(block.kind==='list'){const tag=block.ordered?'ol':'ul';return `<${tag}>${block.items.map(item=>`<li>${inline(item)}</li>`).join('')}</${tag}>`;}
    return `<p class="${block.kind==='note'?'assignment-note':''}">${inline(block.text)}</p>`;
  }).join('');
  return `<article class="page assignment-page"><div class="eyebrow">${words('POLECENIE · LEKCJA 30','REQUIREMENTS · LESSON 30')}</div><h2>${words('Co masz wykonać?','What do you need to build?')}</h2><div class="assignment-content">${content}</div><div class="assignment-meta">${words('Źródło: tasks.md. Nazwy w kodzie i komunikaty zapisano po angielsku.','Source: tasks.md. Code names and program messages are in English.')}</div>${assignment.adaptation && index===assignment.pages[language].length-1 ? `<details class="assignment-adaptation"><summary>${words('Dostosowanie do pokazu w aplikacji','Adaptation for the app demonstration')}</summary><p>${esc(t(assignment.adaptation))}</p></details>`:''}</article>`;
}
function introHTML() {
  return `<article class="page"><div class="eyebrow">${words('JEDEN NOWY MECHANIZM','ONE NEW MECHANISM')}</div><div class="intro-grid"><div><h2>${esc(t(current.title))}</h2><p class="lead">${esc(t(current.intro))}</p></div><div class="number-emblem">${String(current.number).padStart(2,'0')}</div></div><div class="terms">${(current.terms||[]).map(term=>`<div><h3>${esc(term.name)}</h3><p>${esc(t(term.body))}</p></div>`).join('')}</div><button class="primary" data-go="2">${words('Przejdź do obserwacji →','Observe execution →')}</button></article>`;
}
function demoHTML() {
  const editable = Object.keys(current.presets[0].value).length > 0;
  const history = histories[current.number] || [];
  return `<article class="page"><div class="eyebrow">${words('RZECZYWISTY PYTHON · GOTOWE DANE','REAL PYTHON · PREPARED INPUTS')}</div><h2>${words('Najpierw zobacz różnicę','See the difference first')}</h2><p>${esc(t(current.watch))}</p>
    <div class="controlbar"><label>${words('Gotowy wariant','Prepared variant')}<select id="preset">${current.presets.map((p,i) => `<option value="${i}">${esc(p.label)}</option>`).join('')}</select></label><label>${words('Środowisko','Environment')}<select id="backend"><option value="native">${words('Lokalny Python','Local Python')}</option><option value="docker">Docker · 2 CPU / 2 GB</option></select></label><button id="run" class="primary">▶ ${words('Uruchom pokaz','Run demonstration')}</button><button id="cancel" hidden>■ ${words('Zatrzymaj','Stop')}</button>${editable ? `<button id="custom-toggle" class="quiet">${words('Własne dane…','Custom inputs…')}</button><div id="custom" class="custom" hidden></div>` : ''}</div>
    <div id="docker-note" class="callout" hidden>${words('Włącz Docker Desktop. Wymagany obraz lesson30-python:local (budowanie opisano w README). Kontener jest usuwany po pokazie; ma 2 CPU, 2 GB RAM i własną pamięć. Docker wykorzystuje zasoby Twojego komputera.','Start Docker Desktop. Requires lesson30-python:local (see README to build). The container is removed after the demonstration; it has 2 CPUs, 2 GB RAM and separate memory. Docker uses your computer resources.')}</div>
    ${current.number === 20 ? `<div class="axis-note">${words('Wariant 1000×1000 może zużyć ponad 1 GB i trwać dłużej. Mierzony czas obejmuje start i transfer obrazów.','The 1000×1000 variant may use over 1 GB and take longer. Timing includes startup and image transfer.')}</div>` : ''}
    <div id="history" class="history">${history.map((r,i) => `<button data-history="${r.id}" class="${selectedRuns[current.number] === r.id ? 'active' : ''}">${words('Pokaz','Run')} ${i+1} · ${esc(r.presetLabel)} · ${esc(r.backend)}</button>`).join('')}</div>
    <div class="dashboard"><div class="dashboard-heading"><h3>${words('Ślad wykonania','Execution trace')}</h3><span id="run-state" class="state">${words('Gotowe do startu','Ready')}</span><button id="focus-stop" hidden>■ ${words("Zatrzymaj","Stop")}</button><button id="focus-rerun" hidden>▶ ${words("Powtórz","Run again")}</button><button id="focus-observation" class="quiet">${words('⛶ Skup widok / wróć','⛶ Focus view / return')}</button></div><div id="visual"><div class="empty">${words('Uruchom pokaz. Tutaj pojawią się rzeczywiste zdarzenia programu.','Run the demonstration. Actual program events will appear here.')}</div></div><div id="replay-controls"></div><div id="metrics" class="metrics"></div><div id="balance"></div><details id="log-details"><summary>${words('Dziennik zdarzeń · czas, uczestnik i PID','Event log · time, participant and PID')}</summary><div id="log" class="log"></div></details></div>
    <div id="interpretation" hidden><h3>${words('Jak odczytać wynik?','How to read the result')}</h3><p>${esc(t(current.takeaway))}</p></div><details><summary>${words('Warunki i granice tego eksperymentu','Experiment conditions and limits')}</summary><p>${esc(t(current.caveat))}</p></details></article>`;
}
function editorHTML(rows, start, end, full = false, file = current.steps.file) {
  return `<div class="editor ${full ? 'full' : ''}"><div class="editor-head"><span>${esc(file)}</span><span>${start ? `L${start}${end > start ? '–'+end : ''}` : words('kod źródłowy','source code')}</span></div><div class="code">${rows.map((row, i) => `<div class="code-row ${start ? i+1 >= start && i+1 <= end ? 'focus' : 'dim' : ''}" data-line="${i+1}"><span class="ln">${i+1}</span><span class="src">${row || ' '}</span></div>`).join('')}</div></div>`;
}
function studyHTML(page, index) {
  const rows = current.steps.rows;
  if (!rows || codeCache.get(current.number)?.source !== current.steps.source) throw new Error('Niezgodna wersja materiałów. Odśwież stronę / Material version mismatch. Reload the page.');
  return `<article class="page"><div class="study">${editorHTML(rows,page.start,page.end)}<div class="explanation"><div class="step-kind"><span class="chip">${page.kind === 'block' ? words('CAŁY BLOK','WHOLE BLOCK') : words('INSTRUKCJA','STATEMENT')}</span><span>${index+1} / ${countPages(3)}</span></div><h3>${page.kind === 'block' ? words('Co robi ten fragment?','What does this block do?') : `${words('Czytamy zapis','Reading the statement')} · L${page.start}${page.end > page.start ? '–'+page.end : ''}`}</h3><p>${esc(t(page.body))}</p><div class="step-nav">${!continuous ? `<button data-next>${words('Dalej →','Next →')}</button>` : ''}</div></div></div></article>`;
}
function fullHTML(helper = false) {
  const code = codeCache.get(helper ? 'helper' : current.number);
  return `<article class="page"><div class="file-tabs"><button id="task-file" class="${helper ? '' : 'active'}">${current.steps.file}</button><button id="helper-file" class="${helper ? 'active' : ''}">lab_support.py · ${words('obserwacja','observation')}</button><button id="copy-code">${words('Kopiuj kod','Copy code')}</button></div>${helper ? `<p>${words('Warstwa obserwacyjna: config czyta gotowe wejście; event wysyła JSON do UI; span zapisuje początek i koniec; measured mierzy perf_counter; launch otacza przykład zdarzeniami i rejestruje błędy wątków. Nie jest częścią mechanizmu współbieżności.','Observation layer: config reads prepared input; event emits JSON to the UI; span records start and end; measured uses perf_counter; launch wraps the example in events and captures thread errors. It is not part of the concurrency mechanism.')}</p>` : ''}${editorHTML(code?.rows || [],null,null,true,helper ? 'lab_support.py' : current.steps.file)}</article>`;
}
function questionHTML() {
  return `<article class="page"><div class="eyebrow">${words('SPRAWDŹ, CZY POTRAFISZ TO WYJAŚNIĆ','CHECK THAT YOU CAN EXPLAIN IT')}</div><p class="question">${esc(t(current.question))}</p><details><summary>${words('Pokaż odpowiedź','Reveal answer')}</summary><p>${esc(t(current.answer))}</p></details><p class="question" style="font-size:24px;margin-top:32px">${esc(t(current.extra_question))}</p><details><summary>${words('Pokaż odpowiedź','Reveal answer')}</summary><p>${esc(t(current.extra_answer))}</p></details><div class="self-check">${words('Próba przed prezentacją: opowiedz bez patrzenia w tekst, jakie dane wchodzą, kto wykonuje pracę, gdzie czeka i skąd pochodzi wynik. Wskaż te miejsca w kodzie.','Presentation rehearsal: without reading the text, explain the inputs, who does the work, where it waits and where the result comes from. Point to those places in the code.')}</div><div class="nav-footer"><button data-home>${words('Wróć do listy','Back to list')}</button>${current.number < 20 ? `<button class="primary" data-task="${current.number+1}">${words('Następne zadanie →','Next task →')}</button>` : ''}</div></article>`;
}
function pageHTML(s, index) { return [() => assignmentHTML(index), introHTML, demoHTML, () => studyHTML(explanationPages()[index],index), fullHTML, questionHTML][s](); }
function render() {
  document.body.classList.remove('observing');
  if (!current) return catalog();
  preferences();
  const all = continuous ? [0,1,2,3,4,5].map(s => `<h2 class="section-title" id="section-${s}">${names()[s]}</h2>${Array.from({length:countPages(s)},(_,i) => pageHTML(s,i)).join('')}`).join('') : pageHTML(section,pageIndex);
  const footer = continuous ? '' : section === 5
    ? `<div class="nav-footer"><button data-home>${words('Wróć do listy','Back to list')}</button><span>${words('Pytania','Questions')}</span>${current.number < 20 ? `<button class="primary" data-task="${current.number+1}">${words('Następne zadanie →','Next task →')}</button>` : ''}</div>`
    : `<div class="nav-footer"><button id="previous" ${section === 0 ? 'disabled' : ''}>← ${words('Wstecz','Back')}</button><span>${names()[section]} · ${pageIndex+1} / ${countPages()}</span><button id="next" class="primary">${pageIndex+1 < countPages() ? words('Dalej →','Next →') : `${words('Przejdź:','Continue:')} ${names()[section+1]} →`}</button></div>`;
  $('#main').innerHTML = `<div class="task-heading"><div><div class="eyebrow">${words('ZADANIE','TASK')} ${String(current.number).padStart(2,'0')} / 20</div><h1>${esc(t(current.title))}</h1></div><button data-home class="quiet">← ${words('Lista zadań','Task list')}</button></div><nav class="sections" aria-label="${words('Sekcje lekcji','Lesson sections')}">${names().map((name,i) => `<button data-go="${i}" class="${i === section ? 'active' : ''}" aria-current="${i===section?'page':'false'}">${name}</button>`).join('')}</nav>${all}${footer}`;
  bindPage();
  if (!continuous) {
    const code = $('.code'); const focus = $('.code-row.focus');
    if (code && focus) code.scrollTop = Math.max(0, focus.offsetTop - code.offsetTop - 48);
  }
}
function navigate(s, index = 0) {
  section = s; pageIndex = index;
  if (continuous && current) {
    $(`#section-${s}`)?.scrollIntoView({behavior:'smooth'});
    return;
  }
  render(); window.scrollTo({top:0});
}
function next() { if (!current || continuous) return; if (pageIndex+1 < countPages()) navigate(section,pageIndex+1); else if (section<5) navigate(section+1); }
function previous() { if (!current || continuous) return; if (pageIndex>0) navigate(section,pageIndex-1); else if (section>0) navigate(section-1,countPages(section-1)-1); }
async function openTask(number) {
  if (!lessons[number-1]) return;
  current = lessons[number-1]; section = 0; pageIndex = 0;
  $('#drawer').hidden = true;
  codeCache.set(number,current.steps);
  history.replaceState(null,'',`#task-${number}`); render(); window.scrollTo({top:0});
}
function selectedRun() { return (histories[current?.number] || []).find(r => r.id === selectedRuns[current?.number]); }
function inputConfig() {
  if (!$('#custom') || $('#custom').hidden) return current.presets[Number($('#preset').value)].value;
  const field = $('#custom-value'); const key = Object.keys(current.presets[0].value)[0];
  if (key === 'numbers') return {numbers:JSON.parse(field.value)};
  if (['number','size','workers','side'].includes(key)) return {[key]:Number(field.value)};
  return {[key]:field.value};
}
function bindPage() {
  $('#previous')?.addEventListener('click', previous); $('#next')?.addEventListener('click', next);
  document.querySelectorAll('[data-next]').forEach(b => b.onclick = next);
  if ($('#preset')) {
    const saved = controls[current.number] ||= {preset:'0',backend:'native'};
    $('#preset').value=saved.preset; $('#backend').value=saved.backend;
    $('#preset').onchange=()=>{saved.preset=$('#preset').value;};
    $('#docker-note').hidden=saved.backend!=='docker';
    $('#run').disabled = !!activeRun;
    $('#cancel').hidden = !activeRun || activeRun.number !== current.number;
    $('#run').onclick = startRun;
    $('#focus-observation').onclick=()=>{document.body.classList.toggle('observing');window.scrollTo({top:0});};
    $('#focus-stop').onclick=()=>$('#cancel').click();
    $('#focus-rerun').onclick=()=>startRun(selectedRun());
    $('#backend').onchange = () => {saved.backend=$('#backend').value;$('#docker-note').hidden = saved.backend !== 'docker';};
    $('#cancel').onclick = async () => { try { await api(`/api/cancel/${activeRun.id}`,{method:'POST',body:'{}'}); } catch(e){toast(e.message);} };
    function buildCustom() {
      const area = $('#custom'); area.hidden = !saved.custom;
      if(area.hidden)return;
      const [key,value] = Object.entries(current.presets[Number($('#preset').value)].value)[0];
      const label = {number:words('Podstawa potęgi','Base'),size:words('Liczba elementów','Number of elements'),workers:words('Liczba wątków (1–10)','Threads (1–10)'),side:words('Bok obrazu (20–1000)','Image side (20–1000)'),name:words('Imię','Name'),word:words('Słowo','Word'),numbers:words('Lista liczb, np. [1,2,3]','List of numbers, e.g. [1,2,3]')}[key];
      area.innerHTML = `<label>${label}<input id="custom-value" value="${esc(saved.customValue ?? (Array.isArray(value) ? JSON.stringify(value) : value))}" ${['number','size','workers','side'].includes(key) ? 'type="number"' : 'type="text"'}></label><span class="axis-note">${words('Własne dane obowiązują, gdy to pole jest otwarte.','Custom inputs apply while this field is open.')}</span>`;
      $('#custom-value').oninput=()=>{saved.customValue=$('#custom-value').value;};
    }
    $('#custom-toggle')?.addEventListener('click',()=>{saved.custom=!saved.custom;buildCustom();});
    if(saved.custom)buildCustom();
    $('#history').onclick = event => {
      const b=event.target.closest('[data-history]'); if (!b) return;
      selectedRuns[current.number] = b.dataset.history; render();
    };
    updateDashboard();
  }
  $('#task-file')?.addEventListener('click', () => setFull(false));
  $('#helper-file')?.addEventListener('click', () => setFull(true));
  $('#copy-code')?.addEventListener('click', () => copyCode(false));
}
async function copyCode(helper) {
  try { await navigator.clipboard.writeText(codeCache.get(helper ? 'helper' : current.number).source); toast(words('Kod skopiowany','Code copied')); }
  catch { toast(words('Przeglądarka zablokowała schowek. Zaznacz kod ręcznie.','Clipboard blocked. Select the code manually.')); }
}
async function setFull(helper) {
  if (helper && !codeCache.has('helper')) codeCache.set('helper',await api(`/api/code/${current.number}?helper=1`));
  const panel = $('#task-file').closest('article'); panel.outerHTML = fullHTML(helper);
  $('#task-file').onclick=()=>setFull(false); $('#helper-file').onclick=()=>setFull(true); $('#copy-code').onclick=()=>copyCode(helper);
}
async function startRun(repeat = null) {
  if (activeRun) return;
  try {
    const prior=repeat?.input ? repeat : null;
    const input = prior ? prior.input : inputConfig();
    const backend = prior ? prior.backend : $('#backend').value;
    const presetLabel = prior ? prior.presetLabel : $('#custom') && !$('#custom').hidden ? words('własne dane','custom input') : current.presets[Number($('#preset').value)].label;
    $('#run').disabled = true;
    const data = await api(`/api/run/${current.number}`,{method:'POST',body:JSON.stringify({input,backend})});
    const run = {...data,number:current.number,input,backend,presetLabel,status:'running',events:[]};
    (histories[current.number] ||= []).push(run);
    selectedRuns[current.number] = run.id; activeRun = run;
    replay[run.id] = {ratio:1,playing:false};
    render(); document.body.classList.add('observing'); window.scrollTo({top:0}); pollRun(run);
  } catch(error) { toast(error.message); if ($('#run')) $('#run').disabled = false; }
}
async function pollRun(run) {
  try {
    const data = await api(`/api/status/${run.id}`); Object.assign(run,data);
    if (current?.number === run.number) updateDashboard();
    if (run.status === 'running') setTimeout(()=>pollRun(run),300);
    else {
      activeRun = null;
      if ($('#run')) $('#run').disabled = false;
      if ($('#cancel')) $('#cancel').hidden = true;
    }
  } catch(error) { activeRun=null; toast(error.message); if ($('#run')) $('#run').disabled=false; }
}
function recorded(run) {
  const events = [...run.events].sort((a,b)=>a.at-b.at);
  const base = events[0]?.at || 0, duration = Math.max(0.001,(events.at(-1)?.at || base)-base);
  const r = replay[run.id] ||= {ratio:1,playing:false};
  const cursor = duration*r.ratio;
  return {events:events.filter(e=>e.at-base<=cursor+0.00001),base,duration,cursor};
}
function updateDashboard() {
  if (!$('#visual')) return;
  const run = selectedRun(); if (!run) return;
  const {events,base,duration,cursor} = recorded(run);
  const r = replay[run.id];
  const statusNames = {running:words('Pracuje…','Running…'),done:words('Zakończony','Completed'),error:words('Błąd — zobacz dziennik','Error — see log'),cancelled:words('Zatrzymany lub limit 180 s','Stopped or 180 s limit')};
  $('#run-state').textContent = `${statusNames[run.status]} · ${run.backend}`;
  $('#run-state').classList.toggle('running',run.status === 'running');
  $('.dashboard h3').textContent=`${String(run.number).padStart(2,'0')} · ${t(current.title)}`;
  $('#focus-stop').hidden=run.status!=='running';
  $('#focus-rerun').hidden=run.status==='running';
  const spans = [], open = new Map();
  for (const e of events) {
    const key = `${e.actor}:${e.label}`;
    let actor = e.actor;
    if (run.number===19) actor=e.thread;
    if (run.number===20) actor=e.actor.startsWith('Sequential') ? words('Sekwencyjnie','Sequential') : `Proces · PID ${e.pid}`;
    if (e.kind === 'start') { const item = {...e,actor,end:base+cursor}; spans.push(item); (open.get(key) || (open.set(key,[]),open.get(key))).push(item); }
    if (e.kind === 'end') { const item=open.get(key)?.shift(); if(item) item.end=e.at; }
  }
  const actors = [...new Set(spans.map(e=>e.actor))];
  const scale = Math.max(duration,1);
  if (actors.length) {
    $('#visual').innerHTML = `<div class="timeline">${actors.map(actor=>`<div class="lane"><div class="lane-name">${esc(actor)}</div><div class="lane-track">${spans.filter(e=>e.actor===actor).map(e=>`<span class="bar" style="left:${(e.at-base)/scale*100}%;width:${Math.max(.15,(e.end-e.at)/scale*100)}%" title="${esc(e.label)} · PID ${e.pid} · ${(e.end-e.at).toFixed(3)} s"></span>`).join('')}</div></div>`).join('')}</div><div class="axis"><span>0 s</span><span>${(scale/2).toFixed(1)} s</span><span>${scale.toFixed(1)} s</span></div><p class="axis-note">${words('Paski pokazują czas pomiędzy START i KONIEC zadania, łącznie z czekaniem. Nie pokazują wykorzystania rdzeni. Bardzo krótkie zdarzenia mają minimalną widoczną szerokość.','Bars show time between task START and END, including waiting. They do not show core usage. Very short events have a minimum visible width.')}</p>`;
  } else {
    const logs = events.filter(e=>['log','put','get','balance'].includes(e.kind));
    $('#visual').innerHTML = logs.length ? `<div class="callout">${logs.slice(-3).map(e=>`<div><span class="chip">${esc(e.actor)} · PID ${e.pid || '—'}</span><p>${esc(e.label)}</p></div>`).join('')}</div>` : `<div class="empty">${words('Uruchamianie interpretera…','Starting interpreter…')}</div>`;
  }
  const metrics = events.filter(e=>e.kind==='metric');
  const maxTime = Math.max(.001,...metrics.filter(e=>e.unit==='s').map(e=>Number(e.value)));
  $('#metrics').innerHTML = metrics.map(e=>`<div class="metric"><span>${esc(e.label)}</span><strong>${typeof e.value === 'boolean' ? e.value ? words('TAK','YES') : words('NIE','NO') : esc(e.value)} ${esc(e.unit || '')}</strong>${e.unit==='s' ? `<div class="metric-time" style="width:${e.value/maxTime*100}%"></div>` : ''}</div>`).join('');
  if([4,5].includes(run.number)) {
    const snapshots=new Map();
    for(const e of events)if(e.kind==='log'&&e.actor.startsWith('Thread'))snapshots.set(e.actor,e);
    $('#metrics').innerHTML=[...snapshots.values()].map(e=>`<div class="metric"><span>${esc(e.actor)}</span><strong style="font-size:21px">${esc(e.label)}</strong></div>`).join('')+$('#metrics').innerHTML;
  }
  const balanceEvents = events.filter(e=>['put','get','balance'].includes(e.kind));
  let queueCount = 0;
  const amounts = balanceEvents.map(e=>e.kind==='balance' ? e.value : (queueCount += e.kind==='put'?1:-1));
  const maxAmount = Math.max(1,...amounts);
  $('#balance').innerHTML = amounts.length ? `<div class="axis-note">${run.number===18 ? words('Kolejne salda','Successive balances') : words('Bilans dodanych i odebranych elementów','Balance of produced and consumed items')}</div><div class="event-balance">${amounts.map((v,i)=>`<span class="balance-column" style="height:${Math.max(3,v/maxAmount*45)}px" title="${esc(balanceEvents[i].label)} → ${v}"></span>`).join('')}</div>` : '';
  const log = $('#log'); const atBottom = log.scrollHeight-log.scrollTop-log.clientHeight<40;
  log.innerHTML = events.filter(e=>e.kind!=='start'&&e.kind!=='end').map(e=>`<div class="log-row"><time>${(e.at-base).toFixed(2)} s</time><span>${esc(e.actor)}<br><small>PID ${e.pid || '—'}</small></span><span>${esc(e.label)}${e.kind==='metric' ? ': '+esc(e.value)+' '+esc(e.unit||'') : ''}</span></div>`).join('');
  if(atBottom) log.scrollTop=log.scrollHeight;
  $('#interpretation').hidden = run.status !== 'done';
  if(run.status === 'error') $('#log-details').open=true;
  if (run.status !== 'running' && !$('#replay-slider')) {
    $('#replay-controls').innerHTML = `<div class="replay"><button id="replay-play">▶ ${words('Odtwórz ślad','Replay trace')}</button><input id="replay-slider" aria-label="${words('Pozycja odtwarzania','Replay position')}" type="range" min="0" max="1000" value="1000"><span id="replay-time"></span></div><div class="axis-note">${words('Odtwarzanie zapisanych zdarzeń; kod nie uruchamia się ponownie.','Replays recorded events; does not execute the code again.')}</div>`;
    $('#replay-slider').oninput = e => {r.ratio=Number(e.target.value)/1000;r.playing=false;updateDashboard();};
    $('#replay-play').onclick=()=>{
      r.playing=!r.playing;if(r.playing&&r.ratio>=1)r.ratio=0;
      clearInterval(replayTimer);
      if(r.playing)replayTimer=setInterval(()=>{
        if(!current||selectedRun()?.id!==run.id){clearInterval(replayTimer);return;}
        if(!r.playing){clearInterval(replayTimer);return;}
        r.ratio=Math.min(1,r.ratio+.1/Math.max(duration,.1));
        if(r.ratio>=1){r.playing=false;clearInterval(replayTimer);}
        updateDashboard();
      },100);
      updateDashboard();
    };
  }
  if($('#replay-slider')){$('#replay-slider').value=Math.round(r.ratio*1000);$('#replay-time').textContent=`${cursor.toFixed(1)} / ${duration.toFixed(1)} s`;$('#replay-play').textContent=r.playing ? words('Ⅱ Pauza','Ⅱ Pause') : words('▶ Odtwórz ślad','▶ Replay trace');}
}
async function showResources(event) {
  event?.preventDefault(); $('#resource-dialog').showModal(); $('#resources-body').textContent=words('Sprawdzanie zasobów…','Checking resources…');
  try {
    resourceState = await api('/api/resources'); const d=resourceState;
    $('#resources-body').innerHTML=`<div class="resource-grid"><div><small>Python / OS</small>${esc(d.python)} / ${esc(d.system)}</div><div><small>${words('Logiczne CPU lokalnie','Local logical CPUs')}</small>${d.cores}</div><div><small>GIL · ${words('lokalny Python','local Python')}</small>${d.gil ? words('włączony','enabled') : words('wyłączony','disabled')}</div><div><small>Docker</small>${d.docker.ready ? words('silnik dostępny','engine ready') : words('silnik niedostępny','engine unavailable')}<br>${d.docker.image ? words('obraz gotowy','image ready') : words('brak obrazu lekcji','lesson image unavailable')}</div></div><p>${words('Django obsługuje UI lokalnie. Każdy pokaz to osobny proces Pythona. W Dockerze pokaz działa w usuwanym kontenerze Linux: 2 CPU, 2 GB RAM, bez dostępu do Internetu. Uruchom Docker Desktop i zbuduj obraz przed wyborem tego trybu.','Django serves the UI locally. Each demonstration uses a separate Python process. Docker demonstrations use a disposable Linux container: 2 CPUs, 2 GB RAM, no Internet access. Start Docker Desktop and build the image before choosing that mode.')}</p><p class="axis-note">${words('Nie wszystkie przykłady obciążają CPU: sleep jest oznaczoną symulacją oczekiwania. Procesy nie muszą wygrać pomiaru.','Not every example uses CPU heavily: sleep is an explicitly labelled wait simulation. Processes do not have to win a benchmark.')}</p>`;
  }catch(e){$('#resources-body').textContent=e.message;}
}
document.addEventListener('click',event=>{
  const task=event.target.closest('[data-task]');if(task){openTask(Number(task.dataset.task));return;}
  const go=event.target.closest('[data-go]');if(go){navigate(Number(go.dataset.go));return;}
  if(event.target.closest('[data-home]')){history.replaceState(null,'','#');catalog();window.scrollTo({top:0});}
});
document.querySelectorAll('[data-lang]').forEach(b=>b.onclick=()=>{language=b.dataset.lang;if(section===0)pageIndex=0;localStorage.setItem('l30-language',language);render();});
$('#mode').onclick=()=>{continuous=!continuous;localStorage.setItem('l30-mode',continuous?'continuous':'slides');render();};
$('#font').onclick=()=>{large=!large;localStorage.setItem('l30-large',large?'1':'0');preferences();};
$('#present').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch(e){toast(e.message);}};
$('#rail').onclick=()=>$('#drawer').hidden=!$('#drawer').hidden;
$('#rail').onmouseenter=()=>$('#drawer').hidden=false;
$('#drawer').onmouseleave=()=>$('#drawer').hidden=true;
$('#close-drawer').onclick=()=>$('#drawer').hidden=true;
$('.brand').onclick=event=>{event.preventDefault();history.replaceState(null,'','#');catalog();};
$('#resources-link').onclick=showResources;
$('#close-resources').onclick=()=>$('#resource-dialog').close();
document.addEventListener('keydown',event=>{
  if(['INPUT','TEXTAREA','SELECT','BUTTON','SUMMARY'].includes(event.target.tagName)||$('#resource-dialog').open)return;
  if(event.key==='ArrowRight'){event.preventDefault();next();}
  if(event.key==='ArrowLeft'){event.preventDefault();previous();}
  if(event.key==='Escape')$('#drawer').hidden=true;
});
(async()=>{try{lessons=(await api('/api/course')).lessons;const match=location.hash.match(/^#task-(\d+)$/);if(match)await openTask(Number(match[1]));else catalog();}catch(e){$('#main').textContent=e.message;}})();
