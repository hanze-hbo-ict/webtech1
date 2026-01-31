# OOP Python – Methoden en inkapseling

Inkapseling (Engels: *encapsulation*) is één van de fundamenten van object-georiënteerd programmeren. Het wordt gebruikt om onbevoegden niet de gelegenheid te bieden de kenmerken van een object zomaar aan te passen. Als dat mogelijk moet zijn dan dienen zij toegang te krijgen tot de zogenaamde `getters` en `setters`, waarover zo dadelijk meer.

!!! Info "zichtbaarheid"
    Python wijkt nadrukkelijk af van het idee van inkapseling zoals het bijvoorbeeld gedaan wordt bij Java. Python gebruikt niet de sleutel-woorden `private` of `protected` om de zichtbaarheid van een methode aan te geven.

## Het voorbeeld Voorraad

Als voorbeeld hier een uitbreiding van onze webshop, waarbij het mogelijk is voorraad bij te bestellen, producten te verkopen en een geschiedenis van alle voorraad-mutaties bij te houden, inclusief tijdstip. Uiteraard is de opzet erg beperkt.

De code wordt in stapjes opgebouwd; we slaan deze code uiteindelijk op in het bestand [`voorraad.py`](bestanden/webshop/voorraad.py).

## Klasse en methoden

Stap 1: de klasse

```python
class Voorraad:
```

Stap 2: het importeren van de huidige tijd

```python
import datetime
```

Stap 3: een functie om het tijdstip van de mutatie vast te leggen.

```python
@staticmethod
def _current_time():
    now = datetime.datetime.now()
    return f"{now: %Y-%m-%d %H:%M:%S}"
```

De functie `_current_time()` retourneert het tijdstip van de mutatie in het opgegeven formaat, tot op de seconde nauwkeurig. De `@staticmethod` decorator geeft aan dat dit een functie is die bij de klasse hoort maar niet afhankelijk is van een specifieke instantie.

## De constructor

Stap 4: de constructor

```python
def __init__(self, product_naam, aantal):
    self._product_naam = product_naam
    self.__aantal = aantal
    self._mutatie_geschiedenis = []
    print(f"Voorraad aangemaakt voor {self._product_naam}")
```

## Bijbestellen en verkopen

Bij het aanmaken van een nieuwe voorraad wordt gevraagd om een productnaam en een beginhoeveelheid. De variabele `_mutatie_geschiedenis` is een lijst (`[]`) waarin alle mutaties worden vastgelegd.

Stap 5: de methode `bijbestellen()`

```python
def bijbestellen(self, aantal):
    if aantal > 0:
        self.__aantal += aantal
        self._mutatie_geschiedenis.append((Voorraad._current_time(), aantal))
        self.toon_voorraad()
```

Indien het bij te bestellen aantal groter dan nul (`0`) is, wordt de voorraad aangepast en wordt de mutatie toegevoegd aan de lijst `_mutatie_geschiedenis[]` (zie je wat het datatype is van dat wat er aan de lijst wordt toegevoegd?). Ook de actuele voorraad wordt nu getoond.

Stap 6: de methode `verkoop()`

```python
def verkoop(self, aantal):
    if 0 < aantal <= self.__aantal:
        self.__aantal -= aantal
        self._mutatie_geschiedenis.append((Voorraad._current_time(), -aantal))
    else:
        print("Het aantal dient groter dan nul (0) en maximaal gelijk aan de voorraad te zijn")
    self.toon_voorraad()
```

Er vindt een controle plaats of de voorraad toereikend is voor de verkoop. Zo niet, volgt er een passende mededeling. Zo ja, wordt de voorraad bijgewerkt en de mutatie weer in de lijst vastgelegd. Ook hier wordt de actuele voorraad getoond.

Stap 7: de methode `toon_voorraad()`

```python
def toon_voorraad(self):
    print(f"Voorraad {self._product_naam} bedraagt {self.__aantal}")
```

## Mutatie-overzicht

Stap 8: het mutatie-overzicht

```python
def toon_mutaties(self):
    print(f"\nMutatie-geschiedenis voor {self._product_naam}:")
    for datum, aantal in self._mutatie_geschiedenis:
        if aantal > 0:
            mutatie_type = "bijbesteld"
        else:
            mutatie_type = "verkocht"
            aantal = abs(aantal)
        print(f"  {datum}: {aantal} {mutatie_type}")
```

In een lus wordt de volledige lijst van mutaties doorlopen en wordt de informatie naar het scherm geschreven.

## De volledige code

De volledige klasse ziet er nu als volgt uit:

