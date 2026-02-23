# OOP Python – Overerving

In dit deel leer je hoe **overerving** werkt in Python. Dit is een essentiële basis voor het werken met SQLAlchemy, waar je straks modellen maakt die erven van `db.Model`.

## Wat is overerving?

Overerving betekent dat een klasse eigenschappen en methoden overneemt van een andere klasse:

```python
class Product:
    def __init__(self, naam: str, prijs: float):
        self.naam = naam
        self.prijs = prijs

class FysiekProduct(Product):
    def __init__(self, naam: str, prijs: float, gewicht: float):
        super().__init__(naam, prijs)  # Roep parent constructor aan
        self.gewicht = gewicht

laptop = FysiekProduct("Laptop", 799.99, 2.5)
print(laptop.naam)  # Werkt! Overgenomen van Product
```

**Terminologie:**

- `Product` is de **bovenliggende klasse** (ook wel: parent class, superclass)
- `FysiekProduct` is de **subklasse** (ook wel: child class, derived class)

## Wanneer gebruik je overerving?

Gebruik overerving wanneer er een **"is een"** relatie is:

- Een `FysiekProduct` **is een** `Product`
- Een `DigitaalProduct` **is een** `Product`
- Een `User` **is een** `db.Model` (SQLAlchemy!)

!!! note "Is-een vs heeft-een"
    **Overerving (is-een):** Een laptop is een product
    **Compositie (heeft-een):** Een bestelling heeft een klant (zie deel 4)

## `super()` gebruiken

`super()` roept de bovenliggende klasse aan. Dit gebruik je vooral in `__init__`:

```python
class Product:
    def __init__(self, naam: str, prijs: float):
        self.naam = naam
        self.prijs = prijs
        print(f"Product aangemaakt: {naam}")

class FysiekProduct(Product):
    def __init__(self, naam: str, prijs: float, gewicht: float):
        super().__init__(naam, prijs)  # Parent initialisatie
        self.gewicht = gewicht
        print(f"Gewicht: {gewicht} kg")
```

!!! warning "super() is verplicht"
    Als je `super().__init__()` vergeet, worden de attributen van de bovenliggende klasse niet geïnitialiseerd. Je krijgt dan fouten als `AttributeError: 'FysiekProduct' object has no attribute 'naam'`.

## Methoden overerven en overschrijven

Subklassen erven alle methoden van de bovenliggende klasse:

```python
class Product:
    def __init__(self, naam: str, prijs: float, voorraad: int):
        self.naam = naam
        self.prijs = prijs
        self.voorraad = voorraad

    def verkoop(self, aantal: int) -> bool:
        if self.voorraad >= aantal:
            self.voorraad -= aantal
            return True
        return False

    def bereken_waarde(self) -> float:
        return self.prijs * self.voorraad

class FysiekProduct(Product):
    def __init__(self, naam: str, prijs: float, voorraad: int, gewicht: float):
        super().__init__(naam, prijs, voorraad)
        self.gewicht = gewicht

    def bereken_verzendkosten(self) -> float:
        """Nieuwe methode, alleen in FysiekProduct."""
        if self.gewicht <= 1.0:
            return 3.95
        elif self.gewicht <= 5.0:
            return 6.95
        else:
            return 9.95

# Test
boek = FysiekProduct("Python Crash Course", 34.95, 10, 0.6)
boek.verkoop(3)  # Inherited van Product!
print(f"Voorraad: {boek.voorraad}")  # 7
print(f"Verzendkosten: €{boek.bereken_verzendkosten():.2f}")  # €3.95
```

### Methoden overschrijven

Je kunt een methode van de bovenliggende klasse vervangen door dezelfde methode in de child te definiëren:

```python
class Product:
    def __init__(self, naam: str, prijs: float):
        self.naam = naam
        self.prijs = prijs

    def __str__(self) -> str:
        return f"Product: {self.naam} - €{self.prijs:.2f}"

class DigitaalProduct(Product):
    def __init__(self, naam: str, prijs: float, bestandsgrootte: float):
        super().__init__(naam, prijs)
        self.bestandsgrootte = bestandsgrootte

    def __str__(self) -> str:
        """Override: voeg bestandsgrootte toe."""
        return f"Digitaal Product: {self.naam} - €{self.prijs:.2f} ({self.bestandsgrootte} MB)"

photoshop = DigitaalProduct("Photoshop", 29.99, 2480.0)
print(photoshop)  # Gebruikt de overridden __str__
```

!!! tip "Type annotations bij overschrijven"
    Gebruik bij overschrijven dezelfde type annotations als de overschreven methode. Dit houdt je code consistent en voorkomt fouten.

## Overerving met dataclasses

Dataclasses maken overerving nog eenvoudiger - je hoeft geen `super().__init__()` te gebruiken:

```python
from dataclasses import dataclass

@dataclass
class Product:
    naam: str
    prijs: float
    voorraad: int = 0

    def verkoop(self, aantal: int) -> bool:
        if self.voorraad >= aantal:
            self.voorraad -= aantal
            return True
        return False

@dataclass
class FysiekProduct(Product):
    gewicht: float = 0.5  # Nieuw attribuut

    def bereken_verzendkosten(self) -> float:
        if self.gewicht <= 1.0:
            return 3.95
        elif self.gewicht <= 5.0:
            return 6.95
        else:
            return 9.95

# Gebruik
laptop = FysiekProduct("Gaming Laptop", 1299.99, 5, gewicht=2.5)
print(laptop)
# FysiekProduct(naam='Gaming Laptop', prijs=1299.99, voorraad=5, gewicht=2.5)
```

