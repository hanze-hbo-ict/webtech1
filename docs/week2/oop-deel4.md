# OOP Python – Getters en Setters

Getters en setters zijn niet van essentieel belang voor het werken met Python, maar kunnen wel heel nuttig in gebruik zijn. Het belang voor Python is heel gering omdat deze programmeertaal in tegenstelling tot bijvoorbeeld Java de attributen uit een klasse niet de status `private` mee kan geven. Een privaat attribuut kan alleen gewijzigd worden door gebruik te maken van een `setter` (geef het attribuut een waarde) en `getter` (haal de waarde van het attribuut op).

## Het voorbeeld

In dit voorbeeld maken we gebruik van twee python-bestanden. Het kan ook in één bestand ondergebracht worden, maar hier worden er twee voor gebruikt om onnodig scrollen te voorkomen en om nog een andere wijze van importeren te showen.

De files zijn [`main.py`](bestanden/game/main.py) en [`speler.py`](bestanden/game/speler.py). Als eerste bespreken we de file `speler.py`:

```python
class Speler:

    def __init__(self, naam):
        self.naam = naam
        self.levens = 3
        self.level = 1
        self.score = 0
```

Iedere speler heeft een naam en er worden voor iedere speler aan het begin van het spel een aantal standaardinstellingen meegegeven. Nu de eerste regels van `main.py`. De code van `speler.py` wordt in de eerste regel van `main.py` geïmporteerd:

```python
from speler import Speler

bram = Speler("Bram")

print(bram.naam)
print(bram.levens)
```

Uitkomst:

```text
Bram
3
```

## Attributen buiten de klasse

De file `main.py` wordt verder uitgebreid met een aantal spelacties. Bram heeft een spelletje verloren en het aantal levens wordt met 1 verminderd.

```python
bram.levens -= 1
print(bram.levens)
```

Uitkomst:

```text
2
```

Voor veel programmeurs is dit een gruwel: van buiten de klasse kunnen attributen zomaar aangeroepen en gewijzigd worden. Om te voorkomen dat dit kan, kunnen we in Python de attributen voorzien van een dubbele underscore aan het begin (`__`, een soort halve *dunder*). We illustreren dat aan de hand van de onderstaande klasse:

```python hl_lines="5"
# klasse Foo in bestand foo.py

class Foo:
    def __init__(self, var):
        self.__var = var
```

Als we deze klasse in de interactieve shell inladen, zien we de werking van het attribuut `__var`:

```ipython
In [1]: run 'Foo'

In [2]: f = Foo('demo')

In [3]: f.__var
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-3-01a6a7be3a69> in <module>
----> 1 f.__var

AttributeError: 'Foo' object has no attribute '__var'

In [4]:
```

## Getters en Setters

Om toch bij die attributen te kunnen, maken we gebruik van zogenaamde `getters` en `setters`. De eerste gebruiken we om de waarde van een attribuut *op te vragen*, terwijl we de tweede constructie gebruiken om de waarde van het attribuut (drum roll) *aan te passen*. Hieronder zie je hoe die methoden in onze klasse `Speler` eruit zien:


```python
def _get_levens(self):
    return self.__levens

def _set_levens(self, levens):
    if levens >= 0:
        self.__levens = levens
    else:
        print("Levens kunnen geen negatieve waarde krijgen")
        self.__levens = 0
```

Vanwege die enkele underscore moet er ook een regel in `__init__()` veranderd worden:

```python
self.__levens = 3
```

