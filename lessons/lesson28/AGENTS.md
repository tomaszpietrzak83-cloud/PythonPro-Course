# GameShelf: utrzymywanie dokumentacji

- Po każdej zmianie kodu, wymagań lub zakończeniu wersji aktualizuj cztery pliki:
  `taskPL.md`, `roadmapPL.md`, `lesson-28-DONE.md`, `most_interesting.md`.
- Pliki są generowane. Zmieniaj opisy w `docs_pl_data.py`, wymagania w `task.md`
  i `roadmap.md`, a potwierdzony stan wykonania w `roadmap_done.md`.
- Po zakończeniu wersji dodaj jej rzeczywisty wynik do `roadmap_done.md`.
  Nie oznaczaj planowanych etapów API/Swagger jako wykonanych tylko dlatego,
  że kod używa JsonResponse lub wspólne środowisko ma zainstalowany DRF.
- Uruchom z głównego katalogu kursu:
  `python lessons/lesson28/update_docs.py`.
- Przed commitem sprawdź:
  `python lessons/lesson28/update_docs.py --check` oraz właściwe testy aplikacji.
  Włącz odświeżone pliki dokumentacji do commita danej wersji.
- Przy dodaniu wersji do roadmapy dodaj jej polski opis i lokalizację do STAGES.
  Przy zmianie nazw/położenia funkcji popraw odnośniki STAGES i INTERESTING.
- Fragmenty kodu i numery linii w most_interesting.md mają pochodzić z aktualnych
  plików przez AST. Nie utrzymuj oddzielnych, ręcznie przepisanych kopii.
- Zachowaj rolę mentora: tłumacz powód użycia rozwiązania, wskazuj najważniejsze
  ograniczenia, nie przypisuj uczniowi błędów na podstawie kodu wygenerowanego przez agenta.
