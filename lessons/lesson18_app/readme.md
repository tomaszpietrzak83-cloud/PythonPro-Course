Lekcja 18: Flask + PostgreSQL — Master Class
ORM, Optymalizacja, Relacje i Prawdziwy Projekt
#lekcja  #python  #flask  #sqlalchemy  #postgresql  #performance

🎯 Cel lekcji
Po tej lekcji będziesz:
Rozumieć, dlaczego PostgreSQL zamiast SQLite
Umieć modelować skomplikowane relacje (Many-to-Many)
Wiedzieć, co to problem N+1 i jak go rozwiązać
Potrafić pisać wydajne zapytania
Mieć działający mini-projekt: System Rezerwacji Sal Konferencyjnych

📚 Spis treści
1. Dlaczego PostgreSQL?
2. Instalacja krok po kroku
3. Pierwszy kontakt: Flask + PostgreSQL
4. Typy relacji w bazach danych
5. Problem N+1 — Zabójca wydajności
6. Agregacje i statystyki
7. Transakcje — Wszystko albo nic
8. 🚀 PROJEKT: System Rezerwacji Sal
9. Zadania do samodzielnego wykonania

1. Dlaczego PostgreSQL?
SQLite vs PostgreSQL — Analogia z życia
Wyobraź sobie, że prowadzisz sklep:

SQLite
PostgreSQL
Notatnik z zamówieniami
Profesjonalny system kasowy
Działa offline
Działa przez sieć
Jeden użytkownik naraz
Tysiące użytkowników jednocześnie
Plik na dysku
Serwer bazy danych
Świetne do prototypów
Standard w produkcji

Kiedy używać czego?

```python
SQLite używasz gdy:
├── Uczysz się SQL/ORM
├── Budujesz prototyp/MVP
├── Aplikacja desktopowa (1 użytkownik)
└── Testy jednostkowe

PostgreSQL używasz gdy:
├── Aplikacja webowa (wielu użytkowników)
├── Potrzebujesz zaawansowanych funkcji (JSON, full-text search)
├── Dane są krytyczne (bankowość, e-commerce)
└── Praca w zespole (wspólna baza dev/staging)
```

Co PostgreSQL potrafi, a SQLite nie?

```sql
-- 1. Typy JSON (przechowywanie elastycznych danych)
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    metadata JSONB  -- SQLite nie ma tego typu!
);

INSERT INTO events (name, metadata)
VALUES ('Konferencja', '{"attendees": 150, "room": "A1", "catering":
true}');

-- Zapytanie po kluczu JSON
SELECT * FROM events WHERE metadata->>'room' = 'A1';

-- 2. Full-text search (wyszukiwanie pełnotekstowe)
SELECT * FROM articles
WHERE to_tsvector('polish', content) @@ to_tsquery('python & flask');
```

```sql
-- 3. Window functions (zaawansowane analizy)
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) as rank
FROM employees;
```

2. Instalacja krok po kroku
🪟 Windows — Szczegółowa instrukcja
Krok 1: Pobierz instalator

```python
1. Wejdź na: https://www.enterprisedb.com/downloads/postgres-postgresql-
downloads
2. Wybierz najnowszą wersję (np. 16.x) dla Windows x86-64
3. Pobierz plik .exe (~300 MB)
```

Krok 2: Instalacja

```python
1. Uruchom instalator jako Administrator
2. Komponenty do zainstalowania (zostaw wszystkie zaznaczone):
```

   ✅ PostgreSQL Server
   ✅ pgAdmin 4
   ✅ Stack Builder
   ✅ Command Line Tools

```python
3. Katalog instalacji: C:\Program Files\PostgreSQL\16
4. Katalog danych: C:\Program Files\PostgreSQL\16\data
5. 🔑 HASŁO SUPERUŻYTKOWNIKA: ustaw np. "admin123" (ZAPAMIĘTAJ!)
6. Port: 5432 (domyślny, nie zmieniaj)
7. Locale: Polish, Poland (lub Default)
```

Krok 3: Weryfikacja

```bash
# Otwórz PowerShell i sprawdź:
psql --version
# Powinno pokazać: psql (PostgreSQL) 16.x

# Jeśli nie działa, dodaj do PATH:
# C:\Program Files\PostgreSQL\16\bin
```

🍎 macOS — Najłatwiejsza metoda

```bash
# Metoda 1: Postgres.app (ZALECANA)
# 1. Pobierz z: https://postgresapp.com/
# 2. Przeciągnij do Applications
# 3. Uruchom i kliknij "Initialize"
# 4. Słonik w menu bar = serwer działa

# Metoda 2: Homebrew
brew install postgresql@16
brew services start postgresql@16

# Weryfikacja
psql --version
```

🐧 Linux (Ubuntu/Debian)

```bash
# Aktualizacja i instalacja
sudo apt update
sudo apt install postgresql postgresql-contrib libpq-dev python3-dev

# Sprawdź status
sudo systemctl status postgresql
# Powinno być: Active: active (running)

# Ustaw hasło dla użytkownika postgres
sudo -u postgres psql
# W konsoli psql:
\password postgres
# Wpisz hasło dwukrotnie (np. admin123)
\q
```

🐳 Docker — Dla znających kontenery

```bash
# Uruchomienie PostgreSQL w kontenerze
docker run --name flask-postgres \
    -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=admin123 \
    -e POSTGRES_DB=flask_app \
    -p 5432:5432 \
    -v postgres_data:/var/lib/postgresql/data \
    -d postgres:16

# Sprawdzenie
```

```bash
docker ps
docker logs flask-postgres
```

Tworzenie bazy danych
Po instalacji musisz utworzyć bazę dla swojego projektu:
Metoda 1: pgAdmin (graficznie)

```python
1. Uruchom pgAdmin 4
2. Kliknij prawym na "Databases"
3. Create → Database...
4. Nazwa: flask_masterclass
5. Owner: postgres
6. Save
```

Metoda 2: Terminal (szybciej)

```sql
# Windows (PowerShell jako Admin) lub Linux/macOS
psql -U postgres

# W konsoli psql:
CREATE DATABASE flask_masterclass;
\l  -- lista baz (sprawdź czy jest)
\q  -- wyjście
```

3. Pierwszy kontakt: Flask + PostgreSQL
Struktura projektu

```python
flask_masterclass/
├── app.py              # Główna aplikacja
├── models.py           # Modele bazy danych
├── routes.py           # Endpointy API
├── config.py           # Konfiguracja
├── requirements.txt    # Zależności
└── templates/
    └── dashboard.html
```

requirements.txt

```bash
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
psycopg2-binary==2.9.9
python-dotenv==1.0.0

# Instalacja
pip install -r requirements.txt
```

config.py — Bezpieczna konfiguracja

```bash
"""
Konfiguracja aplikacji Flask.
NIGDY nie commituj haseł do repozytorium!
"""
import os
from dotenv import load_dotenv

load_dotenv()  # Ładuje zmienne z pliku .env

class Config:
    """Bazowa konfiguracja."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Konfiguracja deweloperska."""
    DEBUG = True
    # Format: postgresql://USER:PASSWORD@HOST:PORT/DATABASE
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:admin123@localhost:5432/flask_masterclass'
    )
    # Pokaż zapytania SQL w konsoli (pomocne przy debugowaniu)
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Konfiguracja produkcyjna."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ECHO = False

# Słownik do łatwego wyboru
config = {
    'development': DevelopmentConfig,
```

