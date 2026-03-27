# Complete Database Class: WebshopDatabase

In de vorige delen heb je afzonderlijke functies gezien voor database operaties. Nu gaan we alles combineren in een **database class** - een moderne, herbruikbare oplossing voor het werken met de webshop database.

## Waarom een database class?

Een database class biedt verschillende voordelen:

- **Encapsulation**: Alle database logica op één plek
- **Herbruikbaarheid**: Makkelijk te gebruiken in verschillende scripts
- **Consistency**: Altijd dezelfde patterns (context managers, placeholders, etc.)
- **Onderhoudbaarheid**: Aanpassingen hoef je maar op één plek te maken

## De complete WebshopDatabase class

Hier is een complete implementatie met alle patterns die je tot nu toe hebt geleerd:

```python
import sqlite3
from sqlite3 import Row


class WebshopDatabase:
    """Database manager voor de webshop.sqlite database.

    Deze class biedt methoden voor het ophalen van categorieën en producten
    uit de webshop database, inclusief JOIN queries en statistieken.

    Attributes:
        db_path (str): Pad naar de SQLite database file.
    """

    def __init__(self, db_path: str = "webshop.sqlite"):
        """Initialiseer de database manager.

        Args:
            db_path: Pad naar de database file (default: "webshop.sqlite")
        """
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        """Maak database connectie met row_factory ingesteld.

        Returns:
            sqlite3.Connection: Database connectie object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = Row
        return conn

    # ==================== CATEGORIES ====================

    def get_all_categories(self, order_by: str = "name") -> list[Row]:
        """Haal alle categorieën op, gesorteerd.

        Args:
            order_by: Kolom om op te sorteren: "id" of "name" (default: "name")

        Returns:
            Lijst met alle categorieën
        """
        valid_columns = {"id", "name"}
        if order_by not in valid_columns:
            order_by = "name"
        with self._get_connection() as conn:
            cursor = conn.execute(f"SELECT * FROM categories ORDER BY {order_by}")
            return cursor.fetchall()

    def get_category_by_id(self, category_id: int) -> Row | None:
        """Haal één categorie op op basis van ID.

        Args:
            category_id: ID van de categorie

        Returns:
            Categorie record of None als niet gevonden
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM categories WHERE id = ?",
                (category_id,)
            )
            return cursor.fetchone()

    def search_categories(self, search_term: str) -> list[Row]:
        """Zoek categorieën op basis van naam.

        Args:
            search_term: Zoekterm voor categorie naam

        Returns:
            Lijst met matchende categorieën
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM categories WHERE name LIKE ? ORDER BY name",
                (f"%{search_term}%",)
            )
            return cursor.fetchall()

    # ==================== PRODUCTS ====================

    def get_all_products(self) -> list[Row]:
        """Haal alle producten op met categorie informatie."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    p.id,
                    p.name AS product,
                    p.price,
                    p.stock,
                    c.name AS category
                FROM products p
                JOIN categories c ON p.category_id = c.id
                ORDER BY c.name, p.name
            """)
            return cursor.fetchall()

    def get_product_by_id(self, product_id: int) -> Row | None:
        """Haal één product op op basis van ID.

        Args:
            product_id: ID van het product

        Returns:
            Product record of None als niet gevonden
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM products WHERE id = ?",
                (product_id,)
            )
            return cursor.fetchone()

    def get_products_by_category(self, category_id: int) -> list[Row]:
        """Haal alle producten op van een specifieke categorie.

        Args:
            category_id: ID van de categorie

        Returns:
            Lijst met producten van deze categorie
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM products WHERE category_id = ? ORDER BY name",
                (category_id,)
            )
            return cursor.fetchall()

    def search_products(self, search_term: str) -> list[Row]:
        """Zoek producten inclusief categorie informatie.

        Args:
            search_term: Zoekterm voor product naam

        Returns:
            Lijst met matchende producten met volledige informatie
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    c.name AS category,
                    p.name AS product,
                    p.price,
                    p.stock,
                    p.id
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.name LIKE ?
                ORDER BY c.name, p.name
            """, (f"%{search_term}%",))
            return cursor.fetchall()

    def get_products_in_price_range(
        self,
        min_price: float,
        max_price: float
    ) -> list[Row]:
        """Haal producten op binnen een prijsrange.

        Args:
            min_price: Minimale prijs
            max_price: Maximale prijs

        Returns:
            Lijst met producten in de prijsrange
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    c.name AS category,
                    p.name AS product,
                    p.price,
                    p.stock
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.price BETWEEN ? AND ?
                ORDER BY p.price ASC
            """, (min_price, max_price))
            return cursor.fetchall()

    def get_products_in_stock(self, min_stock: int = 1) -> list[Row]:
        """Haal producten op die op voorraad zijn.

        Args:
            min_stock: Minimale voorraad (default: 1)

        Returns:
            Lijst met producten die op voorraad zijn
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    c.name AS category,
                    p.name AS product,
                    p.price,
                    p.stock
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.stock >= ?
                ORDER BY c.name, p.name
            """, (min_stock,))
            return cursor.fetchall()

    # ==================== CATALOG ====================

    def get_category_catalog(self, category_id: int) -> dict:
        """Haal complete catalogus op voor een categorie.

        Args:
            category_id: ID van de categorie

        Returns:
            Dictionary met categorie info en alle producten
        """
        category = self.get_category_by_id(category_id)
        if not category:
            return {}

        products = self.get_products_by_category(category_id)

        catalog = {
            "category": category["name"],
            "category_id": category_id,
            "description": category["description"],
            "products": [
                {
                    "product_id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "stock": product["stock"],
                    "description": product["description"]
                }
                for product in products
            ]
        }

        return catalog

    # ==================== STATISTICS ====================

    def get_statistics(self) -> dict:
        """Haal database statistieken op.

        Returns:
            Dictionary met statistieken
        """
        with self._get_connection() as conn:
            stats = {}

            # Tel categorieën
            cursor = conn.execute("SELECT COUNT(*) as count FROM categories")
            stats["total_categories"] = cursor.fetchone()["count"]

            # Tel producten
            cursor = conn.execute("SELECT COUNT(*) as count FROM products")
            stats["total_products"] = cursor.fetchone()["count"]

            # Tel producten op voorraad
            cursor = conn.execute("SELECT COUNT(*) as count FROM products WHERE stock > 0")
            stats["products_in_stock"] = cursor.fetchone()["count"]

            # Gemiddelde prijs
            cursor = conn.execute("SELECT AVG(price) as avg_price FROM products")
            stats["average_price"] = cursor.fetchone()["avg_price"]

            # Totale voorraad waarde
            cursor = conn.execute("SELECT SUM(price * stock) as total_value FROM products")
            stats["total_inventory_value"] = cursor.fetchone()["total_value"]

            return stats

    def get_category_statistics(self) -> list[Row]:
        """Haal statistieken op per categorie.

        Returns:
            Lijst met statistieken per categorie
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    c.name AS category,
                    COUNT(p.id) AS product_count,
                    AVG(p.price) AS avg_price,
                    SUM(p.stock) AS total_stock,
                    SUM(p.price * p.stock) AS inventory_value
                FROM categories c
                LEFT JOIN products p ON c.id = p.category_id
                GROUP BY c.id, c.name
                ORDER BY product_count DESC
            """)
            return cursor.fetchall()


# ==================== GEBRUIK ====================

if __name__ == "__main__":
    db = WebshopDatabase()

    # Toon statistieken
    stats = db.get_statistics()
    print("=== Webshop Database Statistics ===")
    print(f"Categorieën: {stats['total_categories']}")
    print(f"Producten: {stats['total_products']}")
    print(f"Op voorraad: {stats['products_in_stock']}")
    print(f"Gemiddelde prijs: €{stats['average_price']:.2f}")
    print(f"Totale voorraad waarde: €{stats['total_inventory_value']:.2f}\n")

    # Categorie statistieken
    print("=== Statistieken per categorie ===")
    cat_stats = db.get_category_statistics()
    for cat in cat_stats[:5]:
        print(f"{cat['category']}: {cat['product_count']} producten, "
              f"gemiddeld €{cat['avg_price']:.2f}, "
              f"voorraad: {cat['total_stock']}")

    print()

    # Haal complete catalogus op
    print("=== Electronics Catalogus (category_id=1) ===")
    catalog = db.get_category_catalog(1)
    if catalog:
        print(f"Categorie: {catalog['category']}")
        print(f"Beschrijving: {catalog['description']}\n")
        for product in catalog["products"][:5]:  # Toon eerste 5
            print(f"  {product['name']}: €{product['price']} ({product['stock']} op voorraad)")
        print()

    # Zoek producten
    print("=== Producten met 'book' in de naam ===")
    products = db.search_products("book")
    for product in products[:5]:  # Toon eerste 5
        print(f"{product['category']}: {product['product']} - €{product['price']}")

    print()

    # Prijsrange
    print("=== Producten tussen €10 en €30 ===")
    products = db.get_products_in_price_range(10.0, 30.0)
    for product in products[:5]:
        print(f"{product['product']}: €{product['price']}")
```

