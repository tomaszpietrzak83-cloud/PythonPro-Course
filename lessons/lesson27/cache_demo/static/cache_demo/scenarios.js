// A walkthrough is data rather than a chain of nested click handlers.
// Each step declares an action, explanation and optional expiration gate.
export function stepsFor(number) {
  if (number <= 2) return [{action: 'probe', text: 'probeStep'}];
  if (number === 4) return [{action: 'write', text: 'writeStep'}, {action: 'read', text: 'readStep'}, {action: 'read', text: 'wait', wait: 'read'}];
  if (number === 5) return [{action: 'write', text: 'writeStep'}, {action: 'read', text: 'readStep'}, {action: 'clear', text: 'clearStep'}, {action: 'read', text: 'readStep'}];
  if (number === 8) return [{action: 'list', text: 'listStep'}, {action: 'detail', text: 'detailStep'}, {action: 'detail', text: 'hitDetail'}, {action: 'detail', text: 'wait', wait: 'detail'}, {action: 'list', text: 'staleList'}];
  if (number === 9) return [{action: 'list', text: 'listStep'}, {action: 'detail', text: 'detailStep'}, {action: 'detail', text: 'hitDetail'}, {action: 'update', text: 'updateStep'}, {action: 'detail', text: 'updatedDetail'}, {action: 'list', text: 'staleList'}];
  return [{action: 'read', text: 'first'}, {action: 'read', text: 'second'}, {action: 'read', text: 'wait', wait: 'read'}];
}
export function actionsFor(number) {
  if (number <= 2) return ['probe'];
  if (number === 4) return ['write', 'read', 'delete'];
  if (number === 5) return ['write', 'read', 'clear'];
  if ([8, 9].includes(number)) return ['list', 'detail', 'update'];
  return ['read'];
}
export function preset(name, number, original) {
  return {scenario: name, ttl: name === 'homework' ? original : (number === 7 ? 7 : 10),
    detail_ttl: name === 'homework' ? 60 : 7};
}
