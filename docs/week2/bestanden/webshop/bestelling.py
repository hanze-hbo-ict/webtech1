"""Order klasse voor de webshop - demonstratie van compositie."""

import datetime


class Order:
    """Klasse voor bestellingen in de webshop.

    Een bestelling is samengesteld uit:
    - Een klant (Customer)
    - Een winkelwagen (Cart) met producten
    - Een betaalmethode (PaymentMethod)
    - Verzendkosten
    """

    def __init__(
        self,
        klant: 'Customer',
        winkelwagen: 'Cart',
        betaalmethode: 'PaymentMethod',
        verzendkosten: float = 5.95
    ):
        """Maak een nieuwe bestelling aan.

        Args:
            klant: Customer object
            winkelwagen: Cart object met producten
            betaalmethode: PaymentMethod object
            verzendkosten: Verzendkosten in euro's (default: 5.95)
        """
        self.klant = klant
        self.winkelwagen = winkelwagen
        self.betaalmethode = betaalmethode
        self.verzendkosten = verzendkosten
        self.besteldatum = datetime.datetime.now()
        self.status = "In behandeling"

    def bereken_totaal(self) -> float:
        """Bereken totaalbedrag inclusief verzendkosten.

        Returns:
            Totaalbedrag in euro's (gratis verzending boven €50)
        """
        subtotaal = self.winkelwagen.bereken_totaal()
        if subtotaal >= 50:
            return subtotaal
        return subtotaal + self.verzendkosten

    def plaats_bestelling(self) -> dict | None:
        """Plaats de bestelling en verwerk de betaling.

        Returns:
            Dict met bestellingsgegevens, of None bij lege winkelwagen
        """
        if not self.winkelwagen.items:
            return None

        subtotaal = self.winkelwagen.bereken_totaal()
        verzending = 0.0 if subtotaal >= 50 else self.verzendkosten
        totaal = subtotaal + verzending
        eindtotaal = self.betaalmethode.verwerk_betaling(totaal)

        self.status = "Bevestigd"

        return {
            "klant": self.klant.naam,
            "email": self.klant.email,
            "producten": list(self.winkelwagen.items),
            "subtotaal": subtotaal,
            "verzendkosten": verzending,
            "totaal": eindtotaal,
            "betaalmethode": self.betaalmethode.type,
            "datum": self.besteldatum.strftime("%d-%m-%Y %H:%M"),
        }

    def toon_status(self) -> None:
        """Toon de status van de bestelling."""
        print(f"\nBestellingsnummer: #{id(self)}")
        print(f"Klant: {self.klant.naam}")
        print(f"Datum: {self.besteldatum.strftime('%d-%m-%Y %H:%M')}")
        print(f"Status: {self.status}")
        print(f"Aantal producten: {len(self.winkelwagen.items)}")
        print(f"Totaalbedrag: €{self.bereken_totaal():.2f}")