```python
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

Plik .env (NIE commituj do git!)

```bash
# .env
SECRET_KEY=twoj-super-tajny-klucz-123
DATABASE_URL=postgresql://postgres:admin123@localhost:5432/flask_masterclass
FLASK_ENV=development
```

.gitignore

```python
.env
__pycache__/
*.pyc
.venv/
```

Minimalna aplikacja testowa

```bash
# app.py - Test połączenia
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])
db = SQLAlchemy(app)

# Prosty model testowy
class TestConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100))

@app.route('/')
def index():
    return "Flask + PostgreSQL działa! 🎉"

@app.route('/test-db')
def test_db():
    """Testuje połączenie z bazą."""
    try:
        # Próba wykonania prostego zapytania
```

```python
        db.session.execute(db.text('SELECT 1'))
        return "✅ Połączenie z PostgreSQL OK!"
    except Exception as e:
        return f"❌ Błąd połączenia: {str(e)}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzy tabele
        print("Tabele utworzone!")
    app.run(debug=True)
```

Uruchom i sprawdź:

```bash
python app.py
# Otwórz: http://127.0.0.1:5000/test-db
```

4. Typy relacji w bazach danych
Wizualna mapa relacji

```python
┌─────────────────────────────────────────────────────────────────┐
│                    TYPY RELACJI W SQL                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ONE-TO-MANY (1:N)              MANY-TO-MANY (M:N)             │
│  ─────────────────              ────────────────────            │
│                                                                 │
│  [Kategoria]                    [Produkt]     [Tag]            │
│       │                              │           │              │
│       │ ma wiele                     └─────┬─────┘              │
│       ▼                                    │                    │
│  [Produkt]                          [product_tags]              │
│  [Produkt]                          (tabela łącząca)           │
│  [Produkt]                                                      │
│                                                                 │
│  Przykłady:                     Przykłady:                      │
│  • Autor → Książki              • Studenci ↔ Kursy             │
│  • Klient → Zamówienia          • Aktorzy ↔ Filmy              │
│  • Folder → Pliki               • Użytkownicy ↔ Role           │
│                                                                 │
│  ONE-TO-ONE (1:1)                                               │
│  ─────────────────                                              │
```

```python
│  [User] ←──────→ [Profile]                                     │
│                                                                 │
│  Przykłady:                                                     │
│  • Użytkownik ↔ Profil                                         │
│  • Kraj ↔ Stolica                                              │
│  • Pracownik ↔ Karta dostępu                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Relacja One-to-Many (1:N) — Szczegółowo

```bash
"""
Scenariusz: Kategorie i Produkty
Jedna kategoria może mieć wiele produktów.
Jeden produkt należy do jednej kategorii.
"""

class Category(db.Model):
    __tablename__ = 'categories'  # Nazwa tabeli w bazie

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)

    # RELACJA: "products" to wirtualna właściwość (nie kolumna w bazie!)
    # backref='category' tworzy odwrotną relację w Product
    # lazy=True oznacza "ładuj produkty dopiero gdy ich użyję"
    products = db.relationship(
        'Product',           # Nazwa klasy powiązanej
        backref='category',  # Tworzy Product.category
        lazy=True,           # Lazy loading (domyślnie)
        cascade='all, delete-orphan'  # Usuń produkty gdy usuniesz kategorię
    )

    def __repr__(self):
        return f'<Category {self.name}>'

    def to_dict(self):
        """Serializacja do JSON."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'product_count': len(self.products)
        }
```

```bash
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Lepsze niż Float
dla pieniędzy!
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # KLUCZ OBCY: Łączy produkt z kategorią
    # ForeignKey wskazuje na kolumnę 'id' w tabeli 'categories'
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),  # tabela.kolumna
        nullable=False
    )

    # Dzięki backref='category' w Category, mamy tutaj:
    # self.category → obiekt Category

    def __repr__(self):
        return f'<Product {self.name} ({self.price} PLN)>'
```

Użycie w praktyce:

```bash
# Tworzenie
elektronika = Category(name="Elektronika", description="Sprzęt
elektroniczny")
laptop = Product(name="Laptop Dell", price=3500, category=elektronika)

# Lub przez ID
laptop2 = Product(name="MacBook", price=6000, category_id=elektronika.id)

db.session.add_all([elektronika, laptop, laptop2])
db.session.commit()

# Odczyt - od kategorii do produktów
kategoria = Category.query.filter_by(name="Elektronika").first()
print(f"Kategoria: {kategoria.name}")
for p in kategoria.products:  # Tu wykonuje się zapytanie SQL!
    print(f"  - {p.name}: {p.price} PLN")

# Odczyt - od produktu do kategorii
```

```python
produkt = Product.query.first()
print(f"{produkt.name} jest w kategorii: {produkt.category.name}")
```

Relacja Many-to-Many (M:N) — Szczegółowo

```bash
"""
Scenariusz: Produkty i Tagi
Jeden produkt może mieć wiele tagów (Promocja, Nowość, Bestseller).
Jeden tag może być przypisany do wielu produktów.

W SQL wymaga to TABELI ŁĄCZĄCEJ (association table).
"""

# TABELA ŁĄCZĄCA - to NIE jest klasa modelu!
# To obiekt Table, który przechowuje tylko pary (product_id, tag_id)
product_tags = db.Table(
    'product_tags',  # Nazwa tabeli w bazie
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'),
primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'),
primary_key=True),
    db.Column('added_at', db.DateTime, default=db.func.now())  #
Opcjonalnie: kiedy dodano
)

# Jak to wygląda w bazie:
# +------------+--------+---------------------+
# | product_id | tag_id | added_at            |
# +------------+--------+---------------------+
# | 1          | 1      | 2024-01-15 10:30:00 |
# | 1          | 3      | 2024-01-15 10:30:00 |
# | 2          | 1      | 2024-01-16 14:22:00 |
# +------------+--------+---------------------+

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    color = db.Column(db.String(7), default='#6c757d')  # Kolor HEX dla UI

    def __repr__(self):
        return f'<Tag {self.name}>'
```

```bash
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'),
nullable=False)

    # RELACJA M:N
    tags = db.relationship(
        'Tag',                    # Klasa powiązana
        secondary=product_tags,   # Tabela łącząca (kluczowe!)
        lazy='subquery',          # Ładuj tagi w podzapytaniu
        backref=db.backref(
            'products',           # Tag.products zwróci produkty z tym
tagiem
            lazy=True
        )
    )
```

Użycie M:N w praktyce:

```bash
# Tworzenie tagów
promo = Tag(name="Promocja", color="#dc3545")
nowość = Tag(name="Nowość", color="#28a745")
bestseller = Tag(name="Bestseller", color="#ffc107")

db.session.add_all([promo, nowość, bestseller])
db.session.commit()

# Dodawanie tagów do produktu
laptop = Product.query.filter_by(name="Laptop Dell").first()
laptop.tags.append(promo)      # Dodaj tag
laptop.tags.append(bestseller)
db.session.commit()

# Sprawdzenie tagów produktu
print(f"Tagi produktu {laptop.name}:")
for tag in laptop.tags:
    print(f"  #{tag.name}")

# Odwrotnie: produkty z danym tagiem
tag_promo = Tag.query.filter_by(name="Promocja").first()
print(f"\nProdukty z tagiem 'Promocja':")
```

