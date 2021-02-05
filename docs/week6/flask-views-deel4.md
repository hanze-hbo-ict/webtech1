# Flask en SQL - Migraties

In de vorige paragraaf is uitgelegd hoe een database aan te maken en daar de basishandelingen CRUD op los te laten met Flask-SQLAlchemy.

Nadat een model voor een databasetabel is aangemaakt, kan het natuurlijk voorkomen dat er aanpassingen aan het model gedaan dienen te worden, zoals bijvoorbeeld het toevoegen van een nieuwe kolom. Nadat de wijzigingen zijn aangebracht, dienen deze wijzigingen opgeslagen te worden in het database-model. Hiervoor zijn *migraties* bedacht.

## Flask-Migrate

Flask-Migraties worden gebruikt om versies van het database-model bij te houden. Dit pakket stelt een gebruiker in staat om aanpassingen te maken in een Model-klasse, en ervoor te zorgen dat deze van kracht worden in de SQL-database.

Er zijn vier belangrijke commando’s hierbij die op de command-line worden gebruikt:

- Stel de omgevingsvariabele FLASK_APP in
    - Voor een MacOS / Linux-machine is dat `export FLASK_APP = myapp.py`
    - Voor een Windows-machine `set FLASK_APP = myapp.py`
- `flask db init`  stelt de migratie directory in
- `flask db migrate -m "zomaar een bericht"`  stelt het migratiebestand in
- `flask db upgrade` verwerkt de aanpassing in de database

Wanneer de `FLASK_APP` niet is ingesteld, verschijnt er een foutmelding:

```
Error: Could not locate Flask application. 
You did not provide the FLASK_APP environment variable.
```

Vaak is dit pakket nog niet geïnstalleerd. Dat kan verholpen worden door op de bekende wijze dit pakket toe te voegen. 

Nu weer de praktijk. Wat te doen om het geheel werkend te krijgen zodat migraties kunnen worden doorgevoerd? Op de eerste plaats dienen er een tweetal wijzigingen te worden aangebracht in de file [`BasicModelApp.py`](../bestanden/crud/BasicModelApp.py):

```python hl_lines="4"
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
```

Er komt een extra importregel bij. In hetzelfde bestand volgt nog een tweede toevoeging:

```python hl_lines="8"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app,db)
```

Door deze regel toe te voegen is het mogelijk migraties door te voeren met terminalopdrachten. Ook worden hier de applicatie en de database met elkaar verbonden.

De omgevingsvariabele `FLASK_APP` kan nu ingesteld worden op de command-line. Let erop dat deze in precies dezelfde directory komt te staan als het `.py`-bestand.