# OOP Python – Oefening 2

In deze oefening ga je werken met **dataclasses** en geavanceerde **type hints**. Je zet een reguliere klasse om naar een dataclass en maakt een winkelwagen systeem.

## Deel a: Product omzetten naar dataclass

Je hebt in oefening 1 waarschijnlijk een reguliere `Product` klasse gemaakt. Nu ga je deze omzetten naar een dataclass.

### Opdracht a

Maak een bestand `product.py` met een `Product` dataclass:

**Attributen:**

- `naam` (str): Productnaam
- `prijs` (float): Prijs in euro's
- `voorraad` (int): Aantal op voorraad (default: 0)
- `beschrijving` (str | None): Een optionele beschrijving (default: None)

**Methoden:**

- `verkoop(aantal: int) -> bool`: Verkoop items, geeft True bij succes
- `voorraad_waarde() -> float`: Bereken totale waarde van voorraad

### Startcode

```python
from dataclasses import dataclass

@dataclass
class Product:
    # Jouw code hier
    pass
```

!!! tip "str | None"
    `beschrijving: str | None = None` betekent dat beschrijving een string OF None kan zijn.

### Test je Product

```python
laptop = Product("Laptop", 799.99, 5, "Gaming laptop met RGB")
muis = Product("Muis", 25.50, 20)  # Geen beschrijving

print(laptop)
print(f"Voorraadwaarde: €{laptop.voorraad_waarde():.2f}")

laptop.verkoop(2)

print(laptop)
print(f"Voorraadwaarde: €{laptop.voorraad_waarde():.2f}")
```

**Verwachte output:**

```text
Product(naam='Laptop', prijs=799.99, voorraad=5, beschrijving='Gaming laptop met RGB')
Voorraadwaarde: €3999.95
Product(naam='Laptop', prijs=799.99, voorraad=3, beschrijving='Gaming laptop met RGB')
Voorraadwaarde: €2399.97
```

## Deel b: Winkelwagen met list type hint

Maak een bestand `winkelwagen.py` met een `Winkelwagen` dataclass.

### Opdracht b

**Attributen:**

- `klant_naam` (str): Naam van de klant
- `items` (list[Product]): Lijst met producten

**Methoden:**

- `voeg_toe(product: Product) -> None`: Voeg product toe
- `verwijder(product: Product) -> bool`: Verwijder product, geeft True als gelukt
- `bereken_totaal() -> float`: Bereken totaalprijs
- `aantal_items() -> int`: Geef aantal items terug

!!! warning "Veranderbare standaardwaarden: gebruik field()"
    Voor lists als default waarde **moet** je `field(default_factory=list)` gebruiken!

    ```python
    from dataclasses import dataclass, field

    @dataclass
    class Winkelwagen:
        klant_naam: str
        items: list[Product] = field(default_factory=list)
    ```

### Test je Winkelwagen

```python
from product import Product
from winkelwagen import Winkelwagen

# Maak producten
laptop = Product("Laptop", 799.99, 5)
muis = Product("Muis", 25.50, 20)
toetsenbord = Product("Toetsenbord", 89.99, 15)

# Maak winkelwagen
wagen = Winkelwagen("Jan Jansen")
print(f"Aantal items: {wagen.aantal_items()}")  # Should be 0

# Voeg producten toe
wagen.voeg_toe(laptop)
wagen.voeg_toe(muis)
wagen.voeg_toe(toetsenbord)

print(f"Aantal items: {wagen.aantal_items()}")
print(f"Totaal: €{wagen.bereken_totaal():.2f}")

# Verwijder item
if wagen.verwijder(muis):
    print("Muis verwijderd")

print(f"Nieuw totaal: €{wagen.bereken_totaal():.2f}")
```

**Verwachte output:**

```text
Aantal items: 0
Aantal items: 3
Totaal: €915.48
Muis verwijderd
Nieuw totaal: €889.98
```

## Checklist

Controleer voordat je klaar bent:

- [ ] `Product` gebruikt `@dataclass` decorator (de `@`-aanduiding boven de klasse)
- [ ] `str | None` gebruikt voor beschrijving
- [ ] `Winkelwagen` gebruikt `list[Product]` type hint
- [ ] `field(default_factory=list)` gebruikt voor items
- [ ] Alle methoden hebben return type annotations
- [ ] Code werkt met de testcode

## Wat je geleerd hebt

- `@dataclass` vermindert herhalende code (boilerplate)
- `X | None` voor waarden die None kunnen zijn
- `list[Type]` voor typed lists
- `field(default_factory=list)` voor veranderbare standaardwaarden

**Tip:** Deze patterns zie je later terug in SQLAlchemy modellen!
