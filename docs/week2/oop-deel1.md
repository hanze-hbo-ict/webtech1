# OOP Python – inleiding

Tot nu toe hebben we ons gericht op vormgeving van teksten en dergelijke aan de *client-kant* van onze webapplicatie. Om hier *functionaliteit* aan toe te voegen, kunnen we twee dingen doen:

- met behulp van JavaScript programmacode aan de *client-kant* zelf toevoegen, of
- met behulp van een programmeertaal functionaliteit aan de *server-kant* toevoegen en het resultaat daarvan terugsturen naar de client.

Om dit wat nader toe te lichten, herhalen we hier het plaatje uit week 1; bekijk eventueel [de beschrijving daarbij op de betreffende pagina](../week1/1.html/html-deel1.md):

![Client-server architectuur](../week1/1.html/imgs/database-site.png)

Voor deze module hebben we voor de tweede optie gekozen. JavaScript en front-end development komen uitgebreid aan bod in het tweede jaar.

We beginnen met een stukje herhaling over het object-georiënteerde programmeerparadigma in Python.

## Wat is OOP?

Tot nu toe is er geprogrammeerd volgens het imperatieve paradigma. Een programma gemaakt volgens dit principe bestaat uit een groot aantal coderegels die in een bepaalde volgorde geplaatst zijn en waarop de computer verteld wordt hoe deze regels uit te voeren.

OOP (*Object Oriented Programming*) is een programmeerstijl (of *paradigma*) waarbij logische objecten gemaakt worden die methodes (functies, acties of gebeurtenissen) en eigenschappen (waarden) hebben. De bedoeling is dat dit leidt tot meer leesbare en herbruikbare code. Conceptueel bestaat een programma uit objecten die aangemaakt worden en met elkaar interacteren.

Het is niet zo dat beide stijlen onafhankelijk van elkaar functioneren. Binnen OOP wordt gebruikt gemaakt van de imperatieve coderingswijze en bij het imperatieve paradigma komen objecten regelmatig voor, zonder dat een gebruiker er vaak weet van heeft. 

## Klasse-definitie

Om te beginnen een simpel voorbeeld om het principe van klassen en methoden uit te leggen. Het draait om kroketten (Kwekkeboom en Van Dobben) en het aanzetten van de frituur (`kroket.py`).

```
class Kroket(object):
```

Een klasse wordt gedefinieerd door het woord `class`, gevolgd door de naam van de klasse, beginnend met een hoofdletter. De klassedefinitie wordt afgesloten met een dubbele punt (`:`).

Nu is het de beurt om aan te geven uit welke attributen of eigenschappen deze class bestaat.

```
def __init__(self, leverancier, prijs):
    self.leverancier = leverancier
    self.prijs = prijs
    self.trek = False
```

Het zijn er drie (3), `leverancier`, `prijs` en `trek`. Bij `trek = True` wordt de kroket ondergedompeld in het vet. De notatie `self` lijkt nu nog wat vreemd, maar dat went snel; zie eventueel [deze blogpost](https://www.geeksforgeeks.org/self-in-python-class/) voor meer informatie rondom `self`.

Nu de klasse is gedefinieerd kunnen we er objecten van maken – een ander woord voor hiervoor is *instantie*: we maken *instanties* van de klasse `Kroket`:

```
kwek = Kroket("Kwekkeboom", 2.50)
```

Er is een object aangemaakt met de naam `kwek`. Bij het aanmaken van deze nieuwe instantie is de invulling van twee eigenschappen verplicht. In de definitie van de klasse wordt gevraagd om `leverancier` en `prijs`, dus deze twee waarden moeten opgegeven worden. Gebeurt dat niet, verschijnt er een foutmelding. Dus deze coderegel wil zeggen dat er een instantie (`kwek`) is aangemaakt voor de klasse (`Kroket`) waarbij leverancier (`Kwekkeboom`) en prijs (`2.50`) als verplichte waarden worden meegegeven. De inhoud van de waarden van de velden van de instantie `kwek` kunnen ook getoond worden:

```
print(kwek.leverancier)
print(kwek.prijs)
```

Uiteraard kunnen er meerdere objecten bij deze klasse worden aangemaakt. Een tweede firma die kroketten verkoopt is Van Dobben.

```
dob = Kroket("Van Dobben", 2.35)
```

De gegevens van beide objecten kunnen ook gecombineerd worden getoond.

```
print("Fabrikanten: {} = {}, {} = {}"
    .format(kwek.leverancier, kwek.prijs, dob.leverancier, dob.prijs))
```

Uitkomst:

![Meerdere objecten](img/../imgs/kroketten.png)

Voor de overzichtelijkheid eerst een aantal beschrijvingen:


Term | Omschrijving
-----|------
Klasse | 	template, sjabloon voor het maken van objecten; alle objecten die met dezelfde klasse zijn gemaakt, hebben dezelfde kenmerken.
Object | 	een instantie van een klasse.
Initialisatie | 	een nieuw object van een klasse.
Methode | een functie gedefinieerd in een klasse.
Attribuut | een variabele die is gebonden aan een object van een klasse.

## Kroketten in het vet 

De code wordt uitgebreid met een tweede methode `in_frituur()`. 
Het woord `self` moet je altijd aan een methode-definitie toevoegen, zelfs wanneer de methode zelf verder helemaal geen parameters heeft.

Deze methode laat de frituur weten dat er moet gebakken worden. De waarde van trek wijzigt naar `True`.

```
def in_frituur(self):
    self.trek = True
```

Een testje voor de Van Dobben kroket’:

```
print(dob.trek)
dob.in_frituur()
print(dob.trek)
```

Resultaat:

![De Van-Dobbenkroket in het vet](imgs/in_het_vet.png)

Bij het aanmaken van het object `dob` is de status `False` meegegeven. Het aanroepen van de methode `in_frituur()` zorgt er voor dat trek de status `True` krijgt.

Vaak zijn er meerdere opties het gewenste resultaat te bereiken. Ook hier, alleen nu voor het object `kwek`:

```
Kroket.in_frituur(kwek)  # optie 1
kwek.in_frituur()        # optie 2
```

## Constructors

Nog een belangrijk begrip bij het werken met OOP betreft de `constructor`. Deze worden gebruikt om een object op de juiste manier in te stellen wanneer het wordt aangemaakt. 

In Python heeft een constructor altijd de vorm `__init__(self)`. Eventueel kun je ook meerdere parameters aan de constructor meegeven; die geef je dan aan achter de standaard-parameter `self`.

!!! info "Dunder-methoden"
    Zoals je ziet heeft de `constructor` een opvallende vorm; hij wordt omgeven door twee liggende streepjes, `__`. Python kent meer van dergelijke methoden, zoals `__repr__`, `__len__`, enzovoort. Dit zijn methoden die op specifieke momenten dooor Python worden aangeroepen; bijvoorbeeld wanneer je een object *aannmaakt* (`__init__`), een object wilt *uitprinten* (`__repr__`), of de *lengte* van een object wilt weten (`__len__`).

    Dergelijke methoden worden *dunder-methods* genoemd – van *double underscore*.

Het is ook mogelijk om *object* extra eigenschappen mee te geven nadat deze is geïnitialiseerd. Dit kun je doen door gewoon een eigenschap te definiëren en daar een waarde aan toe te kennen. Dit is dan wel een eigenschap die *alleen* voor het specifieke object geldt en niet wordt doorgegeven aan andere objecten van dezelfde klasse.

Als voorbeeld geven we hieronder een extra attribuut `waardering` aan het object `kwek`. Je zult zien dat deze eigenschap niet eveneens beschikbaar is bij het object `dob`:

```
kwek.waardering = 6.5
print(kwek.waardering)
print(dob.waardering)
```

Als je dit runt, krijg je eerst 6.5 te zien – de waardering die we zojuist hebben toegevoegd. Deze wordt onmiddellijk gevolgd door een foutmelding.

```
6.5
Traceback (most recent call last):
  File "kroket.py", line 20, in <module>
    print(dob.waardering)
AttributeError: 'Kroket' object has no attribute 'waardering'
```

## Klasse-attributen

Naast de attributen die meegegeven worden aan elke nieuwe instantie, is het ook mogelijk de klasse attributen mee te geven:

```
class Kroket(object): 
    soort = "rundvleeskroket"

    #rest van de definitie is weggelaten
```

Met de *dunder* `__dict__` kan bekeken worden wat de specifieke inhoud is van elk object:

```
print(Kroket.__dict__)
print(kwek.__dict__)
print(dob.__dict__)
```

Dit levert het volgende resultaat op;

```
{'__module__': '__main__', 'soort': 'rundvleeskroket', '__init__': <function Kroket.__init__ at 0x109572440>, 'in_frituur': <function Kroket.in_frituur at 0x109572e60>, '__dict__': <attribute '__dict__' of 'Kroket' objects>, '__weakref__': <attribute '__weakref__' of 'Kroket' objects>, '__doc__': None}

{'leverancier': 'Kwekkeboom', 'prijs': 2.5, 'trek': False, 'waardering': 6.5}

{'leverancier': 'Van Dobben', 'prijs': 2.35, 'trek': False}
```

De klasse zelf bevat erg veel eigenschappen terwijl de beide objecten alleen de instantievariabelen laten zien, waarbij `kwek` er eentje meer toont, wat logisch is.

Wat zal er gebeuren als de inhoud van het extra attribuut van de klasse zelf gewijzigd wordt?

```
print("Wijzig rundvleeskroket naar groentekroket”)
Kroket.soort = "groentekroket"
print(Kroket.soort)
print(kwek.soort)
print(dob.soort)
```

Het resultaat is niet echt verrassend: de wijziging in de klasse vindt ook z'n weg naar de instanties die van deze klasse zijn gemaakt.

```
Wijzig rundvleeskroket naar groentekroket
groentekroket
groentekroket
groentekroket
```

Nog een laatste test. Is het ook mogelijk voor `kwek` de inhoud van het attribuut van de klasse te wijzigen?

```
print("Kwekkeboom wordt nu garnalenkroket")
kwek.soort = "garnalenkroket"
print(kwek.soort)
```

Met als resultaat:

```
Kwekkeboom wordt nu garnalenkroket
garnalenkroket
```

De uitkomst laat zien dat het specifieke klasse attribuut voor `kwek` is gewijzigd. Het waarom kan uitgelegd worden door te verwijzen naar de terminologie omtrent `global` en `local`. Het klasse-attribuut zal gelden voor *ieder object* tenzij er lokaal bij het object (de instantie) wijzigingen worden doorgevoerd. De werkwijze is altijd zo dat er eerst wordt gekeken welke eigenschappen met het object worden meegegeven en daarna of er ook nog eigenschappen gelden op een hoger niveau.

De inhoud van de eigenschappen op 'lokaal' niveau hebben prioriteit boven de 'globaal' meegegeven attributen.






