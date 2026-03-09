# Flask – Templates met Jinja2

Tot nu toe heb je HTML als Python strings geretourneerd. Dat werkt voor kleine voorbeelden, maar voor echte webapplicaties gebruik je **templates** - HTML bestanden met placeholders voor dynamische data.

Flask gebruikt **Jinja2** als template engine. Jinja2 laat je variabelen, loops, conditionals en meer gebruiken in HTML. Dit scheidt presentatie (HTML) van logica (Python).

Flask zoekt automatisch naar templates in de `templates/` directory in je project root.

## Project structuur met templates

Voor templates heb je twee extra directories nodig:

```console
mkdir templates
mkdir static
```

Je project structuur wordt dan:

```text
mijn-flask-app/
├── .python-version
├── .venv/
├── app.py
├── pyproject.toml
├── uv.lock
├── static/              # Voor CSS, images, JavaScript
│   └── drums.jpg
└── templates/           # Voor HTML templates
    └── basic.html
```

## Je eerste template

### Stap 1: Maak een HTML template

Maak `templates/basic.html`:

```html
<!DOCTYPE html>
<html lang="nl">
    <head>
        <meta charset="UTF-8">
        <title>Basic Template</title>
    </head>
    <body>
        <h1>Welkom bij muziekschool Session</h1>
        <h2>Dit drumstel wordt gebruikt tijdens de lessen</h2>
        <img src="{{ url_for('static', filename='drums.jpg') }}"
             width="600"
             height="400"
             alt="Drumstel">
    </body>
</html>
```

**Let op:** `{{ url_for('static', filename='drums.jpg') }}`

- Jinja2 syntax voor dynamische URL generatie
- Beter dan een vast ingesteld pad zoals `../static/drums.jpg`
- Werkt ook als je app in een subdirectory draait

### Stap 2: Render de template in Flask

Update `app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Homepage met template rendering."""
    return render_template("basic.html")


if __name__ == "__main__":
    app.run(debug=True)
```

**Code uitleg:**

- `from flask import render_template` - Import render functie
- `render_template("basic.html")` - Flask zoekt in `templates/` en rendert de HTML
- Return type blijft `str` (render_template retourneert HTML string)

### Stap 3: Run en test

```console
uv run python app.py
```

Ga naar `http://127.0.0.1:5000/` - je ziet de template met afbeelding!

> **Verwacht resultaat:** De browser toont de gerenderde template met de kop "Welkom bij muziekschool Session", een subkop "Dit drumstel wordt gebruikt tijdens de lessen", en een afbeelding van een drumstel.

## Variabelen doorgeven aan templates

De kracht van templates zit in **dynamische data**. Je geeft Python variabelen door aan de template:

### Basis voorbeeld

**Template** (`templates/welkom.html`):

```html
<!DOCTYPE html>
<html lang="nl">
    <head>
        <meta charset="UTF-8">
        <title>Welkom</title>
    </head>
    <body>
        <h1>Hallo {{ naam }}!</h1>
        <p>Je bent cursist nummer {{ cursist_id }}</p>
    </body>
</html>
```

**Flask route** (`app.py`):

```python
@app.route("/cursist/<naam>")
def cursist(naam: str) -> str:
    """Cursist welkomstpagina met template.

    Args:
        naam: Naam van de cursist uit URL
    """
    cursist_id = 42  # Later: haal dit op uit database
    return render_template("welkom.html", naam=naam, cursist_id=cursist_id)
```

**Hoe werkt dit:**

- `{{ naam }}` in template wordt vervangen door waarde van `naam=naam`
- `{{ cursist_id }}` wordt vervangen door `cursist_id=cursist_id`
- Eerste `naam` = template variable, tweede `naam` = Python variable

**Result:** Navigeer naar `http://localhost:5000/cursist/Joyce`

> **Verwacht resultaat:** De browser toont de pagina voor `/cursist/Joyce` met de kop "Hallo Joyce!" en de tekst "Je bent cursist nummer 42".

## Data types in templates

Je kunt alle Python types doorgeven: strings, integers, lists, dictionaries, etc.

### Voorbeeld met meerdere types

**Flask route:**

```python
@app.route("/demo")
def demo() -> str:
    """Demonstreer verschillende data types in templates."""
    naam = "Joyce"
    letters = list(naam)  # ['J', 'o', 'y', 'c', 'e']
    cursist_dict = {"1234": "Sietse", "5678": "Carla"}

    return render_template(
        "demo.html",
        naam=naam,
        letters=letters,
        cursist_dict=cursist_dict
    )
```

**Template** (`templates/demo.html`):

```html
<!DOCTYPE html>
<html lang="nl">
    <head>
        <meta charset="UTF-8">
        <title>Demo</title>
    </head>
    <body>
        <h1>Naam: {{ naam }}</h1>
        <h2>Letters als lijst: {{ letters }}</h2>
        <h2>Cursist dict: {{ cursist_dict }}</h2>

        <!-- Specifieke waardes ophalen -->
        <p>Laatste 2 letters: {{ letters[3:] }}</p>
        <p>Cursist 1234: {{ cursist_dict['1234'] }}</p>
    </body>
</html>
```

