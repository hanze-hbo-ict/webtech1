# Oefening 2: JOINs met de Webshop Database

Deze oefening past bij [SQL Deel 3](../sql-deel3.md).

Download de [webshop.sqlite](../bestanden/webshop.sqlite) database en plaats deze in je project folder. Als je deze nog moet maken, run dan eerst `create_webshop.py`.

## Voorbereiding

Maak een Python bestand `webshop_queries.py` met een basis class:

```python
import sqlite3
from sqlite3 import Row

class WebshopDatabase:
    """Database voor webshop queries."""

    def __init__(self, db_path: str = "webshop.sqlite"):
        self.db_path = db_path

    def _execute_query(self, query: str, params: tuple = ()) -> list[Row]:
        """Helper method om queries uit te voeren."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = Row
            cursor = conn.execute(query, params)
            return cursor.fetchall()
```

## Opgave 1: Producten van een Categorie

**Vraag:** Toon alle producten uit de categorie 'Electronics'.

Implementeer deze method:

```python
def get_products_by_category(self, category_name: str) -> list[Row]:
    """Haal alle producten op van een specifieke categorie."""
    # TODO: Implementeer deze query
    # - JOIN products met categories
    # - WHERE categories.name = ?
    # - Gebruik _execute_query helper
    # - SELECT p.name, p.price, p.stock
    pass
```

Test:

```python
db = WebshopDatabase()
products = db.get_products_by_category("Electronics")
for product in products:
    print(f"{product['name']}: €{product['price']}")
```

## Opgave 2: Producten Gesorteerd op Prijs

**Vraag:** Toon dezelfde producten, maar nu gesorteerd op prijs (laag naar hoog).

```python
def get_products_by_category_sorted(self, category_name: str) -> list[Row]:
    """Haal producten op gesorteerd op prijs."""
    # TODO: Voeg ORDER BY price ASC toe
    pass
```

Test opnieuw en vergelijk de output.

## Opgave 3: Producten met Categorie Info

**Vraag:** Toon alle producten met hun categorie naam EN beschrijving.

```python
def get_all_products_with_category(self) -> list[Row]:
    """Haal alle producten op met categorie informatie."""
    # TODO: Implementeer JOIN
    # SELECT p.name AS product, p.price, p.stock,
    #        c.name AS category, c.description
    # FROM products p
    # JOIN categories c ON p.category_id = c.id
    # ORDER BY c.name, p.name
    pass
```

## Opgave 4: Producten in Prijsrange

**Vraag:** Vind alle producten tussen €20 en €50.

```python
def get_products_in_price_range(self, min_price: float, max_price: float) -> list[Row]:
    """Haal producten op binnen prijsrange."""
    # TODO: Gebruik BETWEEN of >= AND <=
    # Include categorie naam via JOIN
    pass
```

Test:

```python
products = db.get_products_in_price_range(20.0, 50.0)
print(f"Gevonden {len(products)} producten tussen €20 en €50")
for product in products[:10]:
    print(f"{product['category']}: {product['name']} - €{product['price']}")
```

## Opgave 5: Laagste Voorraad per Categorie

**Vraag:** Vind het product met de laagste voorraad in elke categorie.

**Hint:** Gebruik `GROUP BY` en `MIN()`

```python
def get_lowest_stock_per_category(self) -> list[Row]:
    """Vind laagste voorraad per categorie."""
    # TODO:
    # SELECT c.name AS category, MIN(p.stock) AS lowest_stock
    # FROM products p
    # JOIN categories c ON p.category_id = c.id
    # GROUP BY c.id, c.name
    # ORDER BY lowest_stock ASC
    pass
```

## Opgave 6: Gemiddelde Prijs per Categorie

**Vraag:** Bereken de gemiddelde prijs per categorie.

```python
def get_average_price_per_category(self) -> list[Row]:
    """Bereken gemiddelde prijs per categorie."""
    # TODO: Gebruik AVG(p.price)
    # GROUP BY categorie
    # ORDER BY gemiddelde prijs DESC
    pass
```

