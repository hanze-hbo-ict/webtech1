# Flask en SQLAlchemy - CRUD operaties

## 3. CRUD operaties (`basic_CRUD.py`)

Je hebt de database en model aangemaakt. Nu voer je de vier basis operaties uit: **Create, Read, Update, Delete**.

Bestudeer het volledige bestand [`basic_CRUD.py`](bestanden/crud/basic_CRUD.py).

!!! note "Vereenvoudigd voorbeeld"
    Dit script toont de basis CRUD operaties. In een echte Flask applicatie gebruik je routes en templates in plaats van losse scripts.

## CREATE - Records toevoegen

```python
from basic_model_app import db, Cursist

# Maak nieuw object aan
elsje = Cursist('Elsje', 19)

# Voeg toe aan database sessie
db.session.add(elsje)

# Schrijf naar database
db.session.commit()
```

Drie stappen: object maken, toevoegen aan sessie, committen.

## READ - Gegevens opvragen

### Alle records ophalen

```python
alle_cursisten = db.session.execute(db.select(Cursist)).scalars().all()
print(*alle_cursisten, sep='\n')
```

`db.session.execute(db.select(Cursist)).scalars().all()` geeft een lijst met alle cursisten terug. De tekst komt uit de `__repr__()` methode.

Output:

```console
Cursist Joyce is 40 jaar oud
Cursist Bram is 24 jaar oud
Cursist Elsje is 19 jaar oud
```

### Specifiek record ophalen op ID

```python
cursist_twee = db.session.get(Cursist, 2)
print(cursist_twee)
print(cursist_twee.leeftijd)
```

`db.session.get(Cursist, 2)` haalt het record op met `id = 2`.

Output:

```console
Cursist Bram is 24 jaar oud
24
```

Je kunt direct attributen ophalen zoals `cursist_twee.leeftijd` of `cursist_twee.naam`.

!!! info "Query API"
    SQLAlchemy biedt veel query methoden:
    - `db.session.execute(db.select(Model)).scalars().all()` - Alle records
    - `db.session.get(Model, id)` - Record op primaire sleutel
    - `db.session.execute(db.select(Model).filter_by(naam='Joyce')).scalar_one_or_none()` - Filteren

## UPDATE - Gegevens wijzigen

```python
# Haal record op
cursist_joyce = db.session.get(Cursist, 1)

# Wijzig attribuut
cursist_joyce.leeftijd = 40

# Voeg toe aan sessie
db.session.add(cursist_joyce)

# Schrijf wijziging naar database
db.session.commit()
```

Vier stappen:

1. Record ophalen met `db.session.get()`
2. Attribuut wijzigen
3. Toevoegen aan sessie
4. Committen

!!! tip "Update zonder add"
    Je kunt `db.session.add()` ook weglaten bij updates. SQLAlchemy houdt bij welke objecten gewijzigd zijn:
    ```python
    cursist_joyce = db.session.get(Cursist, 1)
    cursist_joyce.leeftijd = 40
    db.session.commit()  # Dit werkt ook
    ```

## DELETE - Records verwijderen

```python
# Haal record op
cursist_elsje = db.session.get(Cursist, 3)

# Verwijder uit database
db.session.delete(cursist_elsje)

# Schrijf wijziging naar database
db.session.commit()
```

Drie stappen:

1. Record ophalen
2. `delete()` aanroepen
3. Committen

Na deze wijzigingen blijven deze records over:

```console
Cursist Joyce is 40 jaar oud
Cursist Bram is 24 jaar oud
```

## Overzicht CRUD patterne

| Operatie | Code patroon |
|----------|-------------|
| **Create** | `obj = Model(...)`<br>`db.session.add(obj)`<br>`db.session.commit()` |
| **Read** | `db.session.execute(db.select(Model)).scalars().all()`<br>`db.session.get(Model, id)` |
| **Update** | `obj = db.session.get(Model, id)`<br>`obj.attribuut = nieuwe_waarde`<br>`db.session.commit()` |
| **Delete** | `obj = db.session.get(Model, id)`<br>`db.session.delete(obj)`<br>`db.session.commit()` |

!!! warning "Altijd committen"
    Vergeet `db.session.commit()` niet! Zonder commit worden wijzigingen niet opgeslagen in de database.

**Volgende stap:** [Deel 4](flask-views-deel4.md) - Relaties tussen tabellen.

## Samenvatting

In deze les heb je geleerd:

- **CREATE**: een nieuw record toevoeg je door een object aan te maken, het met `db.session.add()` aan de sessie toe te voegen en daarna `db.session.commit()` aan te roepen.
- **READ (alle records)**: `db.session.execute(db.select(Model)).scalars().all()` geeft een lijst van alle records terug.
- **READ (op primaire sleutel)**: `db.session.get(Model, id)` haalt één record op aan de hand van het ID.
- **READ (filteren)**: met `.filter_by(attribuut=waarde)` gecombineerd met `.scalar_one_or_none()` zoek je op een specifieke kolomwaarde.
- **UPDATE**: haal een record op, pas het gewenste attribuut aan en roep `db.session.commit()` aan; `db.session.add()` is optioneel omdat SQLAlchemy wijzigingen automatisch bijhoudt.
- **DELETE**: haal een record op, roep `db.session.delete(obj)` aan en commit de sessie.
- **Altijd committen**: zonder `db.session.commit()` worden wijzigingen niet definitief opgeslagen in de database.
