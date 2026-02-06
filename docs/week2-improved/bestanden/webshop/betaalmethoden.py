class Creditcard:
    """Klasse voor de betaalmethode Creditcard uit het deel over polymorfisme"""

    def valideer(self):
        print("Creditcardnummer wordt gevalideerd...")

    def verwerk_betaling(self, bedrag):
        print(f"€{bedrag:.2f} wordt afgeschreven van creditcard")

    def bevestig(self):
        print("Betaling bevestigd. Transactie afgerond.")

class iDEAL:
    """Klasse voor de betaalmethode iDEAL uit het deel over polymorfisme"""

    def valideer(self):
        print("Bankrekening wordt geverifieerd...")

    def verwerk_betaling(self, bedrag):
        print(f"€{bedrag:.2f} wordt overgemaakt via iDEAL")

    def bevestig(self):
        print("iDEAL betaling geslaagd!")

class PayPal:
    """Klasse voor de betaalmethode PayPal uit het deel over polymorfisme"""

    def valideer(self):
        print("PayPal account wordt gecontroleerd...")

    def verwerk_betaling(self, bedrag):
        print(f"€{bedrag:.2f} wordt betaald via PayPal")

    def bevestig(self):
        print("PayPal transactie voltooid!")


def test_betaling(betaalmethode, bedrag):
    """ Driver-functie om een betaalmethode te testen"""
    betaalmethode.valideer()
    betaalmethode.verwerk_betaling(bedrag)
    betaalmethode.bevestig()

# De tests
if __name__ == '__main__':
    visa = Creditcard()
    test_betaling(visa, 99.99)

    ideal_betaling = iDEAL()
    test_betaling(ideal_betaling, 49.95)

    paypal = PayPal()
    test_betaling(paypal, 149.99)