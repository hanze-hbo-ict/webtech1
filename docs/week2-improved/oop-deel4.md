# OOP Python – Getters en Setters

Getters en setters zijn niet van essentieel belang voor het werken met Python, maar kunnen wel heel nuttig in gebruik zijn. Het belang voor Python is heel gering omdat deze programmeertaal in tegenstelling tot bijvoorbeeld Java de attributen uit een klasse niet de status `private` mee kan geven. Een privaat attribuut kan alleen gewijzigd worden door gebruik te maken van een `setter` (geef het attribuut een waarde) en `getter` (haal de waarde van het attribuut op).

## Het voorbeeld

In dit voorbeeld maken we gebruik van twee python-bestanden. Het kan ook in één bestand ondergebracht worden, maar hier worden er twee voor gebruikt om onnodig scrollen te voorkomen en om nog een andere wijze van importeren te tonen.

De files zijn [`main.py`](bestanden/webshop/main.py) en [`klant.py`](bestanden/webshop/klant.py). Als eerste bespreken we de file `klant.py`:

```python
class Klant:

    def __init__(self, naam, email):
        self._naam = naam
        self._email = email
        self.__krediet = 1000.0  # Startk rediet voor nieuwe klanten
        self.__korting = 0.0  # Standaard geen korting
```

Iedere klant heeft een naam en email, en er worden voor iedere klant een aantal standaardinstellingen meegegeven (krediet en korting). Nu de eerste regels van `main.py`. De code van `klant.py` wordt in de eerste regel van `main.py` geïmporteerd:

```python
from klant import Klant

jan = Klant("Jan Jansen", "jan@email.nl")

print(jan._naam)
print(jan._email)
```

Uitkomst:

```console
Jan Jansen
jan@email.nl
```

## Attributen buiten de klasse

De file `main.py` wordt verder uitgebreid. Jan krijgt een korting van 10%:

```python
jan.__korting = 0.10
print(jan.__korting)
```

Uitkomst:

```console
0.1
```

Voor veel programmeurs is dit een gruwel: van buiten de klasse kunnen attributen zomaar aangeroepen en gewijzigd worden. Om te voorkomen dat dit kan, kunnen we in Python de attributen voorzien van een dubbele underscore aan het begin (`__`, een soort halve *dunder*). We illustreren dat aan de hand van de onderstaande klasse:

```python
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

Om toch bij die attributen te kunnen, maken we gebruik van zogenaamde `getters` en `setters`. De eerste gebruiken we om de waarde van een attribuut *op te vragen*, terwijl we de tweede constructie gebruiken om de waarde van het attribuut (drum roll) *aan te passen*. Hieronder zie je hoe die methoden in onze klasse `Klant` eruit zien:

```python
def _get_krediet(self):
    return self.__krediet

def _set_krediet(self, krediet):
    if krediet >= 0:
        self.__krediet = krediet
    else:
        print("Krediet kan geen negatieve waarde krijgen")
        self.__krediet = 0
```

Vanwege die enkele underscore moet er ook een regel in `__init__()` veranderd worden:

```python
def __init__(self, naam, email):
    self._naam = naam
    self._email = email
    self.__krediet = 1000.0
    self.__korting = 0.0
```

Voor de korting kunnen we hetzelfde doen:

```python
def _get_korting(self):
    return self.__korting

def _set_korting(self, korting):
    if 0 <= korting <= 1.0:
        self.__korting = korting
    else:
        print("Korting moet tussen 0 en 1.0 liggen")
```

## Gebruik van getters en setters

Nu kunnen we in `main.py` de getters en setters gebruiken:

```python
from klant import Klant

jan = Klant("Jan Jansen", "jan@email.nl")

# Gebruik getter om krediet op te vragen
print(f"Krediet: €{jan._get_krediet():.2f}")

# Gebruik setter om korting te geven
jan._set_korting(0.10)
print(f"Korting: {jan._get_korting() * 100}%")

# Probeer ongeldige waarde
jan._set_korting(1.5)  # Dit wordt afgewezen

# Verlaag krediet
jan._set_krediet(jan._get_krediet() - 250.0)
print(f"Nieuw krediet: €{jan._get_krediet():.2f}")
```

Uitkomst:

```console
Krediet: €1000.00
Korting: 10.0%
Korting moet tussen 0 en 1.0 liggen
Nieuw krediet: €750.00
```

## De @property decorator

Python biedt een elegantere manier om getters en setters te maken: de `@property` decorator. Dit maakt de code leesbaarder en pythonischer:

```python
class Klant:

    def __init__(self, naam, email):
        self._naam = naam
        self._email = email
        self.__krediet = 1000.0
        self.__korting = 0.0

    @property
    def krediet(self):
        """Getter voor krediet"""
        return self.__krediet

    @krediet.setter
    def krediet(self, waarde):
        """Setter voor krediet"""
        if waarde >= 0:
            self.__krediet = waarde
        else:
            print("Krediet kan geen negatieve waarde krijgen")
            self.__krediet = 0

    @property
    def korting(self):
        """Getter voor korting"""
        return self.__korting

    @korting.setter
    def korting(self, waarde):
        """Setter voor korting"""
        if 0 <= waarde <= 1.0:
            self.__korting = waarde
        else:
            print("Korting moet tussen 0 en 1.0 liggen")
```

Met de `@property` decorator kunnen we attributen gebruiken alsof het gewone attributen zijn, maar er worden wel de getters en setters aangeroepen:

```python
jan = Klant("Jan Jansen", "jan@email.nl")

# Gebruik als gewone attributen (maar getter wordt aangeroepen)
print(f"Krediet: €{jan.krediet:.2f}")

# Setter wordt automatisch aangeroepen
jan.korting = 0.15
print(f"Korting: {jan.korting * 100}%")

# Validatie werkt nog steeds
jan.korting = 2.0  # Dit wordt afgewezen

# Krediet aanpassen
jan.krediet = jan.krediet - 300.0
print(f"Nieuw krediet: €{jan.krediet:.2f}")
```

Uitkomst:

```console
Krediet: €1000.00
Korting: 15.0%
Korting moet tussen 0 en 1.0 liggen
Nieuw krediet: €700.00
```

Veel eleganter! Je gebruikt `jan.krediet` in plaats van `jan._get_krediet()`, maar de validatie gebeurt nog steeds.

## Voordelen van properties

De `@property` decorator heeft verschillende voordelen:

1. **Pythonische syntax**: Code ziet er natuurlijker uit
2. **Backward compatibility**: Je kunt later getters/setters toevoegen zonder bestaande code te breken
3. **Validatie**: Je kunt input controleren voordat het attribuut wordt aangepast
4. **Read-only properties**: Je kunt een property zonder setter maken (alleen getter)

Voorbeeld van een read-only property:

```python
@property
def volledige_naam(self):
    """Read-only property die volledige naam returnt"""
    return f"{self._naam} ({self._email})"
```

Gebruik:

```python
jan = Klant("Jan Jansen", "jan@email.nl")
print(jan.volledige_naam)  # Jan Jansen (jan@email.nl)

# Dit werkt NIET - geen setter gedefinieerd:
# jan.volledige_naam = "Andere naam"  # AttributeError!
```

## Samenvatting

In dit deel hebben we geleerd over:

- Het verschil tussen public (`naam`), protected (`_naam`) en private (`__naam`) attributen
- Het gebruik van getters en setters om toegang tot attributen te controleren
- De `@property` decorator voor elegantere properties
- Validatie van input in setters
- Read-only properties

In het volgende deel gaan we kijken naar overerving (inheritance), waarbij klassen eigenschappen van andere klassen overnemen.