```python
import datetime


class Voorraad:
    """Klasse voor het bijhouden van productvoorraad"""

    @staticmethod
    def _current_time():
        now = datetime.datetime.now()
        return f"{now: %Y-%m-%d %H:%M:%S}"

    def __init__(self, product_naam, aantal):
        self._product_naam = product_naam
        self.__aantal = aantal
        self._mutatie_geschiedenis = []
        print(f"Voorraad aangemaakt voor {self._product_naam}")

    def bijbestellen(self, aantal):
        if aantal > 0:
            self.__aantal += aantal
            self._mutatie_geschiedenis.append((Voorraad._current_time(), aantal))
            self.toon_voorraad()

    def verkoop(self, aantal):
        if 0 < aantal <= self.__aantal:
            self.__aantal -= aantal
            self._mutatie_geschiedenis.append((Voorraad._current_time(), -aantal))
        else:
            print("Het aantal dient groter dan nul (0) en maximaal gelijk aan de voorraad te zijn")
        self.toon_voorraad()

    def toon_voorraad(self):
        print(f"Voorraad {self._product_naam} bedraagt {self.__aantal}")

    def toon_mutaties(self):
        print(f"\nMutatie-geschiedenis voor {self._product_naam}:")
        for datum, aantal in self._mutatie_geschiedenis:
            if aantal > 0:
                mutatie_type = "bijbesteld"
            else:
                mutatie_type = "verkocht"
                aantal = abs(aantal)
            print(f"  {datum}: {aantal} {mutatie_type}")
```

## Testen

Nu is het tijd om de voorraad te testen!

```python
laptop_voorraad = Voorraad("Laptop", 10)
laptop_voorraad.bijbestellen(5)
laptop_voorraad.verkoop(3)
laptop_voorraad.verkoop(7)
laptop_voorraad.bijbestellen(10)
laptop_voorraad.toon_mutaties()
```

Dit geeft de volgende uitvoer:

```console
Voorraad aangemaakt voor Laptop
Voorraad Laptop bedraagt 15
Voorraad Laptop bedraagt 12
Voorraad Laptop bedraagt 5
Voorraad Laptop bedraagt 15

Mutatie-geschiedenis voor Laptop:
  2026-01-31 14:23:15: 5 bijbesteld
  2026-01-31 14:23:15: 3 verkocht
  2026-01-31 14:23:15: 7 verkocht
  2026-01-31 14:23:16: 10 bijbesteld
```

## Private versus Protected attributen

Je ziet in de code dat we twee soorten underscores gebruiken:

- **Enkele underscore** (`_product_naam`): Dit is een *conventie* in Python om aan te geven dat een attribuut "protected" is. Het is bedoeld voor intern gebruik maar is nog steeds toegankelijk van buitenaf.
- **Dubbele underscore** (`__aantal`): Dit triggert Python's *name mangling* mechanisme, waardoor het attribuut moeilijker direct toegankelijk wordt van buitenaf.

Laten we dit demonstreren:

```python
laptop_voorraad = Voorraad("Laptop", 10)

# Dit werkt (protected met enkele underscore):
print(laptop_voorraad._product_naam)  # Output: Laptop

# Dit werkt NIET (private met dubbele underscore):
print(laptop_voorraad.__aantal)  # AttributeError!
```

Het tweede voorbeeld geeft een foutmelding:

```console
AttributeError: 'Voorraad' object has no attribute '__aantal'
```

Python heeft het attribuut `__aantal` hernoemd naar `_Voorraad__aantal` (name mangling) om directe toegang te voorkomen. Dit is Python's manier om attributen meer "private" te maken, hoewel ze technisch gezien nog steeds toegankelijk zijn via `laptop_voorraad._Voorraad__aantal`.

## Waarom inkapseling?

Inkapseling heeft verschillende voordelen:

1. **Controle**: Je kunt validatie toevoegen (zoals in `verkoop()` waar we checken of er genoeg voorraad is)
2. **Flexibiliteit**: Je kunt later de interne implementatie aanpassen zonder de interface te wijzigen
3. **Beveiliging**: Je voorkomt dat gebruikers per ongeluk of opzettelijk ongeldige waarden instellen

In het volgende deel gaan we kijken naar getters en setters, en hoe we de `@property` decorator kunnen gebruiken voor elegantere toegang tot private attributen.

## Samenvatting

In dit deel hebben we geleerd over:

- Inkapseling als OOP-principe
- Het verschil tussen `_` (protected) en `__` (private) attributen
- Het gebruik van `@staticmethod` voor klassemethoden
- Het bijhouden van een geschiedenis met tijdstempels
- Het valideren van input in methoden

In het volgende deel gaan we kijken naar meerdere klassen die met elkaar samenwerken.