```bash
for product in tag_promo.products:
    print(f"  - {product.name}")

# Usuwanie taga z produktu
laptop.tags.remove(promo)
db.session.commit()

# Filtrowanie: znajdź produkty z konkretnym tagiem
bestsellery = Product.query.filter(
    Product.tags.any(name='Bestseller')
).all()
```

Relacja One-to-One (1:1)

```bash
"""
Scenariusz: Użytkownik i Profil
Każdy użytkownik ma dokładnie jeden profil.
Każdy profil należy do dokładnie jednego użytkownika.
"""

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # uselist=False oznacza "to nie jest lista, to jeden obiekt"
    profile = db.relationship(
        'Profile',
        backref='user',
        uselist=False,  # KLUCZOWE dla 1:1!
        cascade='all, delete-orphan'
    )

class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
# unique=True!
    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
```

```bash
    phone = db.Column(db.String(20))

# Użycie:
user = User(email="jan@example.com", password_hash="...")
user.profile = Profile(full_name="Jan Kowalski", bio="Developer")
db.session.add(user)
db.session.commit()

# Dostęp
print(user.profile.full_name)  # "Jan Kowalski"
print(user.profile.user.email) # "jan@example.com"
```

5. Problem N+1 — Zabójca wydajności
Co to jest problem N+1?
To najczęstszy błąd wydajnościowy w aplikacjach z ORM. Nazwa pochodzi od liczby zapytań
SQL:
1 zapytanie pobiera listę obiektów
N dodatkowych zapytań pobiera powiązane obiekty (dla każdego z listy)
Wizualizacja problemu

```python
SCENARIUSZ: Wyświetl 100 produktów z nazwą kategorii
```

❌ ZŁE PODEJŚCIE (N+1):

```python
┌─────────────────────────────────────────────────────────────────┐
│ Zapytanie 1: SELECT * FROM products                             │
│ → Zwraca 100 produktów                                          │
├─────────────────────────────────────────────────────────────────┤
│ Pętla po produktach:                                            │
│   Zapytanie 2:  SELECT * FROM categories WHERE id = 1           │
│   Zapytanie 3:  SELECT * FROM categories WHERE id = 1           │
│   Zapytanie 4:  SELECT * FROM categories WHERE id = 2           │
│   ...                                                           │
│   Zapytanie 101: SELECT * FROM categories WHERE id = 5          │
├─────────────────────────────────────────────────────────────────┤
│ RAZEM: 101 zapytań SQL! 🔥                                      │
│ Czas: ~500-1000ms przy lokalnej bazie                           │
│ Czas: ~2-5 sekund przy zdalnej bazie                            │
└─────────────────────────────────────────────────────────────────┘
```

✅ DOBRE PODEJŚCIE (Eager Loading):

```python
┌─────────────────────────────────────────────────────────────────┐
│ Zapytanie 1: SELECT * FROM products                             │
│              LEFT OUTER JOIN categories                          │
│              ON products.category_id = categories.id            │
│ → Zwraca 100 produktów Z KATEGORIAMI w jednym zapytaniu         │
├─────────────────────────────────────────────────────────────────┤
│ RAZEM: 1 zapytanie SQL! ⚡                                       │
│ Czas: ~10-50ms                                                  │
└─────────────────────────────────────────────────────────────────┘
```

Kod demonstracyjny

```bash
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import event
from flask import Flask
import time

app = Flask(__name__)
# ... konfiguracja ...

# DEBUGGING: Licznik zapytań SQL
query_count = 0

@event.listens_for(db.engine, "before_cursor_execute")
def count_queries(conn, cursor, statement, parameters, context,
executemany):
    global query_count
    query_count += 1

@app.route('/demo-n-plus-1')
def demo_n_plus_1():
    """Demonstracja problemu N+1."""
    global query_count
    results = []

    # ❌ ZŁY SPOSÓB - Problem N+1
    query_count = 0
    start = time.time()

    products = Product.query.all()  # Zapytanie 1
    bad_result = []
    for p in products:
```

```html
        # Każde p.category wywołuje NOWE zapytanie!
        bad_result.append(f"{p.name} - {p.category.name}")

    bad_time = time.time() - start
    bad_queries = query_count

    # ✅ DOBRY SPOSÓB - Eager Loading
    query_count = 0
    start = time.time()

    products = Product.query.options(
        joinedload(Product.category)  # Dołącz kategorię od razu
    ).all()  # Jedno zapytanie z JOIN

    good_result = []
    for p in products:
        # Tutaj NIE MA nowych zapytań - dane są już w pamięci
        good_result.append(f"{p.name} - {p.category.name}")

    good_time = time.time() - start
    good_queries = query_count

    return f"""
    <h2>Porównanie wydajności</h2>
    <table border="1" cellpadding="10">
        <tr>
            <th>Metoda</th>
            <th>Zapytań SQL</th>
            <th>Czas</th>
        </tr>
        <tr style="background: #ffcccc">
            <td>❌ Bez optymalizacji (N+1)</td>
            <td>{bad_queries}</td>
            <td>{bad_time*1000:.2f} ms</td>
        </tr>
        <tr style="background: #ccffcc">
            <td>✅ Z joinedload</td>
            <td>{good_queries}</td>
            <td>{good_time*1000:.2f} ms</td>
        </tr>
    </table>
    <p>Różnica: {bad_queries / good_queries:.0f}x mniej zapytań!</p>
    """
```

Metody Eager Loading w SQLAlchemy

```bash
from sqlalchemy.orm import joinedload, selectinload, subqueryload

# 1. JOINEDLOAD - Jeden JOIN (najszybsze dla 1:N i 1:1)
products = Product.query.options(
    joinedload(Product.category)
).all()
# SQL: SELECT ... FROM products LEFT OUTER JOIN categories ...

# 2. SELECTINLOAD - Dwa zapytania (dobre dla M:N)
products = Product.query.options(
    selectinload(Product.tags)
).all()
# SQL 1: SELECT ... FROM products
# SQL 2: SELECT ... FROM tags WHERE id IN (1, 2, 3, ...)

# 3. SUBQUERYLOAD - Podzapytanie
products = Product.query.options(
    subqueryload(Product.tags)
).all()

# 4. ZAGNIEŻDŻONE - Wiele poziomów
products = Product.query.options(
    joinedload(Product.category),
    selectinload(Product.tags)
).all()

# 5. GŁĘBOKO ZAGNIEŻDŻONE - Kategoria -> Produkty -> Tagi
categories = Category.query.options(
    joinedload(Category.products).selectinload(Product.tags)
).all()
```

Kiedy używać której metody?

```python
joinedload:
├── Relacje 1:1 (User → Profile)
├── Relacje 1:N gdy potrzebujesz "rodzica" (Product → Category)
└── Małe ilości danych po stronie "wiele"

selectinload:
├── Relacje M:N (Product ↔ Tags)
├── Relacje 1:N gdy "wiele" to dużo rekordów
└── Gdy JOIN generowałby dużo duplikatów

subqueryload:
```

```python
├── Alternatywa dla selectinload
└── Czasem szybsze przy skomplikowanych filtrach
```

6. Agregacje i statystyki
Import niezbędnych funkcji

```python
from sqlalchemy import func, desc, asc, case, distinct, extract
from sqlalchemy.sql import label
```

Podstawowe agregacje

