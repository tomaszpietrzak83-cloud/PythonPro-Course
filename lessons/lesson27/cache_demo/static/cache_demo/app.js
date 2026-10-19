import {bilingual, getLanguage, t, toggleLanguage, translatePage} from './i18n.js';
import {controlProcess, performAction, processStates, serverHealth} from './api.js';
import {clearTimers, recordTimer, remainingSeconds, renderTimers} from './timers.js';
import {actionsFor, preset, stepsFor} from './scenarios.js';
import {createQuestionPanel} from './questions.js';

const boot = JSON.parse(document.querySelector('#demo-boot').textContent);
const $ = selector => document.querySelector(selector);
translatePage();
$('#language-toggle').addEventListener('click', toggleLanguage);

function translateNavigation() {
  document.querySelectorAll('a[href="/"], a[data-home-link]').forEach(element => {
    element.dataset.homeLink = 'true';
    element.href = boot.control_port ? `http://${location.hostname}:${boot.control_port}/?lang=${getLanguage()}` : `/?lang=${getLanguage()}`;
  });
  for (const task of boot.tasks) {
    document.querySelectorAll(`[data-task-title="${task.number}"]`).forEach(element => element.textContent = bilingual(task.title));
    document.querySelectorAll(`[data-task-link="${task.number}"]`).forEach(element => {
      // Pass the language in the link: localStorage is isolated by port.
      element.href = `http://${location.hostname}:${task.port}/task/${task.number}/?lang=${getLanguage()}`;
      element.setAttribute('aria-label', `${t('task')} ${task.number}: ${bilingual(task.title)}`);
    });
  }
}
translateNavigation();
document.addEventListener('languagechange', translateNavigation);

