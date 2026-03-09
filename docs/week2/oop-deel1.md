# OOP Python – Inleiding tot objecten

Je gaat nu werken met objecten in Python. Dit is een fundamenteel concept - later ga je zien hoe een database rij automatisch een object wordt in je code.

## Waarom objecten?

Tot nu toe heb je geprogrammeerd met losse variabelen en functies. Voor kleine programma's werkt dat prima, maar bij grotere applicaties zoals een webshop wordt het al snel onoverzichtelijk. Objecten groeperen gerelateerde data en functionaliteit.

**Voorbeeld:** In een webshop heeft elk product eigenschappen (naam, prijs, voorraad) en acties (verkopen, prijs aanpassen). In plaats van losse variabelen gebruik je een *klasse* als sjabloon om *objecten* (instanties) te maken.

## Je eerste klasse: Product

```python
class Product:
    def __init__(self, naam: str, prijs: float, voorraad: int):
        self.naam = naam
        self.prijs = prijs
        self.voorraad = voorraad
```

### Klasse definitie

```python
class Product:
```

Met `class` definieer je een nieuwe klasse. De naam begint altijd met een hoofdletter (`Product`, niet `product`).

### Type annotaties

```python
def __init__(self, naam: str, prijs: float, voorraad: int):
```

De **type annotaties** (`: str`, `: float`, `: int`) geven aan welk datatype je verwacht:

- `naam: str` - een string
- `prijs: float` - een getal met decimalen
- `voorraad: int` - een heel getal

!!! info "Waarom type annotaties?"
    Type annotaties zijn nieuw voor je, maar hebben drie grote voordelen:
    1. Je ziet direct wat een functie verwacht - code wordt makkelijker te begrijpen
    2. Je editor helpt je met autocompletion en waarschuwt voor fouten
    3. Later (bij databases en webapplicaties) zijn ze vereist
    Vanaf nu gebruik je ze standaard in je code.

### De constructor: `__init__`

```python
def __init__(self, naam: str, prijs: float, voorraad: int):
    self.naam = naam
    self.prijs = prijs
    self.voorraad = voorraad
```

De `__init__` methode is de **constructor** - deze wordt automatisch aangeroepen wanneer je een nieuw object aanmaakt.

!!! note "`self` - het object zelf"
    `self` verwijst naar het object zelf. Wanneer je `self.naam = naam` schrijft, maak je een **attribuut** aan dat bij dit specifieke object hoort.
    **Belangrijk:** Elke methode moet `self` als eerste parameter hebben - Python geeft het huidige object automatisch door.

### Objecten aanmaken

```python
laptop = Product("Laptop", 799.99, 5)
muis = Product("Draadloze muis", 25.50, 20)
```

Je hebt nu twee **objecten** (instanties) van de klasse `Product`. Elk object heeft zijn eigen waarden:

```python
print(laptop.naam)      # "Laptop"
print(laptop.prijs)     # 799.99
print(muis.naam)        # "Draadloze muis"
print(muis.prijs)       # 25.50
```

### Terminologie

Term | Betekenis
---|---
**Klasse** | Een sjabloon voor het maken van objecten (bijv. `Product`)
**Object/Instantie** | Een concreet exemplaar van een klasse (bijv. `laptop`)
**Attribuut** | Een variabele die bij een object hoort (bijv. `naam`, `prijs`)
**Methode** | Een functie die bij een klasse hoort
**Constructor** | De `__init__` methode die een nieuw object initialiseert

## Methoden toevoegen

Een klasse kan **methoden** bevatten - functies die bij de klasse horen:

```python
class Product:
    def __init__(self, naam: str, prijs: float, voorraad: int):
        self.naam = naam
        self.prijs = prijs
        self.voorraad = voorraad

    def verkoop(self, aantal: int) -> bool:
        """Verkoop een aantal items. Geeft True terug bij succes, False bij onvoldoende voorraad."""
        if self.voorraad >= aantal:
            self.voorraad -= aantal
            return True
        return False
```

**Belangrijke details:**

1. **Return type annotatie**: `-> bool` betekent dat deze methode een boolean teruggeeft
2. **Docstring**: De regel tussen `"""` documenteert wat de methode doet
3. **Return value**: De methode geeft `True` of `False` terug - de aanroepende code beslist wat ermee gebeurt

!!! warning "Print vs Return in webapplicaties"
    De `verkoop()` methode geeft een boolean terug in plaats van te printen. Dit is essentieel voor webapplicaties:
    - `print()` schrijft naar de console - de gebruiker ziet dit niet
    - `return` geeft data terug aan de aanroepende code
    In Flask geef je data terug aan de browser. Je `Product` klasse weet alleen van producten - feedback tonen aan gebruikers doet je Flask route:
    ```python
    # Later in een Flask route:
    if laptop.verkoop(2):
        flash("Product verkocht!")
        return redirect('/winkelwagen')
    else:
        flash("Onvoldoende voorraad")
        return redirect('/producten')
    ```
    Dit heet **scheiding van verantwoordelijkheden** (separation of concerns): elke laag in je applicatie heeft zijn eigen verantwoordelijkheid.

## De `__str__` methode

