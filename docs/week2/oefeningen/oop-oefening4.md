# OOP Python – Oefening 4

In deze oefening werk je met **compositie** - objecten die andere objecten bevatten. Je bouwt een compleet bestellingssysteem dat je voorbereidt op het werken met database relaties (foreign keys).

## Achtergrond

Een bestelling in een webshop is samengesteld uit meerdere objecten:

- Een **Klant** (wie bestelt?)
- Een lijst met **Producten** (wat wordt besteld?)
- Een **Betaalmethode** (hoe betalen?)
-Een **Verzendmethode** (hoe verzenden?)
- Optioneel: een **Kortingscode**

Dit is **compositie**: de `Bestelling` *heeft* een klant, *heeft* producten, etc.

## Deel a: Betaalmethode

Maak een `Betaalmethode` dataclass.

### Opdracht a

**Attributen:**

- `type` (str): Type betaling ("iDEAL", "Creditcard", "PayPal")
- `transactiekosten` (float): Kosten voor deze betaalmethode (default: 0.0)

**Methoden:**

- `bereken_totaal_met_kosten(bedrag: float) -> float`: Geef bedrag + transactiekosten terug

### Code a

```python
from dataclasses import dataclass

@dataclass
class Betaalmethode:
    type: str
    transactiekosten: float = 0.0

    def bereken_totaal_met_kosten(self, bedrag: float) -> float:
        # Jouw code hier
        pass
```

## Deel b: Verzendmethode

Maak een `Verzendmethode` dataclass.

### Opdracht b

**Attributen:**

- `type` (str): Type verzending ("Standaard", "Express", "Afhalen")
- `kosten` (float): Verzendkosten
- `levertijd` (str): Verwachte levertijd (bijv. "2-3 werkdagen")

### Code b

```python
@dataclass
class Verzendmethode:
    type: str
    kosten: float
    levertijd: str
```

## Deel c: Kortingscode (optioneel maar aanbevolen)

Maak een `Kortingscode` dataclass.

### Opdracht c

**Attributen:**

- `code` (str): De kortingscode (bijv. "ZOMER2024")
- `percentage` (float): Kortingspercentage (bijv. 15.0 voor 15%)

**Methoden:**

- `bereken_korting(bedrag: float) -> float`: Bereken kortingsbedrag

### Code c

```python
@dataclass
class Kortingscode:
    code: str
    percentage: float

    def bereken_korting(self, bedrag: float) -> float:
        # Jouw code hier
        pass
```

## Deel d: Bestelling (compositie!)

Nu komt het allemaal samen. Maak een `Bestelling` dataclass die alle andere objecten gebruikt.

### Opdracht d

**Attributen:**

- `klant` (Klant): Klant object
- `producten` (list[Product]): Lijst met producten
- `betaalmethode` (Betaalmethode): Betaalmethode object
- `verzendmethode` (Verzendmethode): Verzendmethode object
- `kortingscode` (Kortingscode | None): Optionele kortingscode (default: None)

**Methoden:**

1. **`bereken_subtotaal() -> float`**
   - Som van alle productprijzen

2. **`bereken_totaal() -> dict`**
   - Bereken complete totaal en geef gestructureerde data terug
   - Return dictionary met alle details (zie voorbeeld)

!!! warning "Return dict, geen print"
    De `bereken_totaal()` methode moet een **dictionary** teruggeven met alle bedragen. Zo kun je de data gemakkelijk aan templates doorgeven!

### Startcode d

```python
from dataclasses import dataclass, field

@dataclass
class Bestelling:
    klant: Klant
    producten: list[Product] = field(default_factory=list)
    betaalmethode: Betaalmethode = None
    verzendmethode: Verzendmethode = None
    kortingscode: Kortingscode | None = None

    def bereken_subtotaal(self) -> float:
        # Jouw code hier
        pass

    def bereken_totaal(self) -> dict:
        """
        Bereken totaal en geef gestructureerde data terug.

        Returns:
            dict met keys: subtotaal, korting, verzendkosten,
                          transactiekosten, totaal
        """
        subtotaal = self.bereken_subtotaal()

        # Bereken korting
        korting = 0.0
        if self.kortingscode:
            korting = self.kortingscode.bereken_korting(subtotaal)

        # Verzendkosten
        verzendkosten = self.verzendmethode.kosten if self.verzendmethode else 0.0

        # Gratis verzending boven €50
        if (subtotaal - korting) >= 50:
            verzendkosten = 0.0

        # Transactiekosten
        tussentotaal = subtotaal - korting + verzendkosten
        transactiekosten = self.betaalmethode.transactiekosten if self.betaalmethode else 0.0

        totaal = tussentotaal + transactiekosten

        return {
            "subtotaal": subtotaal,
            "korting": korting,
            "verzendkosten": verzendkosten,
            "transactiekosten": transactiekosten,
            "totaal": totaal
        }
```

