# OOP Python – Compositie

In deze laatste paragraaf aandacht voor nog een OOP-techniek, compositie (*composition*). Compositie wil zeggen dat een object *samengesteld* wordt aan de hand van verschillende andere objecten. Het samengesteld object kan op die manier taken delegeren aan die samenstellende objecten. Op zich lijkt compositie wel wat op overerving, maar waar overerving *impliciet* is, is compositie *expliciet* (en daarmee ook schaalbaarder, testbaarder en overdraagbaarder).

Compositie biedt een superieure manier om delegatie te beheren, aangezien het selectief de toegang kan delegeren, zelfs sommige attributen of methoden kan maskeren, terwijl overerving dit alles moet ontberen.

Aan het eind van deze paragraaf maken we [oefening 3](oefeningen/oop-oefening3.md).

## Een webshop-voorbeeld

Als voorbeeld wordt hier een klasse `Bestelling` toegevoegd die gebruik maakt van de klassen `Klant` en `Winkelwagen` die we eerder hebben gemaakt. Een bestelling is namelijk een *compositie* van een klant, een winkelwagen met producten, en een betaalmethode.

Eerst maken we een eenvoudige klasse voor een betaalmethode:

```python
class Betaalmethode:
    """Klasse voor betaalmethoden"""

    def __init__(self, type_betaling, kosten=0.0):
        self.type = type_betaling
        self.kosten = kosten  # Eventuele transactiekosten

    def verwerk_betaling(self, bedrag):
        """Verwerk een betaling"""
        totaal = bedrag + self.kosten
        print(f"Betaling van €{totaal:.2f} wordt verwerkt via {self.type}")
        if self.kosten > 0:
            print(f"  (inclusief €{self.kosten:.2f} transactiekosten)")
        return totaal
```

De volgende stap is om de klasse `Bestelling` te maken die gebruik maakt van `Klant`, `Winkelwagen` en `Betaalmethode`:

```python
import datetime


class Bestelling:
    """Klasse voor bestellingen in de webshop

    Een bestelling is samengesteld uit:
    - Een klant
    - Een winkelwagen met producten
    - Een betaalmethode
    - Verzendkosten
    """

    def __init__(self, klant, winkelwagen, betaalmethode, verzendkosten=5.95):
        self.klant = klant
        self.winkelwagen = winkelwagen
        self.betaalmethode = betaalmethode
        self.verzendkosten = verzendkosten
        self.besteldatum = datetime.datetime.now()
        self.status = "In behandeling"

    def bereken_totaal(self):
        """Berekent totaalbedrag inclusief verzendkosten"""
        subtotaal = self.winkelwagen.bereken_totaal()

        # Gratis verzending boven €50
        if subtotaal >= 50:
            verzending = 0.0
        else:
            verzending = self.verzendkosten

        return subtotaal + verzending

    def plaats_bestelling(self):
        """Plaatst de bestelling en verwerkt de betaling"""
        if not self.winkelwagen.items:
            print("Kan geen lege bestelling plaatsen!")
            return False

        print(f"\n{'='*50}")
        print(f"BESTELLING VOOR {self.klant._naam}")
        print(f"{'='*50}")

        # Toon producten
        print("\nProducten:")
        for product in self.winkelwagen.items:
            print(f"  - {product}")

        # Bereken kosten
        subtotaal = self.winkelwagen.bereken_totaal()
        print(f"\nSubtotaal: €{subtotaal:.2f}")

        if subtotaal >= 50:
            print("Verzendkosten: €0.00 (GRATIS verzending!)")
            verzending = 0.0
        else:
            print(f"Verzendkosten: €{self.verzendkosten:.2f}")
            verzending = self.verzendkosten

        totaal = subtotaal + verzending
        print(f"Totaal: €{totaal:.2f}")

        # Verwerk betaling
        print(f"\nBetaalmethode: {self.betaalmethode.type}")
        eindtotaal = self.betaalmethode.verwerk_betaling(totaal)

        # Bevestiging
        self.status = "Bevestigd"
        print(f"\nBestelling bevestigd!")
        print(f"Bevestiging verzonden naar {self.klant._email}")
        print(f"Verwachte levering: 2-3 werkdagen")
        print(f"{'='*50}\n")

        return True

    def toon_status(self):
        """Toont de status van de bestelling"""
        print(f"\nBestellingsnummer: #{id(self)}")
        print(f"Klant: {self.klant._naam}")
        print(f"Datum: {self.besteldatum.strftime('%d-%m-%Y %H:%M')}")
        print(f"Status: {self.status}")
        print(f"Aantal producten: {len(self.winkelwagen.items)}")
        print(f"Totaalbedrag: €{self.bereken_totaal():.2f}")
```

## De compositie in actie

Laten we kijken hoe een bestelling werkt. We gebruiken de klassen die we al hebben (Product, Klant, Winkelwagen) en combineren ze:

