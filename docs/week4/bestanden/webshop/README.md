# Webshop Flask Applicatie

Deze applicatie demonstreert Flask met de webshop database uit Week 3.

## Rode Draad door de Cursus

Deze webshop applicatie bouwt voort op:

- **Week 2 (OOP):** `Product`, `Customer`, `Order`, `Cart` classes
- **Week 3 (SQL):** `webshop.sqlite` database met `products` en `categories`
- **Week 4 (Flask):** Product catalog met routes en templates
- **Week 5 (Forms):** Formulieren voor producten toevoegen (komt nog)
- **Week 6 (SQLAlchemy):** ORM models voor database (komt nog)
- **Week 7 (Auth/Blueprints):** Login en gestructureerde app (komt nog)

## Structuur

```text
webshop/
├── app.py                    # Main Flask applicatie met routes
├── database.py               # WebshopDatabase class voor queries
├── templates/                # Jinja2 templates
│   ├── base.html            # Base template met Bootstrap 5
│   ├── index.html           # Homepage met categorieën
│   ├── category.html        # Categorie overzicht
│   ├── product.html         # Product detail pagina
│   └── 404.html             # Custom error pagina
└── static/                   # CSS, images, JavaScript (optioneel)
```

## Features

**Routes:**

- `/` - Homepage met alle categorieën
- `/category/<id>` - Producten per categorie
- `/product/<id>` - Product detail pagina

**Database Integratie:**

- Gebruikt `webshop.sqlite` uit Week 3
- Hergebruikt SQL queries uit Week 3
- Type hints en modern Python patterns

**Templates:**

- Bootstrap 5.3.0 voor styling
- Template inheritance (`{% extends %}`)
- Jinja2 loops en conditionals
- Responsive design

## Setup

### 1. Installeer Flask

Vanuit deze directory:

```console
uv init
uv add flask
```

### 2. Controleer database pad

De `database.py` zoekt de database in:

```python
db_path = "../../../week3/bestanden/webshop.sqlite"
```

Als je de database elders hebt, pas het pad aan.

### 3. Run de applicatie

```console
uv run python app.py
```

Of met Flask CLI:

```console
uv run flask run
```

### 4. Open in browser

```text
http://127.0.0.1:5000/
```

## Routes Uitleg

### Homepage (`/`)

```python
@app.route("/")
def index() -> str:
    """Homepage met categorieën."""
    categories = db.get_category_stats()
    return render_template("index.html", categories=categories)
```

- Haalt alle categorieën op met statistieken
- Toont categorie cards met product count en gemiddelde prijs

### Category (`/category/<int:id>`)

```python
@app.route("/category/<int:category_id>")
def category(category_id: int) -> str:
    """Categorie overzicht met producten."""
    category_info = db.get_category_by_id(category_id)
    if not category_info:
        abort(404)

    products = db.get_products_by_category(category_id)
    return render_template("category.html",
                         category=category_info,
                         products=products)
```

- Haalt categorie info op
- Haalt alle producten van die categorie op
- Toont product grid met prijzen en voorraad

### Product (`/product/<int:id>`)

```python
@app.route("/product/<int:product_id>")
def product(product_id: int) -> str:
    """Product detail pagina."""
    product_info = db.get_product_by_id(product_id)
    if not product_info:
        abort(404)

    return render_template("product.html", product=product_info)
```

- Haalt product details op met JOIN naar category
- Toont product info, prijs, voorraad, beschrijving
- Breadcrumb navigatie

## Database Class

De `WebshopDatabase` class bevat alle queries:

```python
class WebshopDatabase:
    def get_all_categories(self) -> list[Row]:
        """Haal alle categorieën op."""

    def get_category_by_id(self, category_id: int) -> Row | None:
        """Haal één categorie op."""

    def get_products_by_category(self, category_id: int) -> list[Row]:
        """Haal producten van categorie op."""

    def get_product_by_id(self, product_id: int) -> Row | None:
        """Haal product op met JOIN naar category."""
```

Dit is een uitbreiding van de queries uit Week 3!

## Template Inheritance

**base.html** bevat:

- Navigation bar
- Bootstrap 5.3.0 CDN links
- Footer
- `{% block content %}` placeholder

**Andere templates** extenden base.html:

```html
{% extends "base.html" %}

{% block title %}Mijn Pagina{% endblock %}

{% block content %}
    <h1>Inhoud hier</h1>
{% endblock %}
```

## Jinja2 Features Gebruikt

### Loops

```html
{% for product in products %}
    <div class="card">
        <h5>{{ product.name }}</h5>
        <p>€{{ "%.2f"|format(product.price) }}</p>
    </div>
{% endfor %}
```

### Conditionals

```html
{% if product.stock > 0 %}
    <span class="badge bg-success">Op voorraad</span>
{% else %}
    <span class="badge bg-danger">Uitverkocht</span>
{% endif %}
```

### Filters

```html
<!-- Prijs formatting -->
€{{ "%.2f"|format(product.price) }}

<!-- String slicing -->
{{ product.description[:100] }}...
```

### URL Generation

```html
<a href="{{ url_for('product', product_id=product.id) }}">
    Bekijk Product
</a>
```

## Uitbreidingen (Week 5+)

In latere weken breiden we deze app uit met:

- **Week 5:** Formulieren voor producten toevoegen/wijzigen
- **Week 6:** SQLAlchemy ORM in plaats van raw SQL
- **Week 7a:** Klant login en admin dashboard
- **Week 7b:** Blueprints voor modulaire structuur

## Tips

- Gebruik `debug=True` tijdens development voor auto-reload
- Check de browser console voor JavaScript errors
- Gebruik browser developer tools om HTML/CSS te inspecteren
- Test alle routes: home, category, product, 404

## Referenties

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- [Bootstrap 5.3 Documentation](https://getbootstrap.com/docs/5.3/)
