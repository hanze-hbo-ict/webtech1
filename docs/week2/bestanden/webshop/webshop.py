"""
Webshop met Product, Customer en Cart klassen.
Dit bestand demonstreert hoe meerdere klassen samenwerken.
"""


class Product:
    """Klasse waarin productgegevens worden vastgelegd."""

    def __init__(self, naam: str, prijs: float, voorraad: int = 0):
        """Maak een nieuw product aan.

        Args:
            naam: Naam van het product
            prijs: Prijs in euro's
            voorraad: Aantal beschikbare producten (default: 0)
        """
        self.naam = naam
        self.prijs = prijs
        self.voorraad = voorraad

    def __str__(self) -> str:
        """String representatie van het product."""
        return f"{self.naam} (€{self.prijs:.2f})"


class Cart:
    """Klasse voor een winkelwagen met producten."""

    def __init__(self, klant: 'Customer'):
        """Maak een winkelwagen aan.

        Args:
            klant: Customer die deze winkelwagen gebruikt
        """
        self.items: list[Product] = []
        self.klant = klant

    def voeg_toe(self, product: Product) -> None:
        """Voeg een product toe aan de winkelwagen.

        Args:
            product: Het toe te voegen product
        """
        self.items.append(product)

    def verwijder(self, product: Product) -> bool:
        """Verwijder een product uit de winkelwagen.

        Args:
            product: Het te verwijderen product

        Returns:
            True als product verwijderd, False als product niet gevonden
        """
        if product in self.items:
            self.items.remove(product)
            return True
        return False

    def bereken_totaal(self) -> float:
        """Bereken het totaalbedrag van alle producten.

        Returns:
            Totaalbedrag in euro's
        """
        return sum(product.prijs for product in self.items)

    def toon_inhoud(self) -> None:
        """Toon de volledige inhoud van de winkelwagen."""
        if not self.items:
            print(f"Winkelwagen van {self.klant.naam} is leeg")
        else:
            print(f"\nWinkelwagen van {self.klant.naam}:")
            for product in self.items:
                print(f"  - {product}")
            print(f"Totaal: €{self.bereken_totaal():.2f}")


class Customer:
    """Klasse om klantgegevens op te slaan."""

    def __init__(self, naam: str, email: str):
        """Maak een nieuwe klant aan.

        Args:
            naam: Naam van de klant
            email: Email adres van de klant
        """
        self.naam = naam
        self.email = email
        self.bestellingen: list[dict] = []

    def plaats_bestelling(self, winkelwagen: Cart) -> dict | None:
        """Plaats een bestelling.

        Args:
            winkelwagen: De winkelwagen met producten

        Returns:
            Dict met bestellingsgegevens, of None bij lege winkelwagen
        """
        if not winkelwagen.items:
            return None

        totaal = winkelwagen.bereken_totaal()
        bestelling = {
            "klant": self.naam,
            "email": self.email,
            "items": winkelwagen.items.copy(),
            "totaal": totaal,
        }
        self.bestellingen.append(bestelling)
        winkelwagen.items.clear()
        return bestelling

    def toon_bestellingen(self) -> None:
        """Toon alle bestellingen van deze klant."""
        if not self.bestellingen:
            print(f"{self.naam} heeft nog geen bestellingen geplaatst")
        else:
            print(f"\nBestellingen van {self.naam}:")
            for i, bestelling in enumerate(self.bestellingen, 1):
                print(f"\n  Bestelling {i}:")
                for product in bestelling["items"]:
                    print(f"    - {product}")
                print(f"  Totaal: €{bestelling['totaal']:.2f}")


if __name__ == '__main__':
    laptop = Product("Laptop", 799.99, 5)
    muis = Product("Draadloze muis", 25.50, 20)
    toetsenbord = Product("Mechanisch toetsenbord", 89.99, 15)
    monitor = Product("27-inch monitor", 299.99, 8)

    jan = Customer("Jan Jansen", "jan@email.nl")
    winkelmand = Cart(jan)

    winkelmand.voeg_toe(laptop)
    winkelmand.voeg_toe(muis)
    winkelmand.voeg_toe(toetsenbord)

    winkelmand.toon_inhoud()

    bestelling = jan.plaats_bestelling(winkelmand)
    if bestelling:
        print(f"\nBestelling geplaatst: €{bestelling['totaal']:.2f}")
        print(f"Bevestiging naar: {bestelling['email']}")

    winkelmand.voeg_toe(monitor)
    winkelmand.voeg_toe(muis)
    winkelmand.toon_inhoud()
    jan.plaats_bestelling(winkelmand)

    jan.toon_bestellingen()