```bash
# 1. COUNT - Liczenie rekordów
total_products = db.session.query(func.count(Product.id)).scalar()
# SQL: SELECT COUNT(products.id) FROM products

# 2. SUM - Suma
total_value = db.session.query(func.sum(Product.price)).scalar()
# SQL: SELECT SUM(products.price) FROM products

# 3. AVG - Średnia
avg_price = db.session.query(func.avg(Product.price)).scalar()
# SQL: SELECT AVG(products.price) FROM products

# 4. MIN / MAX
cheapest = db.session.query(func.min(Product.price)).scalar()
most_expensive = db.session.query(func.max(Product.price)).scalar()

# 5. Wszystko naraz
stats = db.session.query(
    func.count(Product.id).label('total'),
    func.sum(Product.price).label('value'),
    func.avg(Product.price).label('avg'),
    func.min(Product.price).label('min'),
    func.max(Product.price).label('max')
).first()

print(f"""
Statystyki magazynu:
- Produktów: {stats.total}
- Wartość: {stats.value:.2f} PLN
- Średnia cena: {stats.avg:.2f} PLN
```

```python
- Najtańszy: {stats.min:.2f} PLN
- Najdroższy: {stats.max:.2f} PLN
""")
```

GROUP BY — Grupowanie

```bash
# Statystyki per kategoria
stats_by_category = db.session.query(
    Category.name,
    func.count(Product.id).label('product_count'),
    func.sum(Product.price).label('total_value'),
    func.avg(Product.price).label('avg_price')
).join(Product).group_by(Category.name).all()

# Wynik:
# [('Elektronika', 50, 125000.00, 2500.00), ('Książki', 30, 1500.00, 50.00)]

for stat in stats_by_category:
    print(f"""
    Kategoria: {stat.name}
    - Produktów: {stat.product_count}
    - Wartość: {stat.total_value:.2f} PLN
    - Średnia: {stat.avg_price:.2f} PLN
    """)
```

HAVING — Filtrowanie grup

```bash
# Znajdź kategorie z więcej niż 10 produktami
popular_categories = db.session.query(
    Category.name,
    func.count(Product.id).label('count')
).join(Product).group_by(Category.name).having(
    func.count(Product.id) > 10
).all()

# SQL:
# SELECT categories.name, COUNT(products.id) as count
# FROM categories JOIN products ON ...
# GROUP BY categories.name
# HAVING COUNT(products.id) > 10
```

Zaawansowane: CASE WHEN

```bash
# Kategoryzacja cenowa produktów
price_distribution = db.session.query(
    case(
        (Product.price < 50, 'Tanie'),
        (Product.price < 200, 'Średnie'),
        (Product.price < 1000, 'Drogie'),
        else_='Premium'
    ).label('price_range'),
    func.count(Product.id).label('count')
).group_by('price_range').all()

# Wynik: [('Tanie', 25), ('Średnie', 40), ('Drogie', 20), ('Premium', 15)]
```

Praktyczny endpoint ze statystykami

```bash
@app.route('/dashboard')
def dashboard():
    """Dashboard ze statystykami sklepu."""

    # Ogólne statystyki
    general = db.session.query(
        func.count(Product.id).label('total_products'),
        func.sum(Product.price * Product.stock).label('inventory_value'),
        func.count(distinct(Category.id)).label('total_categories')
    ).join(Category).first()

    # Top 5 najdroższych produktów
    top_expensive = Product.query.options(
        joinedload(Product.category)
    ).order_by(desc(Product.price)).limit(5).all()

    # Produkty z niskim stanem (<10)
    low_stock = Product.query.filter(
        Product.stock < 10
    ).order_by(Product.stock).all()

    # Statystyki per kategoria
    category_stats = db.session.query(
        Category.name,
        func.count(Product.id).label('products'),
        func.avg(Product.price).label('avg_price')
    ).join(Product).group_by(Category.name).all()

    return render_template(
        'dashboard.html',
```

```python
        general=general,
        top_expensive=top_expensive,
        low_stock=low_stock,
        category_stats=category_stats
    )
```

7. Transakcje — Wszystko albo nic
Czym są transakcje?
Transakcja to zestaw operacji, które muszą się wykonać wszystkie albo żadna. To podstawa
bezpieczeństwa danych.

```python
Przykład: Przelew bankowy
```

❌ BEZ TRANSAKCJI:

```python
1. Odejmij 100 zł z konta A  ✓
2. [BŁĄD SERWERA]
3. Dodaj 100 zł do konta B   ✗ (nie wykonano)
→ 100 zł "zniknęło"!
```

✅ Z TRANSAKCJĄ:

```python
1. START TRANSACTION
2. Odejmij 100 zł z konta A
3. [BŁĄD SERWERA]
4. ROLLBACK (cofnij wszystko)
→ Konto A ma nadal swoje pieniądze
```

ACID — Właściwości transakcji

```python
A - Atomicity (Atomowość)
    Wszystko albo nic. Nie ma stanów pośrednich.

C - Consistency (Spójność)
    Dane zawsze są w poprawnym stanie.

I - Isolation (Izolacja)
    Transakcje nie widzą swoich zmian nawzajem.

D - Durability (Trwałość)
    Po COMMIT dane są bezpiecznie zapisane.
```

Podstawowa obsługa transakcji

```bash
# Flask-SQLAlchemy automatycznie zarządza transakcjami
# db.session.commit() → zatwierdza zmiany
# db.session.rollback() → cofa zmiany

def transfer_money(from_account_id, to_account_id, amount):
    """Bezpieczny przelew między kontami."""
    try:
        # Pobierz konta
        from_acc = Account.query.get(from_account_id)
        to_acc = Account.query.get(to_account_id)

        # Walidacja
        if from_acc is None or to_acc is None:
            raise ValueError("Konto nie istnieje")

        if from_acc.balance < amount:
            raise ValueError("Niewystarczające środki")

        # Operacje (jeszcze nie zapisane w bazie!)
        from_acc.balance -= amount
        to_acc.balance += amount

        # Zatwierdź transakcję
        db.session.commit()
        return True, "Przelew wykonany"

    except Exception as e:
        # Cofnij WSZYSTKIE zmiany z tej sesji
        db.session.rollback()
        return False, f"Błąd: {str(e)}"
```

Masowa aktualizacja z transakcją

```python
@app.route('/apply-discount/<float:percent>', methods=['POST'])
def apply_discount(percent):
    """
    Zastosuj rabat procentowy do wszystkich produktów.
    Jeśli cokolwiek pójdzie nie tak, nic się nie zmieni.
    """
    if percent < 0 or percent > 50:
        return {"error": "Rabat musi być między 0% a 50%"}, 400

    try:
```

```bash
        products = Product.query.all()
        updated_count = 0

        for product in products:
            old_price = float(product.price)
            new_price = old_price * (1 - percent / 100)

            # Walidacja biznesowa
            if new_price < 1:
                raise ValueError(
                    f"Cena produktu '{product.name}' spadłaby poniżej 1
PLN!"
                )

            product.price = round(new_price, 2)
            updated_count += 1

        # Wszystko OK - zatwierdź
        db.session.commit()

        return {
            "success": True,
            "message": f"Zaktualizowano {updated_count} produktów",
            "discount_applied": f"{percent}%"
        }

    except ValueError as e:
        db.session.rollback()
        return {"error": str(e)}, 400

    except Exception as e:
        db.session.rollback()
        return {"error": f"Nieoczekiwany błąd: {str(e)}"}, 500
```

Context manager dla transakcji

```python
from contextlib import contextmanager

@contextmanager
def transaction():
    """
    Context manager dla bezpiecznych transakcji.

    Użycie:
        with transaction():
```

