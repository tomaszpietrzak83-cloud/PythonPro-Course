# Lekcja 37 — Docker i Docker Compose

Z katalogu głównego kursu uruchom:

```powershell
.venv/Scripts/python.exe lessons/lesson37/run_app.py
```

Aplikacja jest dostępna pod adresem http://127.0.0.1:8037/. W razie braku zależności zainstaluj je z `lessons/lesson37/requirements.txt`.

Każde z 20 zadań ma własny katalog `examples/taskXX`. We wstępie zobaczysz, co zrobi pokaz. W zakładce **Obserwuj działanie** uruchomisz przykład, a w **Zrozum kod** możesz najechać na numer wiersza, nazwę lub blok kodu i przypiąć objaśnienie kliknięciem.

Pokazy w przeglądarce działają również bez Dockera. Aby uruchomić rzeczywisty przykład, przejdź do katalogu zadania zawierającego plik Compose, np. `examples/task10`. Użyj `docker compose up --build`, a po zakończeniu `docker compose down`. Zadania 6 i 7 mają jednorazowy proces demonstracyjny. Dla zadania 19 ustaw `DJANGO_SUPERUSER_PASSWORD` przy testowaniu poza lokalnym środowiskiem demonstracyjnym. Zadanie 20 pobiera model Ollama.
