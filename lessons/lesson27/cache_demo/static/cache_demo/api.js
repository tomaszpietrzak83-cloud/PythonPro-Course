// All actions use same-origin POST. Cross-port navigation happens through links.
// The CSRF token protects database edits; cache: no-store avoids browser caching.
const session = localStorage.getItem('cache-demo-session') || crypto.randomUUID();
localStorage.setItem('cache-demo-session', session);
export async function performAction(number, options, action) {
  const token = document.cookie.split('; ').find(value => value.startsWith('csrftoken='))?.split('=')[1];
  const response = await fetch(`/demo/api/${number}/`, {
    method: 'POST', cache: 'no-store',
    headers: {'Content-Type': 'application/json', 'X-CSRFToken': token || ''},
    body: JSON.stringify({...options, session, action}),
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error_type || result.error || `HTTP ${response.status}`);
  return result;
}
export async function serverHealth(port) {
  const response = await fetch(`http://${location.hostname}:${port}/demo/health/`, {
    cache: 'no-store', signal: AbortSignal.timeout(4000),
  });
  return response.json();
}
export async function processStates() {
  const response = await fetch('/control/status/', {cache: 'no-store'});
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}
export async function controlProcess(project, action, token) {
  const response = await fetch(`/control/${project}/`, {
    method: 'POST', cache: 'no-store',
    headers: {'Content-Type': 'application/json', 'X-Control-Token': token},
    body: JSON.stringify({action}),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data;
}