```bash
            # operacje na bazie
            # automatyczny commit lub rollback
    """
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

# Przykład użycia
def create_order(user_id, product_ids):
    with transaction():
        order = Order(user_id=user_id, status='pending')
        db.session.add(order)
        db.session.flush()  # Pobierz ID bez commitowania

        for product_id in product_ids:
            product = Product.query.get(product_id)
            if product.stock < 1:
                raise ValueError(f"Brak {product.name} na stanie")

            product.stock -= 1
            item = OrderItem(order_id=order.id, product_id=product_id)
            db.session.add(item)

        # Commit wykona się automatycznie po wyjściu z 'with'

    return order
```

Blokowanie rekordów (FOR UPDATE)

```bash
def reserve_product(product_id, quantity):
    """
    Rezerwacja produktu z blokadą.
    Zapobiega race conditions przy jednoczesnych zamówieniach.
    """
    try:
        # with_for_update() blokuje rekord dla innych transakcji
        product =
Product.query.filter_by(id=product_id).with_for_update().first()

        if product is None:
            raise ValueError("Produkt nie istnieje")
```

```python
        if product.stock < quantity:
            raise ValueError(f"Dostępne tylko {product.stock} sztuk")

        product.stock -= quantity
        db.session.commit()

        return True, f"Zarezerwowano {quantity}x {product.name}"

    except Exception as e:
        db.session.rollback()
        return False, str(e)
```

8. 🚀 PROJEKT: System Rezerwacji Sal
Zbudujemy prawdziwy system rezerwacji sal konferencyjnych. Wykorzystamy wszystko, czego
się nauczyliśmy!
Wymagania biznesowe

```python
SYSTEM REZERWACJI SAL KONFERENCYJNYCH

Funkcjonalności:
1. Zarządzanie salami (CRUD)
2. Zarządzanie wyposażeniem sal (M:N)
3. Rezerwacje z walidacją konfliktów
4. Dashboard ze statystykami
5. API REST

Relacje:
- Sala ma wiele Rezerwacji (1:N)
- Sala ma wiele Wyposażeń (M:N)
- Użytkownik ma wiele Rezerwacji (1:N)
```

Struktura projektu

```python
room_booking/
├── app/
│   ├── __init__.py      # Fabryka aplikacji
│   ├── models.py        # Modele bazy danych
│   ├── routes/
│   │   ├── __init__.py
```

```python
│   │   ├── rooms.py     # Endpointy sal
│   │   ├── bookings.py  # Endpointy rezerwacji
│   │   └── dashboard.py # Dashboard
│   └── templates/
│       ├── base.html
│       ├── rooms.html
│       ├── bookings.html
│       └── dashboard.html
├── config.py
├── requirements.txt
└── run.py
```

models.py — Kompletne modele

```bash
"""
Modele bazy danych dla systemu rezerwacji sal.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# TABELA ŁĄCZĄCA: Sale i Wyposażenie (M:N)
room_equipment = db.Table(
    'room_equipment',
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id'),
primary_key=True),
    db.Column('equipment_id', db.Integer, db.ForeignKey('equipment.id'),
primary_key=True)
)

class User(db.Model):
    """Model użytkownika systemu."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacja 1:N z rezerwacjami
```

```bash
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'department': self.department,
            'is_admin': self.is_admin
        }

class Equipment(db.Model):
    """Model wyposażenia sali (projektor, tablica, wideokonferencja
itp.)."""
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(50))  # np. "projector", "whiteboard"

    def __repr__(self):
        return f'<Equipment {self.name}>'

class Room(db.Model):
    """Model sali konferencyjnej."""
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    hourly_rate = db.Column(db.Numeric(10, 2), default=0)  # Koszt za
godzinę

    # Relacja 1:N z rezerwacjami
    bookings = db.relationship('Booking', backref='room', lazy='dynamic',
                               cascade='all, delete-orphan')

    # Relacja M:N z wyposażeniem
```

```bash
    equipment = db.relationship(
        'Equipment',
        secondary=room_equipment,
        lazy='subquery',
        backref=db.backref('rooms', lazy=True)
    )

    def __repr__(self):
        return f'<Room {self.name} (cap: {self.capacity})>'

    def to_dict(self, include_equipment=True):
        data = {
            'id': self.id,
            'name': self.name,
            'capacity': self.capacity,
            'floor': self.floor,
            'description': self.description,
            'is_active': self.is_active,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else
0
        }
        if include_equipment:
            data['equipment'] = [e.name for e in self.equipment]
        return data

    def is_available(self, start_time, end_time, exclude_booking_id=None):
        """
        Sprawdza, czy sala jest dostępna w podanym przedziale czasowym.

        Args:
            start_time: Początek rezerwacji (datetime)
            end_time: Koniec rezerwacji (datetime)
            exclude_booking_id: ID rezerwacji do pominięcia (przy edycji)

        Returns:
            bool: True jeśli sala jest dostępna
        """
        query = Booking.query.filter(
            Booking.room_id == self.id,
            Booking.status != 'cancelled',
            # Sprawdzenie nakładania się przedziałów czasowych
            Booking.start_time < end_time,
            Booking.end_time > start_time
        )

        if exclude_booking_id:
```

```bash
            query = query.filter(Booking.id != exclude_booking_id)

        return query.count() == 0

class Booking(db.Model):
    """Model rezerwacji sali."""
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'),
nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    status = db.Column(
        db.String(20),
        default='confirmed',
        nullable=False
    )  # confirmed, cancelled, completed

    attendees_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
onupdate=datetime.utcnow)

    # Indeks dla szybkiego wyszukiwania
    __table_args__ = (
        db.Index('idx_booking_room_time', 'room_id', 'start_time',
'end_time'),
    )

    def __repr__(self):
        return f'<Booking {self.title} ({self.start_time})>'

    @property
    def duration_hours(self):
        """Czas trwania rezerwacji w godzinach."""
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600
```

```bash
    @property
    def total_cost(self):
        """Całkowity koszt rezerwacji."""
        if self.room and self.room.hourly_rate:
            return float(self.room.hourly_rate) * self.duration_hours
        return 0

    def to_dict(self, include_room=False, include_user=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'status': self.status,
            'attendees_count': self.attendees_count,
            'duration_hours': round(self.duration_hours, 2),
            'total_cost': round(self.total_cost, 2)
        }
        if include_room:
            data['room'] = self.room.to_dict(include_equipment=False)
        if include_user:
            data['user'] = self.user.to_dict()
        return data

# --- FUNKCJE POMOCNICZE ---

def find_available_rooms(start_time, end_time, min_capacity=1,
required_equipment=None):
    """
    Znajdź dostępne sale spełniające kryteria.

    Args:
        start_time: Początek (datetime)
        end_time: Koniec (datetime)
        min_capacity: Minimalna pojemność
        required_equipment: Lista nazw wymaganego wyposażenia

    Returns:
        Lista dostępnych sal
    """
    from sqlalchemy.orm import joinedload

    # Podstawowe zapytanie z eager loading
```