Python heeft **speciale methoden** die beginnen en eindigen met dubbele underscores (`__`), ook wel "dunder methods" genoemd (van "double underscore").

De `__str__` methode bepaalt hoe een object als string wordt weergegeven:

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

    def __str__(self) -> str:
        return f"{self.naam}: €{self.prijs:.2f} ({self.voorraad} op voorraad)"
```

Nu kun je een product direct printen:

```python
laptop = Product("Laptop", 799.99, 5)
print(laptop)
# Output: Laptop: €799.99 (5 op voorraad)
```

## Volledige voorbeeld

```python
class Product:
    """Een product in de webshop."""

    def __init__(self, naam: str, prijs: float, voorraad: int):
        self.naam = naam
        self.prijs = prijs
        self.voorraad = voorraad

    def verkoop(self, aantal: int) -> bool:
        """Verkoop een aantal items. Geeft True terug bij succes."""
        if self.voorraad >= aantal:
            self.voorraad -= aantal
            return True
        return False

    def voorraad_bijvullen(self, aantal: int) -> None:
        """Voeg items toe aan de voorraad."""
        self.voorraad += aantal

    def __str__(self) -> str:
        return f"{self.naam}: €{self.prijs:.2f} ({self.voorraad} op voorraad)"


# Gebruik de klasse
laptop = Product("Laptop", 799.99, 5)
print(laptop)
# Output: Laptop: €799.99 (5 op voorraad)

# Verkoop
if laptop.verkoop(2):
    print(f"Verkocht! Nieuwe voorraad: {laptop.voorraad}")
else:
    print("Onvoldoende voorraad")
# Output: Verkocht! Nieuwe voorraad: 3

# Voorraad bijvullen
laptop.voorraad_bijvullen(10)
print(laptop)
# Output: Laptop: €799.99 (13 op voorraad)
```

## Meerdere objecten

Je kunt meerdere objecten van dezelfde klasse maken, elk met eigen data:

```python
laptop = Product("Laptop", 799.99, 5)
muis = Product("Draadloze muis", 25.50, 20)
toetsenbord = Product("Mechanisch toetsenbord", 89.99, 15)

# Elk object is onafhankelijk
laptop.verkoop(2)
muis.verkoop(5)

print(laptop)        # Laptop: €799.99 (3 op voorraad)
print(muis)          # Draadloze muis: €25.50 (15 op voorraad)
print(toetsenbord)   # Mechanisch toetsenbord: €89.99 (15 op voorraad)
```

Elk object heeft zijn eigen `voorraad` attribuut - wijzigingen in `laptop.voorraad` hebben geen effect op `muis.voorraad`.

## Methoden met berekeningen

Methoden kunnen ook berekeningen doen:

```python
class Product:
    def __init__(self, naam: str, prijs: float, voorraad: int):
        self.naam = naam
        self.prijs = prijs
        self.voorraad = voorraad

    def bereken_voorraadwaarde(self) -> float:
        """Bereken de totale waarde van de voorraad."""
        return self.prijs * self.voorraad

    def bereken_prijs_met_btw(self, btw_percentage: float = 21.0) -> float:
        """Bereken prijs inclusief BTW."""
        return self.prijs * (1 + btw_percentage / 100)

    def __str__(self) -> str:
        return f"{self.naam}: €{self.prijs:.2f}"


laptop = Product("Laptop", 799.99, 5)

print(f"Voorraadwaarde: €{laptop.bereken_voorraadwaarde():.2f}")
# Output: Voorraadwaarde: €3999.95

print(f"Prijs incl. BTW: €{laptop.bereken_prijs_met_btw():.2f}")
# Output: Prijs incl. BTW: €968.39

print(f"Prijs met 9% BTW: €{laptop.bereken_prijs_met_btw(9.0):.2f}")
# Output: Prijs met 9% BTW: €871.99
```

!!! tip "Default waarden"
    `btw_percentage: float = 21.0` is een **default waarde** - als je geen waarde meegeeft, wordt 21.0 gebruikt. Dit is handig voor parameters die vaak dezelfde waarde hebben.

## Samenvatting

Je hebt nu gezien:

- **Klassen en objecten**: Een klasse is een sjabloon, een object is een instantie
- **Type annotaties**: `: str`, `: float`, `-> bool` maken code duidelijker en helpen fouten voorkomen
- **Constructor**: `__init__` initialiseert nieuwe objecten
- **Attributen**: Data die bij een object hoort (bijv. `self.naam`)
- **Methoden**: Functies binnen een klasse, eerste parameter is altijd `self`
- **Return values**: Methoden geven data terug (geen print statements)
- **Speciale methoden**: `__str__` bepaalt string representatie

### Belangrijke regels

1. Type annotaties altijd gebruiken
2. Return values in plaats van print statements (web-ready code)
3. Elke methode heeft `self` als eerste parameter
4. Klasse namen beginnen met hoofdletter, methode namen met kleine letter

### Volgende stap

In het volgende deel: **dataclasses** - een moderne manier om klassen te maken die vooral data bevatten. Dit maakt je code nog korter en leesbaarder.

---

**Maak nu [oefening 1](oefeningen/oop-oefening1.md).**
