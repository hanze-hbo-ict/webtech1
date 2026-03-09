# Week 7b: Flask Blueprints - Webshop

In deze week refactoren we de monolithische Week 7a applicatie naar een **modulaire Blueprint architectuur**. Dit maakt de code schaalbaarder, onderhoudbaarder, en beter testbaar.

## Rode draad: Van Monolithisch naar Modulair

| Week | Aanpak | Structuur |
|------|--------|-----------|
| Week 7a | Monolithisch | Alles in één `app.py` (400+ regels) |
| **Week 7b** | **Blueprints** | Gescheiden modules: products, auth, admin |
| Future | Microservices | Volledig onafhankelijke services |

## Wat zijn Blueprints?

Blueprints zijn Flask's manier om een applicatie op te delen in **herbruikbare componenten**. Elk blueprint is een verzameling van:

- Routes (`@blueprint.route()`)
- Templates (in eigen `templates/` folder)
- Forms (in eigen `forms.py`)
- Static files (optioneel)

**Voordelen:**

- **Modulariteit**: Elke feature heeft eigen folder
- **Schaalbaarheid**: Teams kunnen aan verschillende blueprints werken
- **Herbruikbaarheid**: Blueprints kunnen in meerdere apps gebruikt worden
- **Testbaarheid**: Blueprints kunnen apart getest worden
- **Duidelijkheid**: Logische scheiding tussen functionaliteiten

## Nieuwe Structuur

```text
webshop/
├── app.py                      # Entry point
├── requirements.txt            # Dependencies
├── webshop.db                  # SQLite database
├── migrate_database.py         # Database migratie
└── webshop_app/                # Main package
    ├── __init__.py             # Application Factory
    ├── models.py               # Alle models (gedeeld)
    │
    ├── products/               # Products Blueprint
    │   ├── __init__.py
    │   ├── views.py            # Public catalog routes
    │   ├── forms.py            # ContactForm
    │   └── templates/
    │       └── products/
    │           ├── index.html
    │           ├── category.html
    │           └── product.html
    │
    ├── auth/                   # Auth Blueprint
    │   ├── __init__.py
    │   ├── views.py            # Login/register/logout
    │   ├── forms.py            # LoginForm, RegistrationForm
    │   └── templates/
    │       └── auth/
    │           ├── login.html
    │           ├── register.html
    │           └── welcome.html
    │
    ├── admin/                  # Admin Blueprint
    │   ├── __init__.py
    │   ├── views.py            # Product CRUD voor admins
    │   ├── forms.py            # AddProductForm, EditProductForm
    │   └── templates/
    │       └── admin/
    │           ├── products.html
    │           ├── add_product.html
    │           └── edit_product.html
    │
    ├── templates/              # Gedeelde templates
    │   ├── base.html           # Base template
    │   ├── contact.html        # Contact pagina
    │   └── 404.html            # Error page
    │
    └── static/                 # CSS, JS, images (toekomstig)
```

## Belangrijkste Wijzigingen

### 1. Application Factory Pattern

**Week 7a (Monolithisch):**

```python
# app.py
app = Flask(__name__)
app.config['SECRET_KEY'] = '...'
db.init_app(app)

@app.route('/')
def index():
    pass
```

**Week 7b (Factory):**

```python
# webshop_app/__init__.py
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '...'

    db.init_app(app)
    login_manager.init_app(app)

    # Registreer blueprints
    from webshop_app.products.views import products_bp
    app.register_blueprint(products_bp)

    return app

# app.py
from webshop_app import create_app
app = create_app()
```

**Voordelen:**

- Kan meerdere app instances maken (voor tests met verschillende config)
- Extensions worden pas gebonden bij create_app() call
- Config kan per environment verschillen

### 2. Blueprint Routes

**Route definitie in blueprint:**

```python
# webshop_app/products/views.py
from flask import Blueprint

products_bp = Blueprint(
    'products',           # Blueprint naam
    __name__,
    template_folder='templates'
)

@products_bp.route("/")
def index():
    # Deze route is beschikbaar als '/'
    pass

@products_bp.route("/product/<int:product_id>")
def product(product_id):
    # Deze route is beschikbaar als '/product/<id>'
    pass
```

**Blueprint registratie met prefix:**

```python
# webshop_app/__init__.py
app.register_blueprint(products_bp)  # Geen prefix, routes beginnen bij /
app.register_blueprint(auth_bp, url_prefix='/auth')  # Routes beginnen bij /auth
app.register_blueprint(admin_bp, url_prefix='/admin')  # Routes beginnen bij /admin
```

**Resultaat:**

