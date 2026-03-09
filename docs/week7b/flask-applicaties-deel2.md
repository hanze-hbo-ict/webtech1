# Flask-applicaties - Refactored

Aan het einde van de vorige paragraaf is de algemene structuur voor de applicatie waarmee het overzicht van de docenten die als mentor fungeren samen met de door hen begeleide studenten vastgelegd. Nu is het tijd om deze te implementeren.

Omdat al veel van de code geschreven en besproken is in voorgaande delen, wordt hier grotendeels het principe copy en paste gehanteerd.

`Flask` heeft een ingebouwde mogelijkheid waarmee de modulaire componenten voor de Flask-app geregistreerd kunnen worden: [*blueprints*](https://flask.palletsprojects.com/en/1.1.x/blueprints/). Hiermee kan op een eenvoudige wijze een *view* geraadpleegd worden voor ieder aspect van de applicatie.

Zo zijn er bijvoorbeeld een tweetal `view.py`-bestanden: één voor docenten en één voor studenten. En elk van deze *views* heeft zijn eigen `add`-view. Om ervoor te zorgen dat de Flask-applicatie niet in de war raakt door een `/add`-route, maken we gebruik van blueprints. De blueprints registreren een `url_prefix` voor elk `views.py`-bestand:

- `/docenten/add`
- `/studenten/add`

De voornaamste wijzigingen in de code zullen zijn:

- Herstructurering van de projectmappen
- Het toevoegen van blueprints
- Het registreren van de blueprints  `__init__.py`

Nogmaals, in dit deel ligt de nadruk in het opzetten van een algemene structuur voor een applicatie. Daarom wordt er geen nieuwe applicatie vanaf scratch ontwikkeld maar wordt de inhoud van de vorige web-applicatie voornamelijk gekopieerd.

## Stap 1: Het aanmaken van de structuur van de folderset

Het aanmaken van de structuur zal in gedeelten besproken worden, zodat nog een keer duidelijk wordt hoe het opzetten van een uitgebreide applicatie het beste kan geschieden.

```text
.
├── mijnproject
│   ├── docenten
│   ├── studenten
│   ├── templates
│   ├── __init__.py
│   └── models.py
└── app.py
```

Om alles uit elkaar te kunnen houden hebben we een nieuw project aangemaakt met de naam 'Refactor'. Binnen het project zijn op het hoogste niveau een tweetal zaken nodig: een folder waarin de items van de applicatie worden ondergebracht, hier `mijnproject` en een Python-file, hier `app.py` genaamd. Deze file importeert enkele items en kent verder alleen een verwijzing naar de pagina `home.html`. Deze file wordt als allerlaatste gecodeerd.

De folder `templates` bevat een tweetal HTML-bestanden. Allereerst het bestand `base.html` met de links naar Bootstrap, de titel, de navigatiebalk en een leeg blok. Het andere bestand, `home.html` bevat de inhoud van de homepagina.

In `__init__.py` worden weer de bekende aspecten van flask geïmporteerd, de database aangemaakt, de basisdirectory bepaald en de koppeling tussen applicatie en database ingesteld. Later worden hier nog de blueprints aan toegevoegd.

In `models.py` wordt de structuur van de database bepaald, zoals al een aantal keren aan bod is geweest.

De structuur van de folder `mijnproject` is dan als volgt:

```text
.
├── mijnproject
│   ├── docenten
│   │   ├── templates
│   │   │   └── docenten
│   │   ├── forms.py
│   │   └── views.py
│   ├── studenten
│   │   ├── templates
│   │   │   └── studenten
│   │   ├── forms.py
│   │   └── views.py
│   ├── templates
│   ├── __init__.py
│   └── models.py
└── app.py
```

Voor zowel de docenten als de studenten wordt een eigen directory ingericht. Hierin kunnen de onderdelen worden opgenomen die van toepassing zijn voor de verschillende onderwerpen. Voor beide directories zijn formulieren, views en templates ontwikkeld die nu keurig van elkaar gescheiden worden ondergebracht in de applicatie. Voor beide domeinen (docenten en studenten) is een eigen folder gereserveerd waarin de specifieke HTML-bestanden voor ieder doel komen te staan.

## Stap 2: Het toevoegen van de pagina’s die al ontwikkeld zijn

De code van de diverse pagina’s zal nog een keer getoond worden zonder al te veel commentaar erbij.

### `models.py`

Als eerste `models.py`:

```python
# from mijnproject import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Docent(db.Model):
    """
    Model voor docenten die als mentor fungeren.

    Attributes:
        id: Unieke identifier voor de docent
        naam: Naam van de docent
        student: Relatie naar de Student die deze docent begeleidt
    """

    __tablename__ = 'docenten'
    id: Mapped[int] = mapped_column(primary_key=True)
    naam: Mapped[str | None]
    student: Mapped['Student | None'] = relationship(back_populates='docent')

    def __init__(self, naam: str) -> None:
        """
        Initialiseer een nieuwe docent.

        Args:
            naam: De naam van de docent
        """
        self.naam = naam

    def __repr__(self) -> str:
        """
        Geef een tekstuele representatie van de docent.

        Returns:
            String met docent naam en eventuele student
        """
        if self.student:
            return f"Docent {self.naam} is mentor van {self.student.naam}"
        else:
            return f"Docent {self.naam} heeft geen studenten als mentor te begeleiden."


class Student(db.Model):
    """
    Model voor studenten die door een mentor worden begeleid.

    Attributes:
        id: Unieke identifier voor de student
        naam: Naam van de student
        docent_id: Foreign key naar de begeleidende docent
    """

    __tablename__ = 'studenten'

    id: Mapped[int] = mapped_column(primary_key=True)
    naam: Mapped[str | None]
    docent_id: Mapped[int | None] = mapped_column(ForeignKey('docenten.id'))
    docent: Mapped['Docent | None'] = relationship(back_populates='student')

    def __init__(self, naam: str, docent_id: int) -> None:
        """
        Initialiseer een nieuwe student.

        Args:
            naam: De naam van de student
            docent_id: Het ID van de begeleidende docent
        """
        self.naam = naam
        self.docent_id = docent_id

    def __repr__(self) -> str:
        """
        Geef een tekstuele representatie van de student.

        Returns:
            String met de naam van de student
        """
        return f"Deze student heet {self.naam}"
```

Uit het bestand `mentor_site.py` zijn de klassen `Docent` en `Student` overgenomen. Punt van aandacht is nog wel dat er nog een koppeling gemaakt moet worden naar de plek waar db wordt aangemaakt. Dat zal gebeuren in het bestand `__init__.py`. Het is alvast opgenomen als commentaarregel.
Als tweede wordt de folder templates gevuld met de bestanden `base.html` en `home.html`.

### `base.html`

```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

<title>Mentoraat</title>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-light bg-light">

    <div class="navbar-nav">
        <a class="nav-item nav-link" href="{{ url_for('index') }}">Home</a>
        <a class="nav-item nav-link" href="{{ url_for('add_doc') }}">Voeg docent toe</a>
        <a class="nav-item nav-link" href="{{ url_for('list_doc') }}"> Toon mentoren</a>
        <a class="nav-item nav-link" href="{{ url_for('del_doc') }}">Verwijder docent Pup</a>
        <a class="nav-item nav-link" href="{{ url_for('add_stu') }}">Voeg student toe</a>
    </div>

</nav>

{% block content %}

{% endblock %}
</body>
</html>
```

Deze code zorgt voor het tweede aandachtspunt: de URL’s zullen aangepast moeten worden, omdat ze nu naar verschillende directories verwijzen. Dat is ook één van de laatste aanpassingen die geregeld moeten worden.

### `home.html`

```html hl_lines="4"
{% extends "base.html" %}
{% block content %}
<div class="jumbotron">
    <h1>Overzicht mentoraat</h1>
    <p>Selecteer om te beginnen een item uit de navigatiebalk.</p>
</div>
{% endblock %}
```

Als enige is de tekst `<h1>` bijgesteld.

`__init__.py`

```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mijngeheimesleutel'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
```

Ook hierbij is een gedeelte overgenomen uit het bestand `mentor_site.py` van de oefening. Maar het is niet integraal overgenomen: er is een aantal regels weggelaten. De reden daarvoor is dat deze file geen code bevat die nodig is om views aan te maken. Dat wordt straks geregeld is de daarvoor beschikbare folders: `docenten` en `studenten`.

Bovendien dienen er nog een aantal registraties voor de blueprints aan de code te worden toegevoegd. Dat is het derde aandachtspunt voor de volgende paragraaf.

Alleen de gegevens die van toepassing zijn op docenten worden overgenomen uit `forms.py`. De namen van de formulieren zijn aangepast zodat het een meer gangbaar karakter krijgt. Bovendien kan nu steeds dezelfde naam gebruikt worden omdat de formulieren in verschillende directories zijn ondergebracht. Voor toevoegen wordt nu `Add` gebruikt, voor verwijderen `Del`.

### `forms.py` uit de folder `docenten`

```python
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddForm(FlaskForm):
    """Formulier voor het toevoegen van een nieuwe docent."""

    naam = StringField('Naam docent:')
    submit = SubmitField('Voeg toe')


class DelForm(FlaskForm):
    """Formulier voor het verwijderen van een docent."""

    id = IntegerField('Vul het ID in van de docent die verwijderd gaat worden:')
    submit = SubmitField('Verwijder')
```

### `forms.py` uit de folder `studenten`

```python
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddForm(FlaskForm):
    """Formulier voor het toevoegen van een nieuwe student."""

    naam = StringField('Naam student:')
    doc_id = IntegerField("Id van de docent: ")
    submit = SubmitField('Voeg toe')
```

De formulieren zijn uit elkaar gehaald en in een passende folder ingevoegd. Beiden hebben nu een formulier met de naam `AddForm`. Dat gaat helemaal goed, omdat later met blueprints de juiste relaties gelegd zullen worden, zodat er geen verwarring kan ontstaan en de verkeerde formulieren getoond gaan worden.

De nog resterende HTML-files kunnen nu op de juiste plaats gezet worden. Als eerste moeten er drie bestanden in de folder `templates/docenten` aangemaakt worden: `add.html`, `delete.html` en `list.html`. De namen van de oefening worden vervangen door wat meer algemeen geldige namen.

### `add.html`

```html
{% extends "base.html" %}
{% block content %}
<div class="jumbotron">
    <h1>Heeft zich een docent als kandidaat mentor gemeld?</h1>
    <p>Vul de naam in en klik op 'Voeg toe':</p>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.naam.label }} {{ form.naam() }}
        {{ form.submit() }}
    </form>
</div>
{% endblock %}
```

De code is overgenomen uit `voegtoe_docent.html`.

### `delete.html`

```html
{% extends "base.html" %}
{% block content %}
<div class="jumbotron">
    <h1>Een docent afmelden als mentor?</h1>
    <p>Vul het ID in en klik op 'Verwijder'.</p>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.id.label }} {{ form.id() }}
        {{ form.submit() }}
    </form>
</div>
{% endblock %}
```

Deze code komt uit `verwijder_docent.html`

`list.html`

```html
{% extends "base.html" %}
{% block content %}
<div class="jumbotron">
    <h1>Een overzicht van de mentoren en hun studenten.</h1>
    <ul>
        {% for doc in docenten  %}
        <li>{{doc}}</li>
        {% endfor %}
    </ul>

</div>
{% endblock %}
```

En deze code is integraal gekopieerd van `mentor_overzicht.html`

Als laatste is er nog een view nodig om nieuwe studenten in de database te kunnen opnemen. Ook hier wordt gebruik gemaakt van een naam die al eerder gebruikt is: `add.html`. Omdat alle code in aparte folders is ondergebracht is het geen probleem bij de uitvoering van het programma.

### `add.html` (studenten toevoegen)

```html
{% extends "base.html" %}
{% block content %}
<div class="jumbotron">
    <h1>Voeg een student in</h1>
    <p>Voeg tevens het ID van de mentor toe en klik op 'Voeg toe':</p>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.naam.label }} {{ form.naam() }}<br>
        {{ form.doc_id.label }} {{ form.doc_id() }}<br>
        {{ form.submit() }}
    </form>
</div>
{% endblock %}
```

Deze code is overgenomen uit `voegtoe_student.html`.

## Conclusie

De inspanningen in deze paragraaf hebben ertoe geleid dat de structuur die ontworpen is ook daadwerkelijk is aangemaakt. Grote delen van de code van de uitwerking van de oefenopdracht website zijn al op de juiste plaats neergezet.

Er zijn nog een paar aandachtspunten overgebleven waar in de volgende paragraaf een vervolg aan moet worden gegeven.

Bovendien worden er de nodige blueprints in de code opgenomen. Tot slot van deze paragraaf een complete directory-listing na onze majeure refactoring:

```text
.
├── mijnproject
│   ├── docenten
│   │   ├── templates
│   │   │   └── docenten
│   │   │       ├── add.html
│   │   │       ├── delete.html
│   │   │       └── list.html
│   │   ├── forms.py
│   │   └── views.py
│   ├── studenten
│   │   ├── templates
│   │   │   └── studenten
│   │   │       └── add.html
│   │   ├── forms.py
│   │   └── views.py
│   ├── templates
│   │   ├── base.html
│   │   └── home.html
│   ├── __init__.py
│   └── models.py
└── app.py
```

## Samenvatting

In deze les heb je geleerd:

- **Mappenstructuur aanmaken**: de volledige directory-boom wordt stapsgewijs opgezet met mijnproject/, docenten/, studenten/, templates/ en de benodigde Python-bestanden
- **`models.py`**: bevat de SQLAlchemy-modellen Docent en Student met typed mapped columns en een één-op-één relatie; de db-koppeling wordt later gelegd via `__init__.py`
- **`__init__.py`**: initialiseert de Flask-app, configureert de SQLite-database en Flask-Migrate; bevat bewust geen routes, want die worden per subcomponent in eigen views.py-bestanden ondergebracht
- **`forms.py` per module**: elke module (docenten, studenten) heeft een eigen forms.py met een AddForm; dezelfde klassenaam kan hergebruikt worden doordat de bestanden in aparte directories staan
- **HTML-templates**: base.html en home.html op projectniveau; add.html, delete.html en list.html voor docenten; add.html voor studenten, elk geplaatst in een bijbehorende submap
- **Copy-paste-strategie**: bestaande code van de vorige oefenopdracht wordt grotendeels overgenomen en op de juiste locatie in de nieuwe structuur gezet, zonder inhoudelijke wijzigingen
- **Openstaande aandachtspunten**: blueprints moeten nog worden toegevoegd en de url_for()-links in de navigatiebalk moeten worden bijgewerkt naar de nieuwe structuur
