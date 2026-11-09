import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');
  async function submit(event) {
    event.preventDefault();
    setResult('Working…');
    try {
      const response = await fetch('/api/recommendations', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text: query})
      });
      if (!response.ok) throw Error('Request failed');
      const {id} = await response.json();
      for (let attempt = 0; attempt < 120; attempt++) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        const status = await fetch('/api/recommendations/' + id);
        if (!status.ok) throw Error('Status failed');
        const data = await status.json();
        if (data.state === 'SUCCESS') { setResult(data.books.join(', ')); return; }
        if (data.state === 'FAILURE') throw Error('Recommendation failed');
      }
      throw Error('Worker timeout');
    } catch (error) { setResult(error.message); }
  }
  return <main><h1>Book recommendations</h1><form onSubmit={submit}>
    <label>What do you want to read? <input value={query} required maxLength={500}
      onChange={event => setQuery(event.target.value)}/></label>
    <button>Recommend</button></form><p role="status">{result}</p></main>;
}
createRoot(document.getElementById('root')).render(<App/>);