**Result:**

> **Verwacht resultaat:** De browser toont de `/demo` pagina met de naam "Joyce", de letters als lijst (`['J', 'o', 'y', 'c', 'e']`), het cursistenwoordenboek, de laatste twee letters via slicing (`['c', 'e']`), en de waarde voor sleutel "1234" (`Sietse`).

Je kunt Python syntax gebruiken in templates:

- `letters[3:]` - List slicing
- `cursist_dict['1234']` - Dictionary access
- `naam.upper()` - String methods
- En meer!

## Control flow in templates

Jinja2 ondersteunt control flow met `{% ... %}` syntax.

### For loops

**Flask route:**

```python
@app.route("/cursisten")
def cursisten() -> str:
    """Lijst van alle cursisten."""
    cursisten_lijst = ["Joyce", "Sietse", "Carla", "Henk"]
    return render_template("cursisten.html", cursisten=cursisten_lijst)
```

**Template** (`templates/cursisten.html`):

```html
<!DOCTYPE html>
<html lang="nl">
    <head>
        <meta charset="UTF-8">
        <title>Cursisten</title>
    </head>
    <body>
        <h1>Onze cursisten</h1>
        <ul>
        {% for cursist in cursisten %}
            <li>{{ cursist }}</li>
        {% endfor %}
        </ul>
    </body>
</html>
```

**Belangrijke punten:**

- `{% for ... %}` opent de loop
- `{% endfor %}` sluit de loop
- `{{ cursist }}` toont elke waarde
- Geen `:` nodig zoals in Python!

**Result:**

> **Verwacht resultaat:** De browser toont de `/cursisten` pagina met de kop "Onze cursisten" en een ongeordende lijst met de namen Joyce, Sietse, Carla en Henk als afzonderlijke items.

### If statements

Voeg conditionele logica toe aan templates:

```html
<!DOCTYPE html>
<html lang="nl">
    <head>
        <meta charset="UTF-8">
        <title>Cursisten Check</title>
    </head>
    <body>
        <h1>Cursisten lijst</h1>
        <ul>
        {% for cursist in cursisten %}
            <li>{{ cursist }}</li>
        {% endfor %}
        </ul>

        <h2>Komt Carla voor in de lijst?</h2>
        {% if 'Carla' in cursisten %}
            <p class="success">Carla komt in de lijst voor!</p>
        {% else %}
            <p class="error">Carla komt niet in de lijst voor.</p>
        {% endif %}
    </body>
</html>
```

**Result:**

> **Verwacht resultaat:** De browser toont de cursistenlijst gevolgd door de subkop "Komt Carla voor in de lijst?" met daaronder de bevestigende tekst "Carla komt in de lijst voor!" omdat de `if`-conditie waar is.

**If-elif-else:**

```html
{% if niveau == 1 %}
    <p>Beginner cursus</p>
{% elif niveau == 2 %}
    <p>Gevorderde cursus</p>
{% elif niveau == 3 %}
    <p>Expert cursus</p>
{% else %}
    <p>Onbekend niveau</p>
{% endif %}
```

## Filters in templates

Jinja2 heeft ingebouwde **filters** om data te transformeren:

```html
<h1>{{ naam|upper }}</h1>              <!-- JOYCE -->
<h1>{{ naam|lower }}</h1>              <!-- joyce -->
<h1>{{ naam|capitalize }}</h1>         <!-- Joyce -->
<h1>{{ naam|title }}</h1>              <!-- Joyce -->

<p>Prijs: {{ prijs|round(2) }}</p>     <!-- 19.99 -->
<p>Datum: {{ datum|default('Onbekend') }}</p>

<!-- List filters -->
<p>{{ cursisten|length }} cursisten</p>
<p>{{ cursisten|join(', ') }}</p>      <!-- Joyce, Sietse, Carla -->
```

**Veelgebruikte filters:**

- `|upper`, `|lower`, `|capitalize`, `|title` - String transformaties
- `|length` - Lengte van list/string
- `|default('waarde')` - Fallback als variabele None is
- `|join(', ')` - Join list elementen
- `|round(2)` - Rond float af
- `|safe` - Mark HTML als veilig (voorkom escaping)

## Template inheritance (belangrijk!)

Voor grotere apps wil je niet steeds hetzelfde HTML herhalen. Gebruik **template inheritance**!

### Base template

**`templates/base.html`** (parent template):

