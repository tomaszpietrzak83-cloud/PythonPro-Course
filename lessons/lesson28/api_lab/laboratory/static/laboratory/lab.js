(() => {
  const course = document.querySelector('#course');
  if (!course) return;
  const pages = [...document.querySelectorAll('.page')];
  const tabs = [...document.querySelectorAll('[data-page]')];
  let current = new URLSearchParams(location.search).get('section') === 'documentation' ? 1 : 0;
  let continuous = localStorage.getItem('api28-mode') === 'continuous';
  const mode = document.querySelector('#mode');
  function show() {
    pages.forEach((page, i) => { page.hidden = !continuous && i !== current; });
    tabs.forEach((tab, i) => { tab.setAttribute('aria-current', i === current ? 'step' : 'false'); });
    mode.textContent = continuous ? 'Tryb slajdów' : 'Tryb ciągły';
    document.querySelector('.pager').hidden = continuous;
    document.querySelector('#position').textContent = `${current + 1} / ${pages.length}`;
    document.querySelector('#previous').disabled = current === 0;
    document.querySelector('#next').disabled = current === pages.length - 1;
  }
  tabs.forEach((tab, i) => tab.addEventListener('click', () => {
    current = i; show();
    if (continuous) pages[i].scrollIntoView({behavior: 'smooth', block: 'start'});
  }));
  mode.addEventListener('click', () => {
    continuous = !continuous;
    localStorage.setItem('api28-mode', continuous ? 'continuous' : 'slides'); show();
  });
  document.querySelector('#previous').addEventListener('click', () => { current--; show(); });
  document.querySelector('#next').addEventListener('click', () => { current++; show(); });
  show();
  const method = document.querySelector('#method');
  const bodyLabel = document.querySelector('#body-label');
  function updateBody() { bodyLabel.hidden = method.value !== 'POST'; }
  method.addEventListener('change', updateBody); updateBody();
  let stageKey = 'automatic';
  let documentedMethod = 'GET';
  const stageTitles = {automatic: '1. Sam kod', docstring: '2. Dodany docstring', extended: '3. Dodany @extend_schema'};
  const productBase = () => `/api/v1/comparison/${stageKey}/products/`;
  function showDocumentation() {
    document.querySelectorAll('[data-documentation-stage]').forEach(panel => { panel.hidden = panel.dataset.documentationStage !== stageKey; });
    document.querySelectorAll('[data-operation]').forEach(panel => { panel.hidden = panel.dataset.operation !== documentedMethod; });
    document.querySelectorAll('[data-stage]').forEach(button => { button.setAttribute('aria-pressed', String(button.dataset.stage === stageKey)); });
    document.querySelectorAll('[data-doc-method]').forEach(button => { button.setAttribute('aria-pressed', String(button.dataset.docMethod === documentedMethod)); });
    document.querySelector('#active-documentation').textContent = `Testujesz wersję: ${stageTitles[stageKey]}. Zmień wersję w sekcji „Porównaj dokumentację”. Wszystkie wersje mają wspólną bazę produktów.`;
  }
  document.querySelectorAll('[data-stage]').forEach(button => button.addEventListener('click', () => { stageKey = button.dataset.stage; showDocumentation(); }));
  document.querySelectorAll('[data-doc-method]').forEach(button => button.addEventListener('click', () => { documentedMethod = button.dataset.docMethod; showDocumentation(); }));
  document.querySelector('[data-open-demo]').addEventListener('click', () => { current = 2; show(); pages[2].scrollIntoView({behavior: 'smooth', block: 'start'}); });
  document.querySelectorAll('.embedded-swagger').forEach(details => details.addEventListener('toggle', () => {
    const frame = details.querySelector('iframe');
    if (details.open && !frame.getAttribute('src')) frame.src = frame.dataset.src;
  }));
  showDocumentation();
  const deletePreset = document.querySelector('[data-preset="delete"]');
  let productId = Number(localStorage.getItem('api28-created-product'));
  function updateProduct() {
    const known = Number.isSafeInteger(productId) && productId > 0;
    deletePreset.disabled = !known;
    document.querySelector('#created-product').textContent = known ? `Ostatnio dodany notes ma numer ${productId}. Przycisk 3 wskazuje właśnie ten produkt.` : 'Przycisk 3 odblokuje się po dodaniu notesu przyciskiem 2. Dzięki temu usuwasz swój produkt demonstracyjny.';
  }
  updateProduct();
  document.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
    const preset = button.dataset.preset;
    method.value = preset === 'list' ? 'GET' : preset === 'delete' ? 'DELETE' : 'POST';
    document.querySelector('#url').value = preset === 'delete' ? `${productBase()}${productId}/` : productBase();
    document.querySelector('#body').value = preset === 'invalid'
      ? JSON.stringify({name: 'Produkt demonstracyjny', price: '-1', category: 1}, null, 2)
      : JSON.stringify({name: 'Notes z demonstracji', price: '19.90', category: 1}, null, 2);
    document.querySelector('#demo-guide').textContent = {
      list: 'GET pobierze aktualny katalog. Oczekiwana odpowiedź: 200.',
      create: 'POST zapisze nowy produkt. Oczekiwana odpowiedź: 201 i nowe ID. Następnie wybierz DELETE.',
      invalid: 'POST z ujemną ceną pokaże błędy pól. Oczekiwana odpowiedź: 400; produkt nie zostanie zapisany.',
      delete: `DELETE usunie produkt ${productId}. Oczekiwana odpowiedź: 204 bez treści. Wyślij ponownie, aby zobaczyć 404.`,
    }[preset];
    updateBody();
    document.querySelector('#request-form').requestSubmit();
  }));
  document.querySelector('#request-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const status = document.querySelector('#status');
    const result = document.querySelector('#result');
    const headersOutput = document.querySelector('#headers');
    const send = document.querySelector('#send');
    headersOutput.textContent = '—'; result.textContent = '—';
    const humanResult = document.querySelector('#human-result');
    humanResult.replaceChildren();
    document.querySelector('#contract-check').textContent = '';
    try {
      const value = document.querySelector('#url').value.trim();
      if (!value.startsWith('/api/v1/') && value !== '/api/schema/' && value !== '/api/schema/?format=json') {
        throw new Error('Użyj lokalnego adresu /api/v1/… lub /api/schema/.');
      }
      const url = new URL(value, location.origin);
      if (url.origin !== location.origin || url.hash || !url.pathname.startsWith('/api/')) {
        throw new Error('Nieprawidłowy adres API.');
      }
      const options = {method: method.value, credentials: 'same-origin', headers: {
        Accept: 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      }};
      if (method.value === 'POST') {
        const raw = document.querySelector('#body').value;
        try { JSON.parse(raw); } catch { throw new Error('Dane nie są poprawnym JSON.'); }
        options.body = raw; options.headers['Content-Type'] = 'application/json';
      }
      send.disabled = true; status.textContent = 'Wysyłanie żądania…';
      document.querySelectorAll('[data-preset]').forEach(button => { button.disabled = true; });
      document.querySelector('#request-summary').textContent = `${options.method} ${url.pathname}${url.search}`;
      document.querySelector('#response-explanation').textContent = '';
      const response = await fetch(url, options);
      const text = await response.text();
      if (response.status === 201 && options.method === 'POST' && (url.pathname === '/api/v1/products/' || /^\/api\/v1\/comparison\/(automatic|docstring|extended)\/products\/$/.test(url.pathname))) {
        const created = JSON.parse(text);
        if (Number.isSafeInteger(created.id) && created.id > 0) {
          productId = created.id;
          localStorage.setItem('api28-created-product', String(productId));
          updateProduct();
        }
      }
      status.textContent = `HTTP ${response.status} ${response.statusText}`;
      const comparedStage = url.pathname.match(/^\/api\/v1\/comparison\/(automatic|docstring|extended)\//);
      if (comparedStage) {
        const documented = document.querySelector(`[data-documentation-stage="${comparedStage[1]}"] [data-operation="${options.method}"] [data-response-code="${response.status}"]`);
        document.querySelector('#contract-check').textContent = documented
          ? `Porównanie z instrukcją „${stageTitles[comparedStage[1]]}”: kod ${response.status} jest wymieniony w dokumentacji. Wróć do „Porównaj dokumentację” i wybierz ${options.method}, aby go zobaczyć.`
          : `Porównanie z instrukcją „${stageTitles[comparedStage[1]]}”: serwer zwrócił ${response.status}, ale dokumentacja tej wersji nie opisuje tego kodu. Wersja 3 uzupełnia opis błędów — porównaj ją z tą wersją.`;
      }
      document.querySelector('#response-explanation').textContent = {
        200: 'Serwer zwrócił dane. Zobacz wynik poniżej.',
        201: 'Produkt został zapisany. Jego ID jest w wyniku. Teraz kliknij DELETE, aby go usunąć, lub GET, aby zobaczyć go na liście.',
        204: 'Produkt został usunięty. Pusta odpowiedź jest prawidłowa. Powtórz DELETE, aby zobaczyć 404, lub GET, aby sprawdzić listę.',
        400: 'Serwer odrzucił dane. Produkt nie został utworzony. Wynik wskazuje pole wymagające poprawy.',
        404: 'Produkt o tym ID nie istnieje — mógł już zostać usunięty. Dodaj nowy produkt przez POST.',
        403: 'Żądanie zostało odrzucone. Odśwież stronę i spróbuj ponownie.',
      }[response.status] || 'Sprawdź kod HTTP i treść odpowiedzi poniżej.';
      if (!text) result.textContent = '(brak treści odpowiedzi)';
      else { try { result.textContent = JSON.stringify(JSON.parse(text), null, 2); } catch { result.textContent = text; } }
      if (text) {
        let data;
        try { data = JSON.parse(text); } catch { data = null; }
        if (response.ok && data) {
          const products = Array.isArray(data) ? data : data.name && data.id ? [data] : [];
          if (products.length && products.every(product => product.name && product.price)) {
            const heading = document.createElement('p');
            heading.textContent = Array.isArray(data) ? `Liczba produktów w sklepie: ${products.length}. Oto aktualna lista:` : 'Serwer zapisał ten produkt:';
            humanResult.append(heading);
            const list = document.createElement('ul');
            products.forEach(product => {
              const row = document.createElement('li');
              row.textContent = `${product.name} — ${product.price} zł · numer produktu (ID): ${product.id}`;
              list.append(row);
            });
            humanResult.append(list);
          } else if (Array.isArray(data) && data.length === 0) {
            humanResult.textContent = 'Lista jest pusta — nie ma produktów pasujących do tej prośby.';
          } else if (data.sentiment) {
            humanResult.textContent = `Tekst: „${data.input_text}”. Słownik rozpoznał wydźwięk: ${({positive:'pozytywny',negative:'negatywny',neutral:'neutralny'})[data.sentiment]}. Rozpoznane słowa: ${data.matched_words.join(', ') || 'brak'}.`;
          }
        } else if (response.status === 400 && data && data.price) {
          humanResult.textContent = `Serwer nie zaakceptował ceny: ${data.price.join(' ')} To przykład sprawdzania danych przed zapisem.`;
        }
      }
      headersOutput.textContent = [...response.headers.entries()].map(([k, v]) => `${k}: ${v}`).join('\n');
    } catch (error) { status.textContent = `Błąd: ${error.message}`; }
    finally {
      send.disabled = false;
      document.querySelectorAll('[data-preset]').forEach(button => { button.disabled = false; });
      updateProduct();
    }
  });
})();