| Blueprint | Route | URL |
|-----------|-------|-----|
| products  | `@products_bp.route("/")` | `/` |
| products  | `@products_bp.route("/product/<id>")` | `/product/123` |
| auth      | `@auth_bp.route("/login")` | `/auth/login` |
| auth      | `@auth_bp.route("/logout")` | `/auth/logout` |
| admin     | `@admin_bp.route("/products")` | `/admin/products` |

### 3. URL Generation met Blueprints

**Week 7a:**

```python
url_for('index')           # Naar index() functie
url_for('login')           # Naar login() functie
url_for('admin_products')  # Naar admin_products() functie
```

**Week 7b:**

```python
url_for('products.index')        # Blueprint.view syntax!
url_for('auth.login')            # auth blueprint, login view
url_for('admin.products')        # admin blueprint, products view
url_for('products.category', category_id=1)  # Met parameters
```

**In templates:**

```jinja
<!-- base.html -->
<a href="{{ url_for('products.index') }}">Home</a>
<a href="{{ url_for('auth.login') }}">Inloggen</a>
<a href="{{ url_for('admin.products') }}">Admin Panel</a>

<!-- category.html -->
<a href="{{ url_for('products.product', product_id=product.id) }}">
    Bekijk Product
</a>
```

### 4. Template Folders

Elke blueprint heeft eigen template folder:

```python
# products/views.py
products_bp = Blueprint('products', __name__, template_folder='templates')

# De templates staan in products/templates/products/
# Dit voorkomt naming conflicts tussen blueprints
```

**Flask zoekt templates in deze volgorde:**

1. `webshop_app/templates/` (main app templates)
2. `webshop_app/products/templates/` (products blueprint)
3. `webshop_app/auth/templates/` (auth blueprint)
4. `webshop_app/admin/templates/` (admin blueprint)

**Best practice:** Gebruik subfolders met blueprint naam:

```text
products/templates/products/index.html  # Goed!
products/templates/index.html           # Vermijd (kan conflicts geven)
```

### 5. Circular Import Prevention

**Probleem:**

```python
# models.py
from webshop_app import db  # Circular import!

# __init__.py
from webshop_app.models import Customer  # Circular import!
```

**Oplossing:**

```python
# models.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()  # Maak db hier aan

# __init__.py
from webshop_app.models import db  # Import db
db.init_app(app)  # Bind aan app in factory
```

## URL Prefix Voorbeelden

### Zonder Prefix (Products)

```python
app.register_blueprint(products_bp)  # Geen url_prefix
```

| View | Route definitie | Final URL |
|------|----------------|-----------|
| index | `@products_bp.route("/")` | `/` |
| category | `@products_bp.route("/category/<id>")` | `/category/5` |
| product | `@products_bp.route("/product/<id>")` | `/product/10` |

### Met Prefix (Auth)

```python
app.register_blueprint(auth_bp, url_prefix='/auth')
```

| View | Route definitie | Final URL |
|------|----------------|-----------|
| login | `@auth_bp.route("/login")` | `/auth/login` |
| register | `@auth_bp.route("/register")` | `/auth/register` |
| logout | `@auth_bp.route("/logout")` | `/auth/logout` |

### Met Prefix (Admin)

```python
app.register_blueprint(admin_bp, url_prefix='/admin')
```

| View | Route definitie | Final URL |
|------|----------------|-----------|
| products | `@admin_bp.route("/products")` | `/admin/products` |
| add_product | `@admin_bp.route("/product/add")` | `/admin/product/add` |
| edit_product | `@admin_bp.route("/product/edit/<id>")` | `/admin/product/edit/5` |

## Installatie

1. **Installeer dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Migreer data (optioneel):**

   ```bash
   python migrate_database.py
   ```

3. **Start de applicatie:**

   ```bash
   python app.py
   ```

4. **Open in browser:**

   ```text
   http://127.0.0.1:5000
   ```

## Code Vergelijking

### Route Definitie

**Week 7a:**

```python
# app.py (alles in één bestand)
@app.route("/")
def index():
    categories = db.session.execute(db.select(Category)).scalars().all()
    return render_template("index.html", categories=categories)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # ... login logic
    return render_template('login.html', form=form)

@app.route("/admin/products")
@admin_required
def admin_products():
    products = db.session.execute(db.select(Product)).scalars().all()
    return render_template("admin_products.html", products=products)
```

**Week 7b:**

