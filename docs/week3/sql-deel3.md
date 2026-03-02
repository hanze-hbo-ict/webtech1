# SQLite in Python: JOINs en Queries

De webshop database heeft meerdere tabellen (categories, products) die met elkaar verbonden zijn via foreign keys. Met **JOIN** queries haal je data uit meerdere tabellen tegelijk op.

## De webshop database

Download de [`webshop.sqlite`](bestanden/webshop.sqlite) database. Deze bevat twee tabellen met realistische e-commerce data:

- `categories` - Productcategorieën (10 records)
- `products` - Producten (120 records)

### Database structuur inspecteren

Laten we eerst de database verkennen vanuit Python:

```python
import sqlite3
from sqlite3 import Row

def inspect_database(db_path: str = "webshop.sqlite") -> None:
    """Toon basisstatistieken van de webshop database."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        cat_count = conn.execute(
            "SELECT COUNT(*) AS count FROM categories"
        ).fetchone()["count"]

        prod_count = conn.execute(
            "SELECT COUNT(*) AS count FROM products"
        ).fetchone()["count"]

        print("Database tabellen:\n")
        print(f"Tabel: categories")
        print(f"Aantal records: {cat_count}\n")
        print(f"Tabel: products")
        print(f"Aantal records: {prod_count}\n")

# Gebruik
inspect_database()
```

Output:

```text
Database tabellen:

Tabel: categories
Aantal records: 10

Tabel: products
Aantal records: 120
```

!!! info "PRIMARY KEY AUTOINCREMENT"
    SQLite vult automatisch de primary key kolom `id` in wanneer je een nieuwe record toevoegt:
    ```python
    cursor = conn.execute("INSERT INTO categories (name, description) VALUES (?, ?)",
                         ("Furniture", "Tables, chairs, and desks"))
    newid = cursor.lastrowid  # 11
    ```
    Dit werkt hetzelfde als PostgreSQL's `SERIAL` type.

## Eenvoudige queries

Laten we beginnen met een paar eenvoudige queries om weer in te komen:

```python
def get_product_by_id(product_id: int, db_path: str = "webshop.sqlite") -> Row | None:
    """Haal één product op op basis van ID."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row
        cursor = conn.execute(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
        )
        return cursor.fetchone()

# Gebruik
product = get_product_by_id(42)
if product:
    print(f"Product {product['id']}: {product['name']} - €{product['price']}")
```

Output:

```text
Product 42: Sneakers Nike - €89.99
```

### Sorteren met ORDER BY

Je kunt resultaten sorteren met `ORDER BY`:

```python
def get_products_sorted_by_price(
    db_path: str = "webshop.sqlite",
    desc: bool = False
) -> list[Row]:
    """Haal alle producten op, gesorteerd op prijs."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        order = "DESC" if desc else "ASC"
        cursor = conn.execute(f"SELECT * FROM products ORDER BY price {order}")

        return cursor.fetchall()

# Gebruik
products = get_products_sorted_by_price(desc=True)
for product in products[:5]:  # Toon eerste 5 (duurste)
    print(f"{product['name']}: €{product['price']}")
```

Output:

```text
Smartphone Samsung Galaxy: €699.99
Tablet iPad Air: €599.99
Monitor Dell 27 inch: €349.99
4K Blu-ray Player: €199.99
Smartwatch Fitbit: €199.99
```

!!! warning "SQL injection bij ORDER BY"
    In het voorbeeld hierboven gebruiken we f-string voor `order` (`ASC`/`DESC`). Dit is veilig omdat we de waarde zelf controleren (boolean → "ASC" of "DESC").
    Doe dit NOOIT met user input:
    ```python
    # GEVAARLIJK - SQL injection risico!
    order = input("ASC or DESC? ")
    cursor.execute(f"SELECT * FROM products ORDER BY price {order}")
    ```

## JOINs: meerdere tabellen combineren

Tot nu toe hebben we met één tabel gewerkt. Maar de echte kracht van SQL komt pas bij JOINs. Je kent dit al van PostgreSQL - in Python werkt het precies hetzelfde.

### Simpele JOIN: Products met Categories

Laten we producten combineren met hun categorieën om een complete productlijst te maken:

