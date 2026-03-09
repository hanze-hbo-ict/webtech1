# Flask en SQLAlchemy - Database Setup

Je maakt een database voor je Flask applicatie in drie stappen. Dit deel behandelt het opzetten van de database en het definiëren van een model.

## Project structuur

Voor de voorbeelden gebruik je drie Python bestanden:

- `basic_model_app.py` - Database configuratie en model definitie
- `setup_database.py` - Database aanmaken en eerste data toevoegen
- `basic_CRUD.py` - CRUD operaties uitvoeren (volgende deel)

## 1. Database configuratie (`basic_model_app.py`)

Bestudeer het volledige bestand [`basic_model_app.py`](bestanden/crud/basic_model_app.py).

### Imports

```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
```

De `os` module gebruik je om automatisch het juiste pad naar je database te bepalen.

### Basedir bepalen

```python
basedir = os.path.abspath(os.path.dirname(__file__))
```

Deze regel bepaalt waar je database bestand komt te staan:

1. `__file__` - Naam van het huidige Python bestand (`basic_model_app.py`)
2. `os.path.dirname(__file__)` - Directory waar dit bestand staat
3. `os.path.abspath()` - Volledig absoluut pad

Voorbeeld: `/Users/jouw-naam/IdeaProjects/Flask_database/basic_model_app.py`

Deze code werkt op Windows, macOS en Linux - het pad wordt automatisch correct bepaald.

### Flask app aanmaken

```python
app = Flask(__name__)
```

### Database configuratie

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

**Eerste regel**: Vertelt Flask waar de database bestand staat. De database wordt `data.sqlite` genoemd en staat in dezelfde directory als `basic_model_app.py`.

**Tweede regel**: Schakelt modification tracking uit. Deze feature is nuttig voor debugging, maar kost geheugen. Standaard staat het aan (`True`), daarom expliciet uitzetten.

### SQLAlchemy koppelen

```python
db = SQLAlchemy(app)
```

Dit object (`db`) gebruik je voor alle database operaties.

## Model definiëren

Een **model** is een Python class die een database tabel representeert. Je schrijft de class, SQLAlchemy maakt de tabel.

### Basis model

```python
class Cursist(db.Model):
    """Model voor cursisten van de muziekschool."""

    id: Mapped[int] = mapped_column(primary_key=True)
    naam: Mapped[str | None]
    leeftijd: Mapped[int | None]

    def __init__(self, naam: str, leeftijd: int):
        """Maak nieuwe cursist aan.

        Args:
            naam: Voor- en achternaam
            leeftijd: Leeftijd in jaren
        """
        self.naam = naam
        self.leeftijd = leeftijd

    def __repr__(self) -> str:
        """String representatie voor debugging."""
        return f"Cursist {self.naam} is {self.leeftijd} jaar oud."
```

**Class definitie**:

- Erft van `db.Model` - dit maakt het een SQLAlchemy model
- Standaard wordt de tabel ook `cursist` genoemd (kleine letter)

**Kolommen**:

- `id` - Integer, primary key (uniek nummer per cursist)
- `naam` - Text veld
- `leeftijd` - Integer

**Constructor**:

- Naam en leeftijd zijn verplicht bij aanmaken
- ID wordt automatisch gegenereerd

**`__repr__` methode**:

- Geeft leesbare tekst bij printen van objecten
- Handig bij debugging en queries

!!! tip "Custom tabelnaam"
    Wil je een andere tabelnaam dan de class naam? Voeg `__tablename__` toe:
    ```python
    class Cursist(db.Model):
        __tablename__ = 'cursisten'
        # ...
    ```

## 2. Database aanmaken (`setup_database.py`)

Bestudeer het volledige bestand [`setup_database.py`](bestanden/crud/setup_database.py).

Dit eenvoudige script maakt de database aan en voegt eerste data toe.

### Database aanmaken

```python
from basic_model_app import db, Cursist

# Maak database bestand en tabellen aan
db.create_all()
```

`db.create_all()` leest alle models en maakt de bijbehorende tabellen in de database. Het `data.sqlite` bestand wordt nu aangemaakt.

### Records toevoegen

```python
# Maak objecten aan
joyce = Cursist('Joyce', 36)
bram = Cursist('Bram', 24)

# Voeg toe aan database sessie
db.session.add_all([joyce, bram])

# Schrijf definitief naar database
db.session.commit()
```

**Stappen**:

1. Maak Python objecten aan
2. Voeg ze toe aan de database sessie met `add_all()`
3. Commit de sessie - nu worden ze écht opgeslagen

**Database sessie**: Verzamelt alle wijzigingen en schrijft ze in één keer weg. Dit is efficiënter dan elke toevoeging apart opslaan.

### ID's controleren

```python
print(joyce.id)  # 1
print(bram.id)   # 2
```

De ID's worden automatisch toegekend bij `commit()`.

Output:

```console
1
2
```

## Complete code overzicht

Je hebt nu:

1. **`basic_model_app.py`** - Database configuratie + Cursist model
2. **`setup_database.py`** - `db.create_all()` + initiële data

Wanneer je `setup_database.py` runt:

- Database bestand `data.sqlite` wordt aangemaakt
- Tabel `cursist` wordt aangemaakt met drie kolommen
- Twee records worden toegevoegd

**Volgende stap:** [Deel 3](flask-views-deel3.md) - CRUD operaties uitvoeren.

## Samenvatting

In deze les heb je geleerd:

- **Basedir bepalen**: met `os.path.abspath(os.path.dirname(__file__))` stel je platformonafhankelijk het absolute pad in van de map waarin je bestand staat.
- **Database-URI**: via `app.config['SQLALCHEMY_DATABASE_URI']` vertel je Flask waar het SQLite-bestand (`data.sqlite`) staat.
- **SQLALCHEMY_TRACK_MODIFICATIONS**: deze instelling schakel je expliciet uit (op `False`) om onnodig geheugengebruik te vermijden.
- **SQLAlchemy koppelen**: `db = SQLAlchemy(app)` maakt het `db`-object aan waarmee je alle database-operaties uitvoert.
- **Model definiëren**: een modelklasse erft van `db.Model`, gebruikt `Mapped` en `mapped_column` voor kolomdefinities, en bevat een `__init__`- en een `__repr__`-methode.
- **Tabelnaam aanpassen**: met het klasse-attribuut `__tablename__` geef je de databasetabel een andere naam dan de standaard (lowercase klassenaam).
- **Tabellen aanmaken**: `db.create_all()` leest alle models en maakt de bijbehorende tabellen aan in de database.
- **Records toevoegen**: met `db.session.add_all([...])` gevolgd door `db.session.commit()` voeg je meerdere objecten tegelijk toe en sla je ze definitief op.
- **Automatische ID's**: primaire sleutels worden pas toegewezen na `db.session.commit()`; daarna zijn ze als attribuut op het object beschikbaar.
