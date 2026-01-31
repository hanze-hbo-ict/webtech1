# OOP Python – Overriding en polymorfisme

## Overriding

Binnen subklassen kunnen methodes ingebouwd worden die dezelfde naam hebben als methodes in hun super-klasse. Hun gedrag wordt hier nu onderzocht. Het komt al voor in de code (zie de methodes `verkoop()`) maar het kan geen kwaad nog een extra voorbeeld te tonen. En dan wordt de beginregel `import random` ook eindelijk benut.

In de klasse `DigitaalProduct` (een subklasse van `Product`) wordt een tweede methode opgezet met de naam `check_licentie()`. Bij digitale producten moet er soms gecontroleerd worden of de licentie nog beschikbaar is voordat de verkoop doorgaat.

```python
import random

def check_licentie(self):
    if random.randint(1, 3) == 3:
        print(f"***** Licentie voor {self._naam} niet beschikbaar *****")
        return False
    else:
        return True
```

De test:

```python
antivirus = DigitaalProduct("Antivirus Premium", 49.99, 10)
print(antivirus)
antivirus.verkoop(3)
print(antivirus)

while antivirus._beschikbaar and antivirus._voorraad > 0:
    antivirus.verkoop(2)
print(antivirus)
```

Het resultaat hiervan:

```console
Product: Antivirus Premium, Prijs: €49.99, Voorraad: 10
***** Licentie voor Antivirus Premium niet beschikbaar *****
Product: Antivirus Premium, Prijs: €49.99, Voorraad: 10
Verkocht: 2x Antivirus Premium. Nog 8 op voorraad
Verkocht: 2x Antivirus Premium. Nog 6 op voorraad
Verkocht: 2x Antivirus Premium. Nog 4 op voorraad
Verkocht: 2x Antivirus Premium. Nog 2 op voorraad
Verkocht: 2x Antivirus Premium. Nog 0 op voorraad
```

De eerste verkooppoging wordt geblokkeerd door een licentieprobleem. Random zou deze poging één van de drie keer moeten blokkeren. Verder zijn er nog zaken die geoptimaliseerd kunnen worden. Bijvoorbeeld zouden we de licentiecheck automatisch willen uitvoeren bij elke verkoop.

Nu wordt er een tweede methode `verkoop()` gebouwd en toegevoegd aan de klasse `DigitaalProduct`.

```python
def verkoop(self, aantal):
    if self.check_licentie():
        super().verkoop(aantal=aantal)
    else:
        print("Verkoop geannuleerd: licentie niet beschikbaar")
```

Wanneer de testset na deze aanpassing nogmaals wordt uitgevoerd, wordt eerst gekeken of de methode voorkomt in de klasse `DigitaalProduct` en zo niet in de klasse erboven (in de klasse `Product`). De licentiecheck wordt nu automatisch uitgevoerd voordat de verkoop plaatsvindt.

```console
Product: Antivirus Premium, Prijs: €49.99, Voorraad: 10
Verkocht: 3x Antivirus Premium. Nog 7 op voorraad
Product: Antivirus Premium, Prijs: €49.99, Voorraad: 7
Verkocht: 2x Antivirus Premium. Nog 5 op voorraad
***** Licentie voor Antivirus Premium niet beschikbaar *****
Verkoop geannuleerd: licentie niet beschikbaar
Verkocht: 2x Antivirus Premium. Nog 3 op voorraad
***** Licentie voor Antivirus Premium niet beschikbaar *****
Verkoop geannuleerd: licentie niet beschikbaar
Verkocht: 2x Antivirus Premium. Nog 1 op voorraad
***** Licentie voor Antivirus Premium niet beschikbaar *****
Verkoop geannuleerd: licentie niet beschikbaar
```

## Polymorfisme

Het woord *polymorfisme* is samengesteld uit twee Griekse woorden: *polus* (πολύς, wat 'veel' betekent) en *morphè* (μορφή, wat 'vorm' betekent). Iets wat polymorf is, kan dus veel (verschillende) vormen aannemen. In de informatica wil dat zeggen dat een methode met dezelfde *naam* (*signature*) verschillende *vormen* kan hebben. Je kunt dus verschillende methoden op dezelfde manier aanspreken, afhankelijk van de klasse die deze methode implementeert.