```python
from product import Product
from klant import Klant
from winkelwagen import Winkelwagen

# Maak producten aan
laptop = Product("Laptop", 799.99, 5)
muis = Product("Draadloze muis", 25.50, 20)
toetsenbord = Product("Mechanisch toetsenbord", 89.99, 15)

# Maak een klant aan
anna = Klant("Anna de Vries", "anna@email.nl")

# Maak een winkelwagen en voeg producten toe
wagen = Winkelwagen(anna)
wagen.voeg_toe(laptop)
wagen.voeg_toe(muis)
wagen.voeg_toe(toetsenbord)

# Kies een betaalmethode
ideal = Betaalmethode("iDEAL", kosten=0.0)  # Geen transactiekosten

# Maak een bestelling (compositie!)
bestelling = Bestelling(
    klant=anna,
    winkelwagen=wagen,
    betaalmethode=ideal,
    verzendkosten=5.95
)

# Plaats de bestelling
bestelling.plaats_bestelling()

# Toon status
bestelling.toon_status()
```

Resultaat:

```console
==================================================
BESTELLING VOOR Anna de Vries
==================================================

Producten:
  - Laptop (€799.99)
  - Draadloze muis (€25.50)
  - Mechanisch toetsenbord (€89.99)

Subtotaal: €915.48
Verzendkosten: €0.00 (GRATIS verzending!)
Totaal: €915.48

Betaalmethode: iDEAL
Betaling van €915.48 wordt verwerkt via iDEAL

Bestelling bevestigd!
Bevestiging verzonden naar anna@email.nl
Verwachte levering: 2-3 werkdagen
==================================================

Bestellingsnummer: #4426417040
Klant: Anna de Vries
Datum: 31-01-2026 12:45
Status: Bevestigd
Aantal producten: 3
Totaalbedrag: €915.48
```

## Compositie vs. Overerving

Het verschil tussen compositie en overerving:

**Overerving** (is-een relatie):
- Een `FysiekProduct` **is een** `Product`
- Een `DigitaalProduct` **is een** `Product`
- Gebruikt `super()` om functionaliteit over te nemen

**Compositie** (heeft-een relatie):
- Een `Bestelling` **heeft een** `Klant`
- Een `Bestelling` **heeft een** `Winkelwagen`
- Een `Bestelling` **heeft een** `Betaalmethode`
- Gebruikt instantievariabelen om andere objecten te bevatten

## Wanneer compositie gebruiken?

Gebruik compositie wanneer:

1. **Flexibiliteit belangrijker is**: Je kunt tijdens runtime eenvoudig de samenstelling wijzigen (bijvoorbeeld een andere betaalmethode kiezen)
2. **Meerdere bronnen**: Een object functionaliteit nodig heeft van meerdere verschillende klassen
3. **Geen "is-een" relatie**: De objecten zijn niet hetzelfde type, maar werken samen

Voorbeeld waar we de betaalmethode kunnen wijzigen:

```python
# Maak meerdere betaalmethodes
ideal = Betaalmethode("iDEAL", kosten=0.0)
creditcard = Betaalmethode("Creditcard", kosten=2.50)
paypal = Betaalmethode("PayPal", kosten=1.00)

# Maak bestelling met iDEAL
bestelling = Bestelling(anna, wagen, ideal)

# Wijzig de betaalmethode voor het plaatsen
bestelling.betaalmethode = paypal

# Nu wordt PayPal gebruikt
bestelling.plaats_bestelling()
```

## Voordelen van compositie

1. **Flexibiliteit**: Objecten kunnen tijdens runtime worden vervangen
2. **Loskoppeling**: Klassen zijn minder afhankelijk van elkaar
3. **Herbruikbaarheid**: Componenten kunnen in verschillende contexten worden gebruikt
4. **Testbaarheid**: Componenten kunnen afzonderlijk getest worden
5. **Onderhoudbaarheid**: Wijzigingen in één component hebben minder impact

## Samenvatting

In dit deel hebben we geleerd over:

- Compositie als alternatief voor overerving
- Het verschil tussen "is-een" (overerving) en "heeft-een" (compositie) relaties
- Het samenstellen van complexe objecten uit eenvoudigere objecten
- Het delegeren van functionaliteit naar component-objecten
- Wanneer compositie geschikter is dan overerving

## Afsluiting OOP

Je hebt nu alle belangrijke OOP-concepten in Python gezien:

1. **Klassen en objecten**: Het maken van sjablonen en instanties
2. **Encapsulation**: Het afschermen van data met private attributen
3. **Inheritance**: Het hergebruiken van code door overerving
4. **Polymorphism**: Dezelfde interface, verschillende implementaties
5. **Composition**: Het samenstellen van objecten uit andere objecten

Deze concepten vormen de basis voor het bouwen van complexe, onderhoudbare applicaties zoals webshops, games, en veel meer!