```bash
    query = Room.query.options(
        joinedload(Room.equipment)
    ).filter(
        Room.is_active == True,
        Room.capacity >= min_capacity
    )

    # Filtruj po wyposażeniu
    if required_equipment:
        for eq_name in required_equipment:
            query = query.filter(
                Room.equipment.any(Equipment.name == eq_name)
            )

    # Pobierz kandydatów
    candidate_rooms = query.all()

    # Sprawdź dostępność każdej sali
    available = []
    for room in candidate_rooms:
        if room.is_available(start_time, end_time):
            available.append(room)

    return available

def get_booking_statistics(start_date=None, end_date=None):
    """
    Pobierz statystyki rezerwacji.

    Returns:
        dict: Słownik ze statystykami
    """
    from sqlalchemy import func, extract

    base_query = db.session.query(Booking).filter(
        Booking.status != 'cancelled'
    )

    if start_date:
        base_query = base_query.filter(Booking.start_time >= start_date)
    if end_date:
        base_query = base_query.filter(Booking.end_time <= end_date)

    # Ogólne statystyki
    total_bookings = base_query.count()
```

```bash
    # Statystyki per sala
    room_stats = db.session.query(
        Room.name,
        func.count(Booking.id).label('booking_count'),
        func.sum(
            extract('epoch', Booking.end_time - Booking.start_time) / 3600
        ).label('total_hours')
    ).join(Booking).filter(
        Booking.status != 'cancelled'
    ).group_by(Room.name).all()

    # Statystyki per dzień tygodnia
    weekday_stats = db.session.query(
        extract('dow', Booking.start_time).label('weekday'),
        func.count(Booking.id).label('count')
    ).filter(
        Booking.status != 'cancelled'
    ).group_by('weekday').order_by('weekday').all()

    weekdays = ['Nd', 'Pn', 'Wt', 'Śr', 'Cz', 'Pt', 'Sb']

    return {
        'total_bookings': total_bookings,
        'room_stats': [
            {
                'room': r.name,
                'bookings': r.booking_count,
                'hours': round(float(r.total_hours or 0), 1)
            }
            for r in room_stats
        ],
        'weekday_stats': [
            {
                'day': weekdays[int(w.weekday)],
                'count': w.count
            }
            for w in weekday_stats
        ]
    }
```

routes/bookings.py — Endpointy rezerwacji

```python
"""
Endpointy API dla rezerwacji.
```

```bash
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import db, Booking, Room, User

bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')

@bookings_bp.route('/', methods=['GET'])
def get_bookings():
    """
    Pobierz listę rezerwacji z filtrami.

    Query params:
        room_id: Filtruj po sali
        user_id: Filtruj po użytkowniku
        date: Filtruj po dacie (YYYY-MM-DD)
        status: Filtruj po statusie
    """
    from sqlalchemy.orm import joinedload

    query = Booking.query.options(
        joinedload(Booking.room),
        joinedload(Booking.user)
    )

    # Filtry
    if room_id := request.args.get('room_id'):
        query = query.filter(Booking.room_id == room_id)

    if user_id := request.args.get('user_id'):
        query = query.filter(Booking.user_id == user_id)

    if date_str := request.args.get('date'):
        date = datetime.strptime(date_str, '%Y-%m-%d')
        query = query.filter(
            db.func.date(Booking.start_time) == date.date()
        )

    if status := request.args.get('status'):
        query = query.filter(Booking.status == status)

    # Sortowanie
    query = query.order_by(Booking.start_time.desc())

    # Paginacja
```

```bash
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'bookings': [b.to_dict(include_room=True, include_user=True)
                     for b in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@bookings_bp.route('/', methods=['POST'])
def create_booking():
    """
    Utwórz nową rezerwację.

    Body JSON:
        room_id: int
        user_id: int
        title: str
        start_time: str (ISO format)
        end_time: str (ISO format)
        description: str (optional)
        attendees_count: int (optional)
    """
    data = request.get_json()

    # Walidacja wymaganych pól
    required = ['room_id', 'user_id', 'title', 'start_time', 'end_time']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Brak wymaganego pola: {field}'}), 400

    try:
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.fromisoformat(data['end_time'])
    except ValueError:
        return jsonify({'error': 'Niepoprawny format daty. Użyj ISO
format.'}), 400

    # Walidacja logiczna
    if start_time >= end_time:
        return jsonify({'error': 'Czas rozpoczęcia musi być przed czasem
```

```bash
zakończenia'}), 400

    if start_time < datetime.now():
        return jsonify({'error': 'Nie można rezerwować w przeszłości'}), 400

    # Sprawdź czy sala istnieje
    room = Room.query.get(data['room_id'])
    if not room:
        return jsonify({'error': 'Sala nie istnieje'}), 404

    if not room.is_active:
        return jsonify({'error': 'Sala jest nieaktywna'}), 400

    # Sprawdź czy użytkownik istnieje
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'Użytkownik nie istnieje'}), 404

    # Sprawdź dostępność sali
    if not room.is_available(start_time, end_time):
        return jsonify({
            'error': 'Sala jest już zarezerwowana w tym czasie',
            'conflicts': get_conflicts(room.id, start_time, end_time)
        }), 409

    # Sprawdź pojemność
    attendees = data.get('attendees_count', 1)
    if attendees > room.capacity:
        return jsonify({
            'error': f'Zbyt wielu uczestników. Pojemność sali:
{room.capacity}'
        }), 400

    # Utwórz rezerwację
    try:
        booking = Booking(
            room_id=room.id,
            user_id=user.id,
            title=data['title'],
            description=data.get('description'),
            start_time=start_time,
            end_time=end_time,
            attendees_count=attendees
        )

        db.session.add(booking)
```

```python
        db.session.commit()

        return jsonify({
            'message': 'Rezerwacja utworzona',
            'booking': booking.to_dict(include_room=True)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Błąd tworzenia rezerwacji: {str(e)}'}),
500

@bookings_bp.route('/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    """Anuluj rezerwację."""
    booking = Booking.query.get_or_404(booking_id)

    if booking.status == 'cancelled':
        return jsonify({'error': 'Rezerwacja już anulowana'}), 400

    if booking.start_time < datetime.now():
        return jsonify({'error': 'Nie można anulować przeszłej
rezerwacji'}), 400

    try:
        booking.status = 'cancelled'
        db.session.commit()
        return jsonify({'message': 'Rezerwacja anulowana'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/available-rooms', methods=['GET'])
def find_available():
    """
    Znajdź dostępne sale.

    Query params:
        start_time: str (ISO format)
        end_time: str (ISO format)
        capacity: int (optional)
        equipment: str (comma-separated, optional)
    """
    from app.models import find_available_rooms
```

```python
    try:
        start_time = datetime.fromisoformat(request.args['start_time'])
        end_time = datetime.fromisoformat(request.args['end_time'])
    except (KeyError, ValueError):
        return jsonify({'error': 'Wymagane: start_time i end_time w formacie
ISO'}), 400

    capacity = request.args.get('capacity', 1, type=int)

    equipment = None
    if eq_param := request.args.get('equipment'):
        equipment = [e.strip() for e in eq_param.split(',')]

    rooms = find_available_rooms(start_time, end_time, capacity, equipment)

    return jsonify({
        'available_rooms': [r.to_dict() for r in rooms],
        'search_criteria': {
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'min_capacity': capacity,
            'required_equipment': equipment
        }
    })

def get_conflicts(room_id, start_time, end_time):
    """Pomocnicza funkcja zwracająca konfliktujące rezerwacje."""
    conflicts = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.status != 'cancelled',
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).all()

    return [
        {
            'id': b.id,
            'title': b.title,
            'start': b.start_time.isoformat(),
            'end': b.end_time.isoformat()
        }
        for b in conflicts
    ]
```

