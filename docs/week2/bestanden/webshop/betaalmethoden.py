"""Betaalmethode klassen voor polymorfisme demonstratie."""


class Creditcard:
    """Klasse voor de betaalmethode Creditcard."""

    def valideer(self) -> bool:
        """Valideer de Creditcard.

        Returns:
            True als validatie geslaagd
        """
        return True

    def verwerk_betaling(self, bedrag: float) -> str:
        """Verwerk de betaling.

        Args:
            bedrag: Te betalen bedrag in euro's

        Returns:
            Bevestigingsbericht van de betaling
        """
        return f"€{bedrag:.2f} wordt afgeschreven van creditcard"

    def bevestig(self) -> None:
        """Bevestig de transactie."""


class iDEAL:
    """Klasse voor de betaalmethode iDEAL."""

    def valideer(self) -> bool:
        """Valideer de bankrekening.

        Returns:
            True als validatie geslaagd
        """
        return True

    def verwerk_betaling(self, bedrag: float) -> str:
        """Verwerk de betaling.

        Args:
            bedrag: Te betalen bedrag in euro's

        Returns:
            Bevestigingsbericht van de betaling
        """
        return f"€{bedrag:.2f} wordt overgemaakt via iDEAL"

    def bevestig(self) -> None:
        """Bevestig de transactie."""


class PayPal:
    """Klasse voor de betaalmethode PayPal."""

    def valideer(self) -> bool:
        """Valideer het PayPal account.

        Returns:
            True als validatie geslaagd
        """
        return True

    def verwerk_betaling(self, bedrag: float) -> str:
        """Verwerk de betaling.

        Args:
            bedrag: Te betalen bedrag in euro's

        Returns:
            Bevestigingsbericht van de betaling
        """
        return f"€{bedrag:.2f} wordt betaald via PayPal"

    def bevestig(self) -> None:
        """Bevestig de transactie."""


def test_betaling(betaalmethode, bedrag: float) -> None:
    """Testfunctie om een betaalmethode te testen."""
    if betaalmethode.valideer():
        bericht = betaalmethode.verwerk_betaling(bedrag)
        betaalmethode.bevestig()
        print(bericht)
    else:
        print(f"Validatie mislukt voor {type(betaalmethode).__name__}")


if __name__ == '__main__':
    visa = Creditcard()
    test_betaling(visa, 99.99)

    ideal_betaling = iDEAL()
    test_betaling(ideal_betaling, 49.95)

    paypal = PayPal()
    test_betaling(paypal, 149.99)
