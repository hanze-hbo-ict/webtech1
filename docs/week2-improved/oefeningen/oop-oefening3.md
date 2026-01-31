# OOP Python – Oefening 3

In deze oefening gaan we de `Bestelling` klasse uit deel 7 verder uitbreiden.

## a. Bestellingsnummer toevoegen

Pas de code van `bestelling.py` zodanig aan dat elke bestelling automatisch een uniek bestellingsnummer krijgt. Je kunt hiervoor een class-attribuut gebruiken dat bij elke nieuwe bestelling opgehoogd wordt.

**Tip:** Een class-attribuut wordt gedefinieerd buiten de `__init__()` methode:

```python
class Bestelling:
    _volgend_nummer = 1000  # Class attribuut

    def __init__(self, ...):
        self.nummer = Bestelling._volgend_nummer
        Bestelling._volgend_nummer += 1
```

## b. Verzendmethode toevoegen

Er zijn verschillende verzendmethoden mogelijk: standaard verzending (2-3 werkdagen), express verzending (volgende werkdag), of afhalen in de winkel. Maak een nieuwe klasse `Verzendmethode` die de volgende eigenschappen heeft:

- **type**: Het type verzending ("Standaard", "Express", "Afhalen")
- **kosten**: De verzendkosten
- **levertijd**: De levertijd als tekst (bijv. "2-3 werkdagen")

Pas vervolgens de klasse `Bestelling` aan zodat je een `Verzendmethode` object mee kunt geven in plaats van alleen verzendkosten. Zorg ervoor dat de levertijd ook wordt getoond bij het plaatsen van een bestelling.

## c. Kortingscode toevoegen (optionele uitdaging)

Klanten kunnen soms een kortingscode gebruiken. Maak een nieuwe klasse `Kortingscode` die een code en een kortingspercentage bevat. Breid de klasse `Bestelling` op zo'n manier uit, dat het mogelijk is om een kortingscode toe te passen. Maak hiervoor een methode `pas_kortingscode_toe(kortingscode)`. Zorg er ook voor dat bij het *plaatsen* van de bestelling de korting correct wordt toegepast en getoond.

Voorbeeld gebruik:

```python
# Maak kortingscode aan
zomer2026 = Kortingscode("ZOMER2026", 0.15)  # 15% korting

# Pas toe op bestelling
bestelling.pas_kortingscode_toe(zomer2026)
```

Verwachte output bij plaatsen bestelling:
```
Subtotaal: €915.48
Kortingscode ZOMER2026: -€137.32 (15%)
Subtotaal na korting: €778.16
Verzendkosten: €0.00 (GRATIS verzending!)
Totaal: €778.16
```

## d. Meerdere verzendadressen (nog een optionele uitdaging)

In een echte webshop kunnen klanten meerdere adressen hebben (thuisadres, werkadres, etc.). Maak een klasse `Adres` met velden voor straat, huisnummer, postcode en plaats. Pas de klasse `Klant` aan zodat een klant meerdere adressen kan hebben. Bij het aanmaken van een bestelling moet je dan kunnen kiezen naar welk adres verzonden moet worden.

Als je dit is gelukt kun je jezelf feliciteren: je hebt nu een realistische webshop-structuur gemaakt met compositie!

## Testcode

Hier is een voorbeeld hoe je de uitgebreide functionaliteit kunt testen:

```python
from product import Product
from klant import Klant
from winkelwagen import Winkelwagen
from bestelling import Bestelling, Verzendmethode, Kortingscode
from betaalmethode import Betaalmethode

# Maak producten
laptop = Product("Laptop", 799.99, 5)
muis = Product("Draadloze muis", 25.50, 20)

# Maak klant en winkelwagen
jan = Klant("Jan Jansen", "jan@email.nl")
wagen = Winkelwagen(jan)
wagen.voeg_toe(laptop)
wagen.voeg_toe(muis)

# Maak verzendmethode
express = Verzendmethode("Express", 9.95, "volgende werkdag")

# Maak betaalmethode
ideal = Betaalmethode("iDEAL", 0.0)

# Maak bestelling
bestelling = Bestelling(jan, wagen, ideal, verzendmethode=express)

# Pas kortingscode toe
korting = Kortingscode("WELKOM10", 0.10)
bestelling.pas_kortingscode_toe(korting)

# Plaats bestelling
bestelling.plaats_bestelling()

print(f"\nBestellingsnummer: {bestelling.nummer}")
```
