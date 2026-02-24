# Week 7a: User Authentication - Webshop

In deze week voegen we **User Authentication** toe aan de webshop met Flask-Login. Gebruikers kunnen inloggen, registreren, en we onderscheiden tussen **Admin** en **Customer** rollen.

## Rode draad: Van ORM naar Authentication

We bouwen verder op Week 6 SQLAlchemy ORM en voegen authenticatie toe:

| Week | Aanpak | Capabilities |
|------|--------|-------------|
| Week 6 | SQLAlchemy ORM | Iedereen kan alles doen, geen login |
| **Week 7a** | **Flask-Login** | Login/Register, Admin vs Customer, Protected routes |
| Week 7b | Blueprints | Modular app structure |

## Belangrijkste Concepten

### 1. Flask-Login

Flask-Login biedt gebruikerssessie beheer:

- ID van actieve gebruiker wordt opgeslagen in sessie
- Makkelijk inloggen/uitloggen
- Views beperken tot ingelogde gebruikers
- "Remember me" functionaliteit
- Bescherming tegen cookie diefstal

**Wat Flask-Login NIET doet:**

- Geen password hashing (dat doen we met Werkzeug)
- Geen registration forms (dat doen we met Flask-WTF)
- Geen database models (dat doen we met SQLAlchemy)

### 2. Password Hashing met Werkzeug

**Waarom password hashing?**

- Wachtwoorden NOOIT in plain text opslaan in database
- Als database wordt gehackt, zijn wachtwoorden veilig
- Zelfs database admins kunnen wachtwoorden niet zien

**Hoe werkt het?**

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Bij registratie: hash het wachtwoord
hashed = generate_password_hash('mijnwachtwoord')
# Output: 'pbkdf2:sha256:150000$hUiH149n$af71be7ff...'

# Bij login: check of wachtwoord klopt
check_password_hash(hashed, 'mijnwachtwoord')  # True
check_password_hash(hashed, 'fout')  # False
```

**Belangrijke eigenschappen:**

- Zelfde wachtwoord geeft elke keer andere hash (door salt)
- Hash kan niet worden teruggerekend naar origineel wachtwoord
- Check is snel, maar brute force is traag (door PBKDF2)

### 3. UserMixin

UserMixin voegt automatisch methodes toe aan Customer model:

```python
class Customer(db.Model, UserMixin):
    # ...

# Nu beschikbaar zonder dat je ze hoeft te schrijven:
customer.is_authenticated()  # True als ingelogd
customer.is_active()         # True als account actief is
customer.is_anonymous()      # False voor echte users
customer.get_id()           # Geeft ID als string
```

### 4. LoginManager

LoginManager coordineert de authenticatie:

```python
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Waar heen bij @login_required
```

**user_loader decorator:**

```python
@login_manager.user_loader
def load_user(user_id):
    """Flask-Login gebruikt deze functie om user te laden uit sessie."""
    return db.session.get(Customer, int(user_id))
```

### 5. Admin vs Customer Roles

We gebruiken een `is_admin` boolean field om te onderscheiden:

```python
class Customer(db.Model, UserMixin):
    is_admin: Mapped[bool] = mapped_column(default=False)

# Bij aanmaken:
admin = Customer(name='Admin', email='admin@webshop.nl',
                 password='admin123', is_admin=True)
customer = Customer(name='Jan', email='jan@email.nl',
                    password='wachtwoord', is_admin=False)
```

**Admin checks in templates:**

```jinja
{% if current_user.is_admin %}
    <a href="{{ url_for('admin_products') }}">Admin Panel</a>
{% endif %}
```

**Admin checks in routes:**

```python
@app.route('/admin/products')
@admin_required  # Custom decorator!
def admin_products():
    # Alleen admins kunnen hier komen
    pass
