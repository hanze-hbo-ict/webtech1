# Flask en SQL - Relaties

Bij grotere projecten zijn altijd meerdere modellen (tabellen) beschikbaar. Die modellen hebben een relatie met elkaar. Tot nu toe is er gewerkt met `Cursist` als model. Daarnaast bestaat er ook een model `Instrument`, waar de gegevens van de instrumenten beheerd worden, waarin de muziekschool lesgeeft. Een derde model wat erg voor de hand ligt is `Docent`. Docenten geven les aan cursisten om hen een instrument te leren bespelen.

In deze demonstratie is het uitgangspunt dat cursisten meerdere instrumenten kunnen leren bespelen en dat de lessen door een enkele docent gegeven worden. Om de boel op dit moment niet nodeloos complex te maken, stellen we even dat een instrument maar door één cursist kan worden bespeeld. Het strokendiagram van de database wordt dan als volgt:

![Strokendiagram van de database](imgs/strokendiagram.png)

### Sleutels

Om relaties te kunnen begrijpen is het nodig nog even kort aandacht te besteden aan een tweetal belangrijke termen, de primaire sleutel (__primary key__) en de refererende sleutel (__foreign key__).

De modellen (tabellen) krijgen de volgende structuur:

`Cursist`:

- id (primaire sleutel, type integer)
- naam (type text)

`Instrument`:

- id (primaire sleutel, type integer)
- naam (type text)

`Docent`:

- id (primaire sleutel, type integer)
- naam (type text)

Een primair sleutelveld zorgt ervoor dat elke rij uit het model uniek is. Een primaire sleutel mag bij geen enkel model een dubbele waarde krijgen. Omdat er een index als primair sleutelveld gebruikt wordt hoeven we ons daar geen zorgen om te maken.

Telkens wanneer er een nieuw object van de klasse `Instrument` wordt aangemaakt, kunnen we aangeven welke cursist dat instrument gaat bespelen. Hetzelfde geldt voor ieder nieuw object uit de klasse `Docent` – ook hiervan kunnen we aangeven welk instrument die docent gaat doceren. 

Er wordt dan gevraagd welke cursist door deze docent begeleid gaat worden. En daarbij komen dan de refererende sleutels om de hoek kijken. Er moet een relatie worden geïntroduceerd tussen cursist en instrument en tussen cursist en docent. Bij het opzetten van de file `models.py` komt dit nog uitgebreid ter sprake.

## `models.py`
De opzet van deze applicatie wordt gedaan door eerst weer een nieuw project op te starten met de naam ‘Relaties’. Daarom is het nodig als eerste een opzet van de database aan te maken. Daarvoor wordt de file [`models.py`](bestanden/relaties/models.py) in het leven geroepen.

Als eerste moeten natuurlijk weer de gebruikelijke zaken geïmporteerd worden. Daarna wordt aangegeven op welke plaats zich de basis directory bevindt. De actie wordt gevolgd door het aanmaken van de applicatie en de bijbehorende acties met `SQLALCHEMY`. Aan het einde van dit eerste blok worden applicatie en database weer aan elkaar gekoppeld en wordt het migratiepad ingericht.

```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Koppelt de Flask-applicatie met de database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
```

Het model `Cursist`:

```python
class Cursist(db.Model):

    __tablename__ = 'cursisten'

    id = db.Column(db.Integer,primary_key = True)
    naam = db.Column(db.Text)
    # cursist heeft een één-op-veel relatie met instrument
    instrumenten = db.relationship('Instrument',backref='cursist',lazy='dynamic')
    # cursist heeft een één-op-een relatie met docent
    docent = db.relationship('Docent',backref='cursist',uselist=False)
```

Er wordt wat nader ingegaan op de relatie-aspecten. Aangegeven is dat de relatie tussen cursisten en instrumenten, een één-op-een relatie is. De coderegel nader uitgelegd:

```python
instrumenten = db.relationship('Instrument',backref='cursist',lazy='dynamic')
```

In de variabele `instrumenten` wordt vastgelegd dat binnen deze database er een relatie bestaat naar `Instrument` toe en dat er voor de methode `lazy=’dynamic’` gekozen is.

De lazy-parameter bepaalt hoe de gerelateerde objecten worden geladen bij het doorzoeken van relaties. Er kan uit vier (4) verschillende opties gekozen worden. In de meeste gevallen wordt er een keuze voor `‘dynamic’` gemaakt. De andere drie mogelijke parameterinvullingen zijn:

- `select` (of `True`)
- `joined` (of `False`)
- `subquery`

