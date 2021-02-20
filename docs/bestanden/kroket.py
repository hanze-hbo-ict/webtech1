class Kroket:

    soort = "rundvleeskroket"

    def __init__(self, leverancier, prijs):
        self.leverancier = leverancier
        self.prijs = prijs
        self.trek = False

    def in_frituur(self):
        self.trek = True

kwek = Kroket("Kwekkeboom", 2.50)

print(kwek.leverancier)
print(kwek.prijs)

dob = Kroket("Van Dobben", 2.35)

print(f"Fabrikanten: {kwek.leverancier} = {kwek.prijs}, {dob.leverancier} = {dob.prijs}")

print(dob.trek)
dob.in_frituur()
print(dob.trek)

Kroket.in_frituur(kwek)
print(kwek.trek)
kwek.in_frituur()
print(kwek.trek)

kwek.waardering = 6.5
print(kwek.waardering)
#print(dob.waardering)
print(Kroket.__dict__)
print(kwek.__dict__)
print(dob.__dict__)

print(Kroket.soort)
print(kwek.soort)
print(dob.soort)
print("Wijzig rundvleeskroket naar groentekroket")
Kroket.soort = "groentekroket"
print(Kroket.soort)
print(kwek.soort)
print(dob.soort)

print("Kwekkeboom wordt nu garnalenkroket")
kwek.soort = "garnalenkroket"
print(kwek.soort)

