"""Customer klasse voor de webshop."""


class Customer:
    """Klasse voor klanten in de webshop."""

    def __init__(self, naam: str, email: str):
        """Maak een nieuwe klant aan.

        Args:
            naam: Naam van de klant
            email: Email adres van de klant
        """
        self.naam = naam
        self.email = email
        self.krediet: float = 1000.0
        self.korting: float = 0.0  # Decimaal: 0.15 = 15%

    def bereken_korting(self, bedrag: float) -> float:
        """Bereken kortingsbedrag op een bedrag.

        Args:
            bedrag: Bedrag waarop korting berekend wordt

        Returns:
            Kortingsbedrag in euro's
        """
        return bedrag * self.korting

    def __str__(self) -> str:
        """String representatie van de klant."""
        return f"Klant: {self.naam} ({self.email}), krediet: €{self.krediet:.2f}"


if __name__ == '__main__':
    # Test de Customer klasse
    jan = Customer("Jan Jansen", "jan@email.nl")
    print(jan)

    # Korting instellen
    jan.korting = 0.15
    print(f"Korting: {jan.korting * 100:.0f}%")
    print(f"Korting op €100: €{jan.bereken_korting(100):.2f}")

    # Krediet aanpassen
    jan.krediet -= 300.0
    print(f"Resterend krediet: €{jan.krediet:.2f}")
