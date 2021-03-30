# Flask en SQL - het opzetten van een database

In totaal worden een drietal Python-files aangemaakt bij de demonstratie hoe een database aan een Flask-applicatie gekoppeld kan worden.

## 1. `basic_model_app.py`

Beatudeer het bestand [`basic_model_app.py`](../bestanden/crud/basic_model_app.py). De eerste stap bij het opzetten van een database in een Python-file is uiteraard het importeren van de benodigde pakketten en klassen:

```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
```

De middelste coderegel is bekend, en de onderste regel zorgt ervoor dat het pakket SQLAlchemy beschikbaar komt bij het runnen van de file. Het nut van de bovenste regel komt zo ter sprake.

De volgende actie is om het programma te vertellen wat de basis-directory is. Normaal gesproken zou een gebruiker dat zelf moeten opgeven, maar doordat `os` geïmporteerd is, kan dat geheel automatisch geregeld worden:

```python
basedir = os.path.abspath(os.path.dirname(__file__)
```

Er gebeurt hier het volgende:

Er wordt achteraan begonnen. Op de plaats van `__file__` wordt bij het runnen de naam van de Python-file ingevuld, hier wordt dat dan `BasisModelApp.py`.

`(os.path.dirname(__file__)` gaat op zoek naar de plek waar `basic_model_app.py` te vinden is. Dat zou hier zoiets zijn als `IdeaProjects/Flask_database/basic_model_app.py`.

De call naar `os.path.abpath()` levert het gehele pad op. In dit geval wordt het dus `/Users/tath/IdeaProjects/Flask_database/basic_model_app.py`.
Zoals gezegd, deze regel hoeft één keer aangemaakt te worden en kan veel vaker gebruikt worden. Het maakt ook niet uit of het gaat om een Windows-machine, een Mac OS of een Linux, het pad staat vast.
En op die plek wordt de database gebouwd.

Vervolgens wordt de applicatie aangemaakt:

```python
app = Flask(__name__)
```

#### Connectie tussen python en de database

Hierna moet de connectie gelegd worden tussen de Flask-applicatie en de database (let op: deze regels kunnen wat lang zijn, dus je moet misschien even een beetje naar rechts scrollen):

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

De bovenste regel is een *must*, en is vergelijkbaar met de noodzaak een geheime sleutel op te voeren wanneer Flask gekoppeld is aan een formulier. De kern van deze regel is dat hier de applicatie verteld wordt waar de database gevonden kan worden.
In de opgegeven basis-directory wordt dan gezocht naar de file `data.sqlite`.

De tweede regel geeft aan dat in dit geval geen modificaties gewenst zijn. Niet iedere aanpassing hoeft uitgebreid getoond te worden. De default-waarde in ingesteld op `True`, vandaar deze extra regel.

Deze laatste regel koppelt database en applicatie:

```python
db = SQLAlchemy(app)
```

De laatst besproken vier (4) coderegels (`app = Flask(__name__)` telt niet mee) zorgen ervoor dat de SQL-database wordt aangemaakt waarbij uitsluitend coderegels gebruikt worden en geen SQL-statements.

#### Model

Nu kan het *Model* aangemaakt worden. Daarvoor dient een klasse gecreëerd te worden. Model klinkt indrukwekkend, maar het is niets meer dan een representatie van een tabel in de database.
De eerste tabel krijgt de naam ‘Cursist’ mee:

```python
class Cursist(db.Model):
```

De applicatie is gekoppeld aan de database db die nu in elk geval al kan beschikken over een Model-klasse. Zonder tegenspraak wordt de naam van de klasse ook vastgelegd als naam van de tabel. Is er een andere naam gewenst, bijvoorbeeld *cursisten* dan kan dat aangepast worden.

```python
class Cursist(db.Model):
    # __tablename__ = 'cursisten'
```

Alles staat nu klaar, de kolommen kunnen opgegeven worden. Hier is voor de demonstratie gekozen slechts een beperkt aantal kenmerken van iedere cursist op te nemen.
Het zijn er drie: `id`, `voornaam` en `leeftijd`.

Het `id` is van het type `integer` en wordt de primaire sleutel van de tabel. Naam is een tekstveld en in de kolom leeftijd moet een getal komen te staan, dus dat wordt een `integer`:

```python
id = db.Column(db.Integer,primary_key=True)
naam = db.Column(db.Text)
leeftijd = db.Column(db.Integer)
```

Hierna krijgt de klasse Cursist zijn constructor (`__init__()`):

```python
def __init__(self,naam,leeftijd):
    self.naam = naam
    self.leeftijd = leeftijd
```

Bij het invoeren van een nieuwe cursist zijn naam en leeftijd verplicht. Er wordt automatisch een nieuw id toegevoegd op het moment dat er een nieuwe cursist wordt opgevoerd.

Tot slot nog de methode `__repr__()`. Zoals we al eerder hebben gezien wordt deze methode gebruikt om een stringvoorstelling van een Python-object te krijgen. Met de methode `__repr__()` is het mogelijk een query te maken vanuit de database en het resultaat van de query afdrukken.

```python
def __repr__(self):
    return f"Cursist {self.naam} is {self.leeftijd} jaar oud."
```

Tot zover de basiscode voor het opzetten van een database. Een aantal elementen van de code worden geïmporteerd in de file `setup_database.py`, waarin de eerste records aan de database toegevoegd zullen worden.

## 2. `setup_database.py`

Voor de tweede stap maken we gebruik van het bestand [`setup_database.py`](../bestanden/crud/setup_database.py). Let wel: Dit is een heel eenvoudig script dat laat zien hoe een database in te stellen. Later worden hierbij weer templates gebruikt.

Ook voor deze file zal de opbouw van de code stap voor stap beschreven worden. In de eerste plaats worden er een aantal elementen uit de file `basic_model_app.py` geïmporteerd:

```python
from basic_model_app import db, Cursist
```

De database en de tabel Cursist zijn ingeladen en nu moet de database en het bestand worden aangemaakt. Daarvoor is onderstaand commando beschikbaar:

```python
db.create_all()
```

#### Toevoegen van records

Wanneer tabel klaar staat kunnen de eerste records toegevoegd worden:

```python
joyce = Cursist('Joyce', 36)
bram = Cursist('Bram',24)
```

De objecten zijn aangemaakt, maar zijn nog niet bekend bij de database. Dat kan als volgt:

```python
db.session.add_all([joyce, bram])
```

De id's worden dus automatisch aangemaakt zodra de gegevens aan de database zijn toegevoegd.
De data kan definitief vastgelegd worden door de functie `commit()`:

```python
db.session.commit()
```

Als alles naar behoren is ingevoerd kan getest worden of de gegevens inderdaad zijn vastgelegd in de database. Daarvoor vragen we de beide id’s op uit de tabel Cursist. De nummers 1 en 2 zouden te zien moeten zijn:

```python
print(joyce.id)
print(bram.id)
```

Het resultaat:

```console
> 1
> 2
```

