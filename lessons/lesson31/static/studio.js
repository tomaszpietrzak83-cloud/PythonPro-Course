'use strict';
const $ = (s, root = document) => root.querySelector(s);
const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let language = localStorage.getItem('l31-language') || 'pl';
let continuous = localStorage.getItem('l31-mode') === 'continuous';
let large = localStorage.getItem('l31-large') === '1';
let lessons = [], current = null, section = 0, pageIndex = 0;
let codeCache = new Map(), histories = {}, selectedRuns = {}, activeRun = null;
let replay = {}, replayTimer = null, resourceState = null;
let controls = {};
const words = (pl, en) => language === 'pl' ? pl : en;
const t = item => item[language];
const metricNames = {
  'Elapsed time':['Czas wykonania','Elapsed time'],
  'Temperature':['Temperatura','Temperature'],
  'Cities':['Liczba miast','Cities'],
  'Responses':['Odpowiedzi','Responses'],
  'HTTP statuses':['Statusy HTTP','HTTP statuses'],
  'Sum':['Suma wyników','Sum'],
  'Count':['Liczba wyników','Count'],
  'First completed delay':['Czas pierwszego wyniku','First completed delay'],
  'Cancelled tasks':['Anulowane zadania','Cancelled tasks'],
  'Echo matches input':['Odpowiedź identyczna z wejściem','Echo matches input'],
  'Processed items':['Przetworzone liczby','Processed items'],
  'Exactly 1..20':['Komplet liczb od 1 do 20','Exactly 1..20'],
  'Complete lines':['Pełne wiersze','Complete lines'],
  'All records intact':['Wszystkie wpisy poprawne','All records intact'],
  'Granted requests':['Udzielone zezwolenia','Granted requests'],
  'Rolling window respected':['Limit 5 na sekundę zachowany','Rolling window respected'],
  'Posts':['Liczba postów','Posts'],
  'Task cancelled':['Zadanie anulowane','Task cancelled'],
  'Prime count':['Liczba liczb pierwszych','Prime count'],
  'Largest prime':['Największa liczba pierwsza','Largest prime'],
  'Requested delay':['Wylosowany / wybrany czas','Requested delay'],
  'Timeout':['Przekroczenie limitu czasu','Timeout']
};
const metricTitle = label => metricNames[label] ? words(...metricNames[label]) : label;
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
  $('#main').innerHTML = `<div class="catalog-hero"><div><div class="eyebrow">${words('LEKCJA 31 · PRACOWNIA ASYNCIO','LESSON 31 · ASYNCIO WORKSHOP')}</div><h1>${words('Zrozum, kiedy kod<br>oddaje sterowanie.','Understand when code<br>yields control.')}</h1><p>${words('Korutyny, pętla zdarzeń i await — od podstaw składni do samodzielnego wyjaśnienia programu. Wybierz eksperyment, przewidź wynik i sprawdź go na żywo.','Coroutines, the event loop and await — from syntax foundations to explaining a program yourself. Choose an experiment, predict the result and test it live.')}</p></div><div class="orbital" aria-hidden="true"><span>async → await → understand</span></div></div>
  <div class="catalog-intro"><div><div class="eyebrow">${words('20 OSOBNYCH CELÓW NAUKI','20 DISTINCT LEARNING GOALS')}</div><p>${words('Gotowe dane. Rzeczywiste wykonanie. Kod objaśniony krok po kroku.','Prepared inputs. Real execution. Code explained step by step.')}</p></div><button id="open-guide">${words('Jak prezentować?','How to present?')}</button></div>
  <div class="catalog-grid">${lessons.map(l => `<button class="tile" data-task="${l.number}"><span class="num">${String(l.number).padStart(2,'0')} / ${l.number < 9 ? words('PODSTAWY','FOUNDATIONS') : words('PRAKTYKA','PRACTICE')}</span><strong>${esc(t(l.title))}</strong><span class="arrow">↗</span></button>`).join('')}</div>
  <div class="callout">${words('Twoja ścieżka: przeczytaj polecenie → przewidź wynik → uruchom → przeanalizuj metody → opowiedz własnymi słowami. Każdy pokaz uruchamia prawdziwy Python.','Your path: read → predict → run → study the methods → explain in your own words. Every demonstration executes real Python.')}</div>`;
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
  return `<article class="page assignment-page"><div class="eyebrow">${words('POLECENIE · LEKCJA 31','REQUIREMENTS · LESSON 31')}</div><h2>${words('Co masz wykonać?','What do you need to build?')}</h2><div class="assignment-content">${content}</div><div class="assignment-meta">${words('Oryginalne polecenie z tasks.md. Nazwy w rozwiązaniu i komunikaty demonstracji są po angielsku.','Original requirements from tasks.md. Solution identifiers and demo messages are in English.')}</div>${assignment.adaptation && index===assignment.pages[language].length-1 ? `<details class="assignment-adaptation"><summary>${words('Dostosowanie do pokazu w aplikacji','Adaptation for the app demonstration')}</summary><p>${esc(t(assignment.adaptation))}</p></details>`:''}</article>`;
}
function introHTML() {
  return `<article class="page"><div class="eyebrow">${words('JEDEN NOWY MECHANIZM','ONE NEW MECHANISM')}</div><div class="intro-grid"><div><h2>${esc(t(current.title))}</h2><p class="lead">${esc(t(current.intro))}</p></div><div class="number-emblem">${String(current.number).padStart(2,'0')}</div></div><div class="terms">${(current.terms||[]).map(term=>`<div><h3>${esc(term.name)}</h3><p>${esc(t(term.body))}</p></div>`).join('')}</div><button class="primary" data-go="2">${words('Przejdź do obserwacji →','Observe execution →')}</button></article>`;
}
function demoHTML() {
  const history = histories[current.number] || [];
  return `<article class="page"><div class="eyebrow">${words('RZECZYWISTY PYTHON · GOTOWE DANE','REAL PYTHON · PREPARED INPUTS')}</div><h2>${words('Najpierw zobacz różnicę','See the difference first')}</h2><p>${esc(t(current.watch))}</p>
    <div class="controlbar"><label>${words('Gotowy wariant','Prepared variant')}<select id="preset">${current.presets.map((p,i) => `<option value="${i}">${esc(p.label)}</option>`).join('')}</select></label><label>${words('Środowisko','Environment')}<select id="backend"><option value="native">${words('Lokalny Python','Local Python')}</option></select></label><button id="run" class="primary">▶ ${words('Uruchom pokaz','Run demonstration')}</button><button id="cancel" hidden>■ ${words('Zatrzymaj','Stop')}</button></div>


    <div id="history" class="history">${history.map((r,i) => `<button data-history="${r.id}" class="${selectedRuns[current.number] === r.id ? 'active' : ''}">${words('Pokaz','Run')} ${i+1} · ${esc(r.presetLabel)} · ${words('Python lokalny','Local Python')}</button>`).join('')}</div>
    <div class="dashboard"><div class="dashboard-heading"><h3>${words('Ślad wykonania','Execution trace')}</h3><span id="run-state" class="state">${words('Gotowe do startu','Ready')}</span><button id="focus-stop" hidden>■ ${words("Zatrzymaj","Stop")}</button><button id="focus-rerun" hidden>▶ ${words("Powtórz","Run again")}</button><button id="focus-observation" class="quiet">${words('⛶ Skup widok / wróć','⛶ Focus view / return')}</button></div><div id="visual"><div class="empty">${words('Uruchom pokaz. Tutaj pojawią się rzeczywiste zdarzenia programu.','Run the demonstration. Actual program events will appear here.')}</div></div><div id="replay-controls"></div><div id="metrics" class="metrics"></div><div id="balance"></div><details id="log-details"><summary>${words('Dziennik zdarzeń · czas, uczestnik i PID','Event log · time, participant and PID')}</summary><div id="log" class="log"></div></details></div>
    <div id="interpretation" hidden><h3>${words('Jak odczytać wynik?','How to read the result')}</h3><p>${esc(t(current.takeaway))}</p></div><details><summary>${words('Warunki i granice tego eksperymentu','Experiment conditions and limits')}</summary><p>${esc(t(current.caveat))}</p></details></article>`;
}
function editorHTML(rows, start, end, full = false, file = current.steps.file) {
  return `<div class="editor ${full ? 'full' : ''}"><div class="editor-head"><span>${esc(file)}</span><span>${start ? `L${start}${end > start ? '–'+end : ''}` : words('kod źródłowy','source code')}</span></div><div class="code">${rows.map((row, i) => `<div class="code-row ${start ? i+1 >= start && i+1 <= end ? 'focus' : 'dim' : ''}" data-line="${i+1}"><span class="ln">${i+1}</span><span class="src">${row || ' '}</span></div>`).join('')}</div></div>`;
}
function studyHTML(page, index) {
  const rows = current.steps.rows;
  if (!rows || codeCache.get(current.number)?.source !== current.steps.source) throw new Error('Material version mismatch');
  const method = !!page.expression;
  const title = method ? page.name + '()' : page.name || page.id;
  const args = method ? `<div class="argument-list">${page.arguments.length ? page.arguments.map(a=>`<div><b>${esc(a.name)}</b><code>${esc(a.value)}</code></div>`).join('') : `<p>${words('To wywołanie nie ma jawnych argumentów.','This call has no explicit arguments.')}</p>`}</div>` : '';
  return `<article class="page"><div class="study">${editorHTML(rows,page.start,page.end)}<div class="explanation"><div class="step-kind"><span class="chip">${method ? words('METODA / FUNKCJA','METHOD / FUNCTION') : words('CEL I PRZEBIEG','PURPOSE AND FLOW')}</span><span>${index+1} / ${countPages(3)}</span></div><h3>${esc(title)}</h3>${method ? `<div class="step-code">${esc(page.expression)}</div><h4>${words('Argumenty w tym miejscu','Arguments at this call')}</h4>${args}` : ''}<div class="teaching-note"><h4>${method ? words('Jak działa i co zwraca?','How does it work and what does it return?') : words('Czytamy krok po kroku','Read step by step')}</h4><p>${esc(t(page.body))}</p></div>${!method ? `<details><summary>${words('Połącz kod z wynikiem','Connect code to results')}</summary><p>${esc(t(current.takeaway))}</p></details><details><summary>${words('Pułapka i ograniczenia','Pitfall and limits')}</summary><p>${esc(t(current.caveat))}</p></details>` : ''}<details><summary>${words('Próba: co się zmieni, jeśli…','Try: what changes if…')}</summary><p>${esc(t(current.extra_question))}</p><details><summary>${words('Sprawdź rozumowanie','Check your reasoning')}</summary><p>${esc(t(current.extra_answer))}</p></details></details></div></div></article>`;
}

