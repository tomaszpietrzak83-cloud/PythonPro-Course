import {t} from './i18n.js';

// Timers use monotonic browser time plus the server's measured remaining TTL.
// This avoids clock differences between machines and accidental restart on HIT.
// Rendering does not send requests and cannot refresh the server's cache.
const timers = new Map();
export function recordTimer(channel, result) {
  if (!result.expires_at) { timers.delete(channel); return; }
  const remaining = Math.max(0, result.expires_at - result.server_time);
  timers.set(channel, {deadline: performance.now() + remaining * 1000, ttl: result.ttl});
}
export function remainingSeconds(channel) {
  return Math.max(0, ((timers.get(channel)?.deadline || 0) - performance.now()) / 1000);
}
export function clearTimers() { timers.clear(); }
export function renderTimers() {
  const root = document.querySelector('#timers');
  root.replaceChildren();
  if (!timers.size) { root.textContent = t('notStarted'); return; }
  for (const [channel, timer] of timers) {
    const remaining = remainingSeconds(channel);
    const row = document.createElement('div'); row.className = 'timer-row';
    const label = document.createElement('div'); label.className = 'd-flex justify-content-between gap-2';
    const name = document.createElement('strong'); name.textContent = t(channel);
    const value = document.createElement('span');
    value.textContent = remaining > 0 ? t('remaining', {seconds: remaining.toFixed(1)}) : t('expiry');
    label.append(name, value);
    const track = document.createElement('div'); track.className = 'timer-track';
    const fill = document.createElement('div'); fill.className = 'timer-fill';
    fill.style.width = `${Math.min(100, remaining / timer.ttl * 100)}%`;
    track.append(fill); row.append(label, track); root.append(row);
  }
}
