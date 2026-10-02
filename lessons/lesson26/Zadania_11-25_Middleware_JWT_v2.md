## **Zadania podstawowe – poziom 1**

#### **11. 🔧 Zadanie 11 – Własny nagłówek w odpowiedzi**

**Treść zadania**

Stwórz middleware, który do każdej odpowiedzi HTTP dodaje nagłówek `X-App-Name` o wartości `DjangoJWT`. Uruchom aplikację i sprawdź w pliku `.http` klienta REST, czy nagłówek pojawia się zarówno dla zwykłego endpointu, jak i dla endpointu uwierzytelniania.

---

#### **12. 🔧 Zadanie 12 – Sprawdzenie kolejności middleware**

**Treść zadania**

Utwórz `FirstMiddleware` i `SecondMiddleware`. Każdy ma wypisywać komunikat przed oraz po `get_response()`.

---

#### **13. 🔧 Zadanie 13 – Test błędnych nagłówków Authorization**

**Treść zadania**

Przetestuj cztery warianty nagłówka `Authorization` na chronionym endpointcie.

---

#### **14. 🔧 Zadanie 14 – Access token kontra refresh token w praktyce**

**Treść zadania**

Spróbuj użyć refresh tokenu jako tokenu dostępowego, a potem wykonaj to samo zapytanie z access tokenem.

---

#### **15. 🔧 Zadanie 15 – Zmienne w pliku HTTP**

**Treść zadania**

Utwórz w pliku `.http` zmienną `@baseUrl`, a tokeny pobieraj z odpowiedzi nazwanych zapytań logowania i odświeżania. Dopasuj dane logowania do użytkownika istniejącego w bazie projektu.

---

## **Zadania średnie – poziom 2**

#### **16. ⚙️ Zadanie 16 – Pomiar czasu obsługi zapytania przez middleware**

**Treść zadania**

Stwórz middleware mierzący czas obsługi zapytania, dodający `X-Response-Time` i wypisujący wynik w konsoli.

---

#### **17. ⚙️ Zadanie 17 – Middleware wymagający własnego nagłówka**

**Treść zadania**

Dla ścieżek zaczynających się od `/api/private/` wymagaj nagłówka `X-Client-Id`. Bez niego zwróć `403`.

---

#### **18. ⚙️ Zadanie 18 – Endpoint tylko dla administratora**

**Treść zadania**

Utwórz `/api/admin-info/`, dostępny wyłącznie dla administratora.

---

#### **19. ⚙️ Zadanie 19 – Pobieranie danych aktualnego użytkownika przez Djoser**

**Treść zadania**

Wywołaj `/auth/users/me/` z access tokenem, a następnie bez niego.

---

#### **20. ⚙️ Zadanie 20 – Automatyzacja logowania w Pythonie**

**Treść zadania**

Napisz skrypt w Pythonie z użyciem `requests`, który loguje użytkownika, pobiera access token i odpytuje chroniony endpoint.

---

## **Zadania zaawansowane – poziom 3**

#### **21. 🚀 Zadanie 21 – Automatyczne odświeżenie tokenu w skrypcie**

**Treść zadania**

Jeśli chroniony endpoint zwróci `401`, użyj refresh tokenu, pobierz nowy access token i ponów zapytanie.

---

#### **22. 🚀 Zadanie 22 – Identyfikator każdego requestu**

**Treść zadania**

Wygeneruj `request_id`, zapisz go w `request.request_id` i dodaj do nagłówka `X-Request-ID`.

---

#### **23. 🚀 Zadanie 23 – Blokowanie wybranych adresów IP**

**Treść zadania**

Dodaj `BLOCKED_IPS` i stwórz middleware zwracający `403`, jeśli adres klienta jest na liście.

---

#### **24. 🚀 Zadanie 24 – Własne dane w tokenie JWT**

**Treść zadania**

Dodaj do payloadu tokenu własny claim, np. `username`.

---

#### **25. 🚀 Zadanie 25 – Mini-system API z pełnym przepływem uwierzytelniania**

**Treść zadania**

Zbuduj moduł `notes`, w którym:

- `/api/status/` jest publiczny,
- zalogowany użytkownik widzi własne notatki,
- nie widzi notatek innych użytkowników,
- administrator może sprawdzić liczbę wszystkich użytkowników,
- każde zapytanie dostaje `X-Request-ID`,
- logowanie i odświeżanie odbywają się przez JWT.
