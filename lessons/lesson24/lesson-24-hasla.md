## Teoria przechowywania i łamania haseł

Przechowywanie haseł w bazie danych w formie jawnej (plaintext) jest błędem krytycznym. W przypadku wycieku danych wszystkie konta zostają natychmiast skompromitowane. Do bezpiecznego składowania haseł stosuje się **funkcje skrótu (kryptograficzne funkcje hashujące)**.

### Hashowanie a szyfrowanie

* **Szyfrowanie** jest operacją dwukierunkową. Posiadając klucz, można odszyfrować tekst do formy pierwotnej.
* **Hashowanie** jest operacją jednokierunkową. Niemożliwe jest matematyczne odwrócenie skrótu (hasha) w celu poznania pierwotnego hasła.

Aby uniemożliwić ataki przy użyciu **tęczowych tablic** (gotowych baz danych zawierających wygenerowane wcześniej hashe dla popularnych haseł), stosuje się **sól (salt)**. Sól to losowy ciąg znaków doklejany do hasła przed jego zhashowaniem. Każdy użytkownik otrzymuje unikalną sól, co sprawia, że dwa takie same hasła w bazie danych mają zupełnie inne skróty.


Jaś
    hasło: Haslo123! - hashowanie + sól(x2) -> x2:shnn290opsmkjs0912msmk
Małgosia
    hasło: Haslo123! - hashowanie + sól(sdks)-> sdks:2ju90ij2nijwjkojhsj



### Metody łamania haseł

1. **Brute-force:** Sprawdzanie wszystkich możliwych kombinacji znaków po kolei.
2. **Atak słownikowy:** Testowanie słów ze zdefiniowanych baz danych (często wzbogaconych o popularne permutacje, np. dodanie "123").
3. **Akceleracja sprzętowa:** Współczesne ataki nie są wykonywane na procesorach (CPU), lecz na kartach graficznych (GPU) lub dedykowanych układach scalonych (ASIC/FPGA). Układy te potrafią przetwarzać miliardy hashy na sekundę.
4. **Tęczowe tablice:** Dane zawierające pary hasło, hash.

---

## Domyślna konfiguracja Django

Standardowo Django używa algorytmu **PBKDF2** z podpisem **SHA-256**.

### Charakterystyka domyślnego rozwiązania:

* **Liczba iteracji:** Django stale zwiększa tę wartość wraz z kolejnymi wersjami frameworka (obecnie wynosi ona kilkaset tysięcy iteracji).
* **Mechanizm:** Hasło i sól są wielokrotnie wielokrotnie hashowane, co sztucznie wydłuża czas potrzebny na sprawdzenie pojedynczej kombinacji.
* **Wada:** PBKDF2 jest algorytmem obciążającym wyłącznie procesor (CPU-bound). Z tego powodu jest podatny na łamanie przy użyciu układów GPU/ASIC, które potrafią masowo i równolegle przetwarzać operacje matematyczne SHA-256.

---

## Algorytm Argon2

Argon2 to zwycięzca konkursu *Password Hashing Competition (PHC)* z 2015 roku. Jest uznawany za obecny standard branżowy w dziedzinie bezpiecznego przechowywania haseł.

### Warianty algorytmu:

* **Argon2d:** Zoptymalizowany pod kątem odporności na ataki na bazie GPU. Wykorzystuje dostęp do pamięci zależny od danych, co czyni go podatnym na ataki typu *side-channel* (analiza czasu reakcji).
* **Argon2i:** Wykorzystuje dostęp do pamięci niezależny od danych. Jest odporny na ataki *side-channel*, ale mniej odporny na GPU.
* **Argon2id:** Wariant hybrydowy. Łączy cechy obu powyższych (w pierwszej fazie działa jak Argon2i, w kolejnych jak Argon2d). **To ten wariant jest implementowany w Django.**

### Zalety Argon2id:

1. **Memory-hardness (Wymóg pamięciowy):** Algorytm wymaga określonej ilości pamięci RAM do wykonania obliczeń. Układy GPU i ASIC posiadają bardzo szybką, ale ograniczoną pojemnościowo pamięć podręczną na pojedynczy rdzeń obliczeniowy. Wymuszenie zajętości np. 64 MB RAM-u dla jednego hasha drastycznie blokuje możliwość masowego, równoległego łamania haseł na kartach graficznych.
2. **Time-hardness (Koszt czasowy):** Definiuje liczbę przejść przez zaalokowaną pamięć.
3. **Wielowątkowość (Parallelism):** Pozwala na zrównoleglenie obliczeń na procesorze serwera w celu przyspieszenia weryfikacji legalnego użytkownika.

---

## Konfiguracja w Django (Best Practices)

Aby poprawnie wdrożyć Argon2 o niestandardowych parametrach bez wprowadzania błędów architektonicznych (takich jak zapętlenia w plikach konfiguracyjnych), należy oddzielić definicję klasy od plików ustawień projektu.

### 0. Instalacja
`pip install django[argon2]` lub `pip install argon2-cffi`

### 1. Implementacja logiki algorytmu

Klasę modyfikującą parametry umieszcza się w pliku z kodem źródłowym aplikacji (np. `app/hashers.py` lub osobnym module `core/hashers.py`).

```python
# plik: app/hashers.py
from django.contrib.auth.hashers import Argon2PasswordHasher

class CustomArgon2PasswordHasher(Argon2PasswordHasher):
    time_cost = 3         # Liczba iteracji
    memory_cost = 65536   # Zużycie pamięci RAM: 64 MB (65536 KiB)
    parallelism = 4       # Liczba równoległych wątków CPU

```

### 2. Implementacja w konfiguracji

W pliku konfiguracyjnym (np. `settings/auth_settings.py` lub bezpośrednio w sekcji uwierzytelniania) definiuje się listę `PASSWORD_HASHERS`. Pierwsza pozycja na liście określa domyślny algorytm dla nowych haseł.

```python
# plik: settings.py

PASSWORD_HASHERS = [
    'proj.hashers.CustomArgon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

```

> **Uwaga eksploatacyjna:** Dobór parametrów `memory_cost` oraz `time_cost` musi być dostosowany do zasobów sprzętowych serwera produkcyjnego. Zbyt wysokie wartości mogą doprowadzić do ataku typu DoS (Denial of Service) poprzez wysycenie pamięci RAM serwera przy masowych próbach logowania (nawet tych nieudanych).

https://docs.djangoproject.com/en/6.0/topics/auth/passwords/
https://kapitanhack.pl/analiza-lamania-hasel/