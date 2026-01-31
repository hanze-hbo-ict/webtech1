# OOP Python - Meerdere klassen

Het is belangrijk om commentaar op te nemen binnen codeblokken. Het is dan voor iemand die de code niet ontwikkeld heeft, maar deze wel moet refactoren, duidelijk wat de bedoeling is. Dat gaan we hier ook doen.

## De klasse `Product`

Als voorbeeld wordt hier een applicatie opgebouwd, waarbij gegevens vanuit drie klassen aangeroepen zullen worden. Die klassen zijn `Product`, `Klant` en `Winkelwagen`. De code is te vinden in het bestand [webshop.py](bestanden/webshop/webshop.py)

De eerste klasse is `Product`. In het commentaar van deze klasse zetten we een korte beschrijving van de klasse, gevolgd door een omschrijving van de attributen die van objecten deze klasse worden bijgehouden. Na dit commentaar volgt de *constructor*, die we ook voorzien van een korte beschrijving.

```python
class Product:
    """Klasse waarin productgegevens worden vastgelegd

    Attributen:
        naam (str): De naam van het product.
        prijs (float): De prijs van het product in euro's.
        voorraad (int): Het aantal beschikbare producten. Standaard 0.
    """

    def __init__(self, naam, prijs, voorraad=0):
        self._naam = naam
        self._prijs = prijs
        self._voorraad = voorraad

    def __str__(self):
        return f"{self._naam} (€{self._prijs:.2f})"
```

## De klasse `Winkelwagen`

In hetzelfde bestand maken we nu een tweede klasse: `Winkelwagen`. Aan deze winkelwagen kunnen producten worden toegevoegd.

```python
class Winkelwagen:
    """Klasse voor een winkelwagen met producten

    Attributen:
        items (list): Een lijst met producten in de winkelwagen.
        klant (Klant): De klant bij wie deze winkelwagen hoort.

    Methods:
        voeg_toe: Voegt een product toe aan de winkelwagen.
        verwijder: Verwijdert een product uit de winkelwagen.
        bereken_totaal: Berekent het totaalbedrag van alle producten.
    """

    def __init__(self, klant):
        self.items = []
        self.klant = klant

    def voeg_toe(self, product):
        """Voegt een product toe aan de winkelwagen

        Parameters:
            product (Product): Het toe te voegen product
        """
        self.items.append(product)
        print(f"{product._naam} toegevoegd aan winkelwagen van {self.klant._naam}")

    def verwijder(self, product):
        """Verwijdert een product uit de winkelwagen

        Parameters:
            product (Product): Het te verwijderen product
        """
        if product in self.items:
            self.items.remove(product)
            print(f"{product._naam} verwijderd uit winkelwagen")
        else:
            print(f"{product._naam} zit niet in de winkelwagen")

    def bereken_totaal(self):
        """Berekent het totaalbedrag van alle producten in de winkelwagen

        Returns:
            float: Het totaalbedrag
        """
        totaal = sum(product._prijs for product in self.items)
        return totaal

    def toon_inhoud(self):
        """Toont de volledige inhoud van de winkelwagen"""
        if not self.items:
            print(f"Winkelwagen van {self.klant._naam} is leeg")
        else:
            print(f"\nWinkelwagen van {self.klant._naam}:")
            for product in self.items:
                print(f"  - {product}")
            print(f"Totaal: €{self.bereken_totaal():.2f}")
```

Het is hier allemaal een beetje overdone, maar het idee is duidelijk.

## De klasse `Klant`

Er is al verwezen naar de klasse Klant, maar die bestaat op dit moment nog niet. Daar gaat nu verandering in komen.

```python
class Klant:
    """Klasse om klantgegevens op te slaan

    Attributen:
        naam (str): De naam van de klant.
        email (str): Het e-mailadres van de klant.
        bestellingen (list): Een lijst met de bestellingen van deze klant.

    Methods:
        plaats_bestelling: Plaatst een bestelling voor de klant.
    """

    def __init__(self, naam, email):
        self._naam = naam
        self._email = email
        self._bestellingen = []

    def plaats_bestelling(self, winkelwagen):
        """Plaatst een bestelling

        Parameters:
            winkelwagen (Winkelwagen): De winkelwagen met producten
        """
        if not winkelwagen.items:
            print("Winkelwagen is leeg!")
            return

        totaal = winkelwagen.bereken_totaal()
        self._bestellingen.append({
            'items': winkelwagen.items.copy(),
            'totaal': totaal
        })
        print(f"\nBestelling geplaatst voor {self._naam}")
        print(f"Totaalbedrag: €{totaal:.2f}")
        print(f"Bevestiging verstuurd naar {self._email}")

        # Leeg de winkelwagen na bestelling
        winkelwagen.items.clear()

    def toon_bestellingen(self):
        """Toont alle bestellingen van deze klant"""
        if not self._bestellingen:
            print(f"{self._naam} heeft nog geen bestellingen geplaatst")
        else:
            print(f"\nBestellingen van {self._naam}:")
            for i, bestelling in enumerate(self._bestellingen, 1):
                print(f"\n  Bestelling {i}:")
                for product in bestelling['items']:
                    print(f"    - {product}")
                print(f"  Totaal: €{bestelling['totaal']:.2f}")
```

