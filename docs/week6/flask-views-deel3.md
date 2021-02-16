# Flask en SQL - CRUD

## 3. `BasisCrud.py`

Nu bekend is hoe een database opgezet kan een beetje gestoeid worden door een aantal basishandelingen uit te voeren.

Denk erom, vaak worden de scripts op een andere wijze uitgevoerd. Het doel is hier om te laten zien op welke wijze CRUD-commando’s uitgevoerd worden. De Python-file die daarvoor gebruikt wordt, is het bestand [`BasisCRUD.py`](../bestanden/crud/BasicCRUD.py). Iedere basishandeling komt even voorbij. De opbouw geschiedt in een vijftal stappen:

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

Op deze manier kun je data aanmaken, toevoegen en vastleggen.

### Stap 3: READ
Deze stap staat bekend als het opvragen van gegevens uit de database.

Als eerste een overzicht gemaakt van alle cursisten. Met de methode `all()` worden alle records in een python-lijst gestopt. De tekst wordt opgehaald uit `__repr__()`:

```python
alle_cursisten = Cursist.query.all()
print(*alle_cursisten, sep='\n')
```

Dit levert het volgende resultaat op:

```console
Cursist Joyce is 40 jaar oud
Cursist Bram is 24 jaar oud
Cursist Elsje is 19 jaar oud
Cursist Elsje is 19 jaar oud
```

Nu worden de gegevens opgevraagd van de cursist die het id = 2 is toegekend. Eerst worden alle gegevens getoond en op de tweede regel alleen de leeftijd.

```python hl_lines="1"
cursist_twee = Cursist.query.get(2)
print(cursist_twee)
print(cursist_twee.leeftijd)
```

Gegevens van cursist 2:

```console
Cursist Bram is 24 jaar oud
24
```

### Stap 4: UPDATE

Joyce heeft een beetje gejokt over haar leeftijd. In plaats van de opgegeven 36 jaar is ze inmiddels al 40 geworden. Dat wordt in de database doorgevoerd:

```python hl_lines="2"
cursist_joyce = Cursist.query.get(1)
cursist_joyce.leeftijd = 40
db.session.add(cursist_joyce)
db.session.commit()
```

Joyce heeft `id = 1` meegekregen. Er worden vier stappen na elkaar uitgevoerd:

1. Ophalen juiste record;
2. Wijziging aanbrengen;
3. Gegevens toevoegen aan database;
4. Aanpassing definitief vastleggen.

### Stap 5: DELETE

Bij nader inzien besluit Elsje toch maar af te zien van een lidmaatschap. Haar record gaat weer verdwijnen.

```python hl_lines="2"
cursist_elsje = Cursist.query.get(3)
db.session.delete(cursist_elsje)
db.session.commit()
```

Dit spreekt voor zich: record ophalen, verwijderen, en aanpassing vastleggen.

Na het aanpassen en verwijderen zijn onderstaande gegevens overgebleven in de database:

```console
Cursist Elsje is 19 jaar oud
Cursist Joyce is 40 jaar oud
Cursist Bram is 24 jaar oud
```
