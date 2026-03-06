# Flask Forms - Basis Formulieren met WTForms

HTML formulieren zijn essentieel voor webapplicaties - ze laten gebruikers data invoeren. Flask gebruikt [Flask-WTF](https://flask-wtf.readthedocs.io/) en [WTForms](https://wtforms.readthedocs.io/) om formulieren te maken met automatische validatie en CSRF-beveiliging.

!!! warning "Projectwerk"
    Vanaf deze week werk je als duo aan [één van de vier voorgestelde projecten](../projecten/index.md). Tijdens de practica kun je hierover vragen stellen aan je practicumdocent. Bekijk [de omschrijving en beoordeling](../index.md#toetsing) voor details.

## Installatie

Voeg Flask-WTF toe aan je project:

```console
uv add flask-wtf
```

Dit installeert automatisch ook WTForms als dependency.

Controleer de installatie:

```console
uv run pip list
```

Je ziet nu onder andere:

```console
Package      Version
------------ -------
Flask        3.1.0
Flask-WTF    1.2.1
WTForms      3.2.1
```

## Formulier componenten

Een WTForms formulier bestaat uit:

1. **Secret key configuratie** - Voor CSRF-beveiliging
2. **Form class** - Definieert formulier velden
3. **View function** - Verwerkt GET en POST requests
4. **Template** - Rendert het formulier in HTML

## Basis voorbeeld

We maken een eenvoudig formulier dat vraagt welk instrument je wilt leren. Project structuur:

```text
mijn-flask-app/
├── app.py
└── templates/
    └── home.html
```

### Flask applicatie

**`app.py`:**

```python
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

# CSRF-beveiliging vereist een secret key
app.config['SECRET_KEY'] = 'mijngeheimesleutel'


class InstrumentForm(FlaskForm):
    """Formulier om muziekinstrument op te vragen."""

    instrument = StringField('Welk instrument wil je graag leren bespelen?')
    submit = SubmitField('Verzend')


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """Homepage met instrument formulier.

    Returns:
        Gerenderde template met formulier
    """
    instrument = False
    form = InstrumentForm()

    if form.validate_on_submit():
        # Haal data uit formulier
        instrument = form.instrument.data
        # Reset formulier veld
        form.instrument.data = ''

    return render_template('home.html', form=form, instrument=instrument)


if __name__ == '__main__':
    app.run(debug=True)
```

**Code uitleg:**

- `FlaskForm` - Base class voor alle WTForms formulieren
- `StringField` - Tekst invoerveld
- `SubmitField` - Verzendknop
- `app.config['SECRET_KEY']` - Vereist voor CSRF-beveiliging en sessions
- `form.validate_on_submit()` - Checkt of formulier is ingediend én valid
- `form.instrument.data` - Bevat de ingevoerde waarde

!!! warning "Secret key in productie"
    Hardcode nooit je secret key in productie! Gebruik environment variabelen:
    ```python
    import os
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-only')
    ```

### Template

**`templates/home.html`:**

```html
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Muziekschool Session</title>
</head>
<body>
    <h1>Welkom bij muziekschool Session</h1>

    <p>
    {% if instrument %}
        Het instrument van jouw keuze is {{ instrument }}.
        <br>De keuze kan gewijzigd worden in onderstaand formulier:
    {% else %}
        Geef de naam van een instrument op in dit formulier:
    {% endif %}
    </p>

    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.instrument.label }} {{ form.instrument() }}
        {{ form.submit() }}
    </form>
</body>
</html>
```

**Template uitleg:**

- `{{ form.hidden_tag() }}` - CSRF token (verplicht!)
- `{{ form.instrument.label }}` - Label tekst van het veld
- `{{ form.instrument() }}` - Het invoerveld zelf
- `{{ form.submit() }}` - De submit button

### Testen

Start de applicatie:

```console
uv run python app.py
```

Navigeer naar `http://127.0.0.1:5000/`:

> **Verwacht resultaat:** Je ziet een lege pagina met de tekst "Welkom bij muziekschool Session", een tekstveld met het label "Welk instrument wil je graag leren bespelen?" en een knop "Verzend".

Vul "Gitaar" in en klik Verzend:

> **Verwacht resultaat:** De pagina toont nu de tekst "Het instrument van jouw keuze is Gitaar. De keuze kan gewijzigd worden in onderstaand formulier:", gevolgd door een leeg formulier waarmee een nieuw instrument ingevoerd kan worden.

Het formulier toont nu de ingevoerde waarde en is opnieuw beschikbaar.

## Hoe werkt het?

### Request cycle

1. **Eerste bezoek (GET request)**:
   - `instrument = False`
   - `form.validate_on_submit()` is `False`
   - Template toont leeg formulier

2. **Formulier invullen en verzenden (POST request)**:
   - Browser stuurt POST met formulierdata
   - `form.validate_on_submit()` is `True`
   - Data wordt opgehaald: `instrument = form.instrument.data`
   - Veld wordt gereset: `form.instrument.data = ''`
   - Template toont ingevulde waarde + leeg formulier

### CSRF-beveiliging

`{{ form.hidden_tag() }}` voegt een verborgen CSRF token toe:

```html
<input type="hidden" name="csrf_token" value="...">
```

Flask-WTF valideert dit token automatisch. Zonder valid token wordt het formulier geweigerd.

!!! danger "Altijd hidden_tag() gebruiken"
    Zonder `{{ form.hidden_tag() }}` krijg je een foutmelding bij het indienen. Dit beschermt tegen Cross-Site Request Forgery aanvallen.

## Type hints overzicht

Voor moderne Flask + WTForms gebruik je deze type hints:

```python
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """Route handler met return type."""
    form = InstrumentForm()  # Type: InstrumentForm
    instrument: str | bool = False

    if form.validate_on_submit():
        instrument = form.instrument.data  # Type: str

    return render_template('home.html', form=form, instrument=instrument)
```

**Volgende stap:** [Deel 2](flask-forms-deel2.md) - Validators en field types.

## Samenvatting

In deze les heb je geleerd:

- **Flask-WTF installeren**: via `uv add flask-wtf`, wat ook WTForms automatisch als dependency installeert
- **Formulier componenten**: een WTForms formulier bestaat uit vier onderdelen: secret key configuratie, een form class, een view function en een template
- **FlaskForm**: basisklasse voor alle WTForms formulieren; velden zoals `StringField` en `SubmitField` worden gedefinieerd als klasse-attributen
- **SECRET_KEY**: verplichte configuratie voor CSRF-beveiliging en Flask sessions; nooit hardcoden in productie, gebruik in plaats daarvan een environment variabele
- **validate_on_submit()**: controleert of het formulier via POST is ingediend én alle validaties doorstaan heeft; retourneert `False` bij een GET-request
- **form.hidden_tag()**: voegt een verborgen CSRF token toe aan het formulier in de template; zonder dit token weigert Flask-WTF het formulier
- **GET/POST request cycle**: bij een GET-request wordt het lege formulier getoond; bij een POST-request wordt de ingediende data uitgelezen via `form.veld.data`
- **CSRF-beveiliging**: Flask-WTF valideert het CSRF token automatisch bij elke POST-request om Cross-Site Request Forgery aanvallen te voorkomen