Test:

```python
stats = db.get_average_price_per_category()
for cat in stats:
    print(f"{cat['category']}: gemiddeld €{cat['avg_price']:.2f}")
```

## Opgave 7: Producten Op Voorraad

**Vraag:** Toon alleen producten die op voorraad zijn (stock > 0), gesorteerd op categorie.

```python
def get_in_stock_products(self) -> list[Row]:
    """Haal producten op die op voorraad zijn."""
    # TODO: WHERE p.stock > 0
    # Include categorie naam
    pass
```

## Bonusopdracht 1: Totale Voorraadwaarde

Bereken de totale waarde van de voorraad (prijs × stock) per categorie:

```python
def get_inventory_value_per_category(self) -> list[Row]:
    """Bereken totale voorraadwaarde per categorie."""
    # TODO:
    # SELECT c.name AS category,
    #        COUNT(p.id) AS product_count,
    #        SUM(p.price * p.stock) AS total_value
    # FROM categories c
    # LEFT JOIN products p ON c.id = p.category_id
    # GROUP BY c.id, c.name
    # ORDER BY total_value DESC
    pass
```

Verwachte output format:

```text
Voorraadwaarde per categorie:
1. Electronics: €52685.72 (15 producten)
2. Clothing: €18094.45 (15 producten)
...
```

## Bonusopdracht 2: Duurste Product per Categorie

Vind het duurste product in elke categorie:

```python
def get_most_expensive_per_category(self) -> list[Row]:
    """Vind duurste product per categorie."""
    # TODO:
    # Je kunt dit op twee manieren doen:
    # Optie 1: Subquery
    # Optie 2: Window functions (advanced)
    # Begin met MAX(price) per categorie
    pass
```

## Bonusopdracht 3: Complete Categorie Catalogus

Maak een method die een complete catalogus laat zien (categorie → alle producten):

```python
def get_category_catalog(self, category_name: str) -> dict:
    """Haal complete catalogus op van een categorie."""
    # Return format:
    # {
    #     'category': 'Electronics',
    #     'description': 'Electronic devices and accessories',
    #     'product_count': 15,
    #     'total_value': 52685.72,
    #     'products': [
    #         {
    #             'name': 'Laptop HP',
    #             'price': 899.99,
    #             'stock': 12
    #         },
    #         ...
    #     ]
    # }
    pass
```

## Main Functie

Schrijf een main functie die alle queries demonstreert:

```python
def main():
    db = WebshopDatabase()

    print("=== Opgave 1: Electronics Producten ===")
    products = db.get_products_by_category("Electronics")
    for product in products:
        print(f"{product['name']}: €{product['price']}")

    print("\n=== Opgave 2: Gesorteerd op Prijs ===")
    products = db.get_products_by_category_sorted("Electronics")
    for product in products[:5]:
        print(f"{product['name']}: €{product['price']}")

    # etc.

if __name__ == "__main__":
    main()
```

## Verwachte Output Voorbeelden

```text
=== Opgave 1: Electronics Producten ===
Bluetooth Headphones Sony: €149.99
External SSD 1TB: €89.99
Gaming Controller Xbox: €59.99
HDMI Cable 2m: €12.99
...

=== Opgave 6: Gemiddelde Prijs per Categorie ===
Electronics: gemiddeld €226.19
Home & Garden: gemiddeld €50.66
Beauty: gemiddeld €42.49
...

=== Opgave 7: Aantal Producten Op Voorraad ===
Totaal: 120 producten op voorraad
```

## Checklist

- Alle queries gebruiken placeholders (`?`)
- Context managers (`with`) gebruikt
- Type hints op alle methods
- row_factory = Row gebruikt
- JOIN queries correct (INNER JOIN standaard)
- Aggregatiefuncties: COUNT, AVG, SUM, MIN, MAX
- GROUP BY voor groeperen
- ORDER BY voor sortering
- Helper method `_execute_query` gebruikt
