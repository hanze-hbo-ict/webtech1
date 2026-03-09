# Oefening 4: Database Exception Handling

Deze oefening past bij [SQL Deel 6](../sql-deel6.md).

In deze oefening leer je database-specifieke exceptions afvangen en netjes afhandelen. Je bouwt een producten database met constraints en test wat er gebeurt bij verschillende fouten.

## Voorbereiding

Maak een Python bestand `shop_db.py` met een basis product database class:

```python
import sqlite3
from sqlite3 import Row
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductDatabase:
    """Product database met error handling."""

    def __init__(self, db_path: str = "shop.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self) -> None:
        """Maak products tabel aan met constraints."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL CHECK(price > 0),
                    stock INTEGER NOT NULL CHECK(stock >= 0),
                    category TEXT NOT NULL
                )
            """)
            conn.commit()
            logger.info("Products tabel aangemaakt")
```

## Opgave 1: Basic Error Handling

Implementeer een `add_product()` method **zonder** error handling, test deze en observeer wat er gebeurt:

```python
def add_product_unsafe(self, name: str, price: float, stock: int, category: str) -> int:
    """Voeg product toe ZONDER error handling."""
    # TODO: Implementeer deze method ZONDER try/except
    # - Gebruik placeholders (veilig!)
    # - Return lastrowid
    # - Laat de method crashen bij fouten (dat is juist de bedoeling)
    pass
```

Test met verschillende scenario's:

```python
db = ProductDatabase()

# Test 1: Normale toevoeging (werkt)
productid = db.add_product_unsafe("Laptop", 799.99, 10, "Electronics")
print(f"Product toegevoegd met ID {productid}")

# Test 2: Duplicate naam (crasht!)
try:
    db.add_product_unsafe("Laptop", 899.99, 5, "Electronics")
except sqlite3.IntegrityError as e:
    print(f"CRASH: {e}")

# Test 3: Negatieve prijs (crasht!)
try:
    db.add_product_unsafe("Monitor", -50.00, 3, "Electronics")
except sqlite3.IntegrityError as e:
    print(f"CRASH: {e}")

# Test 4: Lege naam (crasht!)
try:
    db.add_product_unsafe("", 299.99, 2, "Electronics")
except sqlite3.IntegrityError as e:
    print(f"CRASH: {e}")
```

**Vraag:** Welke errors krijg je? Wat staat er in de error messages?

## Opgave 2: IntegrityError Handling

Nu ga je errors netjes afvangen. Implementeer een veilige versie:

```python
def add_product(self, name: str, price: float, stock: int, category: str) -> int | None:
    """Voeg product toe met error handling."""
    # TODO: Implementeer met try/except
    # - Vang sqlite3.IntegrityError af (voor UNIQUE, CHECK, NOT NULL)
    # - Check of "UNIQUE" in error message staat
    # - Check of "CHECK" in error message staat
    # - Check of "NOT NULL" in error message staat
    # - Log de juiste foutmelding (logger.warning)
    # - Return None bij fout, lastrowid bij succes
    pass
```

Test dezelfde scenario's:

```python
# Test met error handling
print("\n=== Met Error Handling ===")

# Test 1: Succesvol
productid = db.add_product("Laptop", 799.99, 10, "Electronics")
if productid:
    print(f"Product toegevoegd met ID {productid}")

# Test 2: Duplicate - netjes afgevangen
productid = db.add_product("Laptop", 899.99, 5, "Electronics")
if not productid:
    print("Product niet toegevoegd (bestaat al)")

# Test 3: Negatieve prijs - netjes afgevangen
productid = db.add_product("Monitor", -50.00, 3, "Electronics")
if not productid:
    print("Product niet toegevoegd (ongeldige prijs)")

# Test 4: Lege naam - netjes afgevangen
productid = db.add_product("", 299.99, 2, "Electronics")
if not productid:
    print("Product niet toegevoegd (naam is verplicht)")
```

## Opgave 3: OperationalError Handling

Implementeer een method om producten op te halen met error handling voor database problemen:

