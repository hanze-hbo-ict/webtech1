import random


# class Enemy:
class Aardman:
    def __init__(self, naam="Aardman", hit_points=0, levens=1):
        self._naam = naam
        self._hit_points = hit_points
        self._levens = levens
        self._levend = True

    def schade(self, geraakt):
        punten_over = self._hit_points - geraakt
        if punten_over >= 0:
            self._hit_points = punten_over
            print(
                f"Je bent {geraakt} keer geraakt en hebt nog {self._hit_points} hit points over"
            )
        else:
            self._levens -= 1
            self._hit_points = 12
            if self._levens > 0:
                print(f"{self._naam} heeft een leven verloren")
            else:
                print(f"{self._naam} is dood")
                self._levend = False

    def __str__(self):
        return f"Naam: {self._naam}, Levens: {self._levens}, Hit points: {self._hit_points}"


class Ork(Aardman):
    # pass

    def __init__(self, naam=""):
        # super(Troll, self).__init__(name=name, lives=1, hit_points=23)
        super().__init__(naam=naam, levens=1, hit_points=23)

    def slaan(self):
        print(f"Me {self._naam}. {self._naam} stomp you!")


class Mordor(Ork):
    def __init__(self, naam):
        super().__init__(naam)
        self._hit_points = 140

    def schade(self, geraakt):
        super().schade(geraakt // 4)

