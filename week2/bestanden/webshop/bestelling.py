"""Bestelling klasse voor de webshop - demonstratie van compositie"""

import datetime


class Bestelling:
    """Klasse voor bestellingen in de webshop

    Een bestelling is samengesteld uit:
    - Een klant
    - Een winkelwagen met producten
    - Een betaalmethode
    - Verzendkosten
    """

    def __init__(self, klant, winkelwagen, betaalmethode, verzendkosten=5.95):
        self.klant = klant
        self.winkelwagen = winkelwagen
        self.betaalmethode = betaalmethode
        self.verzendkosten = verzendkosten
        self.besteldatum = datetime.datetime.now()
        self.status = "In behandeling"

    def bereken_totaal(self):
        """Berekent totaalbedrag inclusief verzendkosten"""
        subtotaal = self.winkelwagen.bereken_totaal()

        # Gratis verzending boven €50
        if subtotaal >= 50:
            verzending = 0.0
        else:
            verzending = self.verzendkosten

        return subtotaal + verzending

    def plaats_bestelling(self):
        """Plaatst de bestelling en verwerkt de betaling"""
        if not self.winkelwagen.items:
            print("Kan geen lege bestelling plaatsen!")
            return False

        print(f"\n{'='*50}")
        print(f"BESTELLING VOOR {self.klant._naam}")
        print(f"{'='*50}")

        # Toon producten
        print("\nProducten:")
        for product in self.winkelwagen.items:
            print(f"  - {product}")

        # Bereken kosten
        totaal = self.bereken_totaal()
        print(f"Totaal: €{totaal:.2f}")

        # Verwerk betaling
        print(f"\nBetaalmethode: {self.betaalmethode.type}")
        self.betaalmethode.verwerk_betaling(totaal)

        # Bevestiging
        self.status = "Bevestigd"
        print(f"\nBestelling bevestigd!")
        print(f"Bevestiging per e-mail verzonden naar {self.klant._email}")
        print(f"Verwachte levering: 2-3 werkdagen")
        print(f"{'='*50}\n")

        return True

    def toon_status(self):
        """Toont de status van de bestelling"""
        print(f"\nBestellingsnummer: #{id(self)}")
        print(f"Klant: {self.klant._naam}")
        print(f"Datum: {self.besteldatum.strftime('%d-%m-%Y %H:%M')}")
        print(f"Status: {self.status}")
        print(f"Aantal producten: {len(self.winkelwagen.items)}")
        print(f"Totaalbedrag: €{self.bereken_totaal():.2f}")