```

## Bestanden Structuur

```text
webshop/
├── app.py                  # Flask app met authentication routes
├── models.py               # Customer met UserMixin en password hashing
├── forms.py                # LoginForm, RegistrationForm
├── migrate_database.py     # Database migratie script
├── templates/
│   ├── base.html          # Met login/logout links
│   ├── login.html         # Login formulier
│   ├── register.html      # Registratie formulier
│   ├── welcome.html       # Account pagina
│   ├── index.html
│   ├── category.html
│   ├── product.html
│   ├── admin_products.html
│   ├── add_product.html
│   ├── edit_product.html
│   ├── contact.html
│   └── 404.html
└── webshop.db              # SQLite database
```

## Installatie

1. **Installeer dependencies:**

   ```bash
   pip install flask flask-sqlalchemy flask-wtf flask-login
   ```

2. **Migreer data van Week 6 (optioneel):**

   ```bash
   python migrate_database.py
   ```

3. **Start de applicatie:**

   ```bash
   python app.py
   ```

   Bij eerste start wordt automatisch een demo admin aangemaakt:
   - **Email:** <admin@webshop.nl>
   - **Wachtwoord:** admin123

4. **Open in browser:**

   ```text
   http://127.0.0.1:5000
   ```

## Nieuwe Routes

### Authentication Routes

| Route | Methods | Functie | Access |
|-------|---------|---------|--------|
| `/login` | GET, POST | Inloggen | Iedereen |
| `/register` | GET, POST | Registreren | Iedereen |
| `/logout` | GET | Uitloggen | `@login_required` |
| `/welcome` | GET | Account overzicht | `@login_required` |

### Admin Routes (nu beveiligd!)

| Route | Methods | Functie | Access |
|-------|---------|---------|--------|
| `/admin/products` | GET | Alle producten | `@admin_required` |
| `/admin/product/add` | GET, POST | Product toevoegen | `@admin_required` |
| `/admin/product/edit/<id>` | GET, POST | Product bewerken | `@admin_required` |
| `/admin/product/delete/<id>` | POST | Product verwijderen | `@admin_required` |

### Public Routes (ongewijzigd)

| Route | Functie |
|-------|---------|
| `/` | Categorieën overzicht |
| `/category/<id>` | Producten in categorie |
| `/product/<id>` | Product detail |
| `/contact` | Contact formulier |

## Code Examples

### 1. Login Flow

```python
@app.route("/login", methods=['GET', 'POST'])
def login():
    # Al ingelogd? → redirect naar welcome
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))

    form = LoginForm()

    if form.validate_on_submit():
        # Zoek user op email
        user = db.session.execute(db.select(Customer).filter_by(email=form.email.data)).scalar_one_or_none()

        # Check wachtwoord
        if user and user.check_password(form.password.data):
            # Log in!
            login_user(user)
            flash(f'Welkom terug, {user.name}!', 'success')

            # Redirect naar 'next' parameter of welcome
            next_page = request.args.get('next')
            return redirect(next_page or url_for('welcome'))
        else:
            flash('Ongeldig e-mailadres of wachtwoord.', 'danger')

    return render_template('login.html', form=form)
