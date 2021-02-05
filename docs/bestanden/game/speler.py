class Speler(object):

    def __init__(self, naam):
        self.naam = naam
        self._levens = 3
        self._level = 1
        self._score = 0

    def _get_levens(self):
      return self._levens

    def _set_levens(self, levens):
       if levens >= 0:
           self._levens = levens
       else:
          print("Levens kunnen geen negatieve waarde krijgen")
          self._levens = 0

    def _get_level(self):
        return self._level

    def _set_level(self, level):
        if level > 0:
            delta = level - self._level
            self._score += delta * 1000
            self._level = level
        else:
            print("Het laagste level is level 1")

    levens = property(_get_levens, _set_levens)
    level = property(_get_level, _set_level)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    def __str__(self):
      return "Name: {0.naam}, Levens: {0.levens}, Level: {0.level}, Score {0.score}".format(self)
