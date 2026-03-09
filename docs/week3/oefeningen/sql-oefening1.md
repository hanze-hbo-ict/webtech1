# Oefening 1: CRUD Operaties met Python

CRUD staat voor **Create, Read, Update, Delete**: de vier basisbewerkingen op een database.

Deze oefening past bij [SQL Deel 2](../sql-deel2.md) en [Deel 3](../sql-deel3.md).

## Opgave 1: Database en Tabel Aanmaken

Maak een Python bestand `bedrijf_db.py` en maak een database class:

```python
import sqlite3
from sqlite3 import Row

class BedrijfDatabase:
    """Database voor bedrijfsgegevens."""

    def __init__(self, db_path: str = "bedrijf.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self) -> None:
        """Maak bedrijf tabel aan met constraints."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bedrijf (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    naam TEXT NOT NULL,
                    plaats TEXT NOT NULL,
                    salaris REAL NOT NULL CHECK(salaris > 0)
                )
            """)
            conn.commit()
```

**Vraag:** Waarom gebruiken we `CHECK(salaris > 0)`?

## Opgave 2: Data Toevoegen

Voeg een method toe om werknemers toe te voegen:

```python
def add_werknemer(self, naam: str, plaats: str, salaris: float) -> int | None:
    """Voeg werknemer toe."""
    # TODO: Implementeer deze method
    # - Gebruik placeholders
    # - Return lastrowid bij succes
    # - Return None bij fout (try/except)
    pass
```

Test je code door deze 4 werknemers toe te voegen:

| ID | Naam | Plaats | Salaris |
|----|------|--------|---------|
| 1 | Aad | Amsterdam | 60000 |
| 2 | Bea | Berlijn | 70000 |
| 3 | Coen | Cairo | 65000 |
| 4 | Daphne | Dortmund | 65000 |

**Tip:** Je hoeft de ID niet mee te geven - die wordt automatisch gegenereerd (AUTOINCREMENT).

## Opgave 3: Data Ophalen

Voeg een method toe om alle werknemers op te halen:

```python
def get_all(self) -> list[Row]:
    """Haal alle werknemers op."""
    # TODO: Implementeer deze method
    # - Gebruik with statement
    # - Gebruik row_factory = Row
    # - ORDER BY naam
    pass
```

Voeg ook een method toe om één werknemer op ID op te halen:

```python
def get_byid(self, werknemerid: int) -> Row | None:
    """Haal één werknemer op."""
    # TODO: Implementeer deze method
    pass
```

## Opgave 4: Data Wijzigen

Voeg methods toe voor UPDATE operaties:

```python
def update_salaris(self, werknemerid: int, nieuw_salaris: float) -> bool:
    """Update salaris van een werknemer."""
    # TODO: Implementeer deze method
    # - Return True bij succes
    # - Return False bij fout of niet gevonden
    pass

def update_naam(self, werknemerid: int, nieuwe_naam: str) -> bool:
    """Update naam van een werknemer."""
    # TODO: Implementeer deze method
    pass
```

Test je code:

- Wijzig het salaris van Aad (ID 1) naar 90000
- Wijzig de naam van Bea (ID 2) naar "Beatrix"
- Print telkens alle werknemers om te verifiëren

## Opgave 5: Data Verwijderen

Voeg een method toe om een werknemer te verwijderen:

```python
def delete(self, werknemerid: int) -> bool:
    """Verwijder een werknemer."""
    # TODO: Implementeer deze method
    pass
```

Test door Beatrix (ID 2) te verwijderen.

## Opgave 6: Gebruik de Class

Schrijf een `main()` functie die alle operaties demonstreert:

```python
def main():
    db = BedrijfDatabase()

    # Voeg werknemers toe
    print("=== Toevoegen ===")
    werknemers = [
        ("Aad", "Amsterdam", 60000),
        ("Bea", "Berlijn", 70000),
        ("Coen", "Cairo", 65000),
        ("Daphne", "Dortmund", 65000)
    ]

    for naam, plaats, salaris in werknemers:
        werknemerid = db.add_werknemer(naam, plaats, salaris)
        print(f"{naam} toegevoegd met ID {werknemerid}")

    # TODO: Implementeer de rest
    # - Toon alle werknemers
    # - Update salaris van Aad
    # - Update naam van Bea
    # - Verwijder Beatrix
    # - Toon finale lijst

if __name__ == "__main__":
    main()
```

## Bonusopdracht: Statistieken

Voeg methods toe voor statistieken:

```python
def get_gemiddeld_salaris(self) -> float:
    """Bereken gemiddeld salaris."""
    with sqlite3.connect(self.db_path) as conn:
        cursor = conn.execute("SELECT AVG(salaris) as avg_salaris FROM bedrijf")
        result = cursor.fetchone()
        return result[0] if result[0] else 0.0

def get_werknemers_per_plaats(self) -> list[Row]:
    """Tel werknemers per plaats."""
    # TODO: Gebruik GROUP BY
    pass

def get_hoogste_salaris(self) -> Row | None:
    """Vind werknemer met hoogste salaris."""
    # TODO: Gebruik ORDER BY ... DESC LIMIT 1
    pass
```

## Verwachte Output

```text
=== Toevoegen ===
Aad toegevoegd met ID 1
Bea toegevoegd met ID 2
Coen toegevoegd met ID 3
Daphne toegevoegd met ID 4

=== Alle Werknemers ===
1: Aad (Amsterdam) - €60000.00
2: Bea (Berlijn) - €70000.00
3: Coen (Cairo) - €65000.00
4: Daphne (Dortmund) - €65000.00

=== Na Updates ===
1: Aad (Amsterdam) - €90000.00
2: Beatrix (Berlijn) - €70000.00
3: Coen (Cairo) - €65000.00
4: Daphne (Dortmund) - €65000.00

=== Na Verwijderen ===
1: Aad (Amsterdam) - €90000.00
3: Coen (Cairo) - €65000.00
4: Daphne (Dortmund) - €65000.00

Gemiddeld salaris: €73333.33
```

## Checklist

- Class met `__init__` en `_create_table`
- CRUD methods: add, get_all, get_byid, update, delete
- Placeholders (`?`) gebruikt
- Context managers (`with`) gebruikt
- Type hints op alle methods
- row_factory = Row voor dict-like access
- Error handling (try/except) waar nodig
- main() functie die alles demonstreert
