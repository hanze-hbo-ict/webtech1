# Flask Forms - Flash Messages

Flask kan tijdelijke berichten tonen aan gebruikers - bijvoorbeeld een bevestiging na het verzenden van een formulier. Deze berichten heten **flash messages**.

Flash messages zijn perfect voor:

- Bevestigingen ("Formulier verzonden!")
- Waarschuwingen ("Let op: dit veld is verplicht")
- Errors ("Er ging iets mis")
- Informatie ("Je sessie verloopt over 5 minuten")

Aan het eind van deze tekst maken we [oefening 1](oefeningen/flask-forms-oefening1.md).

## Basis voorbeeld

We maken een formulier met een knop die een flash message toont. Project structuur:

```text
mijn-flask-app/
├── app.py
└── templates/
    └── home.html
```

### Flask applicatie

**`app.py`:**

```python
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mijngeheimesleutel'


class KlikForm(FlaskForm):
    """Simpel formulier met alleen een knop."""

    submit = SubmitField('Klik mij!')


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """Homepage met klik formulier.

    Returns:
        Gerenderde template met formulier en flash messages
    """
    form = KlikForm()

    if form.validate_on_submit():
        flash('Je hebt zojuist de button geactiveerd!')
        return redirect(url_for('index'))

    return render_template('home.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
```

**Code uitleg:**

- `flash('bericht')` - Stuurt bericht naar de template
- `redirect(url_for('index'))` - Navigate terug naar index (voorkomt dubbele submit bij refresh)
- Flash messages worden automatisch verwijderd na 1x tonen

### Template met Bootstrap

We gebruiken Bootstrap 5 voor de styling van flash messages.

**`templates/home.html`:**

```html
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Flash Messages</title>

    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN"
          crossorigin="anonymous">
</head>
<body>
    <div class="container mt-5">
        <h1>Flash Message Demo</h1>

        <!-- Flash messages -->
        {% for message in get_flashed_messages() %}
        <div class="alert alert-warning alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        {% endfor %}

        <!-- Formulier -->
        <form method="POST">
            {{ form.hidden_tag() }}
            {{ form.submit(class="btn btn-primary") }}
        </form>
    </div>

    <!-- Bootstrap 5 JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
            crossorigin="anonymous"></script>
</body>
</html>
```

**Template uitleg:**

- `get_flashed_messages()` - Haalt alle flash messages op
- `{% for message in ... %}` - Loop door alle messages (kan er 0, 1 of meerdere zijn)
- `.alert-dismissible` - Maakt het bericht sluitbaar
- `.btn-close` - Sluit-knopje (X rechtsboven)
- `.fade.show` - Fade animatie bij sluiten

### Testen

Start de applicatie:

```console
uv run python app.py
```

Navigeer naar `http://127.0.0.1:5000/`:

> **Verwacht resultaat:** Je ziet een eenvoudige pagina met de koptekst "Flash Message Demo" en een blauwe knop met de tekst "Klik mij!". Er is nog geen melding zichtbaar.

Klik op de knop:

> **Verwacht resultaat:** Boven de knop verschijnt een gele Bootstrap-waarschuwingsmelding met de tekst "Je hebt zojuist de button geactiveerd!" en een sluitknopje (×) rechts in de melding.

Klik op het X - het bericht verdwijnt.

## Flash message categorieën

Je kunt categorieën toevoegen aan flash messages voor verschillende styling:

```python
flash('Formulier succesvol verzonden!', 'success')
flash('Waarschuwing: vul alle velden in', 'warning')
flash('Er is een fout opgetreden', 'danger')
flash('Ter informatie: sessie verloopt over 5 min', 'info')
```

In de template haal je categorie en message tegelijk op:

```html
{% for category, message in get_flashed_messages(with_categories=true) %}
<div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
    {{ message }}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
{% endfor %}
```

Dit genereert automatisch de juiste Bootstrap classes:

- `alert-success` (groen)
- `alert-warning` (geel)
- `alert-danger` (rood)
- `alert-info` (blauw)

### Voorbeeld met categorieën

```python
@app.route('/contact', methods=['GET', 'POST'])
def contact() -> str:
    """Contact formulier met verschillende flash messages."""
    form = ContactForm()

    if form.validate_on_submit():
        if not form.email.data:
            flash('Email is verplicht!', 'danger')
        else:
            flash('Bericht verzonden!', 'success')
            return redirect(url_for('index'))

    return render_template('contact.html', form=form)
```

## Bootstrap alert klassen

Bootstrap 5 heeft verschillende alert types:

```html
<!-- Success (groen) -->
<div class="alert alert-success">Gelukt!</div>

<!-- Warning (geel) -->
<div class="alert alert-warning">Let op!</div>

<!-- Danger (rood) -->
<div class="alert alert-danger">Fout!</div>

<!-- Info (blauw) -->
<div class="alert alert-info">Info</div>
```

Met `alert-dismissible` kan de gebruiker het bericht sluiten:

```html
<div class="alert alert-warning alert-dismissible fade show" role="alert">
    Bericht hier
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
```

## Accessibility attributen

Bootstrap alerts gebruiken ARIA attributen voor toegankelijkheid:

- `role="alert"` - Screen readers kondigen dit aan als belangrijk bericht
- `aria-label="Close"` - Beschrijft de close button voor screen readers
- `.btn-close` - Gestandaardiseerde close button (Bootstrap 5)

## Complete voorbeeld

**`app.py`:**

```python
from flask import Flask, render_template, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mijngeheimesleutel'


class NaamForm(FlaskForm):
    """Formulier voor voornaam en achternaam."""

    voornaam = StringField('Voornaam', validators=[DataRequired()])
    achternaam = StringField('Achternaam', validators=[DataRequired()])
    submit = SubmitField('Verzend')


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """Homepage met naam formulier.

    Returns:
        Gerenderde template met formulier
    """
    form = NaamForm()

    if form.validate_on_submit():
        # Sla op in session
        session['voornaam'] = form.voornaam.data
        session['achternaam'] = form.achternaam.data

        # Flash message met volledige naam
        volledige_naam = f"{form.voornaam.data} {form.achternaam.data}"
        flash(f'Welkom, {volledige_naam}!', 'success')

        return redirect(url_for('index'))

    return render_template('home.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
```

**`templates/home.html`:**

```html
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Naam Formulier</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN"
          crossorigin="anonymous">
</head>
<body>
    <div class="container mt-5">
        <h1>Welkom</h1>

        <!-- Flash messages met categorieën -->
        {% for category, message in get_flashed_messages(with_categories=true) %}
        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        {% endfor %}

        <!-- Formulier -->
        <form method="POST">
            {{ form.hidden_tag() }}

            <div class="mb-3">
                {{ form.voornaam.label(class="form-label") }}
                {{ form.voornaam(class="form-control") }}
            </div>

            <div class="mb-3">
                {{ form.achternaam.label(class="form-label") }}
                {{ form.achternaam(class="form-control") }}
            </div>

            {{ form.submit(class="btn btn-primary") }}
        </form>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
            crossorigin="anonymous"></script>
</body>
</html>
```

Dit toont een flash message met de volledige naam na het verzenden.

## Type hints voor flash

```python
from flask import flash

def verzend_formulier(naam: str, email: str) -> None:
    """Verzend formulier en toon flash message.

    Args:
        naam: Naam van de gebruiker
        email: Email adres
    """
    flash(f'Bedankt, {naam}! Bevestiging gestuurd naar {email}', 'success')
```

**Volgende stap:** Maak nu [oefening 1](oefeningen/flask-forms-oefening1.md).

## Samenvatting

In deze les heb je geleerd:

- **Flash messages**: tijdelijke berichten versturen naar de template met `flash('bericht')` vanuit een view function
- **get_flashed_messages()**: haalt alle flash messages op in de template via een `{% for %}`-lus; berichten worden automatisch verwijderd na één keer tonen
- **Flash categorieën**: een categorie meegeven als tweede argument aan `flash()`, zoals `'success'`, `'warning'`, `'danger'` of `'info'`, voor gedifferentieerde weergave
- **with_categories**: met `get_flashed_messages(with_categories=true)` haal je zowel de categorie als het bericht op als tuple zodat je de stijl kunt afstemmen op het type bericht
- **Bootstrap 5 integratie**: Bootstrap alert classes (`alert-success`, `alert-warning`, `alert-danger`, `alert-info`) koppelen aan de flash categorie voor automatische kleuropmaak via `alert-{{ category }}`
- **alert-dismissible**: Bootstrap klasse die samen met `.btn-close` een sluitknopje toevoegt waarmee de gebruiker een melding handmatig kan verwijderen
- **fade show**: Bootstrap klassen die een fade-animatie geven bij het sluiten van een alert
- **ARIA-attributen**: `role="alert"` en `aria-label="Close"` maken Bootstrap-alerts toegankelijk voor schermlezers
- **PRG-patroon met flash**: na een succesvolle formulierverwerking redirecten én een flash message toevoegen voorkomt dubbele submissions en geeft de gebruiker directe bevestiging
