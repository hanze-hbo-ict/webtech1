import random


class Product:
    """Basisklasse voor alle producten in de webshop"""

    def __init__(self, naam, prijs, voorraad):
        self._naam = naam
        self._prijs = prijs
        self._voorraad = voorraad

    def verkoop(self, aantal):
        """Verkoop een aantal items van dit product"""
        nieuwe_voorraad = self._voorraad - aantal
        if nieuwe_voorraad >= 0:
            self._voorraad = nieuwe_voorraad
            print(f"Verkocht: {aantal}x {self._naam}. Nog {self._voorraad} op voorraad")
        else:
            print(f"Onvoldoende voorraad. Nog maar {self._voorraad} beschikbaar")

    def __str__(self):
        return f"Product: {self._naam}, Prijs: €{self._prijs:.2f}, Voorraad: {self._voorraad}"


class FysiekProduct(Product):
    """Subklasse voor fysieke producten die verzonden moeten worden"""

    def __init__(self, naam, prijs, voorraad, gewicht=0.0):
        super().__init__(naam=naam, prijs=prijs, voorraad=voorraad)
        self._gewicht = gewicht

    def bereken_verzendkosten(self):
        """Bereken verzendkosten op basis van gewicht"""
        if self._gewicht <= 1.0:
            kosten = 3.95
        elif self._gewicht <= 5.0:
            kosten = 6.95
        else:
            kosten = 9.95
        print(f"Verzendkosten voor {self._naam}: €{kosten:.2f}")
        return kosten


# Hier kun je de klasse DigitaalProduct toevoegen tijdens oefening 2

# Hier kun je de klasse Boek toevoegen tijdens oefening 2

# Hier kun je de klasse Software toevoegen tijdens oefening 2
