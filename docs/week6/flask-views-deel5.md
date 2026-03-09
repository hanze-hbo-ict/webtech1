# Flask en SQLAlchemy - Complete Website

Je combineert nu alle kennis: templates, formulieren, en database. Je bouwt een beheersite voor cursisten van de muziekschool met:

- Formulier om cursisten toe te voegen
- Overzicht van alle cursisten
- Formulier om cursisten te verwijderen

## Project structuur

Je maakt de volgende bestanden:

**Python bestanden**:

- `beheer_cursist.py` - Hoofd applicatie met routes
- `forms.py` - Formulier definities

**Templates directory**:

- `base.html` - Basis template met navigatie
- `home.html` - Homepage
- `voegtoe_cur.html` - Cursist toevoegen
- `toon_cur.html` - Cursisten tonen
- `verwijder_cur.html` - Cursist verwijderen

```text
project/
├── beheer_cursist.py
├── forms.py
└── templates/
    ├── base.html
    ├── home.html
    ├── voegtoe_cur.html
    ├── toon_cur.html
    └── verwijder_cur.html
```

## Stap 1: Database en model setup

**`beheer_cursist.py`** - Bestudeer het volledige bestand [`beheer_cursist.py`](bestanden/relaties/beheer_cursist.py).

### Imports en configuratie

```python
import os
from forms import VoegtoeForm, VerwijderForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mijngeheimesleutel'
```

`SECRET_KEY` is vereist voor formulieren (CSRF-beveiliging).

### Database setup

```python
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
```

### Cursist model

```python
class Cursist(db.Model):
    """Model voor cursisten van de muziekschool."""

    __tablename__ = 'cursisten'

    id: Mapped[int] = mapped_column(primary_key=True)
    naam: Mapped[str | None]

    def __init__(self, naam: str):
        """Maak nieuwe cursist aan.

        Args:
            naam: Voor- en achternaam
        """
        self.naam = naam

    def __repr__(self) -> str:
        """String representatie."""
        return f"Naam van de cursist: {self.naam}"
```

Dit model is eenvoudig - geen relaties, alleen een naam. Perfect om de basis te begrijpen.

## Stap 2: Routes en views

### Homepage route

```python
@app.route('/')
def index() -> str:
    """Homepage route.

    Returns:
        Gerenderde home template
    """
    return render_template('home.html')
```

### Cursist toevoegen

```python
@app.route('/add', methods=['GET', 'POST'])
def add_cur() -> str:
    """Voeg nieuwe cursist toe.

    Returns:
        Bij GET: formulier template
        Bij POST: redirect naar cursisten lijst
    """
    form = VoegtoeForm()

    if form.validate_on_submit():
        naam = form.naam.data

        # Voeg nieuwe cursist toe
        new_cur = Cursist(naam)
        db.session.add(new_cur)
        db.session.commit()

        return redirect(url_for('list_cur'))

    return render_template('voegtoe_cur.html', form=form)
```

**Workflow**:

1. GET request: Toon leeg formulier
2. POST request: Naam opslaan in database, redirect naar lijst

### Cursisten tonen

```python
@app.route('/list')
def list_cur() -> str:
    """Toon alle cursisten.

    Returns:
        Template met lijst van cursisten
    """
    cursisten = db.session.execute(db.select(Cursist)).scalars().all()
    return render_template('toon_cur.html', cursisten=cursisten)
```

Haalt alle cursisten op en geeft ze door aan de template.

### Cursist verwijderen

```python
@app.route('/delete', methods=['GET', 'POST'])
def del_cur() -> str:
    """Verwijder cursist op basis van ID.

    Returns:
        Bij GET: formulier template
        Bij POST: redirect naar cursisten lijst
    """
    form = VerwijderForm()

    if form.validate_on_submit():
        id = form.id.data
        cur = db.session.get(Cursist, id)
        db.session.delete(cur)
        db.session.commit()

        return redirect(url_for('list_cur'))

    return render_template('verwijder_cur.html', form=form)
```