## Test je complete systeem

```python
from product import Product
from klant import Klant
from bestelling import Bestelling, Betaalmethode, Verzendmethode, Kortingscode

# Maak producten
laptop = Product("Laptop", 799.99, 5)
muis = Product("Muis", 25.50, 20)

# Maak klant
jan = Klant("Jan Jansen", "jan@email.nl", 5.0)

# Maak bestelling
bestelling = Bestelling(
    klant=jan,
    producten=[laptop, muis],
    betaalmethode=Betaalmethode("iDEAL", transactiekosten=0.0),
    verzendmethode=Verzendmethode("Standaard", 5.95, "2-3 werkdagen"),
    kortingscode=Kortingscode("WELKOM10", 10.0)
)

# Bereken totaal
totaal_info = bestelling.bereken_totaal()

# Toon resultaten
print(f"Klant: {bestelling.klant.naam}")
print(f"Aantal producten: {len(bestelling.producten)}")
print(f"\nSubtotaal: €{totaal_info['subtotaal']:.2f}")
print(f"Korting (-{bestelling.kortingscode.percentage}%): -€{totaal_info['korting']:.2f}")
print(f"Verzendkosten: €{totaal_info['verzendkosten']:.2f}")
print(f"Transactiekosten: €{totaal_info['transactiekosten']:.2f}")
print(f"Totaal: €{totaal_info['totaal']:.2f}")
```

**Verwachte output:**

```text
Klant: Jan Jansen
Aantal producten: 2

Subtotaal: €825.49
Korting (-10.0%): -€82.55
Verzendkosten: €0.00
Transactiekosten: €0.00
Totaal: €742.94
```

!!! note "Gratis verzending boven €50"
    Let op: de verzendkosten zijn €0.00 omdat het subtotaal na korting boven de €50 is!

## Extra uitdaging: Data overzicht (optioneel)

Voeg een methode `maak_overzicht() -> dict` toe aan `Bestelling` die een volledig overzicht van de bestelling teruggeeft:

```python
def maak_overzicht(self) -> dict:
    """Maak een dict met alle bestellingsgegevens."""
    totaal_info = self.bereken_totaal()

    data = {
        "klant": {
            "naam": self.klant.naam,
            "email": self.klant.email
        },
        "producten": [
            {"naam": p.naam, "prijs": p.prijs}
            for p in self.producten
        ],
        "betaling": self.betaalmethode.type,
        "verzending": self.verzendmethode.type,
        "totaal": totaal_info
    }

    return data
```

Test:

```python
overzicht = bestelling.maak_overzicht()
print(overzicht)
```

## Checklist

- [ ] Alle dataclasses gebruiken `@dataclass`
- [ ] `Bestelling` gebruikt compositie (bevat andere objecten)
- [ ] `bereken_totaal()` geeft dict terug voor templates
- [ ] `Kortingscode | None` gebruikt voor kortingscode
- [ ] `list[Product]` met `field(default_factory=list)`
- [ ] Gratis verzending boven €50 werkt
- [ ] Type annotations overal
- [ ] Code werkt met testcode

## Wat je geleerd hebt

- **Compositie**: Objecten die andere objecten bevatten (has-a relatie)
- **Return dicts**: Gestructureerde data voor templates
- **X | None**: Voor attributen die None kunnen zijn
- **Complex data modeling**: Realistische webshop structuur

**Preview:** Database relaties werken precies zo - een `Order` heeft een foreign key naar `Customer`, `Product`, etc.!
