# Flask en SQL - Migraties

In de vorige paragraaf is uitgelegd hoe een database aan te maken en daar de basishandelingen CRUD op los te laten met Flask-SQLAlchemy.

Volgende stap is het toelichten van de wijze waarop migraties ingezet kunnen worden.
Nadat een model voor een databasetabel is aangemaakt, kan het natuurlijk voorkomen dat er aanpassingen aan het model gedaan dienen te worden, zoals bijvoorbeeld het toevoegen van een nieuwe kolom. Nadat de wijzigingen zijn aangebracht, dienen deze wijzigingen gemigreerd te worden om de databasetabel bij te werken.

## Flask-Migrate

Dit kan gerealiseerd worden door gebruik te maken van Flask-Migrate. Dit pakket stelt een gebruiker in staat om aanpassingen te maken in een Model-klasse, en ervoor te zorgen dat deze van kracht worden in de SQL-database.

Er zijn 4 belangrijke commando’s hierbij die op de command-line worden gebruikt:

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


Nu weer de praktijk. Wat te doen om het geheel werkend te krijgen zodat migraties kunnen worden doorgevoerd. Op de eerste plaats dienen er een tweetal wijzigingen te worden aangebracht in de file `BasicModelApp.py`:

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
De omgevingsvariabele `FLASK_APP` kan nu ingesteld worden op de command-line. Let erop dat deze in precies dezelfde directory komt te staan als het .py-bestand.

![de locatie van de omgevingsvariable FLASK_APP ](imgs/FLASK_APP-path.png)

