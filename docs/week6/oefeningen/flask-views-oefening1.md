# Flask en SQLAlchemy - Oefening 1: Mentor Platform

Je bouwt een platform voor de Hanzehogeschool waar studenten aan mentoren gekoppeld worden. Je combineert:

- [Database relaties](../flask-views-deel4.md) (één-op-veel)
- [Complete Flask website](../flask-views-deel5.md) (routes, forms, templates)

## Opdracht

Maak een beheersysteem waarin docenten en studenten toegevoegd en verwijderd kunnen worden, en waar de mentor-relaties zichtbaar zijn.

> **Verwacht resultaat:** Een homepage met Bootstrap navigatiebalk bovenaan met links naar alle secties (Home, Voeg docent toe, Voeg student toe, Toon overzicht, Verwijder). De pagina toont een welkomsttekst met een uitnodiging om een item uit de navigatiebalk te selecteren.

## Requirements

### Database structuur

Twee modellen met een relatie:

**Docent**:

- `id` (primary key)
- `naam`

**Student**:

- `id` (primary key)
- `naam`
- `mentor_id` (foreign key naar Docent)

**Relatie**: Eén docent kan mentor zijn van meerdere studenten (één-op-veel).

### Functionaliteit

De website moet deze acties ondersteunen:

1. **Docent toevoegen** - Formulier met naam
2. **Student toevoegen** - Formulier met naam + docent ID
3. **Overzicht tonen** - Lijst van studenten met hun mentor
4. **Docent verwijderen** - Formulier met ID
5. **Student verwijderen** - Formulier met ID

!!! tip "Flash messages"
    Toon een flash message na elke toevoeging (bijvoorbeeld: "Student toegevoegd!").

### Navigatie

Navigatiebalk met vijf links:

- Home
- Voeg docent toe
- Voeg student toe
- Toon overzicht
- Verwijder (docent of student)

## Bestandsstructuur

Maak deze bestanden:

**Python**:

- `mentor_site.py` - Hoofd applicatie
- `forms.py` - Drie formulieren

**Templates**:

- `base.html` - Basis template met navigatie
- `home.html` - Homepage
- `voeg_docent_toe.html`
- `voeg_student_toe.html`
- `overzicht.html` - Studenten met mentor
- `verwijder.html` (of twee aparte templates)

## Hints

### Models

```python
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Docent(db.Model):
    __tablename__ = 'docenten'

    id: Mapped[int] = mapped_column(primary_key=True)
    naam: Mapped[str | None]

    # Relatie naar studenten
    studenten: Mapped[list['Student']] = relationship(back_populates='mentor')
```

De `back_populates='mentor'` koppelt aan `mentor: Mapped['Docent | None'] = relationship(back_populates='studenten')` in het `Student` model. Via `student.mentor` krijg je het Docent object.

### Student formulier

Voor het student formulier heb je een `IntegerField` nodig voor de mentor ID:

```python
from wtforms import StringField, IntegerField, SubmitField

class VoegStudentToeForm(FlaskForm):
    naam = StringField('Naam student:')
    mentor_id = IntegerField('ID van mentor:')
    submit = SubmitField('Voeg toe')
```

### Flash messages

In je route:

```python
from flask import flash

if form.validate_on_submit():
    # ... voeg student toe ...
    flash('Student toegevoegd!')
    return redirect(url_for('overzicht'))
```

In `base.html` (na navigatie):

```html
<div class="container mt-4">
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-success">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    {% block content %}
    {% endblock %}
</div>
```

### Overzicht template

Gebruik een for-loop om alle studenten te tonen met hun mentor:

```html
<ul class="list-group">
    {% for student in studenten %}
        <li class="list-group-item">
            {{ student.naam }} - Mentor: {{ student.mentor.naam }}
        </li>
    {% endfor %}
</ul>
```

## Aandachtspunten

- **Naamgeving**: Let op typo's in variabelen en template namen
- **Foreign keys**: Gebruik `ForeignKey('docenten.id')` (tabelnaam, niet class naam)
- **back_populates**: Via `student.mentor` krijg je het Docent object
- **Bootstrap 5**: Gebruik moderne Bootstrap classes

## Uitbreidingen (optioneel)

1. **Validatie**: Check of mentor ID bestaat voordat je student toevoegt
2. **Edit functie**: Wijs student aan andere mentor toe
3. **Docent overzicht**: Toon per docent alle studenten
4. **Error handling**: Wat als je een non-existent ID probeert te verwijderen?

## Test je applicatie

1. Start met een lege database
2. Voeg twee docenten toe (krijgen ID 1 en 2)
3. Voeg drie studenten toe met verschillende mentoren
4. Check overzicht - zie je de juiste mentor per student?
5. Verwijder een student
6. Check of de database klopt met DB Browser

Veel succes!