## Gebruik van de class

### Basis gebruik

```python
# Maak een database instance
db = WebshopDatabase()

# Haal alle categorieën op
categories = db.get_all_categories()
for category in categories:
    print(f"{category['id']}: {category['name']}")

# Zoek specifiek
laptop_products = db.search_products("laptop")
for product in laptop_products:
    print(f"{product['product']}: €{product['price']}")
```

### Catalogus ophalen

```python
# Haal alle producten op voor een categorie
catalog = db.get_category_catalog(category_id=2)  # Books

print(f"Categorie: {catalog['category']}")
print(f"Beschrijving: {catalog['description']}\n")

for product in catalog['products']:
    print(f"  {product['name']}: €{product['price']} ({product['stock']} op voorraad)")
```

### Eigen database pad

```python
# Gebruik een andere database file
db = WebshopDatabase("path/to/other/webshop.sqlite")
```

## Design patterns in de class

Deze class demonstreert verschillende belangrijke patterns:

### 1. Private helper method

```python
def _get_connection(self) -> sqlite3.Connection:
    """Helper method die niet bedoeld is voor extern gebruik."""
    # ...
```

De underscore `_` geeft aan dat dit een interne method is.

### 2. Type hints overal

```python
def get_product_by_id(self, product_id: int) -> Row | None:
    #                              ↑ input type    ↑ return type
```