!!! info "Parent attributen eerst"
    Bij dataclass overerving komen attributen van de bovenliggende klasse automatisch eerst. Attributen van de subklasse komen daarna. Je hoeft niets extra's te doen.

## Overerving op meerdere niveaus

Je kunt ook van een subklasse erven (overervingshiërarchie):

```python
from dataclasses import dataclass

@dataclass
class Product:
    naam: str
    prijs: float
    voorraad: int = 0

@dataclass
class FysiekProduct(Product):
    gewicht: float = 0.5

@dataclass
class Boek(FysiekProduct):
    auteur: str = ""
    isbn: str = ""

    def __str__(self) -> str:
        return f"{self.naam} door {self.auteur} (ISBN: {self.isbn})"

# Boek erft van FysiekProduct, die erft van Product
python_boek = Boek(
    naam="Python Crash Course",
    prijs=34.95,
    voorraad=8,
    gewicht=0.6,
    auteur="Eric Matthes",
    isbn="978-1593279288"
)

print(python_boek)
# Python Crash Course door Eric Matthes (ISBN: 978-1593279288)
```

!!! note "Overervingshiërarchie"
    `Boek` → `FysiekProduct` → `Product`
    Een `Boek` heeft toegang tot alle attributen en methoden van zowel `FysiekProduct` als `Product`.

## Preview: SQLAlchemy modellen

Dit is waarom je overerving leert - straks in week 6 ga je database modellen maken:

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

db = SQLAlchemy()

class User(db.Model):  # Erft van db.Model!
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120))

class Product(db.Model):  # Erft van db.Model!
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    naam: Mapped[str] = mapped_column(String(100))
    prijs: Mapped[float]
```

Door te erven van `db.Model` krijgen je klassen automatisch alle database functionaliteit: opslaan, opvragen, verwijderen, etc.

!!! info "Waarom OOP voor SQLAlchemy?"
    SQLAlchemy gebruikt OOP omdat het perfect past bij database structuur:
    - Elke **klasse** = een database **tabel**
    - Elk **object** = een **rij** in de tabel
    - Overerving geeft je de database functionaliteit

    SQLAlchemy vertaalt je Python code naar SQL. In week 3 schrijf je die SQL zelf - dat laat zien wat er achter de schermen gebeurt.

## Praktijkvoorbeeld: Producttypes

Hier een compleet voorbeeld met verschillende producttypes:

```python
from dataclasses import dataclass

@dataclass
class Product:
    """Basis product klasse."""
    naam: str
    prijs: float
    voorraad: int = 0
    beschrijving: str | None = None

    def verkoop(self, aantal: int) -> bool:
        """Verkoop items. Geeft True terug bij succes."""
        if self.voorraad >= aantal:
            self.voorraad -= aantal
            return True
        return False

    def voorraad_waarde(self) -> float:
        """Bereken totale waarde van voorraad."""
        return self.prijs * self.voorraad

@dataclass
class FysiekProduct(Product):
    """Product dat fysiek verzonden moet worden."""
    gewicht: float = 0.5

    def bereken_verzendkosten(self) -> float:
        """Bereken verzendkosten op basis van gewicht."""
        if self.gewicht <= 1.0:
            return 3.95
        elif self.gewicht <= 5.0:
            return 6.95
        else:
            return 9.95

@dataclass
class DigitaalProduct(Product):
    """Product dat digitaal geleverd wordt."""
    bestandsgrootte: float = 0.0  # MB
    download_link: str = ""
    voorraad: int = 999  # Digitale producten zijn bijna onbeperkt

    def download(self) -> dict:
        """Simuleer download. Geeft download info terug."""
        if self.voorraad > 0:
            self.voorraad -= 1
            return {
                "product": self.naam,
                "link": self.download_link,
                "grootte_mb": self.bestandsgrootte
            }
        return {"error": "Niet beschikbaar"}

# Test
laptop = FysiekProduct("Gaming Laptop", 1299.99, 5, gewicht=2.5)
game = DigitaalProduct(
    "Cyberpunk 2077", 59.99,
    bestandsgrootte=70000.0,
    download_link="https://gog.com/download/cyberpunk"
)

print(f"Laptop verzendkosten: €{laptop.bereken_verzendkosten():.2f}")
info = game.download()
print(f"Download: {info['product']} ({info['grootte_mb']} MB)")
```

## Checklist

Controleer of je het volgende beheerst:

- [ ] Begrijpen wanneer je overerving gebruikt (is-een relatie)
- [ ] `super().__init__()` correct gebruiken in reguliere klassen
- [ ] Overerving met dataclasses (automatische parent attributen)
- [ ] Methoden overschrijven met dezelfde signature
- [ ] Meerdere niveaus overerving (Boek → FysiekProduct → Product)
- [ ] Type annotations bij inherited en overridden methoden
- [ ] Begrijpen waarom SQLAlchemy overerving gebruikt

## Samenvatting

In dit deel heb je geleerd:

- **Overerving**: Een subklasse neemt eigenschappen over van de bovenliggende klasse
- **`super()`**: Roept de bovenliggende klasse aan, vooral in `__init__()`
- **Overschrijven**: Een subklasse kan methoden van de bovenliggende klasse vervangen
- **Dataclass overerving**: Nog eenvoudiger dan reguliere klassen
- **Hierarchie**: Meerdere niveaus overerving mogelijk
- **SQLAlchemy preview**: Database modellen erven van `db.Model`

**Volgende stap:** In deel 4 leer je over compositie - objecten die andere objecten bevatten. Dit is de basis voor foreign keys in databases.

**Oefening:** Maak [Oefening 3](oefeningen/oop-oefening3.md) om overerving te oefenen.