```

**Hoe werkt de 'next' parameter?**

```text
1. User probeert /admin/products te bezoeken (niet ingelogd)
2. @admin_required redirect naar /login?next=/admin/products
3. User logt in
4. Wordt doorgestuurd naar /admin/products
```

### 2. Registration Flow

```python
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Maak nieuwe Customer aan
        new_customer = Customer(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,  # Wordt automatisch gehashed!
            is_admin=False  # Nieuwe users zijn geen admin
        )

        db.session.add(new_customer)
        db.session.commit()

        flash(f'Account aangemaakt! Je kunt nu inloggen.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)
```

### 3. Custom Email Validator

```python
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    # ... andere velden ...

    def validate_email(self, field):
        """WTForms roept validate_<fieldname> automatisch aan!"""
        if db.session.execute(db.select(Customer).filter_by(email=field.data)).scalar_one_or_none():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')
```

**Belangrijk:** WTForms roept `validate_email()` automatisch aan bij validatie!

### 4. Custom Admin Decorator

```python
from functools import wraps

def admin_required(f):
    """Decorator om routes te beschermen voor alleen admins."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check of ingelogd
        if not current_user.is_authenticated:
            flash('Log in om deze pagina te bekijken.', 'warning')
            return redirect(url_for('login'))

        # Check of admin
        if not current_user.is_admin:
            flash('Deze pagina is alleen voor admins.', 'danger')
            return redirect(url_for('index'))

        # Alles OK, ga door
        return f(*args, **kwargs)
    return decorated_function

# Gebruik:
@app.route('/admin/products')
@admin_required
def admin_products():
    products = db.session.execute(db.select(Product)).scalars().all()
    return render_template('admin_products.html', products=products)
```

**Waarom `@wraps(f)`?**

- Behoudt originele functienaam en docstring
- Zonder `@wraps` zou `admin_products.__name__` = "decorated_function" zijn
- Dit breekt `url_for()` en Flask's routing

### 5. Template Context (current_user)

Flask-Login maakt `current_user` automatisch beschikbaar in templates:

```jinja
<!-- base.html -->
{% if current_user.is_authenticated %}
    <li>
        <a href="{{ url_for('logout') }}">
            Uitloggen ({{ current_user.name }})
        </a>
    </li>

    {% if current_user.is_admin %}
    <li><a href="{{ url_for('admin_products') }}">Admin Panel</a></li>
    {% endif %}
{% else %}
    <li><a href="{{ url_for('login') }}">Inloggen</a></li>
    <li><a href="{{ url_for('register') }}">Registreren</a></li>
{% endif %}
```

## Test Scenario's

### Scenario 1: Customer Account

1. Ga naar `http://127.0.0.1:5000/register`
2. Vul formulier in:
   - Naam: Jan Jansen
   - Email: <jan@email.nl>
   - Wachtwoord: test123 (2x)
3. Klik "Registreren"
4. Je wordt naar `/login` gestuurd
5. Log in met <jan@email.nl> / test123
6. Je ziet `/welcome` met je account info
7. Probeer `/admin/products` te bezoeken → Access Denied!

### Scenario 2: Admin Account

1. Log in met <admin@webshop.nl> / admin123
2. Je ziet "Admin" badge in navigation
3. Klik "Admin → Alle Producten"
4. Voeg nieuw product toe
5. Bewerk product
6. Verwijder product

### Scenario 3: Protected Routes

1. Log uit (als je ingelogd bent)
2. Probeer `/welcome` te bezoeken
3. Je wordt naar `/login?next=/welcome` geredirect
4. Log in
5. Je wordt naar `/welcome` gestuurd (de 'next' parameter!)

## Security Best Practices

### 1. Password Requirements

```python
password = PasswordField(
    'Wachtwoord',
    validators=[
        DataRequired(),
        Length(min=6, message="Wachtwoord moet minimaal 6 karakters zijn")
    ]
)
```

**Voor productie:**

- Minimaal 8 karakters
- Verplicht cijfers/speciale tekens
- Gebruik `zxcvbn` library voor strength check

### 2. CSRF Protection

Flask-WTF beveiligt automatisch tegen CSRF:

```python
# In form
{{ form.hidden_tag() }}  # Genereert CSRF token

# In app.py
app.config['SECRET_KEY'] = 'webshop-secret-key-2025'  # Verplicht!
```

**Voor productie:**

```python
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Random key!
# Bewaar in environment variable, NIET in code!
```

### 3. SQL Injection Prevention

SQLAlchemy ORM voorkomt SQL injection automatisch:

```python
# Veilig - ORM escaped automatisch
db.session.execute(db.select(Customer).filter_by(email=user_input)).scalar_one_or_none()

# GEVAARLIJK - nooit doen!
db.session.execute(f"SELECT * FROM customers WHERE email = '{user_input}'")
```

### 4. Session Security

```python
# Voor productie:
app.config['SESSION_COOKIE_SECURE'] = True  # Alleen over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Geen JavaScript toegang
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF bescherming
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
```

## Veelvoorkomende Fouten

### 1. Vergeten login_manager te initialiseren

```python
# Fout
login_manager = LoginManager()
# Vergeet init_app!

# Correct
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
```

### 2. UserMixin verkeerde volgorde

```python
# Fout - UserMixin moet TWEEDE zijn
class Customer(UserMixin, db.Model):
    pass

# Correct
class Customer(db.Model, UserMixin):
    pass
```

### 3. Password niet hashen

```python
# GEVAARLIJK - plain text password!
customer.password_hash = form.password.data

# Correct - hash in __init__
def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password_hash = generate_password_hash(password)
```

### 4. @login_required verkeerde volgorde

```python
# Fout - route moet eerst
@login_required
@app.route('/welcome')
def welcome():
    pass

# Correct - route altijd eerst!
@app.route('/welcome')
@login_required
def welcome():
    pass
```

### 5. Circular import in forms.py

```python
# Fout - importeert Customer te vroeg
from app import db
from models import Customer  # Circular import!

# Correct - import in functie
from flask_wtf import FlaskForm

class RegistrationForm(FlaskForm):
    def validate_email(self, field):
        # Import hier, niet bovenaan!
        from models import Customer
        if db.session.execute(db.select(Customer).filter_by(email=field.data)).scalar_one_or_none():
            raise ValidationError('Email al in gebruik!')
```

## Next Steps: Week 7b

In Week 7b refactoren we de applicatie naar **Blueprints** voor betere modulariteit:

- `products/` blueprint - Catalog functionaliteit
- `auth/` blueprint - Login/register/logout
- `admin/` blueprint - Admin panel
- `orders/` blueprint - Winkelwagen en checkout

## Tips

1. **Test altijd met fresh database**

   ```bash
   rm webshop.db
   python app.py  # Maakt nieuwe DB aan met admin
   ```

2. **Check wachtwoord hash in database**

   ```python
   from app import app, db, Customer
   with app.app_context():
       admin = db.session.execute(db.select(Customer).filter_by(email='admin@webshop.nl')).scalar_one_or_none()
       print(admin.password_hash)
       # pbkdf2:sha256:150000$...
   ```

3. **Debug login issues**

   ```python
   user = db.session.execute(db.select(Customer).filter_by(email=form.email.data)).scalar_one_or_none()
   if user:
       print(f"User found: {user.name}")
       print(f"Password check: {user.check_password(form.password.data)}")
   else:
       print("User not found!")
   ```

## Resources

- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/en/2.3.x/utils/#module-werkzeug.security)
- [Flask-WTF](https://flask-wtf.readthedocs.io/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