```python
# products/views.py
@products_bp.route("/")
def index():
    categories = db.session.execute(db.select(Category)).scalars().all()
    return render_template("products/index.html", categories=categories)

# auth/views.py
@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # ... login logic
    return render_template('auth/login.html', form=form)

# admin/views.py
@admin_bp.route("/products")
@admin_required
def products():
    all_products = db.session.execute(db.select(Product)).scalars().all()
    return render_template("admin/products.html", products=all_products)
```

### Imports

**Week 7a:**

```python
# app.py
from flask import Flask, render_template
from models import db, Category, Product, Customer
from forms import LoginForm, AddProductForm
# Alles in één bestand
```

**Week 7b:**

```python
# products/views.py
from flask import Blueprint, render_template
from webshop_app.models import Category, Product
from webshop_app.products.forms import ContactForm

# auth/views.py
from flask import Blueprint, redirect, url_for
from webshop_app.models import Customer
from webshop_app.auth.forms import LoginForm, RegistrationForm

# admin/views.py
from flask import Blueprint
from webshop_app.models import Product
from webshop_app.admin.forms import AddProductForm
```

## Testing met Blueprints

Blueprints kunnen apart getest worden:

```python
# tests/test_products.py
def test_products_blueprint():
    """Test products blueprint routes."""
    app = create_app('testing')
    client = app.test_client()

    # Test index route
    response = client.get('/')
    assert response.status_code == 200

    # Test product detail
    response = client.get('/product/1')
    assert response.status_code == 200

# tests/test_auth.py
def test_auth_blueprint():
    """Test authentication blueprint."""
    app = create_app('testing')
    client = app.test_client()

    # Test login page
    response = client.get('/auth/login')
    assert response.status_code == 200

    # Test registration
    response = client.post('/auth/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'test123',
        'password_confirm': 'test123'
    })
    assert response.status_code == 302  # Redirect
```

## Best Practices

1. **Één Blueprint per Feature**
   - products/ voor catalog
   - auth/ voor authentication
   - admin/ voor admin panel
   - orders/ voor checkout (toekomstig)

2. **Duidelijke Naming**
   - Blueprint naam: `products_bp`, `auth_bp`, `admin_bp`
   - View functies: `index()`, `login()`, `add_product()`
   - URL constructie: `url_for('blueprint.view')`

3. **Template Organisatie**
   - Main templates: `webshop_app/templates/base.html`
   - Blueprint templates: `blueprint/templates/blueprint_name/view.html`
   - Voorbeeld: `admin/templates/admin/products.html`

4. **Import Patterns**
   - Absolute imports: `from webshop_app.models import Product`
   - Relative imports binnen blueprint: `from .forms import LoginForm`

5. **URL Prefixes**
   - Public routes: geen prefix (`/`, `/product/1`)
   - Feature routes: descriptive prefix (`/auth/login`, `/admin/products`)

## Veelvoorkomende Fouten

### 1. Verkeerde url_for() syntax

```python
# Fout - geen blueprint prefix
url_for('login')

# Correct - met blueprint naam
url_for('auth.login')
```

### 2. Template niet gevonden

```python
# Fout - template in verkeerde folder
# admin/templates/products.html
return render_template('products.html')

# Correct - met blueprint subfolder
# admin/templates/admin/products.html
return render_template('admin/products.html')
```

### 3. Circular imports

```python
# Fout - import bovenaan
# models.py
from webshop_app import db

# Correct - maak db in models.py
# models.py
db = SQLAlchemy()

# __init__.py
from webshop_app.models import db
db.init_app(app)
```

### 4. Blueprint registratie vergeten

```python
# Fout - blueprint niet geregistreerd
# __init__.py
from webshop_app.products.views import products_bp
# Vergeet app.register_blueprint()

# Correct - altijd registreren
from webshop_app.products.views import products_bp
app.register_blueprint(products_bp)
```

## Migration Checklist

Van Week 7a naar Week 7b:

- [ ] Maak `webshop_app/` package met `__init__.py`
- [ ] Verplaats `models.py` naar `webshop_app/`
- [ ] Maak blueprint folders (products, auth, admin)
- [ ] Split routes uit `app.py` naar blueprint `views.py` bestanden
- [ ] Split forms naar blueprint `forms.py` bestanden
- [ ] Verplaats templates naar blueprint template folders
- [ ] Update `url_for()` calls met blueprint prefixes
- [ ] Maak application factory in `__init__.py`
- [ ] Update `app.py` om create_app() te gebruiken
- [ ] Test alle routes
- [ ] Commit!

## Resources

- [Flask Blueprints Documentation](https://flask.palletsprojects.com/en/3.0.x/blueprints/)
- [Application Factories](https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/)
- [Larger Applications](https://flask.palletsprojects.com/en/3.0.x/tutorial/layout/)
