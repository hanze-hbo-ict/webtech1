# Exception Handling bij Database Operaties

Bij het werken met databases kunnen allerlei fouten optreden: database niet gevonden, constraint violations, connection errors, etc.

## Waarom exception handling belangrijk is

In productie Flask applicaties wil je **nooit** dat gebruikers stack traces te zien krijgen. In plaats daarvan:

- Vang fouten af met `try`/`except`
- Log de fout voor debugging
- Toon een gebruiksvriendelijke foutmelding
- Blijf in een consistente staat (geen corrupte data)

## Database exceptions in SQLite

SQLite heeft verschillende exception types die allemaal erven van `sqlite3.Error`:

```python
import sqlite3

# Basis exception types:
# - sqlite3.Error (parent van alle database errors)
# - sqlite3.IntegrityError (constraint violations: UNIQUE, NOT NULL, etc.)
# - sqlite3.OperationalError (database locked, table not found, etc.)
# - sqlite3.ProgrammingError (SQL syntax errors)
```

## Basic exception handling

### Voorbeeld zonder error handling (slecht)

```python
import sqlite3

def add_product_unsafe(name: str, price: float, stock: int, category_id: int) -> int:
    """GEEN error handling - crasht bij fouten!"""
    with sqlite3.connect("webshop.sqlite") as conn:
        cursor = conn.execute(
            "INSERT INTO products (name, price, stock, category_id) VALUES (?, ?, ?, ?)",
            (name, price, stock, category_id)
        )
        conn.commit()
        return cursor.lastrowid

# Dit crasht als name None is (NOT NULL constraint)
productid = add_product_unsafe("Laptop HP", 899.99, 10, 1)  # Werkt
productid = add_product_unsafe(None, 899.99, 10, 1)  # CRASH!
# sqlite3.IntegrityError: NOT NULL constraint failed: products.name
```

### Voorbeeld met error handling (goed)

```python
import sqlite3
from sqlite3 import Row

def add_product_safe(name: str, price: float, stock: int, category_id: int) -> int | None:
    """Met error handling - geeft None terug bij fout."""
    try:
        with sqlite3.connect("webshop.sqlite") as conn:
            cursor = conn.execute(
                "INSERT INTO products (name, price, stock, category_id) VALUES (?, ?, ?, ?)",
                (name, price, stock, category_id)
            )
            conn.commit()
            return cursor.lastrowid

    except sqlite3.IntegrityError as e:
        # NOT NULL of UNIQUE constraint violation
        print(f"Fout: ongeldige waarde voor product '{name}'")
        return None

    except sqlite3.Error as e:
        # Andere database fouten
        print(f"Database fout: {e}")
        return None

# Gebruik
productid = add_product_safe("Laptop HP", 899.99, 10, 1)
if productid:
    print(f"Product aangemaakt met ID {productid}")
else:
    print("Product niet aangemaakt")

# None als naam - geen crash, netjes afgehandeld
productid = add_product_safe(None, 899.99, 10, 1)
if productid:
    print(f"Product aangemaakt met ID {productid}")
else:
    print("Product niet aangemaakt")  # Dit wordt geprint
```

## Specifieke exceptions afhandelen

### IntegrityError (constraint violations)

```python
def add_product(name: str, price: float, stock: int, category_id: int) -> int | None:
    """Voeg product toe met constraint validation."""
    try:
        with sqlite3.connect("webshop.sqlite") as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.execute(
                "INSERT INTO products (name, price, stock, category_id) VALUES (?, ?, ?, ?)",
                (name, price, stock, category_id)
            )
            conn.commit()
            return cursor.lastrowid

    except sqlite3.IntegrityError as e:
        error_msg = str(e)

        if "UNIQUE" in error_msg:
            print(f"Product '{name}' bestaat al")
        elif "NOT NULL" in error_msg:
            print(f"Verplichte velden mogen niet leeg zijn")
        elif "FOREIGN KEY" in error_msg:
            print(f"Ongeldige categorie ID: {category_id}")
        elif "CHECK" in error_msg:
            print(f"Ongeldige waarde (bijv. negatieve prijs of voorraad)")
        else:
            print(f"Database constraint error: {error_msg}")

        return None

# Test
add_product("Laptop HP", 899.99, 10, 1)  # Werkt
add_product(None, 799.99, 5, 1)           # NOT NULL - netjes afgehandeld
add_product("Mouse", 29.99, 10, 999)      # FOREIGN KEY - netjes afgehandeld
```

