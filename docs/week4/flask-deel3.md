# Flask – Basale Werking

Aan het eind van deze tekst maken we [oefening 1](oefeningen/flask-oefening1.md).

## Hoe werkt Flask?

Vanuit vogelvluchtperspectief werkt Flask als volgt:

1. **Client stuurt request** → Browser navigeert naar een URL (bijv. `/products`)
2. **Flask routeert request** → Flask checkt welke functie bij deze route hoort
3. **Functie wordt uitgevoerd** → De view-functie genereert een response (HTML, JSON, etc.)
4. **Response naar client** → Browser toont de HTML of verwerkt de data

Dit patroon heet het **Request-Response Cycle** en is fundamental voor alle webframeworks.

## Je eerste Flask app

We maken een bestand `app.py` waarin we de `Flask` class importeren en een instantie (applicatie object) maken:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Homepage route - retourneert een welkomstbericht."""
    return "<h1>Welkom bij muziekschool Session</h1>"


if __name__ == "__main__":
    app.run(debug=True)
```

### Code uitleg regel voor regel

**Regel 1**: `from flask import Flask`

- Importeer de `Flask` class uit de flask module

**Regel 3**: `app = Flask(__name__)`

- Maak een Flask applicatie instance
- `__name__` vertelt Flask waar templates en static files staan

**Regel 6**: `@app.route("/")`

- **Decorator** die de functie hieronder koppelt aan een route
- `/` is de homepage (root URL)
- Als gebruiker naar `http://127.0.0.1:5000/` gaat, wordt `index()` aangeroepen

**Regel 7**: `def index() -> str:`

- View function die HTML returnt
- `-> str` is een **type hint** (modern Python pattern!)
- Docstring beschrijft wat de functie doet

**Regel 9**: `return "<h1>...</h1>"`

- HTML string die naar de browser wordt gestuurd
- Later vervangen we dit door templates

**Regel 12-13**: `if __name__ == "__main__":`

- Dit blok wordt alleen uitgevoerd als je dit bestand direct runt
- Voorkomt dat de server start bij imports

**Regel 13**: `app.run(debug=True)`

- Start de development server
- `debug=True` activeert auto-reload en betere foutmeldingen

!!! tip "Type hints in Flask"
    We gebruiken type hints (`-> str`) bij alle Flask routes. Dit is modern Python en helpt editors met autocomplete en type checking!

### De app runnen

Start je app met uv (vanuit Week 2/3 workflow):

```console
uv run python app.py
```

Je ziet output zoals:

```console
 * Serving Flask app "app"
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

Open je browser en ga naar `http://127.0.0.1:5000/`:

> **Verwacht resultaat:** De browser toont de homepage met de tekst "Welkom bij muziekschool Session" als grote kop (`<h1>`), zonder verdere opmaak of stijl.

!!! warning "Development server"
    De Flask development server is ALLEEN voor development! Voor productie gebruik je een echte WSGI server zoals Gunicorn of uWSGI.

## Meerdere routes

Een webapplicatie heeft meestal meerdere pagina's. Voeg eenvoudig extra routes toe:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Homepage."""
    return "<h1>Welkom bij muziekschool Session</h1>"


@app.route("/informatie")
def info() -> str:
    """Informatiepagina over de muziekschool."""
    return "<h1>Dit hebben we jou te bieden:</h1><p>Piano, gitaar, drums, zang</p>"


@app.route("/contact")
def contact() -> str:
    """Contactpagina."""
    return "<h1>Neem contact op</h1><p>Email: info@session.nl</p>"


if __name__ == "__main__":
    app.run(debug=True)
```

Nu kun je naar drie verschillende URLs gaan:

- `http://127.0.0.1:5000/` → Homepage
- `http://127.0.0.1:5000/informatie` → Informatiepagina
- `http://127.0.0.1:5000/contact` → Contactpagina

> **Verwacht resultaat:** De browser toont de `/informatie` pagina met de kop "Dit hebben we jou te bieden:" gevolgd door de tekst "Piano, gitaar, drums, zang".