**Workflow**:

1. GET request: Toon leeg formulier
2. POST request: Verwijder cursist op ID, redirect naar lijst

## Stap 3: Database aanmaken en app starten

### Database initialisatie

```python
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

!!! info "Flask application context"
    In moderne SQLAlchemy (3.0+) moet `db.create_all()` binnen een application context draaien:
    ```python
    with app.app_context():
        db.create_all()
    ```
    Dit zorgt ervoor dat SQLAlchemy toegang heeft tot de Flask configuratie.

## Stap 4: Formulieren definiëren

**`forms.py`** - Bestudeer het volledige bestand [`forms.py`](bestanden/forms.py).

```python
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class VoegtoeForm(FlaskForm):
    """Formulier voor nieuwe cursist."""

    naam = StringField('Vul de naam van de nieuwe cursist in:')
    submit = SubmitField('Voeg toe')


class VerwijderForm(FlaskForm):
    """Formulier voor cursist verwijderen."""

    id = IntegerField('Vul het ID van de cursist die verwijderd gaat worden in:')
    submit = SubmitField('Verwijder')
```

Twee eenvoudige formulieren:

- **VoegtoeForm**: Naam (text veld) + submit
- **VerwijderForm**: ID (nummer veld) + submit

## Stap 5: Templates maken

### `base.html` - Basis template

Bestudeer het volledige bestand [`base.html`](bestanden/templates/base.html).

```html
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Beheer cursisten</title>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <div class="navbar-nav">
                <a class="nav-link" href="{{ url_for('index') }}">Home</a>
                <a class="nav-link" href="{{ url_for('add_cur') }}">Voeg cursist toe</a>
                <a class="nav-link" href="{{ url_for('list_cur') }}">Toon cursisten</a>
                <a class="nav-link" href="{{ url_for('del_cur') }}">Verwijder cursist</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}
        {% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**Bootstrap 5** CDN links en navigatie balk. Alle andere templates extenden deze basis.

### `home.html`

Bestudeer het volledige bestand [`home.html`](bestanden/templates/home.html).

```html
{% extends "base.html" %}
{% block content %}
<div class="p-5 mb-4 bg-light rounded-3">
    <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">Welkom bij de beheersite van onze cursisten</h1>
        <p class="col-md-8 fs-4">Om te beginnen, selecteer een item uit de navigatiebalk.</p>
    </div>
</div>
{% endblock %}
```

!!! note "Bootstrap 5 wijziging"
    `jumbotron` bestaat niet meer in Bootstrap 5. Gebruik `p-5 mb-4 bg-light rounded-3` voor hetzelfde effect.

### `voegtoe_cur.html`

Bestudeer het volledige bestand [`voegtoe_cur.html`](bestanden/templates/voegtoe_cur.html).

```html
{% extends "base.html" %}
{% block content %}
<div class="p-5 mb-4 bg-light rounded-3">
    <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">Heeft zich een nieuwe cursist aangemeld?</h1>
        <p>Vul de naam in en klik op Voeg toe:</p>
        <form method="POST">
            {{ form.hidden_tag() }}
            <div class="mb-3">
                {{ form.naam.label(class="form-label") }}
                {{ form.naam(class="form-control") }}
            </div>
            {{ form.submit(class="btn btn-primary") }}
        </form>
    </div>
</div>
{% endblock %}
```

`{{ form.hidden_tag() }}` voegt CSRF token toe (verplicht).

### `toon_cur.html`

Bestudeer het volledige bestand [`toon_cur.html`](bestanden/templates/toon_cur.html).

```html
{% extends "base.html" %}
{% block content %}
<div class="p-5 mb-4 bg-light rounded-3">
    <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">Dit zijn de momenteel ingeschreven cursisten</h1>
        <ul class="list-group list-group-flush">
            {% for cur in cursisten %}
            <li class="list-group-item">{{ cur }}</li>
            {% endfor %}
        </ul>
    </div>
</div>
{% endblock %}
```

Jinja2 `for` loop toont alle cursisten. De tekst komt uit de `__repr__()` methode.

### `verwijder_cur.html`

Bestudeer het volledige bestand [`verwijder_cur.html`](bestanden/templates/verwijder_cur.html).

```html
{% extends "base.html" %}
{% block content %}
<div class="p-5 mb-4 bg-light rounded-3">
    <div class="container-fluid py-5">
        <h1 class="display-5 fw-bold">Afmelding binnen gekomen?</h1>
        <p>Vul het ID van de cursist in en klik op Verwijder.</p>
        <form method="POST">
            {{ form.hidden_tag() }}
            <div class="mb-3">
                {{ form.id.label(class="form-label") }}
                {{ form.id(class="form-control") }}
            </div>
            {{ form.submit(class="btn btn-danger") }}
        </form>
    </div>
</div>
{% endblock %}
```

## Stap 6: Testen

Start de applicatie:

```console
uv run python beheer_cursist.py
```

### Homepage

> **Verwacht resultaat:** Een Bootstrap-pagina met een navigatiebalk bovenaan met links: Home, Voeg cursist toe, Toon cursisten, Verwijder cursist. De pagina toont een jumbotron-blok met de tekst "Welkom bij de beheersite van onze cursisten" en een instructie om een item uit de navigatiebalk te selecteren.

### Cursist toevoegen

Klik "Voeg cursist toe":

> **Verwacht resultaat:** Een formulierpagina met de titel "Heeft zich een nieuwe cursist aangemeld?", een tekstveld met het label "Vul de naam van de nieuwe cursist in:" en een knop "Voeg toe".

Vul "Joyce" in en klik "Voeg toe":

> **Verwacht resultaat:** Hetzelfde formulier als hierboven, maar nu met "Joyce" ingevuld in het naamveld.

Na submit zie je de lijst:

> **Verwacht resultaat:** De cursistenpagina met de titel "Dit zijn de momenteel ingeschreven cursisten" en één item in de lijst: "Naam van de cursist: Joyce" (id=1).

### Nog een cursist toevoegen

Voeg "Bram" toe:

> **Verwacht resultaat:** Het toevoegformulier met "Bram" ingevuld in het naamveld.

Lijst met twee cursisten:

> **Verwacht resultaat:** De cursistenpagina met twee items in de lijst: "Naam van de cursist: Joyce" en "Naam van de cursist: Bram".

### Cursist verwijderen

Klik "Verwijder cursist". Bram heeft `id=2` (zie in database of lijst):

| id | naam  |
|----|-------|
| 1  | Joyce |
| 2  | Bram  |

Vul ID 2 in:

> **Verwacht resultaat:** De verwijderpagina met de titel "Afmelding binnen gekomen?" en een nummerveld met het label "Vul het ID van de cursist in die verwijderd gaat worden", met het getal "2" ingevuld.

Na submit is Bram verwijderd:

> **Verwacht resultaat:** De cursistenpagina met nog maar één item in de lijst: "Naam van de cursist: Joyce". Bram is verwijderd.

### Database controleren

Met DB Browser for SQLite:

| id | naam  |
|----|-------|
| 1  | Joyce |

Eén cursist over - Joyce met ID 1.

## Samenvatting

Je hebt een complete CRUD webapp gemaakt:

**Backend (Flask + SQLAlchemy)**:

- Database setup met `db.Model`
- Routes voor Create, Read, Delete
- Formulieren met Flask-WTF

**Frontend (Jinja2 + Bootstrap)**:

- Basis template met navigatie
- Formulier templates
- Lijst template met data uit database

**Database (SQLite)**:

- Eén tabel (`cursisten`)
- CRUD operaties via SQLAlchemy

**Volgende stap:** [Oefening 1](oefeningen/flask-views-oefening1.md) - Bouw je eigen beheersite.
