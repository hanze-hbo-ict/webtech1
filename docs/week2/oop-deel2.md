# OOP Python – Methoden

Inkapseling is één van de fundamenten van object-georiënteerd programmeren. Het wordt gebruikt om onbevoegden niet de gelegenheid te bieden de kenmerken van een object aan te passen. Als dat mogelijk moet zijn dan dienen zij toegang te krijgen tot de zogenaamde `getters` en `setters`, waarover zo dadelijk meer.

!!! Info "zichtbaarheid"
    Python wijkt nadrukkelijk af van het idee van inkapseling zoals het bijvoorbeeld gedaan wordt bij Java. Python gebruikt niet de sleutel-woorden `private` of `protected` om de zichtbaarheid van een methode aan te geven.

## Het voorbeeld Bank

Als voorbeeld hier een bank, waarbij het mogelijk is een rekening te openen, geld te storten en op te nemen en een overzicht van alle gedane transacties op te vragen, waarbij tevens het tijdstip van de transactie getoond wordt. Uiteraard is de opzet erg beperkt.

De code wordt in stapjes opgebouwd; we slaan deze code uiteindelijk op in het bestand `Bankrekening.py`.

## Klasse en methoden

Stap 1: de klasse

```python
class Bankrekening:
```

Stap 2: het importeren van de huidige tijd

```python
import datetime
```

Stap 3: een functie om het tijdstip van de transactie vast te leggen.

```python
def current_time():
    now = datetime.datetime.now()
    return (now.strftime("%Y-%m-%d %H:%M:%S"))
```

De functie `current_time()` retourneert het tijdstip van storten in het opgegeven formaat, tot op de seconde nauwkeurig.

## De constructor

Stap 4: de constructor

```python
def __init__(self, naam, saldo):
    self._name = naam
    self.__saldo = saldo
    self._transactie_overzicht = []
    print("Bankrekening aangemaakt voor " + self._name)
```

## Storten en opnemen

Bij het openen van een nieuwe rekening wordt gevraagd om een naam en een inlegbedrag. Een rekeningnummer wordt hier niet uitgedeeld. De variabele `transactie_overzicht` is een lijst (`[]`) waarin alle transacties worden vastgelegd. 

Stap 5: de methode `storten()`

```python
def storten(self, bedrag):
    if bedrag > 0:
        self.__saldo += bedrag
        self._transactie_overzicht.append( (Bankrekening._current_time(), bedrag) )
        self.toon_saldo()
```


Indien het te storten bedrag groter dan nul (`0`) is, wordt het saldo aangepast en wordt de transactie toegevoegd aan de lijst `transactie_overzicht[]` (zie je wat het datatype is van dat wat er aan de lijst `transactie_overzicht` wordt toegevoegd?). Ook het actuele saldo wordt nu getoond.

Stap 6: de methode `opnemen()`

```python
def opnemen(self, bedrag):
    if 0 < bedrag <= self.__saldo:
        self.__saldo -= bedrag
        self._transactie_overzicht.append(((Bankrekening._current_time(), -bedrag)))
    else:
        print("Het bedrag dient groter dan nul (0) en maximaal gelijk aan het saldo te zijn")
    self.toon_saldo()
```

Er vindt een controle plaats of het saldo toereikend is voor de aanvraag. Zo niet, volgt er een passende mededeling. Zo ja, wordt het saldo bijgewerkt en de transactie weer in de lijst vastgelegd. Ook hier wordt het actuele saldo getoond.

Stap 7: de methode `toon_saldo()`

```python
def toon_saldo(self):
    print("Saldo bedraagt {}".format(self.__saldo))
```

## Transactie-overzicht

Stap 8: het transactie-overzicht

```python
def toon_transacties(self):
    for date, bedrag in self._transactie_overzicht:
        if bedrag > 0:
            trans_type = "gestort"
        else:
            trans_type = "opgenomen"
            bedrag *= -1
        print("{} {} op {}".format(bedrag, trans_type, (Bankrekening._current_time())))
```

Belangrijk is na te gaan of het bedrag gestort dan wel opgenomen is. Omdat een bedrag altijd groter is dan nul (0), dient dit bedrag bij opnemen met de factor -1 vermenigvuldigd te worden om het saldo te kunnen verlagen. De printopdracht toont alle transacties.

## Interactieve test

Nu gaan we kijken of het werkt. Dit doen we weer in onze interactieve shell, waar we eerst het bestand `Bankrekening.py` inladen

```ipython
In [1]: run "Bankrekening"

In [2]: angela = Bankrekening("Angela", 0)
Bankrekening aangemaakt voor Angela

In [3]: angela.toon_saldo()
Saldo bedraagt 0

In [4]: angela.storten(1000)
Saldo bedraagt 1000

In [5]: angela.opnemen(500)
Saldo bedraagt 500

In [6]: angela.opnemen(1000)
Het bedrag dient groter dan nul (0) en maximaal gelijk aan het saldo te zijn
Saldo bedraagt 500

In [8]: angela.toon_transacties()
1000 gestort op 2021-01-10 13:47:46
500 opgenomen op 2021-01-10 13:47:46

In [9]: 
```

## Oefening 1

Maak nu [oefening 1](oefeningen/oop-oefening1.md)

## Te veel mogelijkheden

Het idee is gewekt dat alles nu in kannen en kruiken geregeld is. Helaas, er zijn toch nog een aantal onvolkomenheden die aanpassing behoeven. Kijk eens naar het volgende scenario, waarbij een min of meer criminele activiteit is aangegeven:

```ipython hl_lines="9"
In [1]: run "Bankrekening"

In [2]: britt = Bankrekening("Britt", 800)
Bankrekening aangemaakt voor Britt

In [3]: britt.storten(100)
Saldo bedraagt 900

In [4]: britt.saldo = 1000

In [5]: britt.opnemen(200)
Saldo bedraagt 700

In [6]: britt.toon_transacties()
100 gestort op 2021-01-10 14:09:06
200 opgenomen op 2021-01-10 14:09:06

In [7]: britt.toon_saldo()
Saldo bedraagt 700

In [8]: 
```

Het is dus mogelijk het saldo van een object te veranderen zodat het niet meer recht doet aan het bedrag dat beschikbaar zou moeten zijn na het uitvoeren van de gedane transacties. Dit komt doordat attributen van instanties door iedereen kunnen worden gemaakt en aanpast.

Wat je zou willen is dat een attribuut alleen door *methoden van binnen de klasse* kunnnen worden aangepast. Helaas is dat in Python niet zonder meer mogelijk (er zijn wel packages voor die dat voor je kunnen regelen, [lees bijvoorbeeld deze blog](https://bogotobogo.com/python/python_private_attributes_methods.php)). Het is evenwel conventie binnen de Python-gemeenschap dat we attributen die niet van buiten mogen worden aangepast voorzien van een liggen streepje (`_`) vóór de variabele-naam, zoals we in de code hierboven al hebben laten zien. 
