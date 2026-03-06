# SQLite in Python: Basics

Python heeft de `sqlite3` library built-in. Hieronder zie je hoe je een database connectie maakt, queries uitvoert, en data ophaalt.

## Database connectie

De basis: database connectie maken en een tabel aanmaken.

```python
import sqlite3
from sqlite3 import Connection

def create_database() -> Connection:
    """Maak database connectie en tabel aan."""
    conn = sqlite3.connect("contacts.db")

    # Maak contacts tabel
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT
        )
    """)

    conn.commit()
    return conn

# Gebruik
conn = create_database()
print("Database en tabel aangemaakt")
conn.close()
```

!!! note "CREATE TABLE IF NOT EXISTS"
    Dit voorkomt errors als de tabel al bestaat. Handig tijdens development wanneer je het script meerdere keren uitvoert.

## Insert: Data toevoegen

Voeg contacten toe aan de database:

```python
import sqlite3

def add_contact(name: str, email: str, phone: str | None = None) -> int:
    """
    Voeg een contact toe aan de database.

    Returns:
        int: ID van het toegevoegde contact
    """
    conn = sqlite3.connect("contacts.db")

    cursor = conn.execute(
        "INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)",
        (name, email, phone)
    )

    contact_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return contact_id

# Gebruik
jan_id = add_contact("Jan Jansen", "jan@email.nl", "06-12345678")
sara_id = add_contact("Sara de Vries", "sara@email.nl")

print(f"Jan toegevoegd met ID: {jan_id}")
print(f"Sara toegevoegd met ID: {sara_id}")
```

!!! warning "SQL Injection voorkomen met placeholders"
    Gebruik **altijd** `?` placeholders in plaats van f-strings:
    **Goed:**
    ```python
    cursor.execute("SELECT * FROM contacts WHERE name = ?", (name,))
    ```
    **FOUT (SQL injection risico!):**
    ```python
    cursor.execute(f"SELECT * FROM contacts WHERE name = '{name}'")
    ```
    Dit wordt uitgebreid besproken in Deel 5 over SQL injection.

## Select: Data ophalen

Haal data op met `SELECT` queries:

```python
import sqlite3
from sqlite3 import Row

def get_all_contacts() -> list[Row]:
    """Haal alle contacten op."""
    conn = sqlite3.connect("contacts.db")
    conn.row_factory = Row  # Zodat we kolommen bij naam kunnen benaderen

    cursor = conn.execute("SELECT * FROM contacts ORDER BY name")
    contacts = cursor.fetchall()

    conn.close()
    return contacts

# Gebruik
contacts = get_all_contacts()

for contact in contacts:
    print(f"{contact['name']}: {contact['email']}")
```

Output:

```text
Jan Jansen: jan@email.nl
Sara de Vries: sara@email.nl
```

!!! info "row_factory = Row"
    Met `row_factory = Row` kun je kolommen benaderen via `row['name']` in plaats van `row[0]`. Dit maakt code leesbaarder.

### Enkele rij ophalen

Gebruik `fetchone()` voor één result:

```python
def get_contact_by_email(email: str) -> Row | None:
    """Haal één contact op op basis van email."""
    conn = sqlite3.connect("contacts.db")
    conn.row_factory = Row

    cursor = conn.execute(
        "SELECT * FROM contacts WHERE email = ?",
        (email,)
    )

    contact = cursor.fetchone()
    conn.close()

    return contact

# Gebruik
contact = get_contact_by_email("jan@email.nl")

if contact:
    print(f"Gevonden: {contact['name']}")
else:
    print("Contact niet gevonden")
```

## Update: Data wijzigen

Wijzig bestaande records met `UPDATE`:

```python
def update_phone(email: str, new_phone: str) -> bool:
    """
    Update telefoonnummer van een contact.

    Returns:
        bool: True als update gelukt, False als contact niet bestaat
    """
    conn = sqlite3.connect("contacts.db")

    cursor = conn.execute(
        "UPDATE contacts SET phone = ? WHERE email = ?",
        (new_phone, email)
    )

    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    return rows_affected > 0

# Gebruik
success = update_phone("jan@email.nl", "06-98765432")

if success:
    print("Telefoonnummer bijgewerkt")
else:
    print("Contact niet gevonden")
```

!!! warning "Altijd WHERE clausule bij UPDATE"
    Zonder `WHERE` clausule worden **alle** rijen geüpdatet:
    ```python
    # GEVAARLIJK - iedereen krijgt hetzelfde telefoonnummer!
    conn.execute("UPDATE contacts SET phone = ?", (phone,))
    ```

## Delete: Data verwijderen

Verwijder records met `DELETE`:

```python
def delete_contact(email: str) -> bool:
    """
    Verwijder een contact op basis van email.

    Returns:
        bool: True als delete gelukt, False als contact niet bestaat
    """
    conn = sqlite3.connect("contacts.db")

    cursor = conn.execute(
        "DELETE FROM contacts WHERE email = ?",
        (email,)
    )

    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    return rows_affected > 0

# Gebruik
deleted = delete_contact("sara@email.nl")

if deleted:
    print("Contact verwijderd")
else:
    print("Contact niet gevonden")
```

!!! warning "Altijd WHERE clausule bij DELETE"
    Zonder `WHERE` clausule worden **alle** rijen verwijderd:
    ```python
    # GEVAARLIJK - ALLE contacten worden gewist!
    conn.execute("DELETE FROM contacts")
    ```

