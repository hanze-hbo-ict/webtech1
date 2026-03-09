# Flask Forms - Oefening 1

Bouw een naam invoerformulier met validators, sessions en flash messages.

## Doel

Je maakt een formulier waarbij gebruikers hun voor- en achternaam kunnen invoeren. Na het verzenden worden de gegevens opgeslagen in een session en wordt een flash message getoond met de volledige naam.

## Setup

Maak een nieuw Flask project:

```console
mkdir flask-forms-oefening1
cd flask-forms-oefening1
uv init
uv add flask flask-wtf
mkdir templates
```

## Opdracht

Implementeer de volgende functionaliteit:

1. **Formulier met twee StringFields:**
   - Voornaam (verplicht veld met `DataRequired()` validator)
   - Achternaam (verplicht veld met `DataRequired()`)

2. **Session opslag:**
   - Sla voornaam en achternaam op in session na verzenden

3. **Flash message:**
   - Toon een success flash message met de volledige naam
   - Formaat: "Welkom, [voornaam] [achternaam]!"

4. **Bootstrap styling:**
   - Gebruik Bootstrap 5 voor de template
   - Gebruik Bootstrap form classes (`form-control`, `form-label`, etc.)
   - Toon flash message met `alert-success` class

## Starter code

**`app.py`:**

```python
from flask import Flask, render_template, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mijngeheimesleutel'


class NaamForm(FlaskForm):
    """Formulier voor voor- en achternaam."""

    # TODO: Voeg voornaam StringField toe met label 'Voornaam'
    # TODO: Voeg DataRequired() validator toe aan voornaam

    # TODO: Voeg achternaam StringField toe met label 'Achternaam'
    # TODO: Voeg DataRequired() validator toe aan achternaam

    # TODO: Voeg SubmitField toe met tekst 'Verzend'
    pass


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """Homepage met naam formulier.

    Returns:
        Gerenderde template met formulier en flash messages
    """
    # TODO: Maak een instantie van NaamForm aan

    # TODO: Check of formulier valid is en verzonden met validate_on_submit()
    # TODO: Sla voornaam op in session['voornaam']
    # TODO: Sla achternaam op in session['achternaam']

    # TODO: Maak een volledige_naam variabele met voornaam + spatie + achternaam

    # TODO: Flash een success message met tekst: f'Welkom, {volledige_naam}!'
    # TODO: Gebruik 'success' als categorie

    # TODO: Redirect naar 'index' route

    # TODO: Return render_template voor 'home.html' met form=form
    pass


if __name__ == '__main__':
    app.run(debug=True)
```

**`templates/home.html`:**

```html
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Naam Formulier - Oefening 1</title>

    <!-- TODO: Voeg Bootstrap 5 CSS link toe -->
    <!-- Gebruik: https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css -->
</head>
<body>
    <div class="container mt-5">
        <h1>Naam Formulier</h1>

        <!-- TODO: Loop door get_flashed_messages(with_categories=true) -->
        <!-- TODO: Toon elke message in een Bootstrap alert met class alert-{{ category }} -->
        <!-- TODO: Voeg alert-dismissible fade show classes toe -->
        <!-- TODO: Voeg close button toe met class btn-close -->

        <!-- Formulier -->
        <form method="POST">
            <!--TODO: Voeg form.hidden_tag() toe voor CSRF protection -->

            <!-- TODO: Voeg div met class mb-3 toe -->
            <!-- TODO: Toon form.voornaam.label met class form-label -->
            <!-- TODO: Toon form.voornaam met class form-control -->

            <!-- TODO: Voeg div met class mb-3 toe -->
            <!-- TODO: Toon form.achternaam.label met class form-label -->
            <!-- TODO: Toon form.achternaam met class form-control -->

            <!-- TODO: Toon form.submit met class btn btn-primary -->
        </form>
    </div>

    <!-- TODO: Voeg Bootstrap 5 JavaScript toe -->
    <!-- Gebruik: https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js -->
</body>
</html>
```

## Testen

Start de applicatie:

```console
uv run python app.py
```

### Test scenario's

1. **Zonder invullen verzenden:**
   - Beide velden moeten validation errors tonen
   - Formulier mag niet verzonden worden

2. **Alleen voornaam invullen:**
   - Achternaam veld moet validation error tonen
   - Formulier mag niet verzonden worden

3. **Beide velden invullen:**
   - Flash message moet verschijnen: "Welkom, [voornaam] [achternaam]!"
   - Message moet groen zijn (success)
   - Message moet sluitbaar zijn met X knop

## Verwachte output

**Leeg formulier:**

- Twee invoervelden (voornaam, achternaam)
- Een verzend knop
- Geen flash messages zichtbaar

**Validation error bij leeg formulier:**

- Rode rand om lege verplichte velden
- Formulier wordt niet verzonden
- Blijft op dezelfde pagina

**Success message na invullen:**

- Groene flash message bovenaan: "Welkom, [voornaam] [achternaam]!"
- Message is sluitbaar met X knop
- Formulier velden zijn leeg (na redirect)

## Bonus opdrachten

### Bonus 1: Email veld toevoegen

Voeg een email veld toe met `Email()` validator:

```python
from wtforms.validators import DataRequired, Email

class NaamForm(FlaskForm):
    voornaam = StringField('Voornaam', validators=[DataRequired()])
    achternaam = StringField('Achternaam', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Verzend')
```

Toon email in flash message: "Welkom, [naam]! Bevestiging gestuurd naar [email]"

### Bonus 2: Bedankpagina

Maak een aparte `/bedankt` route die de session data toont:

```python
@app.route('/bedankt')
def bedankt() -> str:
    """Bedankpagina met session data."""
    # TODO: Implementeer bedankt route
    # TODO: Maak bedankt.html template
    # TODO: Toon voornaam, achternaam uit session
    pass
```

Redirect naar `/bedankt` na formulier verzenden in plaats van terug naar index.

### Bonus 3: Multiple flash messages

Toon meerdere flash messages met verschillende categorieën:

```python
if form.validate_on_submit():
    flash(f'Welkom, {volledige_naam}!', 'success')
    flash('Je gegevens zijn veilig opgeslagen', 'info')
    flash('Controleer je inbox voor een bevestigingsmail', 'warning')
    return redirect(url_for('index'))
```

### Bonus 4: Form reset

Reset het formulier na verzenden door velden leeg te maken:

```python
if form.validate_on_submit():
    # Sla data op
    session['voornaam'] = form.voornaam.data
    session['achternaam'] = form.achternaam.data

    # Flash message
    flash(f'Welkom, {volledige_naam}!', 'success')

    # Reset formulier velden
    form.voornaam.data = ''
    form.achternaam.data = ''

    # Geen redirect - blijf op zelfde pagina
    return render_template('home.html', form=form)
```

## Tips

- Vergeet `{{ form.hidden_tag() }}` niet - zonder CSRF token krijg je een error
- Bootstrap classes zijn optioneel maar maken het formulier mooier
- Test altijd validators door velden leeg te laten
- Gebruik `with_categories=true` in `get_flashed_messages()` voor gekleurde alerts

## Veelvoorkomende fouten

**"CSRF token missing"**

- Oplossing: Voeg `{{ form.hidden_tag() }}` toe in het formulier

**Flash message verschijnt niet**

- Check of je `flash()` aanroept vóór de redirect
- Check of `get_flashed_messages()` in de template staat

**Validators werken niet**

- Check of `DataRequired()` in de validators list staat
- Check of je `form.validate_on_submit()` gebruikt

**Bootstrap styling werkt niet**

- Check of Bootstrap CSS en JS links correct zijn
- Check of `integrity` en `crossorigin` attributen aanwezig zijn