Tevens is er een controle ingebouwd dat het aantal levens niet beneden nul (0) kan komen. Tot slot wordt er [een property](https://docs.python.org/3.8/library/functions.html#property) aan toegevoegd, die de twee methoden gaat aanroepen, om de gegevens op te vragen of te wijzigen. Deze property zetten we *onderaan de klasse* `Speler`.

```python
levens = property(_get_levens, _set_levens)
```

Als laatste wordt er nog een format ingesteld voor iedere printopdracht in dit specifieke geval. Is er een printopdracht gaat Python automatisch op zoek naar een methode en wel deze, `__str__()`. Als deze methode gevonden wordt, wordt een format gebruikt voor het instellen van de gegevens.

```python
def __str__(self):
    return f"Name: {self.naam}, Levens: {self.__levens}, Level: {self.level}, Score {self.score}"
```

!!! Info "`__str__` en `__repr__`"
    In het vorige blok hebben we gewerkt met de methode `__repr__`, die eveneens aangroepen worden wanneer je een string-representatie van een object wilt hebben. Dit zijn twee methoden die toch min of meer hetzelfde doen. [Lees deze blog](https://www.bartbarnard.nl/blog/python-string-representaties/) om een beeld te krijgen van de overeenkomsten en de verschillen tussen deze methoden.

## Een interactieve test

Nu draaien we een testje van de werking:

```ipython
In [1]: run "Speler"

In [2]: bram = Speler("bram")

In [3]: bram
Out[3]: Name: bram, Levens: 3, Level: 1, Score 0

In [4]: bram.levens -= 1

In [5]: bram
Out[5]: Name: bram, Levens: 2, Level: 1, Score 0

In [6]: bram.levens -= 10
Levens kunnen geen negatieve waarde krijgen

In [7]: bram
Out[7]: Name: bram, Levens: 0, Level: 1, Score 0

In [8]:
```

De eerste keer wordt rechtstreeks de inhoud van het object opgevraagd, terwijl als het gevraagde attribuut wordt weggelaten automatisch de properties worden getoond. Iets soortgelijks kan gedaan worden met `level` om de setter-constructie duidelijk te maken.

```python hl_lines="4"
def __init__(self, naam):
    self.naam = naam
    self.__levens = 3
    self.__level = 1
    self.score = 0

def _get_level(self):
    return self.__level

def _set_level(self, level):
    if level > 0:
        delta = level - self.__level
        self.__score += delta * 1000
        self.__level = level
    else:
        print("Het laagste level is level 1")
```

Ook voor `level` is er een property aangemaakt:

```python
level = property(_get_level, _set_level)
```

Een test-script:

```ipython
In [1]: run "Speler"

In [2]: bram = Speler('bram')

In [3]: bram.level=2

In [4]: bram
Out[4]: Name: bram, Levens: 3, Level: 2, Score 1000

In [5]: bram.level += 5

In [6]: bram
Out[6]: Name: bram, Levens: 3, Level: 7, Score 6000

In [7]: bram.score = 500

In [8]: bram
Out[8]: Name: bram, Levens: 3, Level: 7, Score 500

In [9]:
```

## Nog een andere notatie

Voor het laatste attribuut, `score`, gebruiken we nog een andere notatie:

```python
@property
def score(self):
    return self.__score

@score.setter
def score(self, score):
    self.__score = score
```

Een andere schrijfwijze: de bovenste methode geeft de waarde van `score` terug (`getter`), terwijl de onderste methode een waarde vastlegt voor `score` (`setter`).


## Kritische nabeschouwing

Zoals aangegeven is het gebruik van klasse-eigenschappen die alleen van binnen die klasse zelf kunnen worden benaderd (zogenaamde *private* eigenschappen) iets wat uit andere talen dan Python komt (met name Java of C# zijn hier behoorlijk strikt in). In deze talen *moet* je gebruik maken van getters en setters. In principe heeft Python dat niet nodig, omdat alle attributen en methoden van elke klasse te benaderen zijn (alles is *public*).

Het gebruiken van een dubbele underscore aan het begin van een private variabele (`__var`), zoals we hierboven hebben gezien, is een *conventie* die de variabele niet echt privaat maakt (op de manier waarop in Java of C# private variabelen bestaan). Python maakt hier gebruik van een techniek die bekend staat onder de naam [name mangling](https://en.wikipedia.org/wiki/Name_mangling) om het minder waarschijnlijk te maken dat code deze variabelen tegenkomt. Met een trukje zijn deze variabelen nog steeds prima te benaderen. In de praktijk kom je deze notatievorm dan ook eigenlijk niet tegen.

Als je echt de behoefte voelt om attributen alleen via getters en setters te benaderen, kun je het beste gebruik maken van de laatste notatievorm die we hebben besproken. Bestudeer eventueel [de documentatie op python.org zelf](https://docs.python.org/3/library/functions.html#property) om hier een goed beeld bij te krijgen.