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
                "Je bent {} keer geraakt en hebt nog {} hit points over".format(
                    geraakt, self._hit_points
                )
            )
        else:
            self._levens -= 1
            self._hit_points = 12
            if self._levens > 0:
                print("{0._naam} heeft een leven verloren".format(self))
            else:
                print("{0._naam} is dood".format(self))
                self._levend = False

    def __str__(self):
        return "Naam: {0._naam}, Levens: {0._levens}, Hit points: {0._hit_points}".format(
            self
        )


class Ork(Aardman):
    # pass

    def __init__(self, naam=""):
        # super(Troll, self).__init__(name=name, lives=1, hit_points=23)
        super().__init__(naam=naam, levens=1, hit_points=23)

    def slaan(self):
        print("Me {0._naam}. {0._naam} stomp you!".format(self))


class Mordor(Ork):
    def __init__(self, naam):
        super().__init__(naam)
        self._hit_points = 140

    def schade(self, geraakt):
        super().schade(geraakt // 4)

