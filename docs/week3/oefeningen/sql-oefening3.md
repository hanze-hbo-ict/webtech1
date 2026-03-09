# Oefening 3: SQL Injection Beveiliging

Deze oefening past bij [SQL Deel 5](../sql-deel5.md).

In deze oefening ga je zelf ervaren hoe SQL injection werkt en hoe je het voorkomt. Je bouwt een login systeem en test het met bekende SQL injection aanvallen.

## Voorbereiding

Maak een Python bestand `auth_system.py` met een basis class voor gebruikersbeheer:

```python
import sqlite3
from sqlite3 import Row

class AuthDatabase:
    """Gebruikersauthenticatie database."""

    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self) -> None:
        """Maak users tabel aan."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL,
                    is_admin BOOLEAN DEFAULT 0
                )
            """)
            conn.commit()

    def add_user(self, username: str, password: str, email: str, is_admin: bool = False) -> int:
        """Voeg user toe (veilig met placeholders)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)",
                (username, password, email, is_admin)
            )
            conn.commit()
            return cursor.lastrowid
```

## Opgave 1: Onveilige Login (GEVAARLIJK!)

**Doel:** Zie met eigen ogen hoe SQL injection werkt.

Voeg deze **onveilige** login method toe:

```python
def login_unsafe(self, username: str, password: str) -> Row | None:
    """GEVAARLIJK - gebruik f-string in SQL!"""
    # TODO: Implementeer deze ONVEILIGE method
    # - Gebruik een f-string om de query te maken
    # - Query: SELECT * FROM users WHERE username = '{username}' AND password = '{password}'
    # - Return de user row als gevonden, None anders
    # - GEBRUIK GEEN PLACEHOLDERS (dat is juist de fout!)
    pass
```

Test met normale input én SQL injection:

```python
db = AuthDatabase()

# Voeg test users toe
db.add_user("jan", "geheim123", "jan@email.nl", is_admin=False)
db.add_user("admin", "super_secret", "admin@email.nl", is_admin=True)

# Test 1: Normale login (werkt)
user = db.login_unsafe("jan", "geheim123")
print(f"Test 1: {user['username'] if user else 'Geen match'}")

# Test 2: Verkeerd wachtwoord (werkt niet)
user = db.login_unsafe("jan", "fout_wachtwoord")
print(f"Test 2: {user['username'] if user else 'Geen match'}")

# Test 3: SQL injection attack!
user = db.login_unsafe("admin' --", "whatever")
print(f"Test 3: {user['username'] if user else 'Geen match'}")  # GEVAAR: ingelogd als admin!
```

**Vraag:** Wat gebeurt er bij Test 3? Waarom werkt deze aanval?

<details>
<summary>Klik voor uitleg</summary>

De query wordt:

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = 'whatever'
```

De `--` maakt alles daarna commentaar, dus de password check wordt overgeslagen!
</details>

## Opgave 2: SQL Injection Aanvallen Testen

Test je `login_unsafe()` met deze bekende SQL injection strings:

```python
# SQL injection test strings
injection_tests = [
    ("admin' --", "anything"),           # Commentaar truc
    ("' OR '1'='1", "' OR '1'='1"),      # Altijd waar
    ("admin' OR '1'='1' --", ""),        # Combinatie
]

print("\n=== SQL Injection Tests ===")
for username, password in injection_tests:
    user = db.login_unsafe(username, password)
    if user:
        print(f"GEVAAR: Ingelogd als '{user['username']}' (admin={user['is_admin']})")
    else:
        print(f"Geblokkeerd: {username}")
```

**Vraag:** Welke aanvallen werken? Probeer te begrijpen waarom.

## Opgave 3: Veilige Login Method

**Doel:** Implementeer een veilige login met placeholders.

```python
def login_safe(self, username: str, password: str) -> Row | None:
    """Veilige login met placeholders."""
    # TODO: Implementeer deze VEILIGE method
    # - Gebruik placeholders (?)
    # - Query: SELECT * FROM users WHERE username = ? AND password = ?
    # - Gebruik row_factory = Row
    # - Return de user row als gevonden, None anders
    pass
```

Test met dezelfde SQL injection strings:

```python
print("\n=== Veilige Login Tests ===")
for username, password in injection_tests:
    user = db.login_safe(username, password)
    if user:
        print(f"Ingelogd als '{user['username']}'")
    else:
        print(f"Geblokkeerd: {username}")

# Test normale login (moet nog steeds werken!)
user = db.login_safe("jan", "geheim123")
print(f"\nNormale login: {user['username'] if user else 'Geen match'}")
```

**Vraag:** Wat is het verschil? Waarom werken de aanvallen nu niet meer?

## Opgave 4: Veilige Search Functie

Implementeer een veilige zoekfunctie met `LIKE`:

```python
def search_users(self, search_term: str) -> list[Row]:
    """Zoek gebruikers op basis van username of email."""
    # TODO: Implementeer veilige search
    # - Gebruik LIKE met placeholders
    # - Zoek in username EN email (OR)
    # - Return lijst van users (zonder passwords!)
    # Tip: SELECT id, username, email FROM users WHERE username LIKE ? OR email LIKE ?
    pass
