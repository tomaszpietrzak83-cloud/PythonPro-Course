# Lesson 28 - Zadania

## Projekt końcowy - wybierz swój projekt Django

Przeszedłeś już drogę od podstaw Pythona, przez bazy danych, Git, aż po zaawansowane funkcje Django.

Zadanie końcowe polega na stworzeniu w pełni funkcjonalnej aplikacji webowej.

Wybierz jeden z poniższych projektów i zrealizuj go krok po kroku.

## Wspólne wymagania dla wszystkich projektów

Każda aplikacja musi spełniać poniższe wymagania:

- **Rejestracja i uwierzytelnianie** - wykorzystaj wbudowany system `django.contrib.auth`.
- **Rozbudowany panel admina**:
  - dodaj `search_fields`,
  - dodaj `list_filter`,
  - użyj `inlines` do edycji powiązanych modeli,
  - zadbaj o czytelne `list_display`, także z własnymi metodami.
- **Generowanie danych testowych** - użyj bibliotek Seeder/Faker.
- **Komenda management** - stwórz własną komendę, na przykład:

```bash
python manage.py seed_db
```

- **Testy jednostkowe** - napisz kilka podstawowych testów, na przykład:
  - czy modele poprawnie się tworzą,
  - czy widoki zwracają kod `200`.
- **Obsługa mediów** - wykorzystaj `ImageField` do przesyłania i wyświetlania obrazków.
- **Estetyczny interfejs** - aplikacja powinna być przyjazna dla użytkownika i odporna na podstawowe błędy.

<p style="color:red"><strong>Komentarz mentora:</strong> Przy projekcie końcowym lepiej zrobić mniej funkcji, ale działających end-to-end, niż wiele ekranów bez dopracowanej logiki i testów.</p>

## Projekt 1 - Strona kina: KinoMania

Stwórz serwis internetowy dla kina, w którym użytkownicy mogą przeglądać repertuar, poznawać szczegóły filmów i rezerwować bilety na seanse.

### Główne modele

- `Film`
  - `tytul`
  - `opis`
  - `data_premiery`
  - `plakat`
- `Aktor`
  - `imie_nazwisko`
  - `zdjecie`
- `Rezyser`
  - `imie_nazwisko`
  - `zdjecie`
- `Gatunek`
  - `nazwa`
- `Seans`
  - `czas_rozpoczecia`
  - `cena`
- `Rezerwacja`
  - `ilosc_miejsc`
  - `status`
- `Uzytkownik`
  - `username`

### Kluczowe funkcjonalności

- Przeglądanie listy filmów w repertuarze.
- Strona szczegółów filmu z obsadą, reżyserem, opisem i zwiastunem.
- Wyświetlanie harmonogramu seansów na dany dzień.
- System rezerwacji biletów na wybrany seans tylko dla zalogowanych.
- Panel użytkownika z listą jego rezerwacji.

### Co przećwiczysz?

- Złożone relacje `ManyToMany`, na przykład Film-Aktor i Film-Gatunek.
- Pracę z datą i czasem przy obsłudze seansów.
- Logikę biznesową, na przykład sprawdzanie dostępności miejsc.
- Zaawansowane zapytania `QuerySet` do filtrowania repertuaru.

## Projekt 2 - Strona biblioteki: BiblioTech

Zaprojektuj i wdróż system do zarządzania katalogiem książek w bibliotece.

Użytkownicy mogą przeglądać zbiory, wyszukiwać pozycje i rezerwować je online.

### Główne modele

- `Autor`
  - `imie_nazwisko`
  - `zdjecie`
- `Gatunek`
  - `nazwa`
- `Ksiazka`
  - `tytul`
  - `opis`
  - `data_wydania`
  - `okladka`
- `Egzemplarz`
  - `status`, na przykład `dostepny` albo `wypozyczony`
- `Uzytkownik`
  - `username`
- `Rezerwacja`
  - `data_rezerwacji`
  - `data_waznosci`

### Kluczowe funkcjonalności

- Katalog książek z filtrowaniem po autorze i gatunku.
- Wyszukiwarka tekstowa.
- Strona szczegółów książki z informacją o dostępnych egzemplarzach.
- Możliwość rezerwacji dostępnego egzemplarza na 2 tygodnie tylko dla zalogowanych.
- Panel użytkownika z listą aktualnych i historycznych rezerwacji.