function fullHTML(helper = false) {
  const code = codeCache.get(helper ? 'helper' : current.number);
  return `<article class="page"><div class="file-tabs"><button id="task-file" class="${helper ? '' : 'active'}">${current.steps.file}</button><button id="helper-file" class="${helper ? 'active' : ''}">lab_support.py · ${words('obserwacja','observation')}</button><button id="copy-code">${words('Kopiuj kod','Copy code')}</button></div>${helper ? `<p>${words('Pomocnik pokazu: config czyta wariant; event wysyła zdarzenie JSON; span zapisuje początek i koniec także przy wyjątku; metric prezentuje wynik; launch mierzy rzeczywisty czas przez perf_counter. To osobna warstwa obserwacyjna. Kod asyncio znajduje się w pliku zadania.','Demo helper: config reads the preset; event emits JSON; span records start and end even on exceptions; metric displays results; launch measures elapsed time with perf_counter. Asyncio code is in the task file.')}</p>` : ''}${editorHTML(code?.rows || [],null,null,true,helper ? 'lab_support.py' : current.steps.file)}</article>`;
}
function questionHTML() {
  return `<article class="page"><div class="eyebrow">${words('SPRAWDŹ, CZY POTRAFISZ TO WYJAŚNIĆ','CHECK THAT YOU CAN EXPLAIN IT')}</div><p class="question">${esc(t(current.question))}</p><details><summary>${words('Pokaż odpowiedź','Reveal answer')}</summary><p>${esc(t(current.answer))}</p></details><p class="question" style="font-size:24px;margin-top:32px">${esc(t(current.extra_question))}</p><details><summary>${words('Pokaż odpowiedź','Reveal answer')}</summary><p>${esc(t(current.extra_answer))}</p></details><div class="self-check">${words('Próba przed prezentacją: opowiedz bez patrzenia w tekst, jakie dane wchodzą, gdzie kod oddaje sterowanie i skąd pochodzi wynik. Wskaż te miejsca w kodzie.','Presentation rehearsal: explain the inputs, where code yields control and where the result comes from. Point to those places in the code.')}<details><summary>${words('Podpowiedź do wypowiedzi','Speaking prompt')}</summary><p>${esc(t(current.intro))}</p><p>${esc(t(current.takeaway))}</p></details></div><div class="nav-footer"><button data-home>${words('Wróć do listy','Back to list')}</button>${current.number < 20 ? `<button class="primary" data-task="${current.number+1}">${words('Następne zadanie →','Next task →')}</button>` : ''}</div></article>`;
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
  return current.presets[Number($('#preset').value)].value;
}

