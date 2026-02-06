class Klant:
    """Klasse voor klanten in de webshop met krediet en korting"""

    def __init__(self, naam, email):
        self._naam = naam
        self._email = email
        self.__krediet = 1000.0  # Startkrediet voor nieuwe klanten
        self.__korting = 0.0  # Standaard geen korting

    @property
    def krediet(self):
        """Getter voor krediet"""
        return self.__krediet

    @krediet.setter
    def krediet(self, waarde):
        """Setter voor krediet"""
        if waarde >= 0:
            self.__krediet = waarde
        else:
            print("Krediet kan geen negatieve waarde krijgen")
            self.__krediet = 0

    @property
    def korting(self):
        """Getter voor korting"""
        return self.__korting

    @korting.setter
    def korting(self, waarde):
        """Setter voor korting"""
        if 0 <= waarde <= 1.0:
            self.__korting = waarde
        else:
            print("Korting moet tussen 0 en 1.0 liggen")

    @property
    def volledige_naam(self):
        """Read-only property die volledige naam returnt"""
        return f"{self._naam} ({self._email})"

    def __str__(self):
        return f"Klant: {self._naam}, Email: {self._email}, Krediet: €{self.__krediet:.2f}"


if __name__ == '__main__':
    # Test de Klant klasse
    jan = Klant("Jan Jansen", "jan@email.nl")
    print(jan)

    # Test properties
    print(f"\nKrediet: €{jan.krediet:.2f}")

    jan.korting = 0.15
    print(f"Korting: {jan.korting * 100}%")

    # Test validatie
    jan.korting = 2.0  # Dit wordt afgewezen

    jan.krediet = jan.krediet - 300.0
    print(f"Nieuw krediet: €{jan.krediet:.2f}")

    # Test read-only property
    print(f"\nVolledige naam: {jan.volledige_naam}")
