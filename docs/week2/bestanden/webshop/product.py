import random


class Product:
    """Basisklasse voor alle producten in de webshop."""

    def __init__(self, naam: str, prijs: float, voorraad: int):
        """Maak een nieuw product aan.

        Args:
            naam: Naam van het product
            prijs: Prijs in euro's
            voorraad: Aantal items op voorraad
        """
        self.naam = naam
        self.prijs = prijs
        self.voorraad = voorraad

    def verkoop(self, aantal: int) -> bool:
        """Verkoop een aantal items van dit product.

        Args:
            aantal: Aantal items om te verkopen

        Returns:
            True als verkoop succesvol, False bij onvoldoende voorraad
        """
        if self.voorraad >= aantal:
            self.voorraad -= aantal
            return True
        else:
            return False

    def __str__(self) -> str:
        """String representatie van het product."""
        return f"Product: {self.naam}, Prijs: €{self.prijs:.2f}, Voorraad: {self.voorraad}"


class FysiekProduct(Product):
    """Subklasse voor fysieke producten die verzonden moeten worden."""

    def __init__(self, naam: str, prijs: float, voorraad: int, gewicht: float = 0.0):
        """Maak een fysiek product aan.

        Args:
            naam: Naam van het product
            prijs: Prijs in euro's
            voorraad: Aantal items op voorraad
            gewicht: Gewicht in kilogram (default: 0.0)
        """
        super().__init__(naam=naam, prijs=prijs, voorraad=voorraad)
        self.gewicht = gewicht

    def bereken_verzendkosten(self) -> float:
        """Bereken verzendkosten op basis van gewicht.

        Returns:
            Verzendkosten in euro's
        """
        if self.gewicht <= 1.0:
            return 3.95
        elif self.gewicht <= 5.0:
            return 6.95
        else:
            return 9.95


# Hier kun je de klasse DigitaalProduct toevoegen tijdens oefening 2

# Hier kun je de klasse Boek toevoegen tijdens oefening 2

# Hier kun je de klasse Software toevoegen tijdens oefening 2
