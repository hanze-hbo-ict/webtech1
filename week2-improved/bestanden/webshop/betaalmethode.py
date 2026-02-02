"""Betaalmethode-klasse voor de webshop"""


class Betaalmethode:
    """Klasse voor betaalmethoden"""

    def __init__(self, type_betaling, kosten=0.0):
        self.type = type_betaling
        self.kosten = kosten  # Eventuele transactiekosten

    def verwerk_betaling(self, bedrag):
        """Verwerk een betaling"""
        totaal = bedrag + self.kosten
        print(f"Betaling van €{totaal:.2f} wordt verwerkt via {self.type}")
        if self.kosten > 0:
            print(f"  (inclusief €{self.kosten:.2f} transactiekosten)")
        return totaal


if __name__ == '__main__':
    # Test betaalmethoden
    ideal = Betaalmethode("iDEAL", kosten=0.0)
    creditcard = Betaalmethode("Creditcard", kosten=2.50)
    paypal = Betaalmethode("PayPal", kosten=1.00)

    print("=== Test iDEAL ===")
    ideal.verwerk_betaling(99.99)

    print("\n=== Test Creditcard ===")
    creditcard.verwerk_betaling(99.99)

    print("\n=== Test PayPal ===")
    paypal.verwerk_betaling(99.99)
