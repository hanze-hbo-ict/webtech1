"""PaymentMethod klasse voor de webshop."""


class PaymentMethod:
    """Klasse voor betaalmethoden."""

    def __init__(self, type_betaling: str, kosten: float = 0.0):
        """Maak een betaalmethode aan.

        Args:
            type_betaling: Naam van de betaalmethode
            kosten: Eventuele transactiekosten in euro's (default: 0.0)
        """
        self.type = type_betaling
        self.kosten = kosten

    def verwerk_betaling(self, bedrag: float) -> float:
        """Verwerk een betaling.

        Args:
            bedrag: Te betalen bedrag in euro's

        Returns:
            Totaalbedrag inclusief transactiekosten
        """
        return bedrag + self.kosten

    def __str__(self) -> str:
        """String representatie van de betaalmethode."""
        if self.kosten > 0:
            return f"{self.type} (€{self.kosten:.2f} transactiekosten)"
        return self.type


if __name__ == '__main__':
    # Test betaalmethoden
    ideal = PaymentMethod("iDEAL")
    creditcard = PaymentMethod("Creditcard", kosten=2.50)
    paypal = PaymentMethod("PayPal", kosten=1.00)

    for methode in [ideal, creditcard, paypal]:
        totaal = methode.verwerk_betaling(99.99)
        print(f"{methode}: totaal €{totaal:.2f}")
