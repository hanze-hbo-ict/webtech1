# Flask Forms - Validators en Field Types

WTForms biedt veel verschillende veldtypen en validators. Validators controleren of de ingevoerde data correct is (bijvoorbeeld: verplicht veld, geldig email adres, minimum lengte).

## Validators

Validators voeg je toe als parameter aan een veld:

```python
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    naam = StringField('Naam', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bericht = StringField('Bericht', validators=[Length(min=10, max=500)])
```

**Veelgebruikte validators:**

- `DataRequired()` - Veld mag niet leeg zijn
- `Email()` - Moet geldig email adres zijn
- `Length(min=x, max=y)` - Lengte tussen min en max
- `NumberRange(min=x, max=y)` - Getal tussen min en max
- `EqualTo('veldnaam')` - Moet gelijk zijn aan ander veld (wachtwoord bevestiging)
- `URL()` - Moet geldige URL zijn
- `Regexp(regex)` - Moet aan regex pattern voldoen

## Field Types

WTForms ondersteunt alle HTML formulier velden:

- `StringField` - Tekst invoer
- `TextAreaField` - Grote tekst invoer (meerdere regels)
- `BooleanField` - Checkbox
- `RadioField` - Radio buttons (kies één optie)
- `SelectField` - Dropdown menu
- `IntegerField` - Geheel getal
- `FloatField` - Decimaal getal
- `PasswordField` - Wachtwoord (verborgen tekst)
- `SubmitField` - Submit button

## Uitgebreid voorbeeld

We maken een enquêteformulier voor de muziekschool. Project structuur:

```text
mijn-flask-app/
├── app.py
└── templates/
    ├── home.html
    └── bedankt.html
```

### Flask applicatie

**`app.py`:**

```python
from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    RadioField,
    SelectField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mijngeheimesleutel'


class EnqueteForm(FlaskForm):
    """Enquêteformulier voor muziekschool Session."""

    naam = StringField(
        'Wat is je naam?',
        validators=[DataRequired()]
    )
    vrouw = BooleanField('Ben je een vrouw?')
    instrument = RadioField(
        'Welk instrument wil je leren bespelen?',
        choices=[
            ('gitaar', 'Gitaar'),
            ('drums', 'Drums')
        ]
    )
    plaats = SelectField(
        'Welke locatie heeft de voorkeur?',
        choices=[
            ('assen', 'Assen'),
            ('drachten', 'Drachten'),
            ('groningen', 'Groningen')
        ]
    )
    feedback = TextAreaField('Nog andere opmerkingen?')
    submit = SubmitField('Verzend')


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """Homepage met enquête formulier.

    Returns:
        Gerenderde template met formulier
    """
    form = EnqueteForm()

    if form.validate_on_submit():
        # Sla data op in session
        session['naam'] = form.naam.data
        session['vrouw'] = form.vrouw.data
        session['instrument'] = form.instrument.data
        session['plaats'] = form.plaats.data
        session['feedback'] = form.feedback.data

        # Redirect naar bedankt pagina
        return redirect(url_for('bedankt'))

    return render_template('home.html', form=form)


@app.route('/bedankt')
def bedankt() -> str:
    """Bedankpagina met enquête resultaten.

    Returns:
        Gerenderde template met ingevulde data
    """
    return render_template('bedankt.html')


if __name__ == '__main__':
    app.run(debug=True)
```

**Code uitleg:**

- `RadioField(choices=[...])` - Elke choice is een tuple: `(waarde, weergave_tekst)`
- `SelectField(choices=[...])` - Dropdown met tuples
- `session['key'] = value` - Data opslaan in Flask session (tijdelijke opslag)
- `redirect(url_for('bedankt'))` - Navigeer naar andere route
- `DataRequired()` validator - Naam is verplicht

### Sessions

HTTP is **stateless** - elke request is los van de vorige. De server "vergeet" wat je eerder hebt gedaan. Dit is een probleem als je data tussen requests wilt bewaren (bijvoorbeeld formulier gegevens, inlog status, winkelmandje).

**Flask sessions** lossen dit op. Sessions zijn onderdeel van Flask (geen extra package nodig) en werken met **encrypted cookies** aan de client-side:

1. Je slaat data op in `session['key'] = value`
2. Flask versleutelt de data met je `SECRET_KEY`
3. Dit wordt als cookie naar de browser gestuurd
4. Bij volgende requests stuurt de browser de cookie mee
5. Flask ontsleutelt de data en maakt hem beschikbaar via `session['key']`

**Voorbeeldcode:**

```python
from flask import session

# Opslaan in session
session['naam'] = 'Joyce'
session['email'] = 'joyce@example.com'

# Ophalen uit session (in deze of andere route)
naam = session['naam']

# Ook beschikbaar in templates
# {{ session['naam'] }}
```

**Belangrijke punten:**

- Sessions zijn **versleuteld** met je `SECRET_KEY` - zonder geldige key kan niemand de data lezen of aanpassen
- Sessions zijn **tijdelijk** - standaard tot de browser sluit (of na ingestelde timeout)
- Sessions bewaren **kleine hoeveelheden data** - voor grote data gebruik je een database
- Sessions zijn **client-side** - de data zit in de browser cookie, niet op de server

### Templates

**`templates/home.html`:**

