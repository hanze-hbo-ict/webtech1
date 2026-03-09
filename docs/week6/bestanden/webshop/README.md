# Week 6: SQLAlchemy ORM - Webshop

In deze week vervangen we raw SQL queries door **SQLAlchemy ORM** (Object-Relational Mapping). Dit maakt je code meer Pythonic, type-safe, en makkelijker te onderhouden.

## Rode draad: Van Raw SQL naar ORM

We bouwen verder op dezelfde webshop uit Week 3-5, maar vervangen nu alle database operaties door ORM:

| Week | Aanpak | Database Operaties |
|------|--------|-------------------|
| Week 3-4 | Raw SQL | `cursor.execute("SELECT * FROM products WHERE id = ?")` |
| Week 5 | Raw SQL + Forms | `conn.execute("INSERT INTO products VALUES (?, ?, ?)")` |
| **Week 6** | **SQLAlchemy ORM** | `db.get_or_404(Product, product_id)` |

## Belangrijkste Concepten

### 1. ORM Models (models.py)

In plaats van SQL tabellen definiëren we **Python classes**:

```python
class Product(db.Model):
    """Model voor producten."""
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    price: Mapped[float]
    stock: Mapped[int] = mapped_column(default=0)

    # Foreign Key relatie
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
```

**Voordelen:**

- Type hints en autocompletion in je IDE
- Automatische validatie
- Relaties worden objecten (geen JOIN queries nodig)

### 2. Database Relaties

#### One-to-Many: Category → Products

```python
class Category(db.Model):
    # ...
    products: Mapped[list['Product']] = relationship(back_populates='category')
```

Nu kun je eenvoudig:

```python
category = db.session.get(Category, 1)
for product in category.products:  # Automatisch alle producten!
    print(product.name)
```

Of andersom:

```python
product = db.session.get(Product, 1)
print(product.category.name)  # Via backref!
```

#### Many-to-Many: Order ↔ Products (via OrderItem)

```python
class Order(db.Model):
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='order', cascade='all, delete-orphan')

class OrderItem(db.Model):
    order_id: Mapped[int | None] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int | None] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int | None]
```

### 3. Query Examples

#### Week 3-5 (Raw SQL) vs Week 6 (ORM)

**Alle producten ophalen:**

```python
# Raw SQL (Week 3-5)
cursor.execute("SELECT * FROM products")
products = cursor.fetchall()

# ORM (Week 6)
products = db.session.execute(db.select(Product)).scalars().all()
```

**Product filteren op categorie:**

```python
# Raw SQL
cursor.execute("SELECT * FROM products WHERE category_id = ?", (category_id,))

# ORM
products = db.session.execute(db.select(Product).filter_by(category_id=category_id)).scalars().all()
```

**Product met JOIN:**

```python
# Raw SQL
cursor.execute("""
    SELECT p.*, c.name as category_name
    FROM products p
    JOIN categories c ON p.category_id = c.id
    WHERE p.id = ?
""", (product_id,))

# ORM - JOIN gebeurt automatisch via relationship!
product = db.session.get(Product, product_id)
print(product.category.name)  # Automatisch!
```

**Product toevoegen:**

```python
# Raw SQL
cursor.execute(
    "INSERT INTO products (name, price, stock, category_id) VALUES (?, ?, ?, ?)",
    (name, price, stock, category_id)
)
conn.commit()

# ORM
new_product = Product(name=name, price=price, stock=stock, category_id=category_id)
db.session.add(new_product)
db.session.commit()
```

**Product updaten:**

```python
# Raw SQL
cursor.execute(
    "UPDATE products SET name = ?, price = ? WHERE id = ?",
    (new_name, new_price, product_id)
)

# ORM
product = db.session.get(Product, product_id)
product.name = new_name
product.price = new_price
db.session.commit()  # Automatisch UPDATE!
```

**Product verwijderen:**

```python
# Raw SQL
cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

# ORM
product = db.session.get(Product, product_id)
db.session.delete(product)
db.session.commit()
```

### 4. Model Properties

Je kunt eigen properties toevoegen aan modellen:

```python
class Product(db.Model):
    # ...columns...

    @property
    def in_stock(self) -> bool:
        """Check of product op voorraad is."""
        return self.stock > 0

    @property
    def formatted_price(self) -> str:
        """Formatteer prijs als euro bedrag."""
        return f"€{self.price:.2f}"
```

Gebruik in templates:

```jinja
{% if product.in_stock %}
    <span class="badge bg-success">Op voorraad</span>
{% endif %}
```

### 5. Cascade Delete

Als je een Order verwijdert, verwijder je automatisch alle OrderItems:

```python
class Order(db.Model):
    order_items: Mapped[list['OrderItem']] = relationship(
        back_populates='order',
        cascade='all, delete-orphan'
    )
```

## Bestanden Structuur

```text
webshop/
├── app.py                  # Flask app met ORM queries
├── models.py               # SQLAlchemy model definities
├── forms.py                # WTForms (hergebruikt van Week 5)
├── migrate_database.py     # Migratie script van Week 3 → Week 6
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── category.html
│   ├── product.html
│   ├── admin_products.html
│   ├── add_product.html
│   ├── edit_product.html
│   ├── contact.html
│   └── 404.html
└── webshop.db              # SQLite database (gegenereerd)
```

## Installatie

1. **Installeer dependencies:**

   ```bash
   pip install flask flask-sqlalchemy flask-wtf
   ```

2. **Migreer data van Week 3 database:**

   ```bash
   python migrate_database.py
   ```

   Dit script:
   - Maakt nieuwe `webshop.db` aan met ORM schema
   - Kopieert alle categorieën en producten van Week 3
   - Behoudt originele IDs

3. **Start de applicatie:**

   ```bash
   python app.py
   ```

4. **Open in browser:**

   ```text
   http://127.0.0.1:5000
   ```

## Waarom ORM?

### Voordelen

1. **Pythonic Code**

   ```python
   # ORM is veel leesbaarder
   expensive_products = db.session.execute(db.select(Product).filter(Product.price > 100)).scalars().all()

   # vs Raw SQL strings
   cursor.execute("SELECT * FROM products WHERE price > 100")
   ```

2. **Type Safety**

   ```python
   product = db.session.get(Product, 1)
   product.name  # IDE weet dat dit een string is!
   ```

3. **Geen SQL Injection risico**

   ```python
   # ORM escaped automatisch
   db.session.execute(db.select(Product).filter_by(name=user_input)).scalar_one_or_none()
   ```

4. **Databaseonafhankelijk**
   - Wissel makkelijk van SQLite → PostgreSQL → MySQL
   - Zelfde Python code blijft werken

5. **Automatische Relaties**

   ```python
   # Geen JOIN queries schrijven
   product.category.name  # Werkt automatisch!
   ```

### Nadelen

1. **Leercurve** - Je moet ORM concepten leren
2. **Performance** - Complexe queries zijn soms langzamer
3. **N+1 probleem** - Let op met lazy loading
4. **Verborgen complexiteit** - ORM doet veel achter de schermen

## Vergelijking Database Operaties

| Operatie | Raw SQL (Week 3-5) | ORM (Week 6) |
|----------|-------------------|--------------|
| **SELECT** | `cursor.execute("SELECT ...")` | `db.session.execute(db.select(Model)).scalars().all()` |
| **INSERT** | `cursor.execute("INSERT ...")` + `commit()` | `db.session.add()` + `commit()` |
| **UPDATE** | `cursor.execute("UPDATE ...")` | `model.field = value` + `commit()` |
| **DELETE** | `cursor.execute("DELETE ...")` | `db.session.delete()` + `commit()` |
| **JOIN** | `SELECT * FROM a JOIN b ON ...` | `model.relationship_name` |
| **Filter** | `WHERE column = ?` | `.filter_by(column=value)` |
| **Count** | `SELECT COUNT(*) FROM ...` | `db.session.execute(db.select(func.count()).select_from(Model)).scalar()` |

## Flask-SQLAlchemy Query API

Belangrijkste query methodes:

```python
# Alle records ophalen
db.session.execute(db.select(Product)).scalars().all()

# Eerste record ophalen
db.session.execute(db.select(Product)).scalar_one_or_none()

# Record op primary key (of 404)
db.get_or_404(Product, product_id)

# Filteren
db.session.execute(db.select(Product).filter_by(category_id=1)).scalars().all()
db.session.execute(db.select(Product).filter(Product.price > 50)).scalars().all()

# Sorteren
db.session.execute(db.select(Product).order_by(Product.name)).scalars().all()
db.session.execute(db.select(Product).order_by(Product.price.desc())).scalars().all()

# Limiet
db.session.execute(db.select(Product).limit(10)).scalars().all()

# Tellen
db.session.execute(db.select(func.count()).select_from(Product)).scalar()

# Combineren
db.session.execute(db.select(Product).filter_by(category_id=1).order_by(Product.price).limit(5)).scalars().all()
```

## Database Migratie

Het `migrate_database.py` script laat zien hoe je data kunt migreren:

```python
# Open oude database
source_conn = sqlite3.connect("../../../week3/bestanden/webshop.sqlite")

# Lees categorieën
cursor.execute("SELECT * FROM categories")
for row in cursor.fetchall():
    # Maak ORM object
    category = Category(
        name=row['name'],
        description=row['description']
    )
    db.session.add(category)

db.session.commit()
```

**Let op:** IDs worden bewaard met `category.id = row['id']` zodat foreign keys blijven werken!

## Next Steps: Week 7

In Week 7 bouwen we verder op deze ORM foundation:

### Week 7a: User Authentication

- Customer login systeem
- Flask-Login integratie
- Password hashing met werkzeug
- Admin vs Customer rechten

### Week 7b: Blueprints

- Modulariseer de applicatie
- `products/` blueprint voor catalog
- `orders/` blueprint voor winkelwagen
- `admin/` blueprint voor beheer
- `auth/` blueprint voor login

## Tips & Best Practices

1. **Gebruik altijd `with app.app_context()`** bij database operaties buiten routes

   ```python
   with app.app_context():
       db.create_all()
   ```

2. **Commit na wijzigingen**

   ```python
   product.name = "Nieuwe naam"
   db.session.commit()  # Vergeet dit niet!
   ```

3. **Gebruik `get_or_404()` in routes**

   ```python
   product = db.get_or_404(Product, product_id)  # Automatic 404!
   ```

4. **Lazy loading vs Eager loading**

   ```python
   # Lazy (standaard) - query per product.category
   products = db.session.execute(db.select(Product)).scalars().all()
   for p in products:
       print(p.category.name)  # N+1 queries!

   # Eager - 1 query met JOIN
   products = db.session.execute(db.select(Product).options(joinedload(Product.category))).scalars().all()
   for p in products:
       print(p.category.name)  # Efficient!
   ```

5. **Gebruik `__repr__` voor debugging**

   ```python
   def __repr__(self) -> str:
       return f"<Product {self.id}: {self.name}>"
   ```

## Veelvoorkomende Fouten

1. **Vergeten te committen**

   ```python
   product = Product(name="Test")
   db.session.add(product)
   # Vergeet db.session.commit() niet!
   ```

2. **Fout relationship definiëren**

   ```python
   # Fout: string moet exact matchen met class naam
   products = db.relationship('Producten', ...)

   # Correct
   products = db.relationship('Product', ...)
   ```

3. **N+1 probleem**

   ```python
   # Slecht - 1 query voor categories + N queries voor products
   for category in db.session.execute(db.select(Category)).scalars().all():
       print(len(category.products))

   # Beter - gebruik eager loading of custom query
   categories = db.session.execute(db.select(Category).options(joinedload(Category.products))).scalars().all()
   ```

## Opdrachten

1. **Analyse de models.py** - Begrijp alle relaties en properties
2. **Vergelijk queries** - Open Week 5 database.py en Week 6 app.py naast elkaar
3. **Run de migratie** - Voer `migrate_database.py` uit en bekijk de output
4. **Test CRUD operaties** - Voeg producten toe, wijzig ze, verwijder ze
5. **Experimenteer met queries** - Probeer filters, ordering, limiting

## Resources

- [Flask-SQLAlchemy Documentatie](https://flask-sqlalchemy.palletsprojects.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [Flask-WTF + SQLAlchemy](https://wtforms.readthedocs.io/en/3.0.x/ext/#module-wtforms.ext.sqlalchemy)