!!! info "Auto-reload met debug mode"
    Met `debug=True` hoef je de server niet handmatig te herstarten. Flask detecteert wijzigingen en herstart automatisch!

## 404 - Pagina niet gevonden

Als je naar een route gaat die niet bestaat (bijv. `http://127.0.0.1:5000/nope`), krijg je een 404 error:

> **Verwacht resultaat:** De browser toont de standaard Flask 404-foutpagina met de melding "Not Found" en de uitleg dat de gevraagde URL niet op de server bestaat.

Je kunt eigen foutpagina's maken voor 404s.

## Dynamische routes

Wat als je honderden cursisten hebt, elk met hun eigen profielpagina? Je wilt niet voor elke cursist een aparte route schrijven!

**Oplossing:** Dynamische routes met URL parameters.

### Basis voorbeeld

```python
@app.route("/cursist/<naam>")
def cursist(naam: str) -> str:
    """Cursist profielpagina met dynamische naam.

    Args:
        naam: De naam van de cursist uit de URL
    """
    return f"<h1>Dit is de pagina van {naam}</h1>"
```

**Hoe werkt dit:**

- `<naam>` in de route is een **variabele**
- De waarde wordt uit de URL gehaald en doorgegeven aan de functie
- `naam: str` is de parameter met type hint

**Voorbeelden:**

- `http://localhost:5000/cursist/Henk` → Pagina van Henk
- `http://localhost:5000/cursist/Joyce` → Pagina van Joyce
- `http://localhost:5000/cursist/Ralf` → Pagina van Ralf

> **Verwacht resultaat:** De browser toont de pagina voor de route `/cursist/Henk` met de tekst "Dit is de pagina van Henk" als grote kop.

### URL parameters met types

Je kunt het type van URL parameters specificeren:

```python
@app.route("/product/<int:product_id>")
def product(product_id: int) -> str:
    """Product detailpagina.

    Args:
        product_id: ID van het product (integer)
    """
    return f"<h1>Product {product_id}</h1>"


@app.route("/prijs/<float:bedrag>")
def prijs(bedrag: float) -> str:
    """Toon prijs met BTW.

    Args:
        bedrag: Prijs excl. BTW
    """
    btw = bedrag * 0.21
    totaal = bedrag + btw
    return f"<p>Excl: €{bedrag:.2f}<br>BTW: €{btw:.2f}<br>Totaal: €{totaal:.2f}</p>"
```

**Beschikbare types:**

- `<variabele>` → string (default)
- `<int:variabele>` → integer
- `<float:variabele>` → float
- `<path:variabele>` → string met slashes (voor file paths)
- `<uuid:variabele>` → UUID string

> **Verwacht resultaat:** De browser toont de pagina voor `/product/123` met de kop "Product 123". Flask heeft de `<int:product_id>` parameter automatisch als integer verwerkt.

### Meerdere parameters

```python
@app.route("/les/<string:instrument>/<int:niveau>")
def les(instrument: str, niveau: int) -> str:
    """Lesinfo met instrument en niveau.

    Args:
        instrument: Type instrument (gitaar, piano, etc.)
        niveau: Niveau (1=beginner, 2=gevorderd, 3=expert)
    """
    niveau_naam = ["beginner", "gevorderd", "expert"][niveau - 1]
    return f"<h1>{instrument.capitalize()} - {niveau_naam}</h1>"
```

URL: `http://localhost:5000/les/gitaar/2` → "Gitaar - gevorderd"

## Debug mode en foutmeldingen

### Zonder debug mode

Voeg opzettelijk een fout toe:

```python
@app.route("/fout/<naam>")
def fout(naam: str) -> str:
    """Demonstreer foutmelding (opzettelijke bug)."""
    # Bug: probeer 20e karakter terwijl naam meestal korter is
    return f"De 20e letter van {naam} is {naam[20]}"
```

Start server ZONDER debug: `app.run()` (zonder `debug=True`)

Navigeer naar `http://localhost:5000/fout/Jan` (3 karakters, geen 20e):

> **Verwacht resultaat:** De browser toont een generieke "500 Internal Server Error" pagina zonder verdere details. Er is geen uitleg over de oorzaak van de fout zichtbaar.