if (!boot.number) {
  const healthState = new Map();
  let states = {}, refreshing = false, processBusy = false;
  function drawHealth() {
    for (const [port, state] of healthState) {
      const card = $(`[data-port="${port}"]`);
      card.querySelector('.health').textContent = t(state);
      card.dataset.online = state === 'online';
    }
    if (boot.manager) {
      document.querySelectorAll('.process-toggle').forEach(button => {
        const project = button.closest('[data-project]').dataset.project;
        const state = states[project];
        button.textContent = state?.running ? t('stopServer') : 'runserver';
        button.disabled = processBusy || !state;
        button.classList.toggle('btn-outline-primary', Boolean(state?.running));
        button.classList.toggle('btn-primary', !state?.running);
        button.closest('.backend-card').querySelector('.process-state').textContent = state?.running ? `PID ${state.pid}` : t('stopped');
      });
    }
  }
  async function refreshHealth() {
    if (refreshing || processBusy) return;
    refreshing = true;
    $('#refresh-health').disabled = true;
    if (boot.manager) {
      try { states = await processStates(); }
      catch { states = {}; }
    }
    await Promise.all([8000, 8001, 8002].map(async port => {
      try { healthState.set(port, (await serverHealth(port)).online ? 'online' : 'offline'); }
      catch { healthState.set(port, 'offline'); }
    }));
    drawHealth(); $('#refresh-health').disabled = false; refreshing = false;
  }
  if (boot.manager) {
    document.querySelectorAll('.process-toggle').forEach(button => button.addEventListener('click', async () => {
      if (processBusy) return;
      const project = button.closest('[data-project]').dataset.project;
      const action = states[project]?.running ? 'stop' : 'start';
      processBusy = true; drawHealth();
      $('#process-error').hidden = true;
      $('#process-feedback').textContent = t(action === 'start' ? 'starting' : 'stopping');
      try { states = await controlProcess(project, action, boot.control_token); }
      catch (error) { $('#process-error').hidden = false; $('#process-error').textContent = `${t('processFailed')} (${error.message})`; }
      finally {
        processBusy = false; $('#process-feedback').textContent = ''; drawHealth();
        await refreshHealth();
      }
    }));
    // Poll only the open control page. These independent health probes do not
    // read or renew any demonstration entry or countdown.
    setInterval(refreshHealth, 5000);
  }
  $('#refresh-health').addEventListener('click', refreshHealth);
  document.addEventListener('languagechange', drawHealth);
  refreshHealth();
} else {
  const number = boot.number;
  const questionPanel = createQuestionPanel(boot.questions);
  const steps = stepsFor(number);
  const history = [];
  let stepIndex = 0, busy = false, lastResult = null, feedbackKey = '';
  // Persist the task generation across reloads. Reset advances it only for this
  // task, so cache_page keys from other demonstrations remain untouched.
  const generationKey = `cache-demo-generation-${number}`;
  let options = {...preset('quick', number, boot.original_ttl),
    generation: Number(localStorage.getItem(generationKey) || 0)};
  const optionsKey = `cache-demo-options-${number}`;
  try {
    const saved = JSON.parse(localStorage.getItem(optionsKey));
    if (saved && ['quick', 'homework'].includes(saved.scenario) &&
        [saved.ttl, saved.detail_ttl].every(value => Number.isInteger(value) && value >= 1 && value <= 3600)) {
      options = {...options, scenario: saved.scenario, ttl: saved.ttl, detail_ttl: saved.detail_ttl};
    }
  } catch { /* An invalid preference falls back to the documented quick preset. */ }

  function writeInputs() {
    $('#scenario').value = options.scenario;
    $('#ttl').value = options.ttl;
    $('#detail-ttl').value = options.detail_ttl;
  }
  function translateTask() {
    $('#task-title').textContent = bilingual(boot.title);
    document.title = `${t('task')} ${number} · ${bilingual(boot.title)} · Cache Lab`;
    $('#requirements').textContent = bilingual(boot.requirements);
    $('#explanation').textContent = bilingual(boot.explanation);
    questionPanel.translate();
    $('#ttl-note').textContent = t('note', {ttl: options.ttl, original: number === 5 ? t('unspecified') : boot.original_ttl,
      detail: [8, 9].includes(number) ? t('detailNote', {ttl: options.detail_ttl}) : ''});
    $('#manual-actions').replaceChildren();
    for (const action of actionsFor(number)) {
      const button = document.createElement('button');
      button.className = 'btn btn-outline-primary btn-sm'; button.textContent = t(action);
      button.disabled = busy; button.addEventListener('click', () => execute(action));
      $('#manual-actions').append(button);
    }
    $('#step-description').textContent = steps[stepIndex] ? `${stepIndex + 1}/${steps.length} · ${t(steps[stepIndex].text)}` : t('complete');
    $('#next-step').disabled = busy || !steps[stepIndex];
    $('#previous-step').disabled = busy || stepIndex === 0;
    $('#feedback').textContent = feedbackKey ? t(feedbackKey) : '';
    const explanationKeys = {MISS: 'missExplain', HIT: 'hitExplain', WRITE: 'writeExplain',
      DELETED: 'deleteExplain', CLEARED: 'clearExplain', RESET: 'resetExplain',
      CONNECTED: 'connectedExplain', INVALIDATED: 'invalidatedExplain', READ: 'readExplain'};
    const explanationKey = number === 4 && lastResult?.status === 'MISS' ? 'missingExplain' : explanationKeys[lastResult?.status];
    $('#last-explanation').textContent = lastResult ? t(explanationKey || 'readExplain') : '';
    renderHistory(); renderTimers();
  }
  function renderHistory() {
    $('#history').replaceChildren();
    history.forEach((entry, index) => {
      const row = document.createElement('tr');
      [index + 1, t(entry.action), entry.result.status, entry.result.elapsed_ms, entry.result.sql_queries].forEach(value => {
        const cell = document.createElement('td'); cell.textContent = value; row.append(cell);
      });
      $('#history').append(row);
    });
  }
  function setBusy(value) {
    busy = value;
    document.querySelectorAll('main button, main input, main select').forEach(element => element.disabled = value);
    feedbackKey = value ? 'busy' : '';
    translateTask();
  }
  async function execute(action) {
    if (busy) return false;
    $('#error').hidden = true;
    setBusy(true);
    try {
      const result = await performAction(number, options, action);
      lastResult = result; history.push({action, result});
      $('#result-status').textContent = result.status;
      $('#result-status').dataset.status = result.status;
      $('#duration').textContent = `${result.elapsed_ms} ms`;
      $('#queries').textContent = result.sql_queries;
      $('#response').textContent = JSON.stringify(result.data, null, 2);
      if (action === 'reset') clearTimers();
      else if (action === 'update') recordTimer('detail', result);
      else recordTimer(['list', 'detail'].includes(action) ? action : 'read', result);
      if (result.files) {
        $('#file-panel').hidden = false;
        $('#cache-directory').textContent = result.directory;
        $('#cache-files').textContent = JSON.stringify(result.files, null, 2);
      }
      if (typeof result.redis_ping === 'boolean') {
        $('#redis-panel').hidden = false;
        $('#redis-diagnostics').textContent = JSON.stringify({PING: result.redis_ping ? 'PONG' : 'FAILED',
          marker_ttl_seconds: result.redis_ttl}, null, 2);
      }
      return true;
    } catch (error) {
      $('#error').hidden = false;
      $('#error').textContent = `${t(error instanceof TypeError ? 'networkError' : 'requestError')} (${error.message})`;
      return false;
    } finally { setBusy(false); }
  }
  async function resetScenario(pendingOptions = options) {
    if (busy) return;
    const previous = options;
    // Commit settings only when the server accepts the new scenario. A failed
    // reset must not leave the browser claiming that a new lifetime is active.
    options = {...pendingOptions, generation: previous.generation + 1};
    if (await execute('reset')) {
      localStorage.setItem(generationKey, options.generation);
      // Reload must keep the applied TTL, particularly if a long-lived file or
      // Redis entry is still present after leaving and returning to this page.
      localStorage.setItem(optionsKey, JSON.stringify(options));
      history.length = 0; stepIndex = 0;
      $('#file-panel').hidden = true;
      $('#redis-panel').hidden = true;
      feedbackKey = 'ready';
    } else options = previous;
    writeInputs(); translateTask();
  }
  $('#detail-setting').hidden = ![8, 9].includes(number);
  if (number <= 2) {
    // Configuration tasks have no homework TTL; do not invent one in the UI.
    $('#lifetime-settings').hidden = true; $('#ttl-note').hidden = true;
    $('#apply-settings').hidden = true;
  }
  writeInputs(); translateTask();
  document.addEventListener('languagechange', translateTask);
  $('#apply-settings').addEventListener('click', async () => {
    const ttl = Number($('#ttl').value), detailTtl = Number($('#detail-ttl').value);
    if (![ttl, detailTtl].every(value => Number.isInteger(value) && value >= 1 && value <= 3600)) {
      $('#error').hidden = false; $('#error').textContent = t('invalidInput'); return;
    }
    await resetScenario({...options, ttl, detail_ttl: detailTtl, scenario: $('#scenario').value});
  });
  $('#scenario').addEventListener('change', () => {
    // Selecting a preset stages input values; Apply commits and resets it.
    const staged = preset($('#scenario').value, number, boot.original_ttl);
    $('#ttl').value = staged.ttl; $('#detail-ttl').value = staged.detail_ttl;
  });
  $('#reset').addEventListener('click', () => { writeInputs(); resetScenario(); });
  $('#previous-step').addEventListener('click', () => {
    if (busy || stepIndex === 0) return;
    // Revisit the previous instruction without undoing real database writes
    // or fabricating a past cache state. Next step can execute it again.
    stepIndex -= 1;
    feedbackKey = 'previousNote'; translateTask();
  });
  $('#next-step').addEventListener('click', async () => {
    const step = steps[stepIndex];
    if (!step || busy) return;
    if (step.wait && remainingSeconds(step.wait) > 0) {
      $('#feedback').textContent = t('pending', {seconds: Math.ceil(remainingSeconds(step.wait))}); return;
    }
    if (await execute(step.action)) { stepIndex += 1; translateTask(); }
  });
  setInterval(renderTimers, 100);
}