```html
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Enquête - Muziekschool Session</title>
</head>
<body>
    <h1>Welkom bij de enquête van muziekschool Session</h1>

    <form method="POST">
        {{ form.hidden_tag() }}

        <div>
            {{ form.naam.label }}<br>
            {{ form.naam }}
        </div>

        <div>
            {{ form.vrouw.label }}
            {{ form.vrouw }}
        </div>

        <div>
            {{ form.instrument.label }}<br>
            {{ form.instrument }}
        </div>

        <div>
            {{ form.plaats.label }}<br>
            {{ form.plaats }}
        </div>

        <div>
            {{ form.feedback.label }}<br>
            {{ form.feedback }}
        </div>

        <div>
            {{ form.submit() }}
        </div>
    </form>
</body>
</html>
```

**`templates/bedankt.html`:**

```html
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Bedankt</title>
</head>
<body>
    <h1>Bedankt voor de moeite!</h1>
    <h2>Dit zijn de ingevulde gegevens:</h2>

    <ul>
        <li>Naam: {{ session['naam'] }}</li>
        <li>Vrouw: {{ session['vrouw'] }}</li>
        <li>Instrument: {{ session['instrument'] }}</li>
        <li>Plaats: {{ session['plaats'] }}</li>
        <li>Feedback: {{ session['feedback'] }}</li>
    </ul>

    <a href="/">Nieuwe enquête</a>
</body>
</html>
```

### Testen

Start de applicatie:

```console
uv run python app.py
```

Navigeer naar `http://127.0.0.1:5000/`:

> **Verwacht resultaat:** Je ziet het enquêteformulier met de velden: een tekstveld voor de naam, een checkbox "Ben je een vrouw?", radio buttons voor het instrument (Gitaar of Drums), een dropdown voor de locatie (Assen, Drachten, Groningen), een tekstgebied voor opmerkingen en een knop "Verzend".

Vul het formulier in:

> **Verwacht resultaat:** Het formulier is volledig ingevuld met voorbeeldgegevens: een naam in het tekstveld, de checkbox aangevinkt, een instrument geselecteerd, een locatie gekozen en tekst ingevoerd in het feedbackveld.

Klik Verzend - je wordt doorgestuurd naar `/bedankt`:

> **Verwacht resultaat:** De bedankpagina toont de koptekst "Bedankt voor de moeite!" gevolgd door een lijst met de ingediende gegevens: naam, vrouw (true/false), instrument, locatie en feedback.

## Validators in actie

Probeer het formulier te verzenden **zonder naam** in te vullen:

> **Verwacht resultaat:** Het formulier wordt opnieuw getoond met een rood kader rond het naamveld, wat aangeeft dat dit verplichte veld niet ingevuld is; de overige velden behouden hun eerder geselecteerde waarden.

Een rood kader verschijnt rond het naam veld - de `DataRequired()` validator blokkeert het verzenden.

## RadioField en SelectField choices

Let op de tuple structuur:

```python
choices=[
    ('waarde_in_code', 'Tekst voor gebruiker'),
    ('assen', 'Assen'),  # 'assen' wordt opgeslagen, 'Assen' wordt getoond
    ('dr', 'Drachten'),  # 'dr' wordt opgeslagen, 'Drachten' wordt getoond
]
```

Als je "Drachten" selecteert, wordt `'dr'` opgeslagen in `form.plaats.data`.

Om de volledige naam op te slaan, gebruik dezelfde waarde twee keer:

```python
choices=[
    ('Assen', 'Assen'),
    ('Drachten', 'Drachten'),
]
```

## Type hints voor validators

```python
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    """Contact formulier met validators."""

    naam: StringField = StringField(
        'Naam',
        validators=[DataRequired()]
    )
    email: StringField = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
```

## Redirect pattern

Het redirect-after-POST pattern voorkomt dubbele form submissions:

```python
if form.validate_on_submit():
    # Verwerk data
    session['data'] = form.data

    # Redirect naar andere pagina (PRG pattern: Post-Redirect-Get)
    return redirect(url_for('bedankt'))

# GET request: toon formulier
return render_template('form.html', form=form)
```

Als je na POST de template direct returnt, kan de gebruiker de pagina refreshen en het formulier opnieuw verzenden. Met redirect gaat de browser naar een GET request.

**Volgende stap:** [Deel 3](flask-forms-deel3.md) - Flash messages.

## Samenvatting

In deze les heb je geleerd:

- **Validators**: invoercontroles die je als lijst meegeeft aan een veld, zoals `DataRequired()`, `Email()`, `Length(min, max)`, `EqualTo()` en `URL()`
- **Field types**: WTForms biedt velden voor elk HTML-invoertype, waaronder `StringField`, `BooleanField`, `RadioField`, `SelectField`, `TextAreaField` en `PasswordField`
- **RadioField en SelectField**: keuzevelden waarbij elke optie een tuple is van `(opgeslagen_waarde, weergave_tekst)`; de opgeslagen waarde is beschikbaar via `form.veld.data`
- **Flask sessions**: tijdelijke opslag van data tussen requests via versleutelde client-side cookies; opslaan met `session['key'] = value` en uitlezen in templates via `{{ session['key'] }}`
- **Sessions en SECRET_KEY**: session data wordt versleuteld met de `SECRET_KEY`; zonder geldige sleutel kan niemand de data lezen of aanpassen
- **redirect en url_for**: na een POST-verzoek door sturen naar een andere route zodat de browser een GET-request uitvoert
- **Post-Redirect-Get patroon**: na het verwerken van een formulier altijd redirecten om dubbele form submissions bij een pagina-refresh te voorkomen
- **Validator feedback**: wanneer een verplicht veld leeg blijft blokkeert Flask-WTF het verzenden en toont de browser het formulier opnieuw met een foutindicatie