Weinig informatie, moeilijk te debuggen!

### Met debug mode

Zet `debug=True` aan: `app.run(debug=True)`

Nu krijg je een **interactieve debugger**:

> **Verwacht resultaat:** De browser toont de Flask interactieve debugger met de volledige stack trace, de exacte foutmelding (`IndexError: string index out of range`), en de regelnummer in de code waar de fout optrad.

Je ziet:

- Exacte foutmelding (`IndexError: string index out of range`)
- Stack trace met regelnummers
- Code context (welke regel crashte)
- Interactieve console (klik op console icoon, voer PIN in)

!!! danger "Debug mode in productie"
    NOOIT `debug=True` gebruiken in productie! Het toont sourcecode en staat remote code execution toe (via de debug console).
    Productie setup:
    ```python
    if __name__ == "__main__":
        # Development
        app.run(debug=True)
    else:
        # Productie (via Gunicorn/uWSGI)
        pass
    ```

## Best practices

### Type hints overal

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Homepage."""
    return "<h1>Welkom</h1>"


@app.route("/user/<int:user_id>")
def user(user_id: int) -> str:
    """User profile.

    Args:
        user_id: ID van de gebruiker
    """
    return f"<p>User ID: {user_id}</p>"


if __name__ == "__main__":
    app.run(debug=True)
```

### Docstrings voor routes

```python
@app.route("/product/<int:product_id>")
def product(product_id: int) -> str:
    """Product detailpagina.

    Deze route toont details van een specifiek product.

    Args:
        product_id: Unieke identifier van het product

    Returns:
        HTML string met product informatie
    """
    # Later: haal product op uit database
    return f"<h1>Product {product_id}</h1>"
```

### Consistente naming

```python
# Goed: lowercase met underscores
@app.route("/my-page")
def my_page() -> str:
    """Route handler voor /my-page."""
    return "<p>Content</p>"

# Vermijd: CamelCase in functienamen
@app.route("/other-page")
def otherPage() -> str:  # Niet Pythonic!
    return "<p>Content</p>"
```

## Voorbereiding op Templates (Deel 4)

HTML in Python strings is niet handig voor grotere pagina's. Met **Jinja2 templates** scheid je HTML van Python:

```python
# Nu (deel 3):
@app.route("/")
def index() -> str:
    return "<h1>Welkom</h1><p>Dit is de homepage</p>"

# Straks (deel 4):
from flask import render_template

@app.route("/")
def index() -> str:
    return render_template("index.html", title="Welkom")
```

Met templates scheid je HTML (presentatie) van Python (logica)!

## Link met Week 3 (SQL)

Later combineer je Flask routes met databases:

```python
import sqlite3
from flask import Flask

app = Flask(__name__)


@app.route("/products")
def products() -> str:
    """Toon alle producten uit database."""
    with sqlite3.connect("shop.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM products")
        results = cursor.fetchall()

    # Nu: HTML in string (onhandig)
    html = "<h1>Producten</h1><ul>"
    for product in results:
        html += f"<li>{product['name']}: €{product['price']}</li>"
    html += "</ul>"
    return html

# Later (Week 6): met SQLAlchemy + templates!
```

## Samenvatting

Je hebt geleerd:

- **Flask app structuur**: `Flask(__name__)`, routes, `app.run()`
- **Routes maken**: `@app.route("/path")`
- **Type hints**: `-> str` voor return types, `naam: str` voor parameters
- **Dynamische routes**: `<naam>`, `<int:id>`, `<float:prijs>`
- **Debug mode**: Auto-reload en interactieve debugger
- **Best practices**: Type hints, docstrings, consistent naming

**Volgende stap:** [Deel 4](flask-deel4.md) - Jinja2 templates.

**Oefening:** Maak nu [oefening 1](oefeningen/flask-oefening1.md).

!!! tip "Modern Flask pattern"
    Deze patterns (type hints, docstrings, `uv`) gebruik je voor alle Flask projecten in deze cursus. In Week 6 voeg je SQLAlchemy toe voor database operaties!