```

Test met SQL injection pogingen:

```python
# Normale search
users = db.search_users("jan")
print(f"\nSearch 'jan': {len(users)} resultaten")

# SQL injection poging
users = db.search_users("'; DROP TABLE users; --")
print(f"Search met injection: {len(users)} resultaten")  # Moet 0 zijn (veilig!)
```

## Opgave 5: Whitelist Validatie

Soms kun je geen placeholders gebruiken (bijvoorbeeld bij table names). Dan moet je input valideren met een **whitelist**.

Implementeer een method die data ophaalt uit verschillende tabellen:

```python
def get_all_from_table(self, table_name: str) -> list[Row]:
    """Haal alle records op uit een tabel (met whitelist validatie)."""
    # TODO: Implementeer met whitelist
    # - Maak een lijst van toegestane tabellen: ["users"]
    # - Check of table_name in de whitelist staat
    # - Raise ValueError als niet toegestaan
    # - Gebruik f-string voor table name (nu veilig omdat gevalideerd!)
    # - Query: SELECT * FROM {table_name}
    pass
```

Test:

```python
# Toegestane tabel - werkt
users = db.get_all_from_table("users")
print(f"\nUsers tabel: {len(users)} records")

# SQL injection poging - wordt geblokkeerd
try:
    db.get_all_from_table("users; DROP TABLE users; --")
except ValueError as e:
    print(f"Geblokkeerd: {e}")
```

## Bonusopdracht 1: Login Met Rate Limiting

Voeg een simpele vorm van rate limiting toe om brute force aanvallen te voorkomen:

```python
class AuthDatabase:
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self._create_table()
        self.login_attempts = {}  # {username: aantal_pogingen}

    def login_with_rate_limit(self, username: str, password: str, max_attempts: int = 3) -> Row | None:
        """Login met rate limiting."""
        # TODO: Implementeer rate limiting
        # - Check of username al max_attempts heeft bereikt
        # - Zo ja: return None en print waarschuwing
        # - Zo nee: probeer login_safe()
        # - Bij succes: reset attempts voor deze user
        # - Bij falen: verhoog attempts voor deze user
        pass
```

## Bonusopdracht 2: Password Hashing

In productie sla je **nooit** plain text passwords op! Gebruik een hash:

```python
import hashlib

class AuthDatabase:
    def _hash_password(self, password: str) -> str:
        """Hash password met SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user_hashed(self, username: str, password: str, email: str, is_admin: bool = False) -> int:
        """Voeg user toe met gehashed password."""
        # TODO: Gebruik _hash_password() voordat je password opslaat
        pass

    def login_hashed(self, username: str, password: str) -> Row | None:
        """Login met gehashed password compare."""
        # TODO: Hash input password en vergelijk met database
        # Tip: Haal user op met username, vergelijk gehashte passwords
        pass
```

**Let op:** SHA256 is NIET veilig genoeg voor productie! Gebruik in echte applicaties libraries zoals `bcrypt` of `argon2`.

## Verwachte Output

```text
Test 1: jan
Test 2: Geen match
Test 3: admin  ← GEVAAR!

=== SQL Injection Tests ===
GEVAAR: Ingelogd als 'admin' (admin=1)
GEVAAR: Ingelogd als 'jan' (admin=0)
GEVAAR: Ingelogd als 'admin' (admin=1)

=== Veilige Login Tests ===
Geblokkeerd: admin' --
Geblokkeerd: ' OR '1'='1
Geblokkeerd: admin' OR '1'='1' --

Normale login: jan

Search 'jan': 1 resultaten
Search met injection: 0 resultaten

Users tabel: 2 records
Geblokkeerd: Invalid table: users; DROP TABLE users; --
```

## Checklist

- `login_unsafe()` geïmplementeerd (met f-string - FOUT!)
- SQL injection aanvallen getest en begrepen
- `login_safe()` geïmplementeerd (met placeholders)
- `search_users()` met LIKE en placeholders
- `get_all_from_table()` met whitelist validatie
- Verschil tussen unsafe en safe begrepen
- **Nooit** f-strings of concatenatie met user input in SQL
- **Altijd** placeholders (`?`) voor values

## Belangrijke Lessen

1. **Placeholders zijn de ENIGE veilige methode** voor values in SQL
2. **F-strings/concatenatie** met user input = SQL injection risico
3. **Whitelist validatie** voor table/column names (placeholders werken daar niet)
4. **Test altijd** met bekende injection strings
5. **Hash passwords** (nooit plain text)

**Tip:** Test je eigen Flask applicaties altijd met deze strings. Als ze niet gewoon als letterlijke tekst behandeld worden, heb je een probleem!