### Co przećwiczysz?

- Relację `OneToMany`, gdzie jedna książka może mieć wiele egzemplarzy.
- Zarządzanie stanami, na przykład dostępnością egzemplarza.
- Pracę z modułem `datetime` do obsługi terminów rezerwacji.
- Transakcje bazodanowe, aby uniknąć rezerwacji tego samego egzemplarza przez dwie osoby naraz.

## Projekt 3 - Portal muzyczny: BeatHub

Stwórz platformę, która pozwoli użytkownikom odkrywać nową muzykę.

Aplikacja będzie agregować informacje o artystach, albumach i piosenkach, a zalogowani użytkownicy będą mogli tworzyć własne playlisty.

### Główne modele

- `Artysta`
  - `pseudonim`
  - `zdjecie`
- `Album`
  - `tytul`
  - `data_wydania`
  - `okladka`
- `Piosenka`
  - `tytul`
  - `czas_trwania_s`
- `Gatunek`
  - `nazwa`
- `Playlista`
  - `nazwa`
  - `opis`
- `Uzytkownik`
  - `username`

### Kluczowe funkcjonalności

- Baza artystów, albumów i piosenek.
- Strona artysty z listą jego albumów.
- Strona albumu z listą piosenek.
- Możliwość tworzenia, edycji i usuwania własnych playlist tylko dla zalogowanych.
- Dodawanie i usuwanie piosenek z playlist.
- Publiczne profile użytkowników z ich playlistami.

### Co przećwiczysz?

- Intensywną pracę z relacjami `ManyToMany`, na przykład Playlista-Piosenka.
- Możliwość użycia niestandardowej tabeli pośredniej `through`, na przykład do zapisania kolejności piosenek na playliście.
- Zagnieżdżone `QuerySet`, na przykład znajdowanie wszystkich piosenek artysty z danego gatunku.
- Formularze i formsety do zarządzania playlistami.

## Projekt 4 - Wirtualne muzeum: ArtExplorer

Zbuduj stronę internetową muzeum, która pozwoli użytkownikom wirtualnie odkrywać zbiory.

Użytkownicy mogą przeglądać eksponaty, poznawać ich historię i autorów oraz grupować je według epok czy kategorii.

### Główne modele

- `Autor`
  - `imie_nazwisko`
  - `biografia`
  - `zdjecie`
- `Epoka`
  - `nazwa`
  - `opis`
- `Kategoria`
  - `nazwa`, na przykład malarstwo albo rzeźba
- `Eksponat`
  - `nazwa`
  - `opis`
  - `data_utworzenia`
  - `zdjecie`
- `Uzytkownik`
  - `username`

### Kluczowe funkcjonalności

- Galeria eksponatów z zaawansowanym filtrowaniem po autorze, epoce i kategorii.
- Strona szczegółów eksponatu z wysokiej jakości zdjęciem i pełnym opisem.
- Strony biograficzne autorów z listą ich dzieł w muzeum.
- Strony tematyczne dla epok i kategorii.
- Możliwość stworzenia wirtualnej wycieczki, na przykład jako prostej listy ulubionych eksponatów dla zalogowanego użytkownika.

### Co przećwiczysz?

- Budowanie systemów kategoryzacji i tagowania.
- Pracę z `ImageField` i potencjalnie z biblioteką `Pillow`.
- Tworzenie przejrzystych widoków opartych na filtrowaniu `QuerySet`.
- Projektowanie modeli z myślą o dużej ilości treści tekstowej i graficznej.

## Jak zacząć? Krótki plan działania

1. Wybierz projekt, który najbardziej Cię interesuje.
2. Zaprojektuj modele. Zastanów się nad polami i relacjami.
3. Narysuj schemat modeli, na przykład w Mermaid.
4. Stwórz projekt i aplikację Django.
5. Zdefiniuj modele w pliku `models.py`.
6. Uruchom migracje: `makemigrations` i `migrate`.
7. Skonfiguruj panel admina.
8. Napisz seeder, aby wypełnić bazę danymi testowymi.
9. Zacznij tworzyć widoki i szablony.
10. Pisz testy na bieżąco.