```python
def get_products_with_categories(db_path: str = "webshop.sqlite") -> list[Row]:
    """Haal alle producten op met hun categorie naam."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        cursor = conn.execute("""
            SELECT p.name AS product, p.price, p.stock, c.name AS category
            FROM products p
            JOIN categories c ON p.category_id = c.id
            ORDER BY c.name, p.name
        """)

        return cursor.fetchall()

# Gebruik
products = get_products_with_categories()
for product in products[:10]:  # Toon eerste 10
    print(f"{product['category']}: {product['product']} - €{product['price']} ({product['stock']} op voorraad)")
```

Output:

```text
Beauty: Electric Toothbrush - €79.99 (20 op voorraad)
Beauty: Face Cream Anti-Aging - €34.99 (25 op voorraad)
Beauty: Hair Dryer - €49.99 (22 op voorraad)
Beauty: Lipstick Set (5 colors) - €29.99 (30 op voorraad)
Beauty: Makeup Brush Set - €39.99 (28 op voorraad)
Beauty: Nail Polish Kit - €19.99 (40 op voorraad)
Beauty: Perfume Eau de Parfum 50ml - €59.99 (18 op voorraad)
Beauty: Shampoo & Conditioner Set - €24.99 (35 op voorraad)
Books: 1984 - €12.99 (45 op voorraad)
Books: Algorithms Unlocked - €32.99 (25 op voorraad)
```

!!! info "JOIN syntax"
    De JOIN syntax is identiek aan PostgreSQL:
    ```sql
    SELECT kolommen
    FROM tabel1 alias1
    JOIN tabel2 alias2 ON alias1.foreign_key = alias2.primary_key
    ```
    - `p` en `c` zijn **aliases** (afkortingen)
    - `ON` specificeert de relatie tussen tabellen
    - `c.name AS category` geeft de kolom een duidelijke naam

### JOIN met WHERE: Filteren op resultaten

Nu gaan we producten ophalen uit een specifieke categorie, met extra filters:

```python
def get_products_by_category(
    category_name: str,
    db_path: str = "webshop.sqlite"
) -> list[Row]:
    """Haal producten op uit een specifieke categorie."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        cursor = conn.execute("""
            SELECT c.name AS category, p.name AS product, p.price, p.stock
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE c.name = ?
            ORDER BY p.name
        """, (category_name,))

        return cursor.fetchall()

# Gebruik
books = get_products_by_category("Books")
print(f"Gevonden {len(books)} boeken:\n")
for book in books[:5]:  # Toon eerste 5
    print(f"{book['product']} - €{book['price']}")
```

Output:

```text
Gevonden 20 boeken:

1984 - €12.99
Algorithms Unlocked - €32.99
Atomic Habits - €18.99
Clean Code - €34.99
Design Patterns - €44.99
```

### JOIN met aggregatie: Producten tellen per categorie

We kunnen JOINs combineren met aggregatiefuncties zoals `COUNT()` en `GROUP BY`:

```python
def get_category_statistics(db_path: str = "webshop.sqlite") -> list[Row]:
    """Haal statistieken op per categorie."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        cursor = conn.execute("""
            SELECT
                c.name AS category,
                COUNT(p.id) AS product_count,
                AVG(p.price) AS avg_price,
                SUM(p.stock) AS total_stock
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            GROUP BY c.id, c.name
            ORDER BY product_count DESC
        """)

        return cursor.fetchall()

# Gebruik
stats = get_category_statistics()
print("Categorie statistieken:\n")
for cat in stats:
    print(f"{cat['category']}: {cat['product_count']} producten, "
          f"gemiddelde prijs: €{cat['avg_price']:.2f}, "
          f"totale voorraad: {cat['total_stock']}")
```

Output:

```text
Categorie statistieken:

Books: 20 producten, gemiddelde prijs: €24.34, totale voorraad: 703
Clothing: 15 producten, gemiddelde prijs: €37.19, totale voorraad: 570
Electronics: 15 producten, gemiddelde prijs: €189.32, totale voorraad: 413
Home & Garden: 12 producten, gemiddelde prijs: €42.99, totale voorraad: 358
Sports: 12 producten, gemiddelde prijs: €36.24, totale voorraad: 445
...
```