routes/dashboard.py — Dashboard ze statystykami

```bash
"""
Dashboard ze statystykami.
"""
from flask import Blueprint, render_template, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from sqlalchemy.orm import joinedload
from app.models import db, Room, Booking, User, get_booking_statistics

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    """Strona główna dashboardu."""

    # Statystyki ogólne
    stats = {
        'total_rooms': Room.query.filter_by(is_active=True).count(),
        'total_users': User.query.count(),
        'total_bookings':
Booking.query.filter_by(status='confirmed').count(),
        'bookings_today': Booking.query.filter(
            func.date(Booking.start_time) == datetime.today().date(),
            Booking.status == 'confirmed'
        ).count()
    }

    # Najbliższe rezerwacje (następne 24h)
    now = datetime.now()
    upcoming = Booking.query.options(
        joinedload(Booking.room),
        joinedload(Booking.user)
    ).filter(
        Booking.start_time >= now,
        Booking.start_time <= now + timedelta(hours=24),
        Booking.status == 'confirmed'
    ).order_by(Booking.start_time).limit(10).all()

    # Top użytkownicy (najwięcej rezerwacji)
    top_users = db.session.query(
        User.name,
        func.count(Booking.id).label('booking_count')
    ).join(Booking).filter(
```

```bash
        Booking.status != 'cancelled'
    ).group_by(User.id).order_by(desc('booking_count')).limit(5).all()

    # Wykorzystanie sal (% czasu zarezerwowanego w ostatnim miesiącu)
    month_ago = now - timedelta(days=30)

    room_utilization = []
    active_rooms = Room.query.filter_by(is_active=True).all()

    for room in active_rooms:
        # Suma godzin rezerwacji
        total_hours = db.session.query(
            func.sum(
                func.extract('epoch', Booking.end_time - Booking.start_time)
/ 3600
            )
        ).filter(
            Booking.room_id == room.id,
            Booking.start_time >= month_ago,
            Booking.status != 'cancelled'
        ).scalar() or 0

        # Maksymalnie 8h dziennie * 22 dni robocze = 176h
        max_hours = 176
        utilization = (total_hours / max_hours) * 100

        room_utilization.append({
            'room': room.name,
            'hours': round(total_hours, 1),
            'utilization': round(utilization, 1)
        })

    # Sortuj po wykorzystaniu
    room_utilization.sort(key=lambda x: x['utilization'], reverse=True)

    return render_template(
        'dashboard.html',
        stats=stats,
        upcoming=upcoming,
        top_users=top_users,
        room_utilization=room_utilization
    )

@dashboard_bp.route('/api/dashboard/stats')
def api_stats():
```

```python
    """API endpoint dla statystyk (do wykresów JS)."""
    stats = get_booking_statistics()
    return jsonify(stats)
```

templates/dashboard.html

```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - System Rezerwacji</title>
    <link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.cs
s" rel="stylesheet">
    <style>
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }
        .stat-card h3 { font-size: 2.5rem; margin: 0; }
        .stat-card p { margin: 0; opacity: 0.8; }

        .utilization-bar {
            height: 25px;
            background: #e9ecef;
            border-radius: 5px;
            overflow: hidden;
        }
        .utilization-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #ffc107, #dc3545);
            transition: width 0.5s ease;
        }
    </style>
</head>
<body>
    <div class="container-fluid py-4">
        <h1 class="mb-4">📊 Dashboard Rezerwacji</h1>

        <!-- Statystyki ogólne -->
        <div class="row">
```

```html
            <div class="col-md-3">
                <div class="stat-card">
                    <h3>{{ stats.total_rooms }}</h3>
                    <p>🏢 Aktywnych sal</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card" style="background: linear-
gradient(135deg, #11998e 0%, #38ef7d 100%);">
                    <h3>{{ stats.total_bookings }}</h3>
                    <p>📅 Wszystkich rezerwacji</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card" style="background: linear-
gradient(135deg, #fc4a1a 0%, #f7b733 100%);">
                    <h3>{{ stats.bookings_today }}</h3>
                    <p>📆 Rezerwacji dziś</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card" style="background: linear-
gradient(135deg, #4568dc 0%, #b06ab3 100%);">
                    <h3>{{ stats.total_users }}</h3>
                    <p>👥 Użytkowników</p>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <!-- Najbliższe rezerwacje -->
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>🕐 Najbliższe rezerwacje (24h)</h5>
                    </div>
                    <div class="card-body">
                        <table class="table table-sm">
                            <thead>
                                <tr>
                                    <th>Godzina</th>
                                    <th>Sala</th>
                                    <th>Tytuł</th>
                                    <th>Osoba</th>
                                </tr>
                            </thead>
```

```html
                            <tbody>
                                {% for booking in upcoming %}
                                <tr>
                                    <td>{{
booking.start_time.strftime('%H:%M') }}</td>
                                    <td>{{ booking.room.name }}</td>
                                    <td>{{ booking.title[:30] }}{% if
booking.title|length > 30 %}...{% endif %}</td>
                                    <td>{{ booking.user.name }}</td>
                                </tr>
                                {% else %}
                                <tr>
                                    <td colspan="4" class="text-muted text-
center">Brak rezerwacji</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Wykorzystanie sal -->
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📈 Wykorzystanie sal (ostatnie 30 dni)</h5>
                    </div>
                    <div class="card-body">
                        {% for room in room_utilization %}
                        <div class="mb-3">
                            <div class="d-flex justify-content-between">
                                <span>{{ room.room }}</span>
                                <span>{{ room.utilization }}% ({{ room.hours
}}h)</span>
                            </div>
                            <div class="utilization-bar">
                                <div class="utilization-fill" style="width:
{{ room.utilization }}%"></div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
```

```html
        <!-- Top użytkownicy -->
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>🏆 Top rezerwujący</h5>
                    </div>
                    <div class="card-body">
                        <table class="table">
                            <tbody>
                                {% for user in top_users %}
                                <tr>
                                    <td>
                                        <span class="badge bg-primary me-2">
{{ loop.index }}</span>
                                        {{ user.name }}
                                    </td>
                                    <td class="text-end">
                                        <span class="badge bg-secondary">{{
user.booking_count }} rezerwacji</span>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script
src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.m
in.js"></script>
</body>
</html>
```

run.py — Uruchomienie aplikacji

```python
"""
Główny plik uruchamiający aplikację.
"""
from app import create_app
from app.models import db, User, Room, Equipment, Booking
```

```bash
from datetime import datetime, timedelta
import random

app = create_app()

def seed_database():
    """Wypełnia bazę przykładowymi danymi."""
    with app.app_context():
        # Sprawdź czy dane już istnieją
        if User.query.first():
            print("Baza już zawiera dane. Pomijam seeding.")
            return

        print("Tworzenie przykładowych danych...")

        # Wyposażenie
        equipment_list = [
            Equipment(name="Projektor", icon="projector"),
            Equipment(name="Tablica", icon="chalkboard"),
            Equipment(name="Wideokonferencja", icon="video"),
            Equipment(name="Klimatyzacja", icon="snowflake"),
            Equipment(name="Nagłośnienie", icon="volume-up"),
        ]
        db.session.add_all(equipment_list)

        # Sale
        rooms = [
            Room(name="Sala A1", capacity=10, floor=1,
                 description="Mała sala do spotkań zespołowych",
                 hourly_rate=50),
            Room(name="Sala B2", capacity=20, floor=2,
                 description="Średnia sala z projektorem",
                 hourly_rate=80),
            Room(name="Sala Konferencyjna", capacity=50, floor=3,
                 description="Duża sala na prezentacje",
                 hourly_rate=150),
            Room(name="Pokój Kreatywny", capacity=8, floor=1,
                 description="Sala do burzy mózgów z tablicami",
                 hourly_rate=60),
        ]

        # Przypisz wyposażenie
        rooms[0].equipment = [equipment_list[1], equipment_list[3]]  #
Tablica, Klimatyzacja
        rooms[1].equipment = [equipment_list[0], equipment_list[2],
```