### OperationalError (database problemen)

```python
def get_all_products() -> list[Row]:
    """Haal producten op met error handling."""
    try:
        with sqlite3.connect("webshop.sqlite") as conn:
            conn.row_factory = Row
            cursor = conn.execute("SELECT * FROM products")
            return cursor.fetchall()

    except sqlite3.OperationalError as e:
        error_msg = str(e)

        if "no such table" in error_msg:
            print("Database tabel bestaat niet - run eerst create_webshop.py!")
            return []
        elif "locked" in error_msg:
            print("Database is locked - probeer later opnieuw")
            return []
        else:
            print(f"Database error: {error_msg}")
            return []

    except sqlite3.Error as e:
        print(f"Onverwachte database fout: {e}")
        return []

# Gebruik
products = get_all_products()
if products:
    for product in products:
        print(f"{product['name']}: € {product['price']}")
else:
    print("Geen producten gevonden (of fout opgetreden)")
```

## Complete database class met error handling

Hier is een volledige class met exception handling:

```python
import sqlite3
from sqlite3 import Row
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductDatabase:
    """Product database met complete error handling."""

    def __init__(self, db_path: str = "shop.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self) -> None:
        """Maak products tabel aan."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        price REAL NOT NULL CHECK(price > 0),
                        stock INTEGER NOT NULL CHECK(stock >= 0)
                    )
                """)
                conn.commit()
                logger.info("Products tabel aangemaakt")

        except sqlite3.Error as e:
            logger.error(f"Fout bij aanmaken tabel: {e}")
            raise  # Re-raise omdat dit een kritieke fout is

    def add(self, name: str, price: float, stock: int) -> int | None:
        """Voeg product toe met error handling."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
                    (name, price, stock)
                )
                conn.commit()
                productid = cursor.lastrowid
                logger.info(f"Product '{name}' toegevoegd met ID {productid}")
                return productid

        except sqlite3.IntegrityError as e:
            if "UNIQUE" in str(e):
                logger.warning(f"Product '{name}' bestaat al")
            elif "CHECK" in str(e):
                logger.warning(f"Ongeldige waarde voor '{name}': prijs={price}, stock={stock}")
            else:
                logger.error(f"Integrity error bij toevoegen '{name}': {e}")
            return None

        except sqlite3.Error as e:
            logger.error(f"Database fout bij toevoegen '{name}': {e}")
            return None

    def get_all(self) -> list[Row]:
        """Haal alle producten op."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = Row
                cursor = conn.execute("SELECT * FROM products ORDER BY name")
                return cursor.fetchall()

        except sqlite3.Error as e:
            logger.error(f"Fout bij ophalen producten: {e}")
            return []

    def get_byid(self, productid: int) -> Row | None:
        """Haal één product op."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = Row
                cursor = conn.execute(
                    "SELECT * FROM products WHERE id = ?",
                    (productid,)
                )
                return cursor.fetchone()

        except sqlite3.Error as e:
            logger.error(f"Fout bij ophalen product {productid}: {e}")
            return None

    def update_stock(self, productid: int, new_stock: int) -> bool:
        """Update voorraad met validatie."""
        if new_stock < 0:
            logger.warning(f"Negatieve voorraad niet toegestaan: {new_stock}")
            return False

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "UPDATE products SET stock = ? WHERE id = ?",
                    (new_stock, productid)
                )
                conn.commit()

                if cursor.rowcount > 0:
                    logger.info(f"Stock update voor product {productid}: {new_stock}")
                    return True
                else:
                    logger.warning(f"Product {productid} niet gevonden")
                    return False

        except sqlite3.Error as e:
            logger.error(f"Fout bij update stock voor product {productid}: {e}")
            return False

    def delete(self, productid: int) -> bool:
        """Verwijder product."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "DELETE FROM products WHERE id = ?",
                    (productid,)
                )
                conn.commit()

                if cursor.rowcount > 0:
                    logger.info(f"Product {productid} verwijderd")
                    return True
                else:
                    logger.warning(f"Product {productid} niet gevonden")
                    return False

        except sqlite3.Error as e:
            logger.error(f"Fout bij verwijderen product {productid}: {e}")
            return False


# Gebruik
db = ProductDatabase()

# Succesvol toevoegen
productid = db.add("Laptop", 799.99, 10)
if productid:
    print(f"Product toegevoegd met ID {productid}")

# Duplicate - wordt netjes afgevangen
duplicateid = db.add("Laptop", 899.99, 5)
if not duplicateid:
    print("Product niet toegevoegd (bestaat al)")

# Ongeldige waarde - wordt netjes afgevangen
invalidid = db.add("Monitor", -50.00, 3)  # Negatieve prijs
if not invalidid:
    print("Product niet toegevoegd (ongeldige prijs)")

# Stock update
if db.update_stock(1, 15):
    print("Stock bijgewerkt")

# Haal alle producten op
products = db.get_all()
for product in products:
    print(f"{product['name']}: €{product['price']} ({product['stock']} op voorraad)")
```

