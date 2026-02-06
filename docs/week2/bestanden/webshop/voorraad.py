import datetime


class Voorraad:
    """Klasse voor het bijhouden van productvoorraad"""

    @staticmethod
    def _current_time():
        now = datetime.datetime.now()
        return f"{now: %Y-%m-%d %H:%M:%S}"

    def __init__(self, product_naam, aantal):
        self._product_naam = product_naam
        self.__aantal = aantal
        self._mutatie_geschiedenis = []
        print(f"Voorraad aangemaakt voor {self._product_naam}")

    def bijbestellen(self, aantal):
        if aantal > 0:
            self.__aantal += aantal
            self._mutatie_geschiedenis.append((Voorraad._current_time(), aantal))
            self.toon_voorraad()

    def verkoop(self, aantal):
        if 0 < aantal <= self.__aantal:
            self.__aantal -= aantal
            self._mutatie_geschiedenis.append((Voorraad._current_time(), -aantal))
        else:
            print("Het aantal dient groter dan nul (0) en maximaal gelijk aan de voorraad te zijn")
        self.toon_voorraad()

    def toon_voorraad(self):
        print(f"Voorraad {self._product_naam} bedraagt {self.__aantal}")

    def toon_mutaties(self):
        print(f"\nMutatie-geschiedenis voor {self._product_naam}:")
        for datum, aantal in self._mutatie_geschiedenis:
            if aantal > 0:
                mutatie_type = "bijbesteld"
            else:
                mutatie_type = "verkocht"
                aantal = abs(aantal)
            print(f"  {datum}: {aantal} {mutatie_type}")
