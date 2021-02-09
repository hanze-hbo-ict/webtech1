# OOP Python – Overriding en polymorfisme

## Overriding

Binnen subklassen kunnen methodes ingebouwd worden die dezelfde naam hebben als methodes in hun super-klasse. Hun gedrag wordt hier nu onderzocht. Het komt al voor in de code (zie de methodes `schade()`) maar het kan geen kwaad nog een extra voorbeeld te tonen. En dan wordt de beginregel `import  random` ook eindelijk benut.

In de klasse `Uruk_Hai` (een subklasse van `Ork`) wordt een tweede methode opgezet met de naam `dodges()`. Een bekend spel in de USA is dodgeball, in Nederland *trefbal* genoemd. Het idee van het spel is te duiken (de letterlijke vertaling van dodge) om een treffer te voorkomen. Daarom wordt het `dodges()`.

```python
def dodges(self):
    if random.randint(1, 3) == 3:
        print("***** {0.name} dodges *****".format(self))
        return True
    else:
        return False
```

De test:

```python
lurtz = Uruk_Hai("Lurtz")
print(lurtz)
lurtz.schade(14)
print(lurtz)

while lurtz._levend:
    lurtz.schade(5)
print(lurtz)
```

Het resultaat hiervan:

```shell
Naam: Lurtz, Levens: 3, Hit points: 12
***** Lurtz dodges *****
Naam: Lurtz, Levens: 3, Hit points: 12
Je bent 5 keer geraakt en hebt nog 7 hit points over
Je bent 5 keer geraakt en hebt nog 2 hit points over
Lurtz heeft een leven verloren
Lurtz heeft een leven verloren
Lurtz is dood
```

De eerste aanval kan Lurtz nog ontwijken. Random zou deze Uruk_Hai één van de drie pogingen moeten kunnen ontwijken. Maar verder zijn er nog zaken die niet optimaal functioneren. Onder meer worden de hit points niet bijgewerkt als er een leven verloren is gegaan. Dan zou verholpen kunnen worden in de methode `schade()` uit de klasse `Aardman`.

Nu wordt er een tweede methode `schade()` gebouwd en toegevoegd aan de klasse `Uruk_Hai`.

```python
def schade(self, geraakt):
    if not self.dodges():
        super().schade(geraakt=geraakt)
```

Wanneer de testset na deze aanpassing nogmaals wordt uitgevoerd, wordt eerst gekeken of de methode voorkomt in de klasse `Uruk_Hai` en zo niet in de klasse erboven, en dat is de klasse `Aardman`. Lurtz krijgt als er een leven verloren is, weer 12 hit points uitgereikt.

```shell
Naam: Lurtz, Levens: 3, Hit points: 12
Lurtz heeft een leven verloren
Naam: Lurtz, Levens: 2, Hit points: 12
Je bent 5 keer geraakt en hebt nog 7 hit points over
Je bent 5 keer geraakt en hebt nog 2 hit points over
Lurtz heeft een leven verloren
***** Lurtz dodges *****
***** Lurtz dodges *****
***** Lurtz dodges *****
Je bent 5 keer geraakt en hebt nog 7 hit points over
***** Lurtz dodges *****
Je bent 5 keer geraakt en hebt nog 2 hit points over
***** Lurtz dodges *****
Lurtz is dood
```

## Polymorfisme

Het woord *polymorfisme* is samengesteld uit twee Griekse woorden: *polus* (πολύς, wat 'veel' betekent) en *morphè* (μορφή, wat 'vorm' betekent). Iets wat polymorf is, kan dus veel (verschillende) vormen aannemen. In de informatica wil dat zeggen dat een methode met dezelfde *naam* (*signature*) verschillende *vormen* kan hebben. Je kunt dus verschillende methoden op dezelfde manier aanspreken, afhankelijk van de klasse die deze methode implementeert.

Een tweetal voorbeelden. Bekijk onderstaande code:

```python
a =3
b = "tim"
c = 1, 2, 3

print(a)
print(b)
print(c)
```

Het resultaat hiervan is niet zo heel spannend:

```shell
3
tim
(1, 2, 3)
```

Python heeft er geen enkele moeite mee om meerdere verschillende typen objecten (hier: `int`, `string` en `tuple`) naar het scherm te schrijven. Dat komt omdat alle typen kunnen beschikken over de methode `__str__()`. Dat wil aangeven dat hier sprake is van polymorfisme. De functie `print()` kan in vele situaties succesvol toegepast worden.

Een tweede en waarschijnlijk meer aansprekend voorbeeld. Er is zelfs [een pagina in Wikipedia](https://nl.wikipedia.org/wiki/Duck-typing) aan gewijd, de ducktest. De ducktest is een gedachtegang en retorisch middel in de vorm van een inductieve redenering. De redeneerwijze is als volgt te omschrijven:

"Als iets eruitziet als een eend, zwemt als een eend en kwaakt als een eend, dan is het waarschijnlijk een eend."

Deze 'test' benoemt een categorie, in dit geval de categorie 'ducks' en maakt dan aannemelijk dat een bepaald fenomeen tot die categorie behoort. De 'test' onderzoekt of bewijst niets, maar wijst op overeenkomsten. Prima om hiermee polymorfisme te bespreken. Bekijk het bestand [`duck.py`](../bestanden/ducks.py).

De klasse `Duck` kent een drietal methoden.

```python
class Duck:
    def lopen(self):
        print("Waggel, waggel, waggel")

    def zwemmen(self):
        print("Kom er lekker in, het water is heerlijk")

    def kwaken(self):
        print("Kwak, kwak, kwak")
```

Een test naar de werking door een object aan te maken en de methodes aan te roepen. Voor het aanroepen van de verschillende functies wordt een definitie aangemaakt.

```python
def test_duck(duck):
    duck.lopen()
    duck.zwemmen()
    duck.kwaken()
```

Wat is er nu logischer dan om als object uit de klasse `Duck` een ‘Donald’ te nemen?

```python
if __name__ == '__main__':
    donald = Duck()
    test_duck(donald)
```

Ook hier is de uitkomst niet per se heel spannend:

```python
Waggel, waggel, waggel
Kom er lekker in, het water is heerlijk
Kwak, kwak, kwak
```

Nu maken we een tweede klasse `Pinguin` met exact dezelfde methoden – althans, wat de *namen* (*signatures*) betreft:

```python
class Pinguin:

    def lopen(self):
        print("Waggel, waggel, ik waggel ook")

    def zwemmen(self):
        print("Kom er in, maar het is wel een beetje koud, zo zuidelijk")

    def kwaken(self):
        print("Kwaken? Lachen, ik ben een pinquin, hoor!")
```

Het beest krijgt de naam ‘percy’ mee en we laten hem ook de duck-test ondergaan.

```python
percy = Pinguin()
test_duck(percy)
```

Wat blijkt? Moeiteloos!

```shell
Waggel, waggel, ik waggel ook
Kom er in, maar het is wel een beetje koud, zo zuidelijk
Kwaken? Lachen, ik ben een pinquin, hoor!
```

Dit is een mooi voorbeeld van polymorfisme. Je hebt twee compleet verschillende implementaties (één voor een eend, één voor een pinguin) die je toch op exact dezelfde manier kunt aanspreken (we gebruiken in beide gevallen dezelfde methode `test_duck`). De drie methoden hebben dus verschillende vormen, waarbij de concrete vorm afhangt van de implementerende klasse (`Duck` of `Pinguin`).

Er is nog (heel veel) meer te zeggen over polymorfisme; [check eventueel de wiki-pagina hierover](https://nl.wikipedia.org/wiki/Polymorfisme_(informatica)). Voor nu is het voldoende als je weet dat dit bestaat – in een later stadium komen we hier nog uitgebreid op terug.