Nu het uitgangspunt is dat er tussen docent en cursist een één-op-één relatie bestaat, moet hier nu ingevuld worden `uselist=False`. Een cursist kan niet meer dan één docent als leraar hebben en een docent, in onze bijzondere muziekschool, heeft maar één cursist.

De klasse `Cursist` krijgt ook nog de beschikking over de volgende methoden:

```python
    def __init__(self,naam):
        self.naam = naam

    def __repr__(self):
        if self.docent:
            return f"Cursist {self.naam} heeft {self.docent.naam} als docent"
        else:
            return f"Cursist {self.naam} heeft nog geen docent toegewezen gekregen"

    def overzicht_instrumenten(self):
        print("Mijn instrumenten:")
        for instr in self.instrumenten:
            print(instr.naam)
```

De methode `overzicht_instrumenten` toont de instrumenten waar een cursist momenteel les in volgt.

Het model `Instrument`:

```python
class Instrument(db.Model):

    __tablename__ = 'instrumenten'

    id = db.Column(db.Integer,primary_key = True)
    naam = db.Column(db.Text)
    # Er wordt cursisten.id ingevuld vanwege de tabelnaam ='cursisten'
    cursist_id = db.Column(db.Integer,db.ForeignKey('cursisten.id'))

    def __init__(self,naam,cursist_id):
        self.naam = naam
        self.cursist_id = cursist_id
```


Het model `Docent`:

```python
class Docent(db.Model):

    __tablename__ = 'docenten'

    id = db.Column(db.Integer,primary_key= True)
    naam = db.Column(db.Text)
    cursist_id = db.Column(db.Integer,db.ForeignKey('cursisten.id'))

    def __init__(self,naam,cursist_id):
        self.naam = naam
        self.cursist_id = cursist_id
```

Tot zover de code van de file `models.py`. Om de database aan te maken en om de wijzigingen door te voeren dienen nu de vier stappen van de vorige paragraaf uitgevoerd te worden:

- Stel de omgevingsvariabele FLASK_APP in
    - Voor een MacOS / Linux-machine is dat `export FLASK_APP = models.py`
    - Voor een Windows-machine, met cmd: `set FLASK_APP = models.py`, met PowerShell: `$Env:FLASK_APP = "models.py"`

- `flask db init`

- `flask db migrate`

- `flask db upgrade`

## Demonstratie
Nu de tabel is aangemaakt kunnen er gegevens ingebracht worden. Voor deze demonstratie gebruiken we de file [`populate_database.py`](bestanden/relaties/populate_database.py):

```python
from models import db,Cursist,Instrument,Docent

# Maak twee cursisten aan
joyce = Cursist("Joyce")
bram = Cursist("Bram")

# Voeg de cursisten toe aan de database en leg ze vast
db.session.add_all([joyce,bram])
db.session.commit()

# Ter controle een print van alle cursisten, met de teksten van __repr__ uit Cursist
print(Cursist.query.all())

# Vind alle cursisten met de naam “Joyce",
# worden er meerdere gevonden in de lijst , dan alleen de eerste daarom index [0]
# Kan ook gevonden worden door .first() te gebruiken i plaats van  .all()[0]
joyce = Cursist.query.filter_by(naam='Joyce').all()[0]

# Maak een docent aan voor Joyce
david = Docent("David", joyce.id)

# De instrumenten waar Joyce les in heeft
instr1 = Instrument('Drums', joyce.id)
instr2 = Instrument("Piano", joyce.id)

# Leg de aanpassingen vast in de database
# Merk op dat het om verschillende objecten gaat
db.session.add_all([david, instr1, instr2])
db.session.commit()

# Nagaan wat de veranderingen voor Joyce hebben opgeleverd.
joyce = Cursist.query.filter_by(naam='Joyce').first()
print(joyce)

# Een overzicht van de instrumenten waar Joyce les in heeft
print(joyce.overzicht_instrumenten())

# Het is ook mogelijk zaken te verwijderen uit de database:
# find_cur = Cursist.query.get(1)
# db.session.delete(find_cur)
# db.session.commit()
```

Na het runnen is dit het resultaat:

```console
[Cursist Joyce heeft nog geen docent toegewezen gekregen, Cursist Bram heeft nog geen docent toegewezen gekregen]
Cursist Joyce heeft David als docent
Mijn instrumenten:
Drums
Piano
```

Bovendien kan nagegaan worden hoe de structuur van de database is opgebouwd:

![De structuur van de database](imgs/structuur-database.png)
