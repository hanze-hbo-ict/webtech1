class Vleugel:
    def __init__(self, ratio):
        self.ratio = ratio

    def vliegen(self):
        if self.ratio > 1:
            print("Wauwwww, dit is fun")
        elif self.ratio == 1:
            print("Pff, hard werken, maar ik vlieg tenminste")
        else:
            print("Ik denk dat ik maar weer gewoon ga waggelen")


class Duck:
    def __init__(self):
        self._vleugel = Vleugel(1.8)

    def lopen(self):
        print("Waggel, waggel, waggel")

    def zwemmen(self):
        print("Kom er lekker in, het water is heerlijk")

    def kwaken(self):
        print("Kwak, kwak, kwak")

    def vliegen(self):
        self._vleugel.vliegen()


class Pinguin:
    def lopen(self):
        print("Waggel, waggel, ik waggel ook")

    def zwemmen(self):
        print("Kom er in, maar het is wel een beetje koud, zo zuidelijk")

    def kwaken(self):
        print("Kwaken? Lachen, ik ben een pinquin, hoor!")


class Toom:
    def __init__(self):
        self.toom = []

    def add_duck(self, duck):
        self.toom.append(duck)

    def migratie(self):
        for duck in self.toom:
            duck.vliegen()


def test_duck(duck):
    duck.lopen()
    duck.zwemmen()
    duck.kwaken()


if __name__ == "__main__":
    donald = Duck()
    donald.vliegen()
    # test_duck(donald)
    #
    # percy = Pinguin()
    # test_duck(percy)