function bindPage() {
  $('#previous')?.addEventListener('click', previous); $('#next')?.addEventListener('click', next);
  document.querySelectorAll('[data-next]').forEach(b => b.onclick = next);
  if ($('#preset')) {
    const saved = controls[current.number] ||= {preset:'0',backend:'native'};
    $('#preset').value=saved.preset; $('#backend').value=saved.backend;
    $('#preset').onchange=()=>{saved.preset=$('#preset').value;};
    $('#run').disabled = !!activeRun;
    $('#cancel').hidden = !activeRun || activeRun.number !== current.number;
    $('#run').onclick = startRun;
    $('#focus-observation').onclick=()=>{document.body.classList.toggle('observing');window.scrollTo({top:0});};
    $('#focus-stop').onclick=()=>$('#cancel').click();
    $('#focus-rerun').onclick=()=>startRun(selectedRun());
    $('#backend').onchange = () => {saved.backend=$('#backend').value;};
    $('#cancel').onclick = async () => {
      if (!activeRun) return;
      try { await api(`/api/cancel/${activeRun.id}`,{method:'POST',body:'{}'}); }
      catch(e){toast(e.message);}
    };
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
    const presetLabel = prior ? prior.presetLabel : current.presets[Number($('#preset').value)].label;
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
  $('#run-state').textContent = `${statusNames[run.status]} · ${words('Python lokalny','Local Python')}`;
  $('#run-state').classList.toggle('running',run.status === 'running');
  $('.dashboard h3').textContent=`${String(run.number).padStart(2,'0')} · ${t(current.title)}`;
  $('#focus-stop').hidden=run.status!=='running';
  $('#focus-rerun').hidden=run.status==='running';
  const spans = [], open = new Map();
  for (const e of events) {
    const key = `${e.actor}:${e.label}`;
    let actor = e.actor;
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
  $('#metrics').innerHTML = metrics.map(e=>`<div class="metric"><span>${esc(metricTitle(e.label))}</span><strong>${typeof e.value === 'boolean' ? e.value ? words('TAK','YES') : words('NIE','NO') : esc(e.value)} ${esc(e.unit || '')}</strong>${e.unit==='s' ? `<div class="metric-time" style="width:${e.value/maxTime*100}%"></div>` : ''}</div>`).join('');
  const balanceEvents = events.filter(e=>['put','get','balance'].includes(e.kind));
  let queueCount = 0;
  const amounts = balanceEvents.map(e=>e.kind==='balance' ? e.value : (queueCount += e.kind==='put'?1:-1));
  const maxAmount = Math.max(1,...amounts);
  $('#balance').innerHTML = amounts.length ? `<div class="axis-note">${words('Liczby oczekujące w kolejce (bez sygnałów końca)','Queued numbers (excluding shutdown markers)')}</div><div class="event-balance">${amounts.map((v,i)=>`<span class="balance-column" style="height:${Math.max(3,v/maxAmount*45)}px" title="${esc(balanceEvents[i].label)} → ${v}"></span>`).join('')}</div>` : '';
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
    $('#resources-body').innerHTML=`<div class="resource-grid"><div><small>Python / OS</small>${esc(d.python)} / ${esc(d.system)}</div><div><small>${words('Środowisko','Environment')}</small>asyncio · aiohttp · aiofiles</div></div><p>${words('Każdy pokaz to osobny proces lokalnego Pythona. Wewnątrz przykładów korutynami zarządza asyncio. HTTP i TCP używają lokalnego adresu; pliki są tymczasowe. Pogoda, ping i opóźnienia API są symulowane.','Each demo is a separate local Python process. Within each example asyncio manages the coroutines. HTTP and TCP use loopback; files are temporary. Weather, ping and API delays are simulated.')}</p><p><a href="https://docs.python.org/3/library/asyncio-task.html" target="_blank" rel="noopener">Python: coroutines and tasks ↗</a></p>`;
  }catch(e){$('#resources-body').textContent=e.message;}
}
document.addEventListener('click',event=>{
  const task=event.target.closest('[data-task]');if(task){openTask(Number(task.dataset.task));return;}
  const go=event.target.closest('[data-go]');if(go){navigate(Number(go.dataset.go));return;}
  if(event.target.closest('[data-home]')){history.replaceState(null,'','#');catalog();window.scrollTo({top:0});}
});
document.querySelectorAll('[data-lang]').forEach(b=>b.onclick=()=>{language=b.dataset.lang;if(section===0)pageIndex=0;localStorage.setItem('l31-language',language);render();});
$('#mode').onclick=()=>{continuous=!continuous;localStorage.setItem('l31-mode',continuous?'continuous':'slides');render();};
$('#font').onclick=()=>{large=!large;localStorage.setItem('l31-large',large?'1':'0');preferences();};
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
