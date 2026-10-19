import {bilingual, t} from './i18n.js';

// Keep disclosure state in the DOM: translating updates text in place rather
// than rebuilding the questions and closing answers the student already opened.
export function createQuestionPanel(bank) {
  const root = document.querySelector('#question-list');
  const entries = [];

  function translate() {
    entries.forEach((entry, index) => {
      entry.summary.textContent = bilingual(bank[index].question);
      entry.answer.textContent = bilingual(bank[index].answer);
      entry.more.textContent = t(entries.length < bank.length ? 'moreQuestions' : 'allQuestions');
      entry.more.disabled = entries.length >= bank.length;
    });
  }

  function revealNext() {
    if (entries.length >= bank.length) return;
    const details = document.createElement('details');
    details.className = 'practice-question';
    const summary = document.createElement('summary');
    const answerBox = document.createElement('div'); answerBox.className = 'question-answer';
    const answer = document.createElement('p');
    const more = document.createElement('button');
    more.type = 'button'; more.className = 'btn btn-outline-primary btn-sm';
    more.addEventListener('click', () => {
      revealNext();
      // The newly revealed question stays collapsed, so the learner can try
      // answering it before reading the explanation.
      entries.at(-1).summary.focus();
    });
    answerBox.append(answer, more); details.append(summary, answerBox); root.append(details);
    entries.push({summary, answer, more}); translate();
  }

  revealNext(); revealNext();
  return {translate};
}
