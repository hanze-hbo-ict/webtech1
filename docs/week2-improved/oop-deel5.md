# OOP Python – Overerving

Overerving is een mechanisme waarmee het probleem van gedupliceerde code opgelost kan worden. Het concept is eenvoudig. Stel je voor dat we een model willen maken van verschillende typen vogels. Dan kun je je voorstellen dat dat model er bijvoorbeeld als volgt uit zou komen te zien:

Aan het eind van deze tekst maken we [oefening nummer 2](oefeningen/oop-oefening2.md).

![Plaatje van overerving](imgs/klasse-diagram.png)

## Het principe van overerving

Deze afbeelding laat het principe van overerving duidelijk zien. Op het plaatje zijn allemaal vogels te zien. Een kenmerk van alle vogels is dat zij allen een snavel hebben en vleugels. De kenmerken die voor alle vogels gelden, worden zoveel mogelijk centraal vastgelegd, hier dus in de klasse `VOGEL`.

Daarna is er een tweedeling te zien tussen vogels die kunnen vliegen en vogels die die capaciteit niet beheersen. Alle vogels die kunnen vliegen bezitten de methode `vlieg()`. Deze methode wordt zo hoog mogelijk in de hiërarchie opgeslagen, hier in `VLIEGEND`. De vogels die niet kunnen vliegen hebben blijkbaar geen gemeenschappelijke methode. De struisvogel kan hardlopen (`ren()`) en de pinguïn kan zwemmen (`zwem()`). Omdat er dus allemaal individuele methoden zijn worden ze in de klasse zelf opgeslagen.

Dat levert het volgende overzicht op:

Term | Omschrijving
---|---
Overerving | Het definiëren van een klasse als uitbreiding van een andere klasse.
Superklasse | Een klasse die uitgebreid wordt door een andere klasse.
Subklasse | Een klasse die een uitbreiding erft van een andere klasse. Een subklasse erft alle attributen en methoden van de bijbehorende superklasse.

Zo is `VOGEL` een superklasse van `VLIEGEND` en is `VLIEGEND` en subklasse van `VOGEL`. Maar `VLIEGEND` is tegelijkertijd een superklasse van `ADELAAR`, `KRAAI` en `MEEUW`. Super- en subklasse is een transitieve eigenschap: `VOGEL` is ook een superklasse van `KRAAI`.

De onderste drie (3) klassen erven van de bovenliggende klassen en zij kunnen in ieder geval beschikken over de attributen snavel en vleugels en ook over de methode `vlieg()`.

## De klasse `Product`

We gaan een webshop bouwen. Dit project staat nog in de kinderschoenen en kent momenteel twee files, [`main.py`](bestanden/webshop/main.py) (waarmee we de code runnen) en [`klant.py`](bestanden/webshop/klant.py). Daar wordt een derde file aan toegevoegd met de naam [`product.py`](bestanden/webshop/product.py). Daarin wordt als eerste een superklasse, `Product`, aangemaakt. Het is de bedoeling in deze webshop verschillende producten te verkopen. In deze klasse worden prijs, voorraad en beschikbaarheid bijgehouden.

!!! Info "Werken vanuit een bestand"
    Vanaf nu werken we met het bestand `main.py` om de werking van de code te demonstreren. Dat is directer en makkelijker dan telkens alles in de interactieve shell opnieuw in te laden. Probeer dit voor je eigen project ook op deze manier te doen.

De basis van de klasse `Product`:

```python
class Product:

    def __init__(self, naam="Product", prijs=0.0, voorraad=0):
        self._naam = naam
        self._prijs = prijs
        self._voorraad = voorraad
        self._beschikbaar = True
```

Er wordt nog een tweede methode toegevoegd `verkoop()`. Het aantal keer dat een product verkocht is, wordt van de `voorraad` afgetrokken. Komt dat aantal onder nul (0), is dit product niet meer beschikbaar.

```python
def verkoop(self, aantal):
    nieuwe_voorraad = self._voorraad - aantal
    if nieuwe_voorraad >= 0:
        self._voorraad = nieuwe_voorraad
        print(f"Verkocht: {aantal}x {self._naam}. Nog {self._voorraad} op voorraad")
    else:
        print(f"Onvoldoende voorraad. Nog maar {self._voorraad} beschikbaar")
        self._beschikbaar = False
```

Voor de mooi nog even de `__str__()`-methode.

```python
def __str__(self):
    return f"Product: {self._naam}, Prijs: €{self._prijs:.2f}, Voorraad: {self._voorraad}"
```

Om te testen vullen we de onderstaande code in in `main.py`:

```python
from product import Product

basis_product = Product("Laptop", 799.99, 5)
print(basis_product)

basis_product.verkoop(2)
print(basis_product)

basis_product.verkoop(2)
print(basis_product)

basis_product.verkoop(2)
print(basis_product)
```

Wanneer we dit runnen, krijgen we het volgende resultaat:

```console
Product: Laptop, Prijs: €799.99, Voorraad: 5
Verkocht: 2x Laptop. Nog 3 op voorraad
Product: Laptop, Prijs: €799.99, Voorraad: 3
Verkocht: 2x Laptop. Nog 1 op voorraad
Product: Laptop, Prijs: €799.99, Voorraad: 1
Onvoldoende voorraad. Nog maar 1 beschikbaar
Product: Laptop, Prijs: €799.99, Voorraad: 1
```