Ook deze klasse moet de mogelijkheid hebben bestellingen te plaatsen. Bijzondere aandacht voor het feit dat de winkelwagen wordt geleegd na een bestelling.

## Het geheel in actie

Nu de drie klassen af zijn, kunnen we deze gebruiken. Eerst importeren we alles:

```python
# Maak enkele producten aan
laptop = Product("Laptop", 799.99, 5)
muis = Product("Draadloze muis", 25.50, 20)
toetsenbord = Product("Mechanisch toetsenbord", 89.99, 15)
monitor = Product("27-inch monitor", 299.99, 8)

# Maak een klant aan
jan = Klant("Jan Jansen", "jan@email.nl")

# Maak een winkelwagen voor Jan
winkelmand = Winkelwagen(jan)

# Voeg producten toe
winkelmand.voeg_toe(laptop)
winkelmand.voeg_toe(muis)
winkelmand.voeg_toe(toetsenbord)

# Toon de inhoud
winkelmand.toon_inhoud()

# Plaats de bestelling
jan.plaats_bestelling(winkelmand)

# Voeg nog meer producten toe en plaats een tweede bestelling
winkelmand.voeg_toe(monitor)
winkelmand.voeg_toe(muis)  # Nog een muis
winkelmand.toon_inhoud()
jan.plaats_bestelling(winkelmand)

# Toon alle bestellingen
jan.toon_bestellingen()
```

Dit geeft de volgende uitvoer:

```console
Laptop toegevoegd aan winkelwagen van Jan Jansen
Draadloze muis toegevoegd aan winkelwagen van Jan Jansen
Mechanisch toetsenbord toegevoegd aan winkelwagen van Jan Jansen

Winkelwagen van Jan Jansen:
  - Laptop (€799.99)
  - Draadloze muis (€25.50)
  - Mechanisch toetsenbord (€89.99)
Totaal: €915.48

Bestelling geplaatst voor Jan Jansen
Totaalbedrag: €915.48
Bevestiging verstuurd naar jan@email.nl

27-inch monitor toegevoegd aan winkelwagen van Jan Jansen
Draadloze muis toegevoegd aan winkelwagen van Jan Jansen

Winkelwagen van Jan Jansen:
  - 27-inch monitor (€299.99)
  - Draadloze muis (€25.50)
Totaal: €325.49

Bestelling geplaatst voor Jan Jansen
Totaalbedrag: €325.49
Bevestiging verstuurd naar jan@email.nl

Bestellingen van Jan Jansen:

  Bestelling 1:
    - Laptop (€799.99)
    - Draadloze muis (€25.50)
    - Mechanisch toetsenbord (€89.99)
  Totaal: €915.48

  Bestelling 2:
    - 27-inch monitor (€299.99)
    - Draadloze muis (€25.50)
  Totaal: €325.49
```

## Waarom meerdere klassen?

Het gebruik van meerdere klassen heeft verschillende voordelen:

1. **Scheiding van verantwoordelijkheden**: Elke klasse heeft zijn eigen taak (Product: productinfo, Klant: klantinfo, Winkelwagen: producten verzamelen)
2. **Herbruikbaarheid**: De `Product` klasse kan worden hergebruikt in andere delen van de applicatie
3. **Onderhoudbaarheid**: Wijzigingen in één klasse hebben minder impact op andere klassen
4. **Realistische modellering**: Het komt overeen met hoe een echte webshop werkt

## Samenvatting

In dit deel hebben we geleerd over:

- Het werken met meerdere klassen die elkaar gebruiken
- Het documenteren van klassen met docstrings
- Het modelleren van een realistische applicatie (webshop)
- Het gebruik van lijsten om collecties van objecten op te slaan
- Het doorgeven van objecten als parameters

In het volgende deel gaan we dieper in op getters en setters met de `@property` decorator.