```html
<!DOCTYPE html>
<html lang="nl">
    <head>
        <meta charset="UTF-8">
        <title>{% block title %}Muziekschool Session{% endblock %}</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    </head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/cursisten">Cursisten</a>
            <a href="/contact">Contact</a>
        </nav>

        <main>
            {% block content %}
            <!-- Child templates vullen dit in -->
            {% endblock %}
        </main>

        <footer>
            <p>&copy; 2024 Muziekschool Session</p>
        </footer>
    </body>
</html>
```

### Child template

**`templates/home.html`** (extends base):

```html
{% extends "base.html" %}

{% block title %}Home - Muziekschool Session{% endblock %}

{% block content %}
    <h1>Welkom bij Muziekschool Session</h1>
    <p>We bieden lessen in piano, gitaar, drums en zang.</p>
{% endblock %}
```

**`templates/cursisten.html`** (extends base):

```html
{% extends "base.html" %}

{% block title %}Cursisten - Muziekschool Session{% endblock %}

{% block content %}
    <h1>Onze cursisten</h1>
    <ul>
    {% for cursist in cursisten %}
        <li>{{ cursist }}</li>
    {% endfor %}
    </ul>
{% endblock %}
```

## Complete voorbeeld met types

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Homepage."""
    return render_template("home.html")


@app.route("/cursisten")
def cursisten() -> str:
    """Cursisten overzicht met template."""
    cursisten_lijst = ["Joyce", "Sietse", "Carla"]
    return render_template("cursisten.html", cursisten=cursisten_lijst)


@app.route("/cursist/<int:cursist_id>")
def cursist_detail(cursist_id: int) -> str:
    """Cursist detail pagina.

    Args:
        cursist_id: ID van de cursist
    """
    # Later: haal uit database
    cursist_data = {
        "id": cursist_id,
        "naam": "Joyce",
        "instrument": "Piano",
        "niveau": 2
    }
    return render_template("cursist_detail.html", cursist=cursist_data)


if __name__ == "__main__":
    app.run(debug=True)
```

**Template** (`templates/cursist_detail.html`):

```html
{% extends "base.html" %}

{% block title %}{{ cursist.naam }} - Cursisten{% endblock %}

{% block content %}
    <h1>Cursist: {{ cursist.naam }}</h1>
    <dl>
        <dt>ID:</dt>
        <dd>{{ cursist.id }}</dd>

        <dt>Instrument:</dt>
        <dd>{{ cursist.instrument }}</dd>

        <dt>Niveau:</dt>
        <dd>
            {% if cursist.niveau == 1 %}
                Beginner
            {% elif cursist.niveau == 2 %}
                Gevorderd
            {% else %}
                Expert
            {% endif %}
        </dd>
    </dl>
{% endblock %}
```

## Link met Week 3 (SQL)

Straks combineer je templates met database queries:

```python
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/products")
def products() -> str:
    """Product lijst uit database."""
    with sqlite3.connect("shop.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM products ORDER BY name")
        products_list = cursor.fetchall()

    return render_template("products.html", products=products_list)
```

**Template** (`templates/products.html`):

```html
{% extends "base.html" %}

{% block content %}
    <h1>Producten</h1>
    <table>
        <thead>
            <tr>
                <th>Naam</th>
                <th>Prijs</th>
                <th>Voorraad</th>
            </tr>
        </thead>
        <tbody>
        {% for product in products %}
            <tr>
                <td>{{ product.name }}</td>
                <td>€{{ product.price|round(2) }}</td>
                <td>{{ product.stock }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
{% endblock %}
```

Met SQLAlchemy wordt dit nog makkelijker - dat zie je in Week 6.

## Best practices

### 1. Type hints in Flask routes

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Homepage met type hint."""
    return render_template("home.html")


@app.route("/user/<int:user_id>")
def user(user_id: int) -> str:
    """User pagina met typed parameter."""
    return render_template("user.html", user_id=user_id)
```

### 2. Template inheritance

Gebruik altijd `base.html` voor consistente layout.

### 3. Comments in templates

```html
{# Dit is een Jinja2 comment - wordt niet gerenderd #}

{#
Multi-line comment
Ook mogelijk
#}

<!-- HTML comment - wordt WEL naar browser gestuurd -->
```

### 4. Template organization

```text
templates/
├── base.html
├── components/
│   ├── navbar.html
│   └── footer.html
├── cursisten/
│   ├── list.html
│   └── detail.html
└── home.html
```

Gebruik subdirectories voor grotere apps!

## Samenvatting

Je hebt geleerd:

- **Templates maken** in `templates/` directory
- **Static files** serveren uit `static/` directory
- **Variabelen doorgeven** met `render_template()`
- **Template syntax**: `{{ variabele }}` en `{% control %}`
- **For loops**: `{% for item in items %}`
- **If statements**: `{% if conditie %}`
- **Filters**: `{{ naam|upper }}`, `{{ prijs|round(2) }}`
- **Template inheritance**: `{% extends "base.html" %}`
- **Type hints**: `-> str` voor render_template returns

**Volgende stap:** Week 5 - Flask Forms en WTForms.
