# Flask en SQL - CRUD

## III. BasisCrud.py

Nu bekend is hoe een database opgezet kan een beetje gestoeid worden door een aantal basishandelingen uit te voeren.  

Denk erom, vaak worden de scripts op een andere wijze uitgevoerd. Het doel is hier om te laten zien op welke wijze CRUD-commando’s uitgevoerd worden. De Python-file die daarvoor gebruikt wordt, krijgt de naam `BasisCRUD.py` mee. Iedere basishandeling komt even voorbij. De opbouw geschiedt in een vijftal stappen:

### Stap 1: Importeren
```python
from BasicModelApp import db, Cursist
```

### Stap 2: CREATE
```python
elsje = Cursist('Elsje',19)
db.session.add(elsje)
db.session.commit()
```

aanmaken, toevoegen en vastleggen.

### Stap 3: READ
Staat bekend als het opvragen van gegevens uit de database.

Als eerste een overzicht gemaakt van alle cursisten:

```python
alle_cursisten = Cursist.query.all()
print(alle_cursisten)
```

Met de methode `all()` kunnen alle records uit een tabel getoond worden in een lijst. De tekst wordt opgehaald uit `__repr__()`.

![Alle gegevens die in de database staan](imgs/alle-cursisten.png)

Nu worden de gegevens opgevraagd van de cursist die het id = 2 is toegekend. Eerst worden alle gegevens getoond en op de tweede regel alleen de leeftijd.

```python
cursist_twee = Cursist.query.get(2)
print(cursist_twee)
print(cursist_twee.leeftijd)
```

Gegevens van cursist 2:

![De gegevens van cursist 2: Bram. Hij is 24 jaar oud](imgs/gegevens-cursist-2.png)

### Stap 4: UPDATE

Joyce heeft een beetje gejokt over haar leeftijd. In plaats van de opgegeven 36 jaar is ze inmiddels al 40 geworden. Dat wordt in de database doorgevoerd:

```python
cursist_joyce = Cursist.query.get(1)
cursist_joyce.leeftijd = 40
db.session.add(cursist_joyce)
db.session.commit()
```

Joyce heeft id = 1 meegekregen. Er worden vier stappen na elkaar uitgevoerd:

1. Ophalen juiste record;
2. Wijziging aanbrengen;
3. Gegevens toevoegen aan database;
4. Aanpassing definitief vastleggen.

### Stap 5: DELETE

Bij nader inzien besluit Elsje toch maar af te zien van een lidmaatschap. Haar record gaat weer verdwijnen.

```python
cursist_elsje = Cursist.query.get(3)
db.session.delete(cursist_elsje)
db.session.commit()
```

Dit spreekt voor zich: record ophalen, verwijderen, en aanpassing vastleggen.

Na het aanpassen en verwijderen zijn onderstaande gegevens overgebleven in de database:

![de overgebleven gegevens in de database](imgs/gegevens-in-database.png)