Een tweetal voorbeelden. Bekijk onderstaande code:

```python
a = 3
b = "tim"
c = 1, 2, 3

print(a)
print(b)
print(c)
```

Het resultaat hiervan is niet zo heel spannend:

```console
3
tim
(1, 2, 3)
```

Python heeft er geen enkele moeite mee om meerdere verschillende typen objecten (hier: `int`, `string` en `tuple`) naar het scherm te schrijven. Dat komt omdat alle typen kunnen beschikken over de methode `__str__()`. Dat wil aangeven dat hier sprake is van polymorfisme. De functie `print()` kan in vele situaties succesvol toegepast worden.

Een tweede en waarschijnlijk meer aansprekend voorbeeld. We gaan kijken naar verschillende betaalmethoden in een webshop. Bekijk het bestand [`betaalmethoden.py`](bestanden/webshop/betaalmethoden.py).

De klasse `Creditcard` kent een drietal methoden.

```python
class Creditcard:
    def valideer(self):
        print("Creditcard nummer wordt gevalideerd...")

    def verwerk_betaling(self, bedrag):
        print(f"€{bedrag:.2f} wordt afgeschreven van creditcard")

    def bevestig(self):
        print("Betaling bevestigd. Transactie afgerond.")
```

Een test naar de werking door een object aan te maken en de methodes aan te roepen. Voor het aanroepen van de verschillende functies wordt een definitie aangemaakt.

```python
def test_betaling(betaalmethode, bedrag):
    betaalmethode.valideer()
    betaalmethode.verwerk_betaling(bedrag)
    betaalmethode.bevestig()
```

We maken een object uit de klasse `Creditcard`:

```python
if __name__ == '__main__':
    visa = Creditcard()
    test_betaling(visa, 99.99)
```

Ook hier is de uitkomst niet per se heel spannend:

```console
Creditcard nummer wordt gevalideerd...
€99.99 wordt afgeschreven van creditcard
Betaling bevestigd. Transactie afgerond.
```

Nu maken we een tweede klasse `iDEAL` met exact dezelfde methoden – althans, wat de *namen* (*signatures*) betreft:

```python
class iDEAL:
    def valideer(self):
        print("Bankrekening wordt geverifieerd...")

    def verwerk_betaling(self, bedrag):
        print(f"€{bedrag:.2f} wordt overgemaakt via iDEAL")

    def bevestig(self):
        print("iDEAL betaling geslaagd!")
```

We maken een object en laten deze ook de betalingstest ondergaan.

```python
ideal_betaling = iDEAL()
test_betaling(ideal_betaling, 49.95)
```

Wat blijkt? Moeiteloos!

```console
Bankrekening wordt geverifieerd...
€49.95 wordt overgemaakt via iDEAL
iDEAL betaling geslaagd!
```

Dit is een mooi voorbeeld van polymorfisme. Je hebt twee compleet verschillende implementaties (één voor creditcard, één voor iDEAL) die je toch op exact dezelfde manier kunt aanspreken (we gebruiken in beide gevallen dezelfde methode `test_betaling`). De drie methoden hebben dus verschillende vormen, waarbij de concrete vorm afhangt van de implementerende klasse (`Creditcard` of `iDEAL`).

We kunnen zelfs een derde betaalmethode toevoegen, zoals PayPal:

```python
class PayPal:
    def valideer(self):
        print("PayPal account wordt gecontroleerd...")

    def verwerk_betaling(self, bedrag):
        print(f"€{bedrag:.2f} wordt betaald via PayPal")

    def bevestig(self):
        print("PayPal transactie voltooid!")
```

En deze werkt op exact dezelfde manier:

```python
paypal = PayPal()
test_betaling(paypal, 149.99)
```

Resultaat:

```console
PayPal account wordt gecontroleerd...
€149.99 wordt betaald via PayPal
PayPal transactie voltooid!
```

Er is nog (heel veel) meer te zeggen over polymorfisme; [check eventueel de wiki-pagina hierover](https://nl.wikipedia.org/wiki/Polymorfisme_(informatica)). Voor nu is het voldoende als je weet dat dit bestaat – in een later stadium komen we hier nog uitgebreid op terug.
