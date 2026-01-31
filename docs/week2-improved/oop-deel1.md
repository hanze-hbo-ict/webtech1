# OOP Python – inleiding

Tot nu toe hebben we ons gericht op vormgeving van teksten en dergelijke aan de *client-kant* van onze webapplicatie. Om hier *functionaliteit* aan toe te voegen, kunnen we twee dingen doen:

- met behulp van JavaScript programmacode aan de *client-kant* zelf toevoegen, of
- met behulp van een zogenaamde backend-programmeertaal functionaliteit aan de *server-kant* toevoegen en het resultaat daarvan terugsturen naar de client.

Om dit wat nader toe te lichten, herhalen we hier het plaatje uit week 1; bekijk eventueel [de beschrijving daarbij op de betreffende pagina](../week1/1.html/html-deel1.md):

![Een site met een database](../week1/1.html/imgs/database-site.png)

Voor deze module hebben we voor de tweede optie gekozen. JavaScript en front-end development komen uitgebreid aan bod in het tweede jaar.

We beginnen met een stukje herhaling over het object-georiënteerde programmeerparadigma in Python.

## Wat is OOP?

Tot nu toe is er geprogrammeerd volgens het imperatieve paradigma. Een programma gemaakt volgens dit principe bestaat uit een groot aantal coderegels die in een bepaalde volgorde geplaatst zijn en waarop de computer verteld wordt hoe deze regels uit te voeren.

OOP (*Object Oriented Programming*) is een programmeerstijl (of *paradigma*) waarbij logische objecten gemaakt worden die methodes (functies, acties of gebeurtenissen) en eigenschappen (waarden) hebben. De bedoeling is dat dit leidt tot herbruikbare en beter leesbare programmacode. Conceptueel bestaat een programma uit objecten die aangemaakt worden en met elkaar interacteren.

Het is niet zo dat beide stijlen onafhankelijk van elkaar functioneren. Binnen OOP wordt gebruikt gemaakt van de imperatieve coderingswijze en bij het imperatieve paradigma komen objecten regelmatig voor, zonder dat een gebruiker er vaak weet van heeft.

## Klasse-definitie

Om te beginnen een simpel voorbeeld om het principe van klassen en methoden uit te leggen. We bouwen een eenvoudige webshop waarbij we producten kunnen beheren. Bekijk het bestand [`product.py`](bestanden/webshop/product.py).

```ipython
In [1]: class Product:
   ...:
```

Een klasse wordt gedefinieerd door het woord `class`, gevolgd door de naam van de klasse, beginnend met een hoofdletter. De klassedefinitie wordt afgesloten met een dubbele punt (`:`).

Nu is het de beurt om aan te geven uit welke attributen of eigenschappen deze class bestaat. Dit geven we mee aan de methode die aangeroepen wordt wanneer er een object van een klasse wordt aangemaakt: de zogenaamde *constructor*. In Python is deze methode `__init__` (we komen daar zo wat uitgebreider op terug):

```ipython
   ...:     def __init__(self, naam="Product", prijs=0.0, voorraad=0):
   ...:         self._naam = naam
   ...:         self._prijs = prijs
   ...:         self._voorraad = voorraad
   ...:         self._beschikbaar = True
   In [2]:
```