```python
def get_all_products(self) -> list[Row]:
    """Haal alle producten op met error handling."""
    # TODO: Implementeer met try/except
    # - Vang sqlite3.OperationalError af
    # - Check of "no such table" in error message staat
    # - Check of "locked" in error message staat
    # - Log de fout (logger.error)
    # - Return lege lijst bij fout
    pass
```

Test:

```python
# Normale ophaling
products = db.get_all_products()
print(f"\n{len(products)} producten gevonden")

# Simuleer locked database (moeilijk te testen, maar error handling is klaar!)
```

## Opgave 4: Update Met Error Handling

Implementeer een method om voorraad te updaten met validatie en error handling:

```python
def update_stock(self, productid: int, new_stock: int) -> bool:
    """Update voorraad met validatie en error handling."""
    # TODO: Implementeer met error handling
    # - Valideer dat new_stock >= 0 (return False als niet)
    # - Gebruik try/except voor database errors
    # - Check cursor.rowcount om te zien of product bestaat
    # - Log succesvolle updates (logger.info)
    # - Log failures (logger.warning of logger.error)
    # - Return True bij succes, False bij fout
    pass
```

Test:

```python
# Test stock updates
print("\n=== Stock Updates ===")

# Succesvolle update
if db.update_stock(1, 15):
    print("Voorraad bijgewerkt")

# Negatieve voorraad (validatiefout)
if not db.update_stock(1, -5):
    print("Negatieve voorraad niet toegestaan")

# Non-existent product
if not db.update_stock(999, 10):
    print("Product niet gevonden")
```

## Opgave 5: Delete Met Error Handling

Implementeer een delete method:

```python
def delete_product(self, productid: int) -> bool:
    """Verwijder product met error handling."""
    # TODO: Implementeer met error handling
    # - Gebruik try/except voor sqlite3.Error
    # - Check cursor.rowcount
    # - Log succesvolle deletes
    # - Log als product niet bestaat
    # - Return True bij succes, False bij fout
    pass
```

## Opgave 6: Complete Error Handler

Maak een method die verschillende errors kan onderscheiden:

```python
def safe_add_product(self, name: str, price: float, stock: int, category: str) -> tuple[bool, str]:
    """Voeg product toe en return (success, message)."""
    # TODO: Implementeer met gedetailleerde error messages
    # Return voorbeelden:
    # - (True, "Product toegevoegd met ID 5")
    # - (False, "Product naam bestaat al")
    # - (False, "Prijs moet positief zijn")
    # - (False, "Naam is verplicht")
    # - (False, "Database error: ...")
    #
    # Vang verschillende exceptions af:
    # - sqlite3.IntegrityError met specifieke checks
    # - sqlite3.OperationalError
    # - sqlite3.Error (catch-all)
    pass
```

Test:

```python
print("\n=== Safe Add Product ===")

test_cases = [
    ("Keyboard", 49.99, 20, "Electronics"),      # Succes
    ("Keyboard", 59.99, 10, "Electronics"),      # Duplicate
    ("Mouse", -10.00, 5, "Electronics"),         # Negatieve prijs
    ("", 29.99, 3, "Electronics"),               # Lege naam
    ("Webcam", 89.99, -2, "Electronics"),        # Negatieve stock
]

for name, price, stock, category in test_cases:
    success, message = db.safe_add_product(name, price, stock, category)
    status = "OK" if success else "Fout"
    print(f"{status} {message}")
```

## Bonusopdracht 1: Custom Exception Class

Maak een eigen uitzondering voor product-specifieke fouten:

```python
class ProductError(Exception):
    """Custom exception voor product errors."""
    pass


class ProductDatabase:
    def add_product_custom(self, name: str, price: float, stock: int, category: str) -> int:
        """Voeg product toe met eigen uitzonderingen."""
        # TODO: Implementeer met custom exceptions
        # - Raise ProductError("Product naam bestaat al") bij duplicate
        # - Raise ProductError("Prijs moet positief zijn") bij < 0
        # - Raise ProductError("Voorraad kan niet negatief zijn") bij < 0
        # - Vang sqlite3 errors en converteer naar ProductError
        pass
```

Gebruik:

```python
try:
    db.add_product_custom("Laptop", 799.99, 10, "Electronics")
    print("Product toegevoegd")
except ProductError as e:
    print(f"Fout: {e}")
```

## Bonusopdracht 2: Transaction Error Handling

Implementeer een method die meerdere producten toevoegt in een transactie:

```python
def add_products_batch(self, products: list[tuple]) -> tuple[int, list[str]]:
    """Voeg meerdere producten toe in één transactie.

    Returns:
        (aantal_toegevoegd, lijst_met_errors)
    """
    # TODO: Implementeer met transactie
    # - Gebruik één connection voor alle inserts
    # - Bij fout: rollback (automatisch met context manager)
    # - Bij succes: commit (automatisch met context manager)
    # - Return aantal succesvolle inserts en lijst met error messages
    # - Hint: Gebruik niet automatisch commit, doe handmatig conn.rollback() bij fout
    pass
```

Test:

```python
products = [
    ("Phone", 599.99, 15, "Electronics"),
    ("Tablet", 399.99, 8, "Electronics"),
    ("Invalid", -50.00, 3, "Electronics"),  # Deze faalt
]

added, errors = db.add_products_batch(products)
print(f"\n{added} producten toegevoegd, {len(errors)} fouten")
for error in errors:
    print(f"  - {error}")
```

## Verwachte Output

```text
INFO:__main__:Products tabel aangemaakt
Product toegevoegd met ID 1
CRASH: UNIQUE constraint failed: products.name
CRASH: CHECK constraint failed: price > 0
CRASH: NOT NULL constraint failed: products.name

=== Met Error Handling ===
INFO:__main__:Product 'Laptop' toegevoegd met ID 1
Product toegevoegd met ID 1
WARNING:__main__:Product 'Laptop' bestaat al
Product niet toegevoegd (bestaat al)
WARNING:__main__:Ongeldige waarde voor 'Monitor': prijs=-50.0, stock=3
Product niet toegevoegd (ongeldige prijs)
WARNING:__main__:Product '' kon niet worden toegevoegd
Product niet toegevoegd (naam is verplicht)

3 producten gevonden

=== Stock Updates ===
INFO:__main__:Stock update voor product 1: 15
Voorraad bijgewerkt
WARNING:__main__:Negatieve voorraad niet toegestaan: -5
Negatieve voorraad niet toegestaan
WARNING:__main__:Product 999 niet gevonden
Product niet gevonden

=== Safe Add Product ===
OK Product toegevoegd met ID 2
Fout Product naam bestaat al
Fout Prijs moet positief zijn
Fout Naam is verplicht
Fout Voorraad kan niet negatief zijn
```

## Checklist

- Database-specifieke exceptions gebruikt (`IntegrityError`, `OperationalError`)
- Error messages onderscheiden (UNIQUE, CHECK, NOT NULL)
- Logging gebruikt (`logger.info`, `logger.warning`, `logger.error`)
- Type hints met `|` syntax gebruikt (`int | None`, `Row | None`)
- Return `None`, `False`, of lege lijst bij fouten (geen crash!)
- `cursor.rowcount` gebruikt om te checken of iets gewijzigd is
- Try/except patterns consequent toegepast
- Context managers gebruikt (`with sqlite3.connect()`)
- Gebruiksvriendelijke error messages
- Validatie VOOR database operaties waar mogelijk

## Belangrijke Lessen

1. **Specifieke exceptions**: Gebruik `IntegrityError`, `OperationalError`, niet alleen `Exception`
2. **Logging, niet print**: `logger.error()` voor productie code
3. **Graceful degradation**: Return safe defaults (None, [], False) bij errors
4. **Error message parsing**: Check `str(e)` voor specifieke constraint violations
5. **Validatie**: Check input voor database operaties
6. **Type hints**: `int | None`, `list[Row]`, `bool` voor duidelijkheid
7. **cursor.rowcount**: Controleer of UPDATE/DELETE iets veranderd heeft

**Volgende stap:** In Week 6 leer je SQLAlchemy, een ORM die veel van deze error handling automatisch doet!
