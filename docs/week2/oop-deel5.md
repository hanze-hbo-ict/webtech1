# OOP Python – Overerving

Overerving is een mechanisme waarmee het probleem van gedupliceerde code opgelost kan worden. Het concept is eenvoudig. Stel je voor dat we een model willen maken van verschillende typen volgens. Dan kun je je voorstellen dat dat model er bijvoorbeeld als volgt uit zou komen te zien:

Aan het eind van deze tekst maken we [oefening nummer 2](oefeningen/oop-oefening2.md)

![Plaatje van overerving](imgs/klasse-diagram.png)

## Het principe van overerving

Deze afbeelding laat het principe van overerving duidelijk zijn. Op het plaatje zijn allemaal vogels te zien. Een kenmerk van alle vogels is dat zij allen een snavel hebben en vleugels. De kenmerken die voor alle vogels gelden, worden zoveel mogelijk centraal vastgelegd, hier dus in de klasse `VOGEL`.

Daarna is er een tweedeling te zien tussen vogels die kunnen vliegen en vogels die die capaciteit niet beheersen. Alle vogels die kunnen vliegen bezitten de methode `vlieg()`. Deze methode wordt zo hoog mogelijk in de hiërarchie opgeslagen, hier in `VLIEGEND`. De vogels die niet kunnen vliegen hebben blijkbaar geen gemeenschappelijke methode. De struisvogel kan hardlopen (`ren()`) en de pinguïn kan zwemmen (`zwem()`). Omdat er dus allemaal individuele methoden zijn worden ze in de klasse zelf opgeslagen.

Dat levert het volgende overzicht op:

Term | Omschrijving
---|---
Overerving | Het definiëren van een klasse als uitbreiding van een andere klasse.
Superklasse | Een klasse die uitgebreid wordt door een andere klasse.
Subklasse | Een klasse die een uitbreiding erft van een andere klasse. Een subklasse erft alle attributen en methoden van de bijbehorende superklasse.

Zo is `VOGEL` een superklasse van `VLIEGEND` en is `VLIEGEND` en subklasse van `VOGEL`. Maar `VLIEGEND` is tegelijkertijd een superklasse van `ADELAAR`, `KRAAI` en `MEEUW`. Super- en subklasse is een transitieve eigenschap: `VOGEL` is ook een superklasse van `KRAAI`.

De onderste drie (3) klassen erven van de bovenliggende klassen en zij kunnen in ieder geval beschikken over de attributen snavel en vleugels en ook over de methode `vlieg()`.

## De klasse `Aardman`

Verder met het project `Game`. Dit project staat nog in de kinderschoenen en kent momenteel twee files, [`main.py`](../bestanden/game/main.py) (waarmee we de code runnen) en [`Speler.py`](../bestanden/game/speler.py). Daar wordt een derde file aan toegevoegd met de naam [`aardman.py`](../bestanden/game/aardman.py). Daarin wordt als eerste een superklasse, `Aardman`, aangemaakt. Het is de bedoeling in dit spel monsters en trollen uit te schakelen. In deze klasse worden hit-points en levens bijgehouden en of de tegenstander nog in leven is.

!!! Info "Werken vanuit een bestand"
    Vanaf nu werken we met het bestand `main.py` om de werking van de code te demonstreren. Dat is directer en makkelijker dan telkens alles in de interactieve shell opnieuw in te laden. Probeer dit voor je eigen project ook op deze manier te doen.

De basis van de klasse `Aardman`:

```python
import random

class Aardman:

    def __init__(self, naam="Aardman", hit_points=0, levens=1):
        self._naam = naam
        self._hit_points = hit_points
        self._levens = levens
        self._levend = True
```

Er wordt nog een tweede methode toegevoegd `schade()`. Het aantal keer dat een tegenstander geraakt is door vijandig vuur, wordt van de `hit_points` afgetrokken. Komt dat aantal onder nul (0), is deze vijand een leven kwijt.

```python
def schade(self,geraakt):
    punten_over = self._hit_points - geraakt
    if punten_over >= 0:
        self._hit_points = punten_over
        print("Je bent {} keer geraakt en hebt nog {} hit points over".format(geraakt, self._hit_points))
    else:
        self._levens -= 1
```

Voor de mooi nog even de `__str__()`-methode.

```python
def __str__(self):
    return "Naam: {0._naam}, Levens: {0._lives}, Hit points: {0._hit_points}".format(self)
```

Om te testen vullen we de onderstaande code in in `main.py`:

```python
from aardman import Aardman

random_aardman = Aardman("Aardman", 12, 1)
print(random_aardman)

random_aardman.schade(4)
print(random_aardman)

random_aardman.schade(8)
print(random_aardman)

random_aardman.schade(9)
print(random_aardman)
```

Wanneer we dit runnen, krijgen we het volgende resultaat:

```shell
Naam: Aardman, Levens: 1, Hit points: 12
Je bent 4 keer geraakt en hebt nog 8 hit points over
Naam: Aardman, Levens: 1, Hit points: 8
Je bent 8 keer geraakt en hebt nog 0 hit points over
Naam: Aardman, Levens: 1, Hit points: 0
Naam: Aardman, Levens: 0, Hit points: 12
```

## De klasse `Ork`

Het is tot nu toe alleen mogelijk om een enkele aardman aan te maken, en dat is niet uitdagend genoeg. Er kunnen meerdere types gecreëerd worden om het spel interessanter te maken. De Orks (Lord of the Rings) vormen een groep aardmannen. Dat wordt de eerste subklasse: let op de wijze waarop we aangeven dat `Ork` een subklasse is van `Aardman`.

```python hl_lines="1"
class Ork(Aardman):
    pass
```

Een beetje apart om een commando op te nemen in de definitie van een klasse dat niets doet. Het commando `pass` heeft tot doel invulling te zijn op het moment dat er een actie gevraagd wordt, maar er eigenlijk geen reden toe is een actie in de code op te nemen.

Het kenmerkende voor de klasse `Aardman` wordt nu dat het de algemene kenmerken voor alle groepen vijanden als basiscode herbergt, zodat die code niet bij iedere subklasse (iedere tegenstander) hoeft te worden opgenomen. Daarom kunnen de testgegevens voor de klasse `Aardman` verwijderd worden uit `main.py` en vervangen worden door gegevens die naar vijandgroepen verwijzen. Vandaaruit kunnen de benodigde gegevens uit de superklasse aangeroepen worden. Een bekende ork is Shagrat. Dat wordt het eerste object uit de klasse `Ork`.

```python
from aardman import Aardman, Ork

shagrat = Ork()
print(shagrat)
```

Dat levert het volgende resultaat op:

```shell
Naam: Aardman, Levens: 1, Hit points: 0
```


Bij het initialiseren van het object ‘shagrat’ worden geen parameters meegegeven. De klasse `Ork` kent geen methode `__init__()`. Voor de invulling wordt daarom gekeken of de superklasse wel een methode `__init__()` kent, waarvan de attributen gebruikt kunnen worden. Die is er dus worden de default waarden van de klasse `Aardman` aan dit object uit de klasse `Ork` toegewezen.

Er wordt een tweede object uit de klasse `Ork` aangemaakt, Gorbag, nu wel met de benodigde parameters erbij en een nette lay-out.

```python
gorbag = Ork("Gorbag", 18, 1)
print("Gorbag - {}".format(gorbag))
```

De volgorde van de parameters klopt niet helemaal, maar Python snapt de bedoeling.

```shell
Gorbag - Naam: Gorbag, Levens: 1, Hit points: 18
```

Een derde object, nu met gedeeltelijke parameters.

```python
duergar = Aardman("Duergar", 23)
print(duergar)
```

Resultaat:

```shell
Naam: Duergar, Levens: 1, Hit points: 23
```

Er worden een tweetal parameters meegegeven en de derde wordt opgehaald uit de superklasse, vandaar dat ‘Levens: 1’ ook in beeld verschijnt.

Het is niet handig dit allemaal te regelen via de `__init__()` van de superklasse. De klasse `Ork` zou zelf ook een `__init__` moeten hebben. Dat om iedere groep tegenstanders een ander aantal levens en een ander aantal hit points te mee te geven aan het begin.  We passen de klasse `Ork` dus aan met de volgende constructor:

```python
def __init__(self, naam):
    super().__init__(naam=naam, levens=1, hit_points=23)
```

Iedere object van de klasse `Ork` krijgt nu de attributen mee die meegegeven zijn in de `__init__`. De enige parameter die gevuld moet zijn is de naam, de rest wordt automatisch toegekend. De aanroep `super().__init__()` zorgt ervoor dat er een actie wordt uitgevoerd, waarbij de methode `__init__` uit de klasse `Aardman` wordt aangeroepen. De gegevens worden dan vastgelegd in de attributen, waarna de methode `__str__()` uitgevoerd wordt.

## Extra eigenschappen in de subklasse

Het is ook mogelijk extra eigenschappen bij een subklasse in te bouwen. Als voorbeeld een methode voor de klasse `Ork`.

```python
def slaan(self):
    print("Me {0._naam}. {0._naam} stomp you".format(self))
```

Als we deze methode aan `main.py` toevoegen, krijgen we het resultaat dat eronder staat:

```python
gorbag.slaan()
```

Resultaat:

```shell
Me Gorbag. Gorbag stomp you!
```

Deze methode is alleen beschikbaar voor de objecten uit de klasse `Ork`. Een object uit de klasse `Aardman` kan deze methode niet benaderen.

Maak nu [oefening nummer 2](oefeningen/oop-oefening2.md)

