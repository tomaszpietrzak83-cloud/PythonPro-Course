'use strict';
/* Independent, multiple draggable notes. Source annotations come from the AST. */
const CodeStudy = (() => {
  let task = null, file = 'main.py', sources = {}, language = 'pl';
  let pins = new Map(), transient = null, hideTimer, showTimer, layer, sequence = 0;
  let drag = null, hoveredId = null;
  const escape = text => String(text ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const say = (pl,en) => language === 'pl' ? pl : en;
  const kinds = {block:['BLOK','BLOCK'],function:['FUNKCJA','FUNCTION'],method:['METODA','METHOD'],line:['LINIA','LINE']};
  const noteFor = id => Object.values(sources).map(s=>s.notes[id]).find(Boolean);
  function ensureLayer() {
    if (layer) return;
    layer = document.createElement('div'); layer.id='code-note-layer'; document.body.append(layer);
    document.addEventListener('keydown',event=>{
      if(event.key !== 'Escape')return;
      if(transient){dismiss();event.stopImmediatePropagation();}
      else if(pins.size){const last=[...pins.values()].at(-1);remove(last.id);event.stopImmediatePropagation();}
    },true);
    window.addEventListener('resize',()=>layer.querySelectorAll('.code-note').forEach(clamp));
  }
  function clearHighlight() { document.querySelectorAll('.code-row.note-highlight').forEach(row=>row.classList.remove('note-highlight')); }
  function highlight(note) {
    clearHighlight();
    document.querySelectorAll('.hover-editor').forEach(editor=>{
      if(editor.dataset.file!==note.file)return;
      editor.querySelectorAll('.code-row').forEach(row=>row.classList.toggle('note-highlight',Number(row.dataset.line)>=note.start&&Number(row.dataset.line)<=note.end));
    });
  }
  function clamp(el) {
    const r=el.getBoundingClientRect();
    el.style.left=`${Math.max(8,Math.min(r.left,innerWidth-r.width-8))}px`;
    el.style.top=`${Math.max(8,Math.min(r.top,innerHeight-r.height-8))}px`;
  }
  function updateCount(){document.querySelectorAll('[data-pin-count]').forEach(el=>el.textContent=String(pins.size));}
  function remove(id){const pin=pins.get(id);if(!pin)return;pin.el.remove();pins.delete(id);clearHighlight();updateCount();}
  function dismiss(){clearTimeout(hideTimer);clearTimeout(showTimer);transient?.el.remove();transient=null;clearHighlight();}
  function closeAll(){dismiss();for(const id of [...pins.keys()])remove(id);}
  function leaveCode(){clearTimeout(showTimer);hoveredId=null;}
  function markup(note,pinned) {
    return `<div class="note-heading" ${pinned?'title="'+say('Przeciągnij dymek','Drag note')+'"':''}><span>${say(...kinds[note.kind])} · ${escape(note.file)} · L${note.start}${note.end!==note.start?'–'+note.end:''}</span><div>${pinned?`<button data-clear-all>${say('Wyczyść','Clear all')}</button>`:''}<button data-close aria-label="${say('Zamknij dymek','Close note')}">×</button></div></div><div class="note-content"><h3>${escape(note.title)}</h3>${note.expression?`<pre>${escape(note.expression)}</pre>`:''}<p>${escape(note.body[language])}</p>${pinned?`<button class="note-locate" data-locate>${say('Pokaż w kodzie','Show in code')} ↗</button>`:`<small>${say('Kliknij fragment kodu, aby przypiąć. Podgląd znika po 3 s.','Click the code to pin. Preview disappears after 3 s.')}</small>`}</div>${pinned?['nw','ne','sw','se'].map(c=>`<span class="note-resize ${c}" data-resize="${c}" title="${say('Zmień rozmiar','Resize')}"></span>`).join(''):''}`;
  }
  function wireNote(entry,pinned){
    const el=entry.el;
    el.innerHTML=markup(entry.note,pinned);
    el.onpointerenter=()=>highlight(entry.note);
    el.onpointerleave=clearHighlight;
    el.querySelector('[data-close]').onclick=()=>pinned?remove(entry.id):dismiss();
    el.querySelector('[data-clear-all]')?.addEventListener('click',closeAll);
    el.querySelector('[data-locate]')?.addEventListener('click',()=>{
      if(file!==entry.note.file){file=entry.note.file;replaceEditor();}
      const row=document.querySelector(`.hover-editor .code-row[data-line="${entry.note.start}"]`);
      row?.scrollIntoView({block:'center',behavior:'smooth'});highlight(entry.note);
    });
    if(pinned){
      el.querySelectorAll('[data-resize]').forEach(handle=>{
        let sizing=null;
        handle.onpointerdown=e=>{
          const r=el.getBoundingClientRect();
          sizing={x:e.clientX,y:e.clientY,left:r.left,top:r.top,right:r.right,bottom:r.bottom,corner:handle.dataset.resize};
          el.style.zIndex=String(++sequence+1010);handle.setPointerCapture(e.pointerId);e.preventDefault();e.stopPropagation();
        };
        handle.onpointermove=e=>{
          if(!sizing)return;
          const r=sizing,dx=e.clientX-r.x,dy=e.clientY-r.y;
          const minW=Math.min(260,innerWidth-16),minH=Math.min(150,innerHeight-16);
          let left=r.left,right=r.right,top=r.top,bottom=r.bottom;
          if(r.corner.includes('w'))left=Math.max(8,Math.min(r.right-minW,r.left+dx));
          else right=Math.min(innerWidth-8,Math.max(r.left+minW,r.right+dx));
          if(r.corner.includes('n'))top=Math.max(8,Math.min(r.bottom-minH,r.top+dy));
          else bottom=Math.min(innerHeight-8,Math.max(r.top+minH,r.bottom+dy));
          Object.assign(el.style,{left:left+'px',top:top+'px',width:(right-left)+'px',height:(bottom-top)+'px'});
        };
        handle.onpointerup=handle.onpointercancel=()=>{sizing=null;};
      });
      const head=el.querySelector('.note-heading');
      head.onpointerdown=e=>{
        if(e.target.closest('button'))return;
        const rect=el.getBoundingClientRect();drag={x:e.clientX-rect.left,y:e.clientY-rect.top,id:e.pointerId};
        el.style.zIndex=String(++sequence+1010);head.setPointerCapture(e.pointerId);e.preventDefault();
      };
      head.onpointermove=e=>{if(!drag||drag.id!==e.pointerId)return;el.style.left=`${e.clientX-drag.x}px`;el.style.top=`${e.clientY-drag.y}px`;clamp(el);};
      head.onpointerup=head.onpointercancel=()=>{drag=null;};
    }
  }
  function show(id,anchor){
    const note=noteFor(id);if(!note)return;
    if(transient?.note.id===id)return;
    dismiss();ensureLayer();
    const el=document.createElement('aside');el.className='code-note';el.setAttribute('role','dialog');el.setAttribute('aria-label',note.title);
    el.style.visibility='hidden';layer.append(el);
    transient={note,el};wireNote(transient,false);
    const rect=anchor.getBoundingClientRect(),r=el.getBoundingClientRect();
    let left=innerWidth-r.width-20,top=rect.top;
    if(rect.width<180 && rect.left>left-40)left=Math.max(8,rect.left-r.width-20);
    el.style.left=left+'px';el.style.top=top+'px';el.style.visibility='';clamp(el);highlight(note);
    hideTimer=setTimeout(dismiss,3000);
  }
  function pin(entry){
    const existing=pins.get(entry.note.id);
    if(existing){existing.el.style.zIndex=String(++sequence+1010);existing.el.querySelector('[data-close]').focus();dismiss();return;}
    clearTimeout(hideTimer);clearTimeout(showTimer);
    transient=null;entry.id=entry.note.id;entry.el.classList.add('pinned');pins.set(entry.id,entry);wireNote(entry,true);
    // Pack visible cards into columns before allowing intentional user overlap.
    let left=Math.max(8,innerWidth-430),top=90;
    const height=entry.el.getBoundingClientRect().height;
    for(const prior of [...pins.values()].slice(0,-1)){
      const r=prior.el.getBoundingClientRect();
      if(Math.abs(r.left-left)<420&&top<r.bottom+10&&top+height>r.top)top=r.bottom+10;
      if(top+height>innerHeight-8){left=Math.max(8,left-425);top=90;}
    }
    entry.el.style.left=left+'px';entry.el.style.top=top+'px';
    entry.el.style.zIndex=String(++sequence+1010);clamp(entry.el);entry.el.querySelector('[data-close]').focus();updateCount();
  }
  function editorHTML(){
    const data=sources[file];
    return `<div class="editor full hover-editor" data-file="${escape(file)}"><div class="editor-head"><span>● ${escape(file)}</span><span>Python · ${data.annotated_rows.length} ${say('linii','lines')}</span></div><div class="code">${data.annotated_rows.map(row=>`<div class="code-row" data-line="${row.line}" data-block-note="${escape(row.block_note)}"><button class="ln" data-note="${escape(row.line_note)}" aria-label="${say('Wyjaśnij linię','Explain line')} ${row.line}">${row.line}</button><span class="src">${row.html||' '}</span></div>`).join('')}</div></div>`;
  }
  function html(number,data,lang){
    ensureLayer();
    if(task!==number){closeAll();file='main.py';task=number;}
    sources=data;language=lang;if(!sources[file])file='main.py';
    for(const entry of pins.values()){entry.note=noteFor(entry.id);wireNote(entry,true);}
    dismiss();
    return `<article class="page hover-study"><div class="study-toolbar"><div><div class="eyebrow">${say('ZROZUM KOD · EKSPLORUJ','UNDERSTAND CODE · EXPLORE')}</div><p>${say('Najedź na blok, nazwę funkcji, metodę albo numer linii.','Hover a block, function name, method or line number.')}</p></div><div class="study-actions"><button data-code-focus>${say('⛶ Skup kod / wróć','⛶ Focus code / return')}</button><button data-close-pins>${say('Zamknij przypięte','Close pinned')} (<span data-pin-count>${pins.size}</span>)</button></div></div><div class="hover-legend"><span>▌ ${say('tło kodu → blok','code background → block')}</span><span>ƒ ${say('nazwa → funkcja / metoda','name → function / method')}</span><span>＃ ${say('numer → linia','number → line')}</span><span>＋ ${say('kliknij kod → przypnij · narożnik → zmień rozmiar','click code → pin · corner → resize')}</span></div><div class="file-tabs study-files">${Object.keys(sources).map(name=>`<button data-study-file="${escape(name)}" class="${name===file?'active':''}">${escape(name)}</button>`).join('')}</div><div id="study-editor">${editorHTML()}</div><p class="study-keyboard">${say('Klawiatura: Tab → numer lub nazwa, Enter → przypnij opis. Esc zamyka bieżący dymek, potem ostatni przypięty.','Keyboard: Tab → number or name, Enter → pin explanation. Esc closes the current note, then the last pinned note.')}</p></article>`;
  }
  function replaceEditor(){
    dismiss();document.querySelector('#study-editor').innerHTML=editorHTML();
    document.querySelectorAll('[data-study-file]').forEach(b=>b.classList.toggle('active',b.dataset.studyFile===file));bindEditor();
  }
  function bindEditor(){
    const root=document.querySelector('.hover-editor');if(!root)return;
    function targetFor(target){
      const specific=target.closest('[data-note]');if(specific)return [specific.dataset.note,specific];
      const row=target.closest('[data-block-note]');return row?[row.dataset.blockNote,row.querySelector('.src')]:null;
    }
    root.onpointerover=event=>{
      const target=targetFor(event.target);if(!target||hoveredId===target[0])return;
      hoveredId=target[0];clearTimeout(showTimer);
      showTimer=setTimeout(()=>show(...target),220);
    };
    root.onpointerleave=leaveCode;
    root.addEventListener('focusin',event=>{const target=targetFor(event.target);if(target)show(...target);});
    function pinTarget(target){
      if(!target)return;
      clearTimeout(showTimer);show(...target);
      if(transient)pin(transient);
    }
    root.onclick=event=>pinTarget(targetFor(event.target));
    root.onkeydown=event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();pinTarget(targetFor(event.target));}};

  }
  function bind(){
    if(!document.querySelector('#study-editor'))return;
    document.querySelector('[data-code-focus]').onclick=()=>{document.body.classList.toggle('code-focused');};
    document.querySelectorAll('[data-study-file]').forEach(b=>b.onclick=()=>{file=b.dataset.studyFile;replaceEditor();});
    document.querySelector('[data-close-pins]').onclick=closeAll;bindEditor();updateCount();
  }
  function suspend(){dismiss();pins.forEach(entry=>entry.el.hidden=true);}
  function resume(){pins.forEach(entry=>entry.el.hidden=false);}
  return {html,bind,closeAll,suspend,resume};
})();