Het zijn er vier (4): `naam`, `prijs`, `voorraad` en `beschikbaar`. De eigenschap `beschikbaar` krijgt automatisch de waarde `True` bij het aanmaken van een product. De notatie `self` lijkt nu nog wat vreemd, maar dat went snel; zie eventueel [deze blogpost](https://www.bartbarnard.nl/programmeerblogs/python/self.html) voor meer informatie rondom `self`.

Nu de klasse is gedefinieerd kunnen we er objecten van maken – een ander woord voor hiervoor is *instantie*: we maken *instanties* van de klasse `Product`:

```ipython
In [2]: laptop = Product("Laptop", 799.99, 5)
```

Er is een object aangemaakt met de naam `laptop`. Bij het aanmaken van deze nieuwe instantie is de invulling van drie eigenschappen verplicht. In de definitie van de klasse wordt gevraagd om `naam`, `prijs` en `voorraad`, dus deze drie waarden moeten opgegeven worden. Gebeurt dat niet, verschijnt er een foutmelding. Dus deze coderegel wil zeggen dat er een instantie (`laptop`) is aangemaakt voor de klasse (`Product`) waarbij naam (`Laptop`), prijs (`799.99`) en voorraad (`5`) als verplichte waarden worden meegegeven. De inhoud van de waarden van de velden van de instantie `laptop` kunnen ook getoond worden:

```ipython
In [4]: laptop._naam
Out[4]: 'Laptop'

In [5]: laptop._prijs
Out[5]: 799.99

In [6]:
```

Uiteraard kunnen er meerdere objecten bij deze klasse worden aangemaakt. Een tweede product is bijvoorbeeld een boek.

```ipython
In [6]: python_boek = Product("Python Crash Course", 34.95, 12)
```

De gegevens van beide objecten kunnen ook gecombineerd worden getoond.

```ipython
In [7]: print(f"Producten: {laptop._naam} = €{laptop._prijs}, {python_boek._naam} = €{python_boek._prijs}")
Producten: Laptop = €799.99, Python Crash Course = €34.95

In [8]:
```

Voor de overzichtelijkheid eerst een aantal beschrijvingen:

Term | Omschrijving
-----|------
Klasse | template, sjabloon voor het maken van objecten; alle objecten die met dezelfde klasse zijn gemaakt, hebben dezelfde kenmerken.
Object | een instantie van een klasse.
Initialisatie | een nieuw object van een klasse.
Methode | een functie gedefinieerd in een klasse.
Attribuut | een variabele die is gebonden aan een object van een klasse.

## Producten verkopen

We breiden de definitie van `Product` uit met een tweede methode `verkoop()`. Het woord `self` moet je altijd aan een methode-definitie toevoegen, zelfs wanneer de methode zelf verder helemaal geen parameters heeft.

Deze methode verkoopt een aantal producten en past de voorraad aan. De waarde van `_beschikbaar` wijzigt naar `False` wanneer de voorraad niet toereikend is.

```python
def verkoop(self, aantal):
    """Verkoop een aantal items van dit product"""
    nieuwe_voorraad = self._voorraad - aantal
    if nieuwe_voorraad >= 0:
        self._voorraad = nieuwe_voorraad
        print(f"Verkocht: {aantal}x {self._naam}. Nog {self._voorraad} op voorraad")
    else:
        print(f"Onvoldoende voorraad. Nog maar {self._voorraad} beschikbaar")
        self._beschikbaar = False
```

De volledige klasse ziet er nu als volgt uit:

```python
class Product:
    """Basisklasse voor alle producten in de webshop"""

    def __init__(self, naam="Product", prijs=0.0, voorraad=0):
        self._naam = naam
        self._prijs = prijs
        self._voorraad = voorraad
        self._beschikbaar = True

    def verkoop(self, aantal):
        """Verkoop een aantal items van dit product"""
        nieuwe_voorraad = self._voorraad - aantal
        if nieuwe_voorraad >= 0:
            self._voorraad = nieuwe_voorraad
            print(f"Verkocht: {aantal}x {self._naam}. Nog {self._voorraad} op voorraad")
        else:
            print(f"Onvoldoende voorraad. Nog maar {self._voorraad} beschikbaar")
            self._beschikbaar = False
```

Tijd voor de test! We maken een nieuw product en verkopen er een aantal:

```python
laptop = Product("Laptop", 799.99, 5)
laptop.verkoop(2)
```

En de uitkomst:

```console
Verkocht: 2x Laptop. Nog 3 op voorraad
```

## Een mooiere weergave met `__str__()`

Het kan handig zijn als we een product netjes kunnen printen. Daarvoor gebruiken we de speciale methode `__str__()`:

```python
def __str__(self):
    return f"Product: {self._naam}, Prijs: €{self._prijs:.2f}, Voorraad: {self._voorraad}"
```

Nu kunnen we eenvoudig een product weergeven:

```python
laptop = Product("Laptop", 799.99, 5)
print(laptop)
```

Resultaat:

```console
Product: Laptop, Prijs: €799.99, Voorraad: 5
```

## Testen van meerdere verkopen

Laten we nu meerdere verkopen uitvoeren om te zien hoe de voorraad wordt bijgehouden:

```python
laptop = Product("Laptop", 799.99, 5)
print(laptop)

laptop.verkoop(2)
print(laptop)

laptop.verkoop(2)
print(laptop)

laptop.verkoop(2)  # Dit zal niet lukken - onvoldoende voorraad!
print(laptop)
```

Resultaat:

```console
Product: Laptop, Prijs: €799.99, Voorraad: 5
Verkocht: 2x Laptop. Nog 3 op voorraad
Product: Laptop, Prijs: €799.99, Voorraad: 3
Verkocht: 2x Laptop. Nog 1 op voorraad
Product: Laptop, Prijs: €799.99, Voorraad: 1
Onvoldoende voorraad. Nog maar 1 beschikbaar
Product: Laptop, Prijs: €799.99, Voorraad: 1
```

Perfect! Onze product-klasse houdt netjes de voorraad bij en waarschuwt wanneer er niet genoeg producten beschikbaar zijn.

## Samenvatting

In dit deel hebben we kennisgemaakt met:

- Het definiëren van een klasse met `class`
- De constructor `__init__()` om objecten te initialiseren
- Attributen (eigenschappen) van een klasse
- Methoden (functies binnen een klasse)
- Het aanmaken van instanties (objecten)
- De speciale methode `__str__()` voor nette weergave

In het volgende deel gaan we dieper in op het beschermen van attributen met getters en setters.
