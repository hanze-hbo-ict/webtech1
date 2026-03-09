# Webshop Flask Applicatie met Formulieren (Week 5)

Deze applicatie bouwt voort op Week 4 door Flask-WTF formulieren toe te voegen voor product beheer.

## Rode Draad door de Cursus

Deze webshop applicatie bouwt voort op:

- **Week 2 (OOP):** `Product`, `Customer`, `Order`, `Cart` classes
- **Week 3 (SQL):** `webshop.sqlite` database met `products` en `categories`
- **Week 4 (Flask):** Product catalog met routes en templates
- **Week 5 (Forms):** WTForms voor product CRUD operaties
- **Week 6 (SQLAlchemy):** ORM models voor database (komt nog)
- **Week 7 (Auth/Blueprints):** Login en gestructureerde app (komt nog)

## Nieuwe Features in Week 5

### Forms met Flask-WTF

- **AddProductForm** - Formulier om producten toe te voegen

- Validators voor naam, prijs, voorraad
- Dropdown voor categorie selectie
- CSRF-beveiliging

- **EditProductForm** - Formulier om producten te bewerken

- Pre-filled met huidige product data
- Alle velden editable
- Delete functionaliteit

- **ContactForm** - Contact formulier voor klanten

- Naam, email, onderwerp, bericht
- Email validatie
- Flash messages na verzenden

### Admin Routes

- `/admin/products` - Overzicht van alle producten
- `/admin/product/add` - Product toevoegen
- `/admin/product/edit/<id>` - Product bewerken
- `/admin/product/delete/<id>` - Product verwijderen (POST only)

### Database Updates

De `database.py` is uitgebreid met CRUD operaties:

- `add_product()` - INSERT query
- `update_product()` - UPDATE query
- `delete_product()` - DELETE query
- `get_category_choices()` - Helper voor SelectField

## Structuur

```text
webshop/
├── app.py                    # Flask app met formulier routes
├── database.py               # Database class met CRUD
├── forms.py                  # WTForms definities
├── templates/
│   ├── base.html            # Base template met nav + flash messages
│   ├── index.html           # Homepage
│   ├── category.html        # Categorie overzicht
│   ├── product.html         # Product detail (+ edit knop)
│   ├── admin_products.html  # Admin product lijst
│   ├── add_product.html     # Product toevoegen formulier
│   ├── edit_product.html    # Product bewerken formulier
│   ├── contact.html         # Contact formulier
│   └── 404.html             # Error pagina
└── static/                   # CSS, images (optioneel)
```

## Setup

### 1. Installeer dependencies

```console
uv init
uv add flask flask-wtf
```

### 2. Controleer database pad

De `database.py` zoekt de database in:

```python
db_path = "../../../week3/bestanden/webshop.sqlite"
```

Pas aan indien nodig.

### 3. Run de applicatie

```console
uv run python app.py
```

### 4. Open in browser

```text
http://127.0.0.1:5000/
```

## Flash Messages

De applicatie gebruikt Flask's `flash()` voor gebruikersfeedback:

```python
flash('Product succesvol toegevoegd!', 'success')
flash('Er ging iets mis.', 'danger')
```

Bootstrap alert categories:

- `success` - Groen (succes)
- `danger` - Rood (error)
- `warning` - Oranje (waarschuwing)
- `info` - Blauw (informatie)

## WTForms Validators

### AddProductForm & EditProductForm

| Veld | Type | Validators |
|------|------|-----------|
| `name` | StringField | DataRequired, Length(min=2, max=200) |
| `price` | FloatField | DataRequired, NumberRange(min=0.01, max=999999.99) |
| `stock` | IntegerField | DataRequired, NumberRange(min=0, max=999999) |
| `description` | TextAreaField | Optional, Length(max=1000) |
| `category_id` | SelectField | DataRequired, coerce=int |

### ContactForm

| Veld | Type | Validators |
|------|------|-----------|
| `name` | StringField | DataRequired, Length(min=2, max=100) |
| `email` | StringField | DataRequired, Length(max=120) |
| `subject` | StringField | DataRequired, Length(min=3, max=200) |
| `message` | TextAreaField | DataRequired, Length(min=10, max=2000) |

## Routes Uitleg

### Admin Routes

#### POST /admin/product/add

```python
@app.route("/admin/product/add", methods=['GET', 'POST'])
def admin_add_product() -> str:
    form = AddProductForm()
    form.category_id.choices = db.get_category_choices()

    if form.validate_on_submit():
        new_product_id = db.add_product(
            name=form.name.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data,
            description=form.description.data
        )
        flash(f'Product "{form.name.data}" toegevoegd!', 'success')
        return redirect(url_for('product', product_id=new_product_id))

    return render_template("add_product.html", form=form)
```

**GET:** Toont leeg formulier
**POST:** Valideert en voegt product toe aan database

#### GET/POST /admin/product/edit/<id>

```python
@app.route("/admin/product/edit/<int:product_id>", methods=['GET', 'POST'])
def admin_edit_product(product_id: int) -> str:
    product_info = db.get_product_by_id(product_id)
    form = EditProductForm()
    form.category_id.choices = db.get_category_choices()

    if form.validate_on_submit():
        db.update_product(...)
        flash('Product gewijzigd!', 'success')
        return redirect(url_for('product', product_id=product_id))

    # Pre-fill form bij GET request
    elif not form.is_submitted():
        form.name.data = product_info['name']
        form.price.data = product_info['price']
        # ... etc

    return render_template("edit_product.html", form=form, product=product_info)
```

**GET:** Toont formulier met huidige product data
**POST:** Valideert en update product

#### POST /admin/product/delete/<id>

```python
@app.route("/admin/product/delete/<int:product_id>", methods=['POST'])
def admin_delete_product(product_id: int) -> str:
    product_info = db.get_product_by_id(product_id)
    db.delete_product(product_id)
    flash(f'Product "{product_info["name"]}" verwijderd.', 'success')
    return redirect(url_for('admin_products'))
```

**Alleen POST** voor veiligheid (CSRF protection)

## Template Patterns

### Formulier Rendering

```html
<form method="POST">
    {{ form.hidden_tag() }}  {# CSRF token #}

    <div class="mb-3">
        {{ form.name.label(class="form-label") }}
        {{ form.name(class="form-control" + (" is-invalid" if form.name.errors else "")) }}

        {% if form.name.errors %}
            <div class="invalid-feedback">
                {% for error in form.name.errors %}
                    <div>{{ error }}</div>
                {% endfor %}
            </div>
        {% endif %}
    </div>

    {{ form.submit(class="btn btn-primary") }}
</form>
```

### Flash Messages

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
        <div class="alert alert-{{ category }} alert-dismissible fade show">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

## Security Features

### CSRF Protection

Flask-WTF biedt automatische CSRF-beveiliging:

```python
app.config['SECRET_KEY'] = 'webshop-secret-key-2025'
```

Elke form heeft een hidden CSRF token:

```python
{{ form.hidden_tag() }}
```

### POST-only Delete

Delete operaties zijn alleen via POST toegestaan:

```python
@app.route("/admin/product/delete/<int:id>", methods=['POST'])
```

Dit voorkomt accidentele deletes via GET requests.

### Confirm Dialog

JavaScript confirm bij delete:

```html
<form onsubmit="return confirm('Weet je het zeker?');">
    <button type="submit">Verwijderen</button>
</form>
```

## Validatie

WTForms valideert automatisch:

1. **DataRequired:** Veld mag niet leeg zijn
2. **NumberRange:** Getal binnen min/max
3. **Length:** String lengte binnen min/max
4. **Email:** Geldig email adres (optioneel)
5. **Optional:** Veld mag leeg zijn

Custom foutmeldingen:

```python
validators=[
    DataRequired(message="Product naam is verplicht"),
    Length(min=2, max=200, message="Naam moet tussen 2 en 200 karakters zijn")
]
```

## Tips

### Form Flow

1. **Create form instance**

   ```python
   form = AddProductForm()
   ```

2. **Populate choices** (voor SelectField)

   ```python
   form.category_id.choices = db.get_category_choices()
   ```

3. **Check validation**

   ```python
   if form.validate_on_submit():
       # Process form data
   ```

4. **Access form data**

   ```python
   form.name.data  # User input
   ```

5. **Flash message & redirect**

   ```python
   flash('Success!', 'success')
   return redirect(url_for('index'))
   ```

### Edit Form Pattern

```python
if form.validate_on_submit():
    # Update database
    ...
elif not form.is_submitted():
    # Pre-fill form (GET request)
    form.name.data = existing_data['name']
```

## Testing

Test alle formulieren:

**Add Product:**

1. Ga naar `/admin/product/add`
2. Vul alle velden in
3. Submit
4. Check flash message & redirect

**Edit Product:**

1. Ga naar een product detail pagina
2. Klik "Bewerken (Admin)"
3. Wijzig velden
4. Submit
5. Check updates

**Delete Product:**

1. Ga naar edit pagina
2. Klik "Product Verwijderen"
3. Bevestig dialog
4. Check flash message & redirect

**Contact Form:**

1. Ga naar `/contact`
2. Vul formulier in
3. Test validators (lege velden, te korte tekst)
4. Submit
5. Check flash message

## Debugging

### Form Errors

Print form errors in development:

```python
if form.errors:
    print(form.errors)
```

### CSRF Errors

Als je CSRF errors krijgt:

1. Check of SECRET_KEY is geconfigureerd
2. Check of `{{ form.hidden_tag() }}` in template staat
3. Check of je POST gebruikt voor formulier

## Volgende Stappen

In Week 6 gaan we:

- SQLAlchemy ORM gebruiken in plaats van raw SQL
- Models maken voor Product, Category, Customer, Order
- Relationships definiëren tussen models
- Formulieren koppelen aan ORM models

## Referenties

- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)
- [WTForms Documentation](https://wtforms.readthedocs.io/)
- [WTForms Validators](https://wtforms.readthedocs.io/en/stable/validators/)
- [Bootstrap 5 Forms](https://getbootstrap.com/docs/5.3/forms/overview/)
