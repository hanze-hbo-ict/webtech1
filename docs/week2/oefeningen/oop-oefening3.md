# OOP Python – Oefening 3

In deze oefening pas je **overerving** toe. Je maakt subklassen van `Product` voor verschillende producttypen, wat je voorbereidt op het werken met database modellen die erven van `db.Model`.

## Achtergrond

In een webshop heb je verschillende soorten producten:

- **Fysieke producten**: hebben gewicht en verzendkosten
- **Digitale producten**: hebben bestandsgrootte en geen verzending

Dit is een perfect geval voor overerving: beide zijn producten, maar met specifieke eigenschappen.

## Deel a: FysiekProduct

Maak een `FysiekProduct` klasse die erft van `Product`.

### Opdracht a

**Extra attributen:**

- `gewicht` (float): Gewicht in kg

**Extra methoden:**

- `bereken_verzendkosten() -> float`: Bereken verzendkosten op basis van gewicht
  - Tot 1 kg: €3.95
  - Tot 5 kg: €6.95
  - Meer dan 5 kg: €9.95

### Startcode a

```python
from dataclasses import dataclass
from product import Product

@dataclass
class FysiekProduct(Product):
    gewicht: float = 0.5  # Default 0.5 kg

    def bereken_verzendkosten(self) -> float:
        # Jouw code hier
        pass
```

!!! tip "Werken met dataclass overerving"
    Bij dataclasses hoef je geen `super().__init__()` te gebruiken - de attributen van de bovenliggende klasse worden automatisch overgenomen!

### Test je FysiekProduct

```python
boek = FysiekProduct(
    naam="Python Crash Course",
    prijs=34.95,
    voorraad=8,
    gewicht=0.6
)

print(boek)
print(f"Verzendkosten: €{boek.bereken_verzendkosten():.2f}")

laptop = FysiekProduct("Gaming Laptop", 1299.99, 3, gewicht=2.5)
print(f"Verzendkosten laptop: €{laptop.bereken_verzendkosten():.2f}")
```

**Verwachte output:**

```text
FysiekProduct(naam='Python Crash Course', prijs=34.95, voorraad=8, beschrijving=None, gewicht=0.6)
Verzendkosten: €3.95
Verzendkosten laptop: €6.95
```

## Deel b: DigitaalProduct

Maak een `DigitaalProduct` klasse die erft van `Product`.

### Opdracht b

**Extra attributen:**

- `bestandsgrootte` (float): Grootte in MB
- `download_link` (str): URL voor download

**Defaults:**

- `voorraad`: 999 (digitale producten zijn bijna onbeperkt beschikbaar)

**Extra methoden:**

- `download() -> dict`: Simuleer een download
  - Verminder voorraad met 1
  - Geef een dictionary terug met info: `{"product": naam, "link": download_link, "grootte_mb": bestandsgrootte}`

### Startcode b

```python
@dataclass
class DigitaalProduct(Product):
    bestandsgrootte: float = 0.0  # MB
    download_link: str = ""
    voorraad: int = 999  # Override parent default

    def download(self) -> dict:
        # Jouw code hier
        pass
```

### Test je DigitaalProduct

```python
photoshop = DigitaalProduct(
    naam="Adobe Photoshop",
    prijs=29.99,
    bestandsgrootte=2480.0,
    download_link="https://adobe.com/download/ps"
)

print(photoshop)
info = photoshop.download()
print(f"Download info: {info}")
print(f"Voorraad na download: {photoshop.voorraad}")
```

## Deel c: Subklasse van subklasse

Maak een `Boek` klasse die erft van `FysiekProduct`.

### Opdracht c

**Extra attributen:**

- `auteur` (str): Naam van de auteur
- `isbn` (str): ISBN nummer

**Defaults:**

- `gewicht`: 0.5 kg (boeken zijn meestal licht)

**Override `__str__()`:**
Maak een eigen string-representatie die ook auteur en ISBN toont.

### Startcode c

```python
@dataclass
class Boek(FysiekProduct):
    auteur: str = ""
    isbn: str = ""
    gewicht: float = 0.5

    def __str__(self) -> str:
        # Hint: gebruik f-string met alle relevante info
        pass
```

### Test je Boek

```python
python_boek = Boek(
    naam="Python Crash Course",
    prijs=34.95,
    voorraad=8,
    auteur="Eric Matthes",
    isbn="978-1593279288"
)

print(python_boek)
print(f"Verzendkosten: €{python_boek.bereken_verzendkosten():.2f}")

# Test verkoop (inherited van Product)
python_boek.verkoop(3)
print(f"Voorraad na verkoop: {python_boek.voorraad}")
```

## Extra uitdaging: Software klasse (optioneel)

Maak een `Software` klasse die erft van `DigitaalProduct` met extra attributen:

- `versie` (str): Versienummer
- `besturingssysteem` (str): "Windows", "Mac", "Linux", etc.

Test door een instantie te maken en downloads te simuleren.

## Checklist

Controleer voordat je klaar bent:

- [ ] `FysiekProduct` erft van `Product`
- [ ] `DigitaalProduct` erft van `Product`
- [ ] `Boek` erft van `FysiekProduct`
- [ ] Alle type annotations aanwezig
- [ ] `download()` geeft een dictionary terug (geen print)
- [ ] `bereken_verzendkosten()` werkt correct
- [ ] `__str__()` overschreven in de `Boek`-klasse
- [ ] Code werkt met alle testcode

## Wat je geleerd hebt

- Overerving met dataclasses
- Override van default waarden in subklassen
- Override van methoden (`__str__`)
- Overerving hierarchie (Boek → FysiekProduct → Product)
- Return dicts voor gestructureerde data

**Preview:** Database modellen werken precies zo - je maakt klassen die erven van `db.Model`!
