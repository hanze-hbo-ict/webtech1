"""Inventory klasse voor het bijhouden van productvoorraad."""

import datetime


class Inventory:
    """Klasse voor het bijhouden van productvoorraad."""

    def __init__(self, product_naam: str, aantal: int):
        """Maak een voorraadadministratie aan.

        Args:
            product_naam: Naam van het product
            aantal: Beginhoeveelheid op voorraad
        """
        self.product_naam = product_naam
        self.aantal = aantal
        self.mutatie_geschiedenis: list[tuple[str, int]] = []

    @staticmethod
    def _current_time() -> str:
        """Geeft huidige datum en tijd als string."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def bijbestellen(self, aantal: int) -> bool:
        """Bestel extra voorraad bij.

        Args:
            aantal: Aantal bij te bestellen (moet > 0 zijn)

        Returns:
            True als bijbestelling geslaagd, False bij ongeldig aantal
        """
        if aantal > 0:
            self.aantal += aantal
            self.mutatie_geschiedenis.append((Inventory._current_time(), aantal))
            return True
        return False

    def verkoop(self, aantal: int) -> bool:
        """Verkoop een aantal items.

        Args:
            aantal: Aantal te verkopen items

        Returns:
            True als verkoop geslaagd, False bij onvoldoende voorraad
        """
        if 0 < aantal <= self.aantal:
            self.aantal -= aantal
            self.mutatie_geschiedenis.append((Inventory._current_time(), -aantal))
            return True
        return False

    def toon_voorraad(self) -> None:
        """Toon huidige voorraad."""
        print(f"Voorraad {self.product_naam}: {self.aantal}")

    def toon_mutaties(self) -> None:
        """Toon de volledige mutatie-geschiedenis."""
        print(f"\nMutatie-geschiedenis voor {self.product_naam}:")
        for datum, aantal in self.mutatie_geschiedenis:
            if aantal > 0:
                print(f"  {datum}: {aantal} bijbesteld")
            else:
                print(f"  {datum}: {abs(aantal)} verkocht")


if __name__ == '__main__':
    inv = Inventory("Laptop", 10)
    inv.toon_voorraad()

    inv.bijbestellen(5)
    inv.toon_voorraad()

    geslaagd = inv.verkoop(3)
    print(f"Verkoop geslaagd: {geslaagd}")
    inv.toon_voorraad()

    # Test ongeldige verkoop
    geslaagd = inv.verkoop(100)
    print(f"Oververkoop geslaagd: {geslaagd}")

    inv.toon_mutaties()
