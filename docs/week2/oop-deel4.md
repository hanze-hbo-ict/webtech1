# OOP Python – Objecten & Relaties

In dit deel leer je hoe objecten andere objecten kunnen bevatten (**compositie**). Dit is essentieel voor het werken met databases, waar tabellen aan elkaar gereleerd zijn via foreign keys.

## Wat is compositie?

Compositie betekent dat een object andere objecten bevat. Dit is een **"heeft een"** relatie:

```python
from dataclasses import dataclass

@dataclass
class Customer:
    naam: str
    email: str

@dataclass
class Product:
    naam: str
    prijs: float

@dataclass
class Order:
    klant: Customer  # Order HEEFT EEN klant
    product: Product  # Order HEEFT EEN product

# Gebruik
jan = Customer("Jan Jansen", "jan@email.nl")
laptop = Product("Laptop", 799.99)
order = Order(jan, laptop)

print(f"{order.klant.naam} bestelde {order.product.naam}")
# Jan Jansen bestelde Laptop
```

!!! note "Compositie vs Inheritance"
    **Inheritance (is-een):** Een laptop **is een** product
    **Compositie (heeft-een):** Een order **heeft een** klant
    In databases: compositie = foreign keys!

## Waarom compositie?

In webapplicaties heb je vaak objecten die aan elkaar gerelateerd zijn:

- Een **order** heeft een **klant**
- Een **order** heeft **producten**
- Een **blogpost** heeft een **auteur**
- Een **comment** heeft een **user** en een **post**

Dit modelleer je met compositie in je code, en met foreign keys in je database.

## Objects in lists

Een object kan een lijst met andere objecten bevatten:

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    naam: str
    prijs: float

@dataclass
class Cart:
    klant_naam: str
    items: list[Product] = field(default_factory=list)

    def voeg_toe(self, product: Product) -> None:
        """Voeg product toe aan winkelcart."""
        self.items.append(product)

    def bereken_totaal(self) -> float:
        """Bereken totaalprijs van alle producten."""
        return sum(product.prijs for product in self.items)

# Gebruik
cart = Cart("Jan Jansen")
cart.voeg_toe(Product("Laptop", 799.99))
cart.voeg_toe(Product("Muis", 25.50))

print(f"Totaal: €{cart.bereken_totaal():.2f}")
# Totaal: €825.49
```

!!! warning "field(default_factory=list)"
    Voor een lijst als attribuut moet je altijd `field(default_factory=list)` gebruiken, anders delen alle instanties dezelfde lijst!

## Return dictionaries voor gestructureerde data

In webapplicaties wil je vaak gestructureerde data teruggeven aan templates:

```python
from dataclasses import dataclass

@dataclass
class Customer:
    naam: str
    email: str
    korting_percentage: float = 0.0

    def bereken_korting(self, bedrag: float) -> float:
        """Bereken kortingsbedrag."""
        return bedrag * (self.korting_percentage / 100)

@dataclass
class Order:
    klant: Customer
    subtotaal: float
    verzendkosten: float = 5.95

    def bereken_totaal(self) -> dict:
        """
        Bereken totaal en geef gestructureerde data terug.

        Returns:
            dict met keys: subtotaal, korting, verzendkosten, totaal
        """
        korting = self.klant.bereken_korting(self.subtotaal)

        # Gratis verzending boven €50 (na korting)
        verzendkosten = self.verzendkosten
        if (self.subtotaal - korting) >= 50:
            verzendkosten = 0.0

        totaal = self.subtotaal - korting + verzendkosten

        return {
            "subtotaal": self.subtotaal,
            "korting": korting,
            "verzendkosten": verzendkosten,
            "totaal": totaal
        }

# Gebruik
jan = Customer("Jan Jansen", "jan@email.nl", 10.0)
order = Order(jan, subtotaal=125.50)

totaal_info = order.bereken_totaal()
print(f"Subtotaal: €{totaal_info['subtotaal']:.2f}")
print(f"Korting: -€{totaal_info['korting']:.2f}")
print(f"Verzendkosten: €{totaal_info['verzendkosten']:.2f}")
print(f"Totaal: €{totaal_info['totaal']:.2f}")
```

!!! info "Waarom dictionaries teruggeven?"
    Dictionaries zijn handig voor templates. In Flask kun je ze doorgeven aan Jinja2 templates:
    ```python
    @app.route('/order/<int:id>')
    def toon_order(id):
        order = db.session.get(Order, id)
        totaal_info = order.bereken_totaal()
        return render_template('order.html',
                             order=order,
                             totaal=totaal_info)
    ```
    In het template (`order.html`) kun je dan de dictionary gebruiken:
    ```html
    <p>Subtotaal: €{{ totaal.subtotaal }}</p>
    <p>Korting: -€{{ totaal.korting }}</p>
    <p>Totaal: €{{ totaal.totaal }}</p>
    ```

## Complexe compositie: Complete order

Hier een realistisch voorbeeld met meerdere gecomponeerde objecten:

```python
from dataclasses import dataclass, field