## Context managers (with statement)

Bovenstaande code heeft een probleem: als er een error optreedt, wordt `conn.close()` niet aangeroepen. Gebruik `with` voor automatic cleanup:

!!! info "De `with` statement"
    `with` is een codeblok voor resources die opgeruimd moeten worden. Python roept aan het einde van het blok altijd de opruimcode aan, ook als er een error optreedt.

    `as conn` geeft de resource een naam waarmee je in het blok werkt.

```python
def add_contact_safe(name: str, email: str, phone: str | None = None) -> int:
    """Voeg contact toe met automatic connection cleanup."""
    with sqlite3.connect("contacts.db") as conn:
        cursor = conn.execute(
            "INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone)
        )
        contact_id = cursor.lastrowid
        conn.commit()
        return contact_id
    # conn.close() wordt automatisch aangeroepen

# Gebruik
try:
    contact_id = add_contact_safe("Piet Bakker", "piet@email.nl")
    print(f"Contact toegevoegd met ID: {contact_id}")
except sqlite3.IntegrityError:
    print("Email bestaat al (UNIQUE constraint)")
```

`sqlite3.IntegrityError` is een exception die sqlite3 gooit als een database-constraint wordt geschonden - hier de UNIQUE constraint op het email-veld.

!!! tip "Altijd with gebruiken"
    De `with` statement zorgt dat de connectie altijd wordt gesloten, ook bij errors. Dit is de **aangeraden manier** om met databases te werken.

## Complete voorbeeld

Hier een volledig voorbeeld dat alle CRUD operaties (Create, Read, Update, Delete) combineert:

```python
import sqlite3
from sqlite3 import Row

class ContactDatabase:
    """Database manager voor contacten."""

    def __init__(self, db_path: str = "contacts.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self) -> None:
        """Maak contacts tabel aan als deze niet bestaat."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT
                )
            """)
            conn.commit()

    def add(self, name: str, email: str, phone: str | None = None) -> int:
        """Voeg contact toe."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)",
                (name, email, phone)
            )
            conn.commit()
            return cursor.lastrowid

    def get_all(self) -> list[Row]:
        """Haal alle contacten op."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = Row
            cursor = conn.execute("SELECT * FROM contacts ORDER BY name")
            return cursor.fetchall()

    def get_by_email(self, email: str) -> Row | None:
        """Haal één contact op."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = Row
            cursor = conn.execute(
                "SELECT * FROM contacts WHERE email = ?",
                (email,)
            )
            return cursor.fetchone()

    def update_phone(self, email: str, phone: str) -> bool:
        """Update telefoonnummer."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE contacts SET phone = ? WHERE email = ?",
                (phone, email)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, email: str) -> bool:
        """Verwijder contact."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM contacts WHERE email = ?",
                (email,)
            )
            conn.commit()
            return cursor.rowcount > 0

# Gebruik
db = ContactDatabase()

# Create
jan_id = db.add("Jan Jansen", "jan@email.nl", "06-12345678")
sara_id = db.add("Sara de Vries", "sara@email.nl")

# Read
contacts = db.get_all()
for contact in contacts:
    print(f"{contact['name']}: {contact['email']}")

# Update
db.update_phone("jan@email.nl", "06-98765432")

# Delete
db.delete("sara@email.nl")

# Verify
print("\nNa delete:")
for contact in db.get_all():
    print(f"{contact['name']}: {contact['email']}")
```

## Verschillen met PostgreSQL

Je bent gewend aan PostgreSQL. Enkele verschillen met SQLite:

| Aspect | PostgreSQL | SQLite |
|--------|-----------|--------|
| **Datatypes** | Veel expliciete types (VARCHAR, TIMESTAMP, etc.) | Type affinity: TEXT, INTEGER, REAL, BLOB, NULL — kolomtype is een hint, geen harde eis |
| **Constraints** | Alle constraints, ook achteraf via ALTER TABLE | Zelfde constraints bij `CREATE TABLE`; maar toevoegen of verwijderen van constraints achteraf is niet mogelijk |
| **ALTER TABLE** | Volledig | `RENAME TABLE`, `RENAME COLUMN`, `ADD COLUMN` en `DROP COLUMN` worden ondersteund; kolomtype wijzigen vereist een nieuwe tabel |
| **Type checking** | Strikt | Losjes (string in INTEGER kolom kan!) |
| **Concurrent writes** | Meerdere schrijvers tegelijk | Één schrijver tegelijk; WAL-mode verbetert leesgelijktijdigheid, maar SQLite is bedoeld voor single-user gebruik |

!!! warning "SQLite type validatie is losjes"
    SQLite accepteert dit zonder error:
    ```python
    conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER, score INTEGER)")
    conn.execute("INSERT INTO test VALUES (?, ?)", (1, "geen-integer"))  # string in INTEGER kolom
    ```
    PostgreSQL zou dit afwijzen. Zorg dus zelf voor correcte types!

## Samenvatting

Je hebt geleerd:

- Database connectie maken met `sqlite3.connect()`
- CRUD operaties: `INSERT`, `SELECT`, `UPDATE`, `DELETE`
- Placeholders (`?`) gebruiken tegen SQL injection
- `row_factory = Row` voor dict-like access
- Context managers (`with`) voor automatic cleanup
- Type annotations en moderne Python patterns

**Volgende stap:** [Deel 3](sql-deel3.md) - JOINs met meerdere tabellen.
