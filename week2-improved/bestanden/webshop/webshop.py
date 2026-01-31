"""
Webshop met Product, Klant en Winkelwagen klassen
Dit bestand demonstreert hoe meerdere klassen samenwerken
"""


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


if __name__ == '__main__':
    # Test de klassen
    laptop = Product("Laptop", 799.99, 5)
    muis = Product("Draadloze muis", 25.50, 20)
    toetsenbord = Product("Mechanisch toetsenbord", 89.99, 15)
    monitor = Product("27-inch monitor", 299.99, 8)

    jan = Klant("Jan Jansen", "jan@email.nl")
    winkelmand = Winkelwagen(jan)

    winkelmand.voeg_toe(laptop)
    winkelmand.voeg_toe(muis)
    winkelmand.voeg_toe(toetsenbord)

    winkelmand.toon_inhoud()
    jan.plaats_bestelling(winkelmand)

    winkelmand.voeg_toe(monitor)
    winkelmand.voeg_toe(muis)
    winkelmand.toon_inhoud()
    jan.plaats_bestelling(winkelmand)

    jan.toon_bestellingen()