```bash
equipment_list[3]]  # Projektor, Video, Klima
        rooms[2].equipment = equipment_list  # Wszystko
        rooms[3].equipment = [equipment_list[1]]  # Tylko tablica

        db.session.add_all(rooms)

        # Użytkownicy
        users = [
            User(name="Jan Kowalski", email="jan@firma.pl",
department="IT"),
            User(name="Anna Nowak", email="anna@firma.pl", department="HR"),
            User(name="Piotr Wiśniewski", email="piotr@firma.pl",
department="Marketing"),
            User(name="Maria Dąbrowska", email="maria@firma.pl",
department="IT", is_admin=True),
        ]
        db.session.add_all(users)
        db.session.commit()

        # Przykładowe rezerwacje
        titles = [
            "Spotkanie zespołu", "Code review", "Prezentacja projektu",
            "Rozmowa rekrutacyjna", "Szkolenie", "Planning sprint",
            "Retrospektywa", "Demo dla klienta"
        ]

        now = datetime.now().replace(minute=0, second=0, microsecond=0)

        for i in range(20):
            room = random.choice(rooms)
            user = random.choice(users)

            # Losowa data w najbliższych 14 dniach
            days_offset = random.randint(0, 14)
            hour = random.randint(9, 16)
            duration = random.choice([1, 2, 3])

            start = now + timedelta(days=days_offset, hours=hour - now.hour)
            end = start + timedelta(hours=duration)

            # Sprawdź dostępność
            if room.is_available(start, end):
                booking = Booking(
                    room=room,
                    user=user,
                    title=random.choice(titles),
```

```python
                    start_time=start,
                    end_time=end,
                    attendees_count=random.randint(2, room.capacity)
                )
                db.session.add(booking)

        db.session.commit()
        print("✅ Baza danych wypełniona przykładowymi danymi!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()

    app.run(debug=True, port=5000)
```

9. Zadania do samodzielnego wykonania
Zadanie 1: Konfiguracja środowiska (⭐)
1. Zainstaluj PostgreSQL na swoim systemie
2. Utwórz bazę danych room_booking
3. Skonfiguruj plik .env  z poprawnym connection string
4. Uruchom aplikację i sprawdź endpoint /test-db
Oczekiwany rezultat: Aplikacja łączy się z bazą i wyświetla "Połączenie OK!"

Zadanie 2: Analiza problemu N+1 (⭐⭐)
Dodaj do aplikacji endpoint /debug/n-plus-1  który:
1. Pobiera wszystkie rezerwacje BEZ optymalizacji
2. Dla każdej wyświetla: tytuł, nazwę sali, imię użytkownika
3. Mierzy czas wykonania i liczbę zapytań
4. Powtarza to samo Z optymalizacją ( joinedload )
5. Zwraca porównanie w formacie JSON
Podpowiedź: Użyj dekoratora @event.listens_for  do liczenia zapytań.

Zadanie 3: Rozszerzone statystyki (⭐⭐)
Rozszerz dashboard o:
1. Wykres kołowy - rozkład rezerwacji per departament
2. Heatmapa - które godziny są najpopularniejsze (macierz dzień tygodnia × godzina)
3. Trend - liczba rezerwacji dziennie w ostatnich 30 dniach
Podpowiedź: Użyj func.extract('dow', ...)  dla dnia tygodnia i func.extract('hour',
...)  dla godziny.

Zadanie 4: System powiadomień (⭐⭐⭐)
Zaimplementuj model Notification  i logikę:
1. Model z polami: user_id, message, is_read, created_at
2. Automatyczne tworzenie powiadomień:
Gdy ktoś rezerwuje salę → powiadomienie dla admina
Gdy rezerwacja jest za 1h → przypomnienie dla użytkownika
3. Endpoint GET /api/notifications  - lista nieprzeczytanych
4. Endpoint POST /api/notifications/{id}/read  - oznacz jako przeczytane
Podpowiedź: Użyj @event.listens_for(Booking, 'after_insert')  dla automatycznych
powiadomień.

Zadanie 5: Cykliczne rezerwacje (⭐⭐⭐⭐)
Zaimplementuj możliwość tworzenia cyklicznych rezerwacji:
1. Dodaj do modelu Booking pole recurrence_rule  (np. "WEEKLY", "BIWEEKLY")
2. Dodaj pole series_id  (UUID) łączące rezerwacje w serię
3. Endpoint tworzący serię rezerwacji (np. "co tydzień przez 3 miesiące")
4. Możliwość anulowania pojedynczej lub całej serii
5. Walidacja konfliktów dla wszystkich wystąpień
Podpowiedź: Użyj biblioteki python-dateutil  dla rrule .

Zadanie 6: Eksport do PDF (⭐⭐⭐⭐)
Stwórz endpoint generujący raport PDF:
1. /api/reports/monthly?month=2024-01
2. Raport zawiera:
Podsumowanie (liczba rezerwacji, łączny czas, przychód)
Tabela: top 10 sal
Tabela: top 10 użytkowników
Wykres wykorzystania (jako obraz)
3. Użyj biblioteki reportlab  lub weasyprint

📖 Materiały dodatkowe
Dokumentacja
SQLAlchemy ORM Tutorial
Flask-SQLAlchemy
PostgreSQL Documentation
Narzędzia do debugowania

```bash
# Włącz logowanie wszystkich zapytań SQL
app.config['SQLALCHEMY_ECHO'] = True

# Lub bardziej szczegółowo:
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

Przydatne query patterns

```bash
# Istnieje czy nie istnieje?
exists = db.session.query(
    Product.query.filter_by(name='Laptop').exists()
).scalar()

# Pierwszy lub None (bez wyjątku)
product = Product.query.filter_by(name='Laptop').first()
```

```bash
# Pierwszy lub 404
product = Product.query.filter_by(name='Laptop').first_or_404()

# Unikalne wartości
categories = db.session.query(distinct(Product.category_id)).all()

# LIKE (wyszukiwanie)
products = Product.query.filter(Product.name.ilike('%laptop%')).all()

# IN (lista wartości)
products = Product.query.filter(Product.id.in_([1, 2, 3])).all()

# BETWEEN
products = Product.query.filter(Product.price.between(100, 500)).all()

# NULL / NOT NULL
products = Product.query.filter(Product.description.is_(None)).all()
products = Product.query.filter(Product.description.isnot(None)).all()
```

✅ Checklist po lekcji
Zainstalowałem PostgreSQL i utworzyłem bazę danych
Rozumiem różnicę między SQLite a PostgreSQL
Potrafię modelować relacje 1:N, M:N, 1:1
Wiem, co to problem N+1 i jak go rozwiązać
Umiem używać joinedload , selectinload
Potrafię pisać zapytania z agregacjami ( func.count , func.sum , etc.)
Rozumiem transakcje i rollback
Zbudowałem działający mini-projekt

Autor: LearnIT