### 3. Docstrings met Args en Returns

```python
def search_products(self, search_term: str) -> list[Row]:
    """Zoek producten op basis van naam.

    Args:
        search_term: Zoekterm voor product naam

    Returns:
        Lijst met matchende producten
    """
```

### 4. Context managers

```python
with self._get_connection() as conn:
    # Gebruik connection
    # Automatische cleanup
```

### 5. Placeholders tegen SQL injection

```python
cursor.execute(
    "SELECT * FROM products WHERE name LIKE ?",
    (f"%{search_term}%",)  # Veilig!
)
```

## Uitbreidingen (optioneel)

Je kunt de class uitbreiden met extra functionaliteit:

### Data toevoegen

```python
def add_product(
    self,
    name: str,
    price: float,
    stock: int,
    category_id: int,
    description: str | None = None
) -> int:
    """Voeg een nieuw product toe."""
    with self._get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO products (name, price, stock, category_id, description)
               VALUES (?, ?, ?, ?, ?)""",
            (name, price, stock, category_id, description)
        )
        conn.commit()
        return cursor.lastrowid
```

### Data wijzigen

```python
def update_stock(self, product_id: int, new_stock: int) -> bool:
    """Update de voorraad van een product."""
    with self._get_connection() as conn:
        cursor = conn.execute(
            "UPDATE products SET stock = ? WHERE id = ?",
            (new_stock, product_id)
        )
        conn.commit()
        return cursor.rowcount > 0
```

### Error handling

```python
def get_product_by_id(self, product_id: int) -> Row | None:
    """Haal product op met error handling."""
    try:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM products WHERE id = ?",
                (product_id,)
            )
            return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
```

## Samenvatting

Je hebt geleerd:

- Een complete database class bouwen
- Methods organiseren per entiteit (categories, products)
- Private helper methods gebruiken (`_get_connection`)
- Complexe data structuren returnen (catalogus dictionary)
- Statistieken berekenen met aggregatiefuncties
- Type hints en docstrings consequent toepassen
- Alle patterns combineren (context managers, placeholders, row_factory)

**Volgende stap:** [Deel 5](sql-deel5.md) - SQL injection preventie.

Deze class is een startpunt: je voegt zelf methoden toe voor de queries die jouw applicatie nodig heeft. Met SQLAlchemy schrijf je geen raw SQL meer, maar Python code die de queries automatisch genereert - dat zie je in week 6.