## Flask specifieke error handling

In Flask wil je errors netjes afhandelen voor gebruikers:

```python
from flask import Flask, jsonify, request
import sqlite3
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/products', methods=['POST'])
def add_product():
    """Voeg product toe via API."""
    data = request.get_json()

    try:
        name = data['name']
        price = float(data['price'])
        stock = int(data['stock'])

        db = ProductDatabase()
        productid = db.add(name, price, stock)

        if productid:
            return jsonify({
                'success': True,
                'id': productid,
                'message': f'Product {name} toegevoegd'
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Product kon niet worden toegevoegd (mogelijk duplicate)'
            }), 400

    except KeyError as e:
        return jsonify({
            'success': False,
            'message': f'Ontbrekend veld: {e}'
        }), 400

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': f'Ongeldige waarde: {e}'
        }), 400

    except Exception as e:
        logger.error(f"Onverwachte fout: {e}")
        return jsonify({
            'success': False,
            'message': 'Server error'
        }), 500


@app.route('/products/<int:productid>')
def get_product(productid):
    """Haal product op via API."""
    try:
        db = ProductDatabase()
        product = db.get_byid(productid)

        if product:
            return jsonify({
                'success': True,
                'product': dict(product)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Product niet gevonden'
            }), 404

    except Exception as e:
        logger.error(f"Fout bij ophalen product {productid}: {e}")
        return jsonify({
            'success': False,
            'message': 'Server error'
        }), 500
```

## Best practices

**DOE WEL:**

- Gebruik specifieke exceptions (`IntegrityError`, `OperationalError`)
- Log errors voor debugging (`logging.error()`)
- Return None of lege lijst bij fouten (geen crash)
- Gebruik type hints (`int | None`, `list[Row]`)
- Test error paths (wat gebeurt bij duplicates?)

**DOE NIET:**

- Bare `except:` zonder exception type
- Fouten negeren (silent failures)
- Stack traces tonen aan gebruikers
- Exceptions gebruiken voor flow control
- Sensitive info in error messages (geen SQL queries!)

## Common patterns

### Pattern 1: Try-except met return

```python
def safe_operation() -> Row | None:
    """Veilige operatie die Row of None teruggeeft."""
    try:
        # Database operatie
        return result
    except sqlite3.Error as e:
        logger.error(f"Fout: {e}")
        return None
```

### Pattern 2: Try-except met boolean

```python
def safe_update() -> bool:
    """Update met success boolean."""
    try:
        # Update operatie
        return True
    except sqlite3.Error as e:
        logger.error(f"Fout: {e}")
        return False
```

### Pattern 3: Try-except met default waarde

```python
def get_count() -> int:
    """Haal count op, return 0 bij fout."""
    try:
        # Count query
        return count
    except sqlite3.Error as e:
        logger.error(f"Fout: {e}")
        return 0
```

## Samenvatting

Je hebt geleerd:

- **Database-specifieke exceptions** (`IntegrityError`, `OperationalError`)
- **Try-except patterns** voor veilige database operaties
- **Logging** voor debugging (niet print!)
- **Return types** die fouten aangeven (`None`, `False`, empty list)
- **Flask error handling** voor API's
- **Best practices** voor production code

**Tip:** Test altijd je error handling! Probeer bewust fouten te veroorzaken (duplicates, missing tables, etc.) om te zien of je code netjes reageert.

**Volgende stap:** Je hebt nu alle SQLite basics! Met deze patterns kun je veilig databases gebruiken in Flask applicaties.