!!! tip "LEFT JOIN vs JOIN"
    We gebruiken hier `LEFT JOIN` in plaats van `JOIN`:
    - `JOIN` (of `INNER JOIN`): alleen categorieën MET producten
    - `LEFT JOIN`: ALLE categorieën, ook als ze geen producten hebben
    Voor statistieken wil je vaak `LEFT JOIN` om lege categorieën ook te zien.

### JOIN met WHERE en LIKE: Zoeken in resultaten

We kunnen ook filteren op JOIN resultaten met een `WHERE` clausule. Bijvoorbeeld: zoek alle producten met "phone" in de naam:

```python
def search_products_by_name(
    search_term: str,
    db_path: str = "webshop.sqlite"
) -> list[Row]:
    """Zoek producten op basis van naam, inclusief categorie info."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        cursor = conn.execute("""
            SELECT
                c.name AS category,
                p.name AS product,
                p.price,
                p.stock
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.name LIKE ?
            ORDER BY c.name, p.name
        """, (f"%{search_term}%",))

        return cursor.fetchall()

# Gebruik
phone_products = search_products_by_name("phone")
print(f"Gevonden {len(phone_products)} producten met 'phone' in de naam:\n")
for product in phone_products:
    print(f"{product['category']}: {product['product']} - €{product['price']} ({product['stock']} op voorraad)")
```

Output:

```text
Gevonden 3 producten met 'phone' in de naam:

Electronics: Bluetooth Headphones Sony - €149.99 (18 op voorraad)
Electronics: Smartphone Samsung Galaxy - €699.99 (8 op voorraad)
Music & Movies: DJ Headphones - €89.99 (16 op voorraad)
```

!!! info "LIKE operator en wildcard"
    - `LIKE '%phone%'` zoekt overal in de string
    - `%` is een wildcard (= 0 of meer karakters)
    - We gebruiken `?` placeholder met `f"%{search_term}%"` voor veiligheid
    Dit is identiek aan PostgreSQL's `LIKE` operator.

### Complexe WHERE clausules: Prijs en voorraad filteren

Je kunt meerdere voorwaarden combineren met `AND` en `OR`:

```python
def get_affordable_in_stock_products(
    max_price: float,
    min_stock: int,
    db_path: str = "webshop.sqlite"
) -> list[Row]:
    """Haal betaalbare producten op die op voorraad zijn."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row

        cursor = conn.execute("""
            SELECT
                c.name AS category,
                p.name AS product,
                p.price,
                p.stock
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.price <= ? AND p.stock >= ?
            ORDER BY p.price ASC
        """, (max_price, min_stock))

        return cursor.fetchall()

# Gebruik
products = get_affordable_in_stock_products(max_price=30.0, min_stock=40)
print(f"Gevonden {len(products)} betaalbare producten met voldoende voorraad:\n")
for product in products[:10]:
    print(f"{product['product']}: €{product['price']} ({product['stock']} op voorraad)")
```

Output:

```text
Gevonden 21 betaalbare producten met voldoende voorraad:

Card Game Uno: €9.99 (60 op voorraad)
The Art of War: €9.99 (48 op voorraad)
The Great Gatsby: €10.99 (50 op voorraad)
Sticky Notes Pack: €11.99 (65 op voorraad)
Honey Natural 500g: €11.99 (30 op voorraad)
...
```

## Views (optioneel)

Een **view** is een virtuele tabel - een opgeslagen query die je kunt gebruiken alsof het een echte tabel is. Views worden gebruikt voor:

- **Security**: Gevoelige kolommen verbergen (zoals salaris)
- **Simplificatie**: Complexe queries herbruikbaar maken
- **Abstraction layer**: Database structuur verbergen voor gebruikers

!!! note "Views in modern Python apps"
    In Python/Flask apps gebruik je views minder vaak. Met een ORM zoals SQLAlchemy schrijf je queries direct in Python en gebruik je geen SQL views meer.
    Views zijn wel handig als je een database deelt met andere applicaties of rapportage tools.

### View maken en gebruiken in Python

Laten we een view maken voor de "producten op voorraad" query:

```python
def create_in_stock_view(db_path: str = "webshop.sqlite") -> None:
    """Maak een view voor producten die op voorraad zijn."""
    with sqlite3.connect(db_path) as conn:
        # Verwijder view als deze al bestaat
        conn.execute("DROP VIEW IF EXISTS vInStockProducts")

        # Maak nieuwe view
        conn.execute("""
            CREATE VIEW vInStockProducts AS
            SELECT
                c.name AS category,
                p.name AS product,
                p.price,
                p.stock
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.stock > 0
            ORDER BY c.name, p.name
        """)

        conn.commit()
        print("View 'vInStockProducts' aangemaakt")

def query_view(view_name: str, db_path: str = "webshop.sqlite") -> list[Row]:
    """Haal data op uit een view."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row
        cursor = conn.execute(f"SELECT * FROM {view_name}")
        return cursor.fetchall()

# Gebruik
create_in_stock_view()

# Query de view alsof het een tabel is
products = query_view("vInStockProducts")
for product in products[:10]:
    print(f"{product['category']}: {product['product']} - €{product['price']}")
```

Output:

```text
View 'vInStockProducts' aangemaakt
Beauty: Electric Toothbrush - €79.99
Beauty: Face Cream Anti-Aging - €34.99
Beauty: Hair Dryer - €49.99
Beauty: Lipstick Set (5 colors) - €29.99
Beauty: Makeup Brush Set - €39.99
...
```

!!! warning "SQL injection bij view/tabelnamen"
    In `query_view` gebruiken we een f-string voor `view_name`. Dit is een SQL injection risico als `view_name` uit user input komt:
    ```python
    # GEVAARLIJK - SQL injection risico!
    view_name = request.args.get("view")
    query_view(view_name)  # aanvaller kan eigen SQL injecteren
    ```
    Tabel- en viewnamen kunnen niet met `?` geparametriseerd worden. De veilige oplossing is een whitelist:
    ```python
    ALLOWED_VIEWS = {"vInStockProducts"}
    if view_name not in ALLOWED_VIEWS:
        raise ValueError(f"Ongeldige viewnaam: {view_name}")
    ```

### View met filter

Je kunt de view ook filteren, net als een normale tabel:

```python
def search_in_view(
    view_name: str,
    category_filter: str,
    db_path: str = "webshop.sqlite"
) -> list[Row]:
    """Zoek in een view met extra filtering."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = Row
        cursor = conn.execute(
            f"SELECT * FROM {view_name} WHERE category LIKE ?",
            (f"%{category_filter}%",)
        )
        return cursor.fetchall()

# Gebruik
electronics = search_in_view("vInStockProducts", "Electronics")
print(f"\nElectronics op voorraad ({len(electronics)} producten):\n")
for product in electronics[:5]:
    print(f"{product['product']}: €{product['price']} ({product['stock']} op voorraad)")
```

Output:

```text
Electronics op voorraad (15 producten):

Bluetooth Headphones Sony: €149.99 (18 op voorraad)
External SSD 1TB: €89.99 (40 op voorraad)
Gaming Controller Xbox: €59.99 (20 op voorraad)
HDMI Cable 2m: €12.99 (60 op voorraad)
Keyboard Mechanical: €119.99 (22 op voorraad)
```

!!! tip "Views bekijken"
    Je kunt alle views in de database opvragen:
    ```python
    cursor = conn.execute("""
        SELECT name, sql
        FROM sqlite_master
        WHERE type='view'
    """)
    ```

## Samenvatting

Je hebt geleerd:

- Database statistieken opvragen per tabel
- **JOINs** gebruiken om meerdere tabellen te combineren
- JOIN tussen products en categories
- **WHERE** clausules combineren met JOINs
- **Aggregatiefuncties** zoals `COUNT()`, `AVG()`, `SUM()` met `GROUP BY`
- **LIKE** operator voor tekst zoeken met wildcards
- **LEFT JOIN** vs **JOIN** voor inclusieve queries
- **Views** maken en gebruiken (optioneel)
- Placeholders gebruiken voor SQL injection preventie

**Volgende stap:** [Deel 4](sql-deel4.md) - Complete database class.

**Oefening:** Maak nu [oefening 1](oefeningen/sql-oefening1.md).