## De klasse `FysiekProduct`

Het is tot nu toe alleen mogelijk om een enkel generiek product aan te maken, en dat is niet uitdagend genoeg. Er kunnen meerdere types producten gecreëerd worden om de webshop interessanter te maken. Fysieke producten vormen een groep die verzonden moet worden. Dat wordt de eerste subklasse: let op de wijze waarop we aangeven dat `FysiekProduct` een subklasse is van `Product`.

```python hl_lines="1"
class FysiekProduct(Product):
    pass
```

Een beetje apart om een commando op te nemen in de definitie van een klasse dat niets doet. Het commando `pass` heeft tot doel invulling te zijn op het moment dat er een actie gevraagd wordt, maar er eigenlijk geen reden toe is een actie in de code op te nemen.

Het kenmerkende voor de klasse `Product` wordt nu dat het de algemene kenmerken voor alle groepen producten als basiscode herbergt, zodat die code niet bij iedere subklasse (ieder producttype) hoeft te worden opgenomen. Daarom kunnen de testgegevens voor de klasse `Product` verwijderd worden uit `main.py` en vervangen worden door gegevens die naar productgroepen verwijzen. Van daaruit kunnen de benodigde gegevens uit de superklasse aangeroepen worden. Een bekend fysiek product is een boek. Dat wordt het eerste object uit de klasse `FysiekProduct`.

```python
from product import Product, FysiekProduct

python_boek = FysiekProduct()
print(python_boek)
```

Dat levert het volgende resultaat op:

```console
Product: Product, Prijs: €0.00, Voorraad: 0
```

Bij het initialiseren van het object 'python_boek' worden geen parameters meegegeven. De klasse `FysiekProduct` kent geen methode `__init__()`. Voor de invulling wordt daarom gekeken of de superklasse wel een methode `__init__()` kent, waarvan de attributen gebruikt kunnen worden. Die is er dus worden de default waarden van de klasse `Product` aan dit object uit de klasse `FysiekProduct` toegewezen.

Er wordt een tweede object uit de klasse `FysiekProduct` aangemaakt, nu wel met de benodigde parameters erbij en een nette lay-out.

```python
java_boek = FysiekProduct("Java voor beginners", 34.95, 12)
print(f"Boek - {java_boek}")
```

De volgorde van de parameters klopt en Python snapt de bedoeling.

```console
Boek - Product: Java voor beginners, Prijs: €34.95, Voorraad: 12
```

Een derde object, nu met gedeeltelijke parameters.

```python
laptop = Product("MacBook Pro", 1499.99)
print(laptop)
```

Resultaat:

```console
Product: MacBook Pro, Prijs: €1499.99, Voorraad: 0
```

Er worden een tweetal parameters meegegeven en de derde wordt opgehaald uit de superklasse, vandaar dat 'Voorraad: 0' ook in beeld verschijnt.

Het is niet handig dit allemaal te regelen via de `__init__()` van de superklasse. De klasse `FysiekProduct` zou zelf ook een `__init__` moeten hebben. Dat om iedere groep producten andere eigenschappen mee te geven aan het begin. We passen de klasse `FysiekProduct` dus aan met de volgende constructor:

```python
def __init__(self, naam, prijs, voorraad, gewicht=0.0):
    super().__init__(naam=naam, prijs=prijs, voorraad=voorraad)
    self._gewicht = gewicht
```

Ieder object van de klasse `FysiekProduct` krijgt nu de attributen mee die meegegeven zijn in de `__init__`. De eerste drie parameters moeten gevuld zijn, gewicht heeft een standaardwaarde. De aanroep `super().__init__()` zorgt ervoor dat er een actie wordt uitgevoerd, waarbij de methode `__init__` uit de klasse `Product` (de superklasse) wordt aangeroepen. De gegevens worden dan vastgelegd in de attributen, waarna de methode `__str__()` uitgevoerd wordt.

## Extra eigenschappen in de subklasse

Het is ook mogelijk extra eigenschappen bij een subklasse in te bouwen. Als voorbeeld een methode voor de klasse `FysiekProduct`.

```python
def bereken_verzendkosten(self):
    if self._gewicht <= 1.0:
        kosten = 3.95
    elif self._gewicht <= 5.0:
        kosten = 6.95
    else:
        kosten = 9.95
    print(f"Verzendkosten voor {self._naam}: €{kosten:.2f}")
    return kosten
```

Als we deze methode aan `main.py` toevoegen, krijgen we het resultaat dat eronder staat:

```python
java_boek = FysiekProduct("Java voor beginners", 34.95, 12, 0.8)
java_boek.bereken_verzendkosten()
```

Resultaat:

```console
Verzendkosten voor Java voor beginners: €3.95
```

Deze methode is alleen beschikbaar voor de objecten uit de klasse `FysiekProduct`. Een object uit de klasse `Product` kan deze methode niet benaderen.

Maak nu [oefening nummer 2](oefeningen/oop-oefening2.md).