@dataclass
class Customer:
    naam: str
    email: str
    korting_percentage: float = 0.0

    def bereken_korting(self, bedrag: float) -> float:
        return bedrag * (self.korting_percentage / 100)

@dataclass
class Product:
    naam: str
    prijs: float
    voorraad: int = 0

@dataclass
class PaymentMethod:
    type: str  # "iDEAL", "Creditcard", "PayPal"
    transactiekosten: float = 0.0

    def bereken_totaal_met_kosten(self, bedrag: float) -> float:
        return bedrag + self.transactiekosten

@dataclass
class ShippingMethod:
    type: str  # "Standaard", "Express", "Afhalen"
    kosten: float
    levertijd: str

@dataclass
class DiscountCode:
    code: str
    percentage: float

    def bereken_korting(self, bedrag: float) -> float:
        return bedrag * (self.percentage / 100)

@dataclass
class Order:
    """Complete order met alle relaties."""
    klant: Customer
    producten: list[Product] = field(default_factory=list)
    betaalmethode: PaymentMethod | None = None
    verzendmethode: ShippingMethod | None = None
    kortingscode: DiscountCode | None = None

    def bereken_subtotaal(self) -> float:
        """Som van alle productprijzen."""
        return sum(p.prijs for p in self.producten)

    def bereken_totaal(self) -> dict:
        """
        Bereken complete totaal met alle kortingen en kosten.

        Returns:
            dict met alle bedragen - handig voor templates
        """
        subtotaal = self.bereken_subtotaal()

        # DiscountCode
        korting = 0.0
        if self.kortingscode:
            korting = self.kortingscode.bereken_korting(subtotaal)

        # Verzendkosten (gratis boven €50 na korting)
        verzendkosten = 0.0
        if self.verzendmethode:
            verzendkosten = self.verzendmethode.kosten
            if (subtotaal - korting) >= 50:
                verzendkosten = 0.0

        # Transactiekosten
        tussentotaal = subtotaal - korting + verzendkosten
        transactiekosten = 0.0
        if self.betaalmethode:
            transactiekosten = self.betaalmethode.transactiekosten

        totaal = tussentotaal + transactiekosten

        return {
            "subtotaal": subtotaal,
            "korting": korting,
            "verzendkosten": verzendkosten,
            "transactiekosten": transactiekosten,
            "totaal": totaal
        }

# Test complete systeem
laptop = Product("Gaming Laptop", 799.99, 5)
muis = Product("Gaming Muis", 89.99, 20)

jan = Customer("Jan Jansen", "jan@email.nl", 5.0)

order = Order(
    klant=jan,
    producten=[laptop, muis],
    betaalmethode=PaymentMethod("iDEAL", transactiekosten=0.0),
    verzendmethode=ShippingMethod("Standaard", 5.95, "2-3 werkdagen"),
    kortingscode=DiscountCode("WELKOM10", 10.0)
)

totaal_info = order.bereken_totaal()

print(f"Customer: {order.klant.naam}")
print(f"Producten: {len(order.producten)}x")
print(f"\nSubtotaal: €{totaal_info['subtotaal']:.2f}")
print(f"Korting: -€{totaal_info['korting']:.2f}")
print(f"Verzendkosten: €{totaal_info['verzendkosten']:.2f}")
print(f"Transactiekosten: €{totaal_info['transactiekosten']:.2f}")
print(f"TOTAAL: €{totaal_info['totaal']:.2f}")
```

## Preview: Database relaties (Foreign Keys)

Dit is waarom je compositie leert - in databases werk je zo met gerelateerde tabellen:

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120))

    # Relationship
    posts: Mapped[list['BlogPost']] = relationship(back_populates='author')

class BlogPost(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str]

    # Foreign key: elke post HEEFT EEN auteur
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # Relationship: geeft toegang tot het User object
    author: Mapped['User'] = relationship(back_populates='posts')

# Gebruik (week 6!)
user = db.session.get(User, 1)
post = BlogPost(title="Mijn blog", content="...", author=user)
db.session.add(post)
db.session.commit()

# Compositie in actie:
print(f"{post.title} door {post.author.username}")
```

!!! info "OOP → Database mapping"
    - **Compositie in Python** → **Foreign key in database**
    - `order.klant` → `orderen.klant_id` (foreign key naar `klanten.id`)
    - Objecten bevatten objecten → Tabellen verwijzen naar tabellen

## Gestructureerde data voor templates

Voor webapplicaties wil je vaak je data in een gestructureerde vorm aan templates doorgeven:

```python
from dataclasses import dataclass

@dataclass
class Customer:
    naam: str
    email: str

@dataclass
class Product:
    naam: str
    prijs: float

@dataclass
class Order:
    klant: Customer
    producten: list[Product]

    def bereken_overzicht(self) -> dict:
        """Maak een overzicht voor de template."""
        subtotaal = sum(p.prijs for p in self.producten)
        return {
            "klant_naam": self.klant.naam,
            "aantal_producten": len(self.producten),
            "subtotaal": subtotaal,
            "btw": subtotaal * 0.21,
            "totaal": subtotaal * 1.21
        }

# Test
jan = Customer("Jan Jansen", "jan@email.nl")
order = Order(
    klant=jan,
    producten=[
        Product("Laptop", 799.99),
        Product("Muis", 25.50)
    ]
)

overzicht = order.bereken_overzicht()
print(overzicht)
```

Output:

```python
{
    'klant_naam': 'Jan Jansen',
    'aantal_producten': 2,
    'subtotaal': 825.49,
    'btw': 173.35,
    'totaal': 998.84
}
```

!!! tip "Dataclass → dictionary voor debugging"
    Je kunt `asdict()` gebruiken om een dataclass automatisch naar een dictionary te converteren. Dit is vooral handig voor debugging:
    ```python
    from dataclasses import asdict
    klant_dict = asdict(jan)
    print(klant_dict)
    # {'naam': 'Jan Jansen', 'email': 'jan@email.nl'}
    ```
    Let op: in productiecode maak je meestal zelf specifieke dictionaries met alleen de data die je template nodig heeft.

## Praktijk: Flask routes met templates

Hier zie je hoe dit in een echte Flask applicatie werkt:

```python
from flask import Flask, render_template
from dataclasses import dataclass

app = Flask(__name__)

@dataclass
class Product:
    id: int
    naam: str
    prijs: float

# In-memory "database" (later: echte database!)
producten = [
    Product(1, "Laptop", 799.99),
    Product(2, "Muis", 25.50),
    Product(3, "Toetsenbord", 89.99)
]

@app.route('/producten')
def toon_producten():
    """Toon alle producten in een template."""
    return render_template('producten.html', producten=producten)

@app.route('/product/<int:product_id>')
def toon_product(product_id):
    """Toon één product."""
    product = next((p for p in producten if p.id == product_id), None)

    if product:
        return render_template('product.html', product=product)
    else:
        return "Product niet gevonden", 404
```

In je template (`producten.html`) kun je dan de objecten gebruiken:

```html
<h1>Producten</h1>
<ul>
{% for product in producten %}
    <li>{{ product.naam }} - €{{ product.prijs }}</li>
{% endfor %}
</ul>
```

!!! note "Return values → Templates"
    Zie je waarom we altijd **return values** gebruiken en niet **print**? In een Flask route moet je data doorgeven aan je template, niet naar de console printen.

## Scheiding van verantwoordelijkheden (separation of concerns)

Goede code scheidt verantwoordelijkheden:

**Bedrijfslogica (modellen):**

```python
@dataclass
class Order:
    """Bevat bedrijfslogica en data."""
    klant: Customer
    producten: list[Product]

    def bereken_totaal(self) -> dict:
        """Bereken totaal - RETURN data."""
        return {"totaal": sum(p.prijs for p in self.producten)}
```

**Presentatielaag (routes):**

```python
@app.route('/order/<int:id>')
def toon_order(id):
    """Haalt data op en presenteert het."""
    order = get_order(id)  # Haal op
    totaal_info = order.bereken_totaal()  # Bereken

    # Presenteer in template
    return render_template('order.html',
                         order=order,
                         totaal=totaal_info)
```

!!! info "Waarom scheiden?"
    - De bedrijfslogica is herbruikbaar (webapplicatie, CLI, tests)
    - Makkelijker te testen (geen Flask nodig voor tests)
    - Duidelijke verantwoordelijkheden

## Checklist

Controleer of je het volgende beheerst:

- [ ] Compositie: objecten die andere objecten bevatten
- [ ] `list[Object]` met `field(default_factory=list)`
- [ ] `X | None` voor attributen die None kunnen zijn
- [ ] Methoden die dictionaries teruggeven voor templates
- [ ] Begrijpen: compositie in code = foreign keys in database
- [ ] Scheiding van verantwoordelijkheden: bedrijfslogica vs presentatie

## Samenvatting

In dit deel heb je geleerd:

- **Compositie**: Objecten die andere objecten bevatten (heeft-een relatie)
- **Type hints**: `list[Product]`, `Customer | None`
- **Return dictionaries**: Gestructureerde data voor templates
- **Database preview**: Compositie = foreign keys
- **Scheiding van verantwoordelijkheden**: Bedrijfslogica apart van presentatie

**Je kunt nu:**

- Complexe datastructuren modelleren met objecten
- Web-ready code schrijven die data aan templates doorgeeft
- Begrijpen hoe SQLAlchemy relaties werkt (foreign keys)
- Code schrijven die geschikt is voor Flask applicaties

**Volgende stap:** Later ga je dit toepassen met SQLAlchemy. Je modellen krijgen foreign keys en relationships om tabellen aan elkaar te koppelen.

**Oefening:** Maak [Oefening 4](oefeningen/oop-oefening4.md) om compositie te oefenen met een compleet orderssysteem.
