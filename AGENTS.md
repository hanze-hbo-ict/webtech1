# Context voor AI Agents & Contributors

Dit document beschrijft de ontwerpprincipes, schrijfstijl en architectuur beslissingen voor het Webtechnologie 1 cursusmateriaal. Lees dit **eerst** voordat je wijzigingen maakt.

## Projectdoel

Modernisering van het OOP/Flask cursusmateriaal voor HBO-ICT eerstejaars studenten. Focus op:
- Moderne Python conventies (type annotations, dataclasses)
- Voorbereiding op SQLAlchemy 2.0+ en Flask
- Web-ready code patterns (return values, separation of concerns)
- Pythonic code in plaats van Java-achtige patronen

## Schrijfstijl Principes

### 1. Schrijf naar de student toe

**Goed:**
```markdown
Je gaat nu werken met objecten in Python.
Vanaf nu gebruik je type annotaties standaard.
Je hebt nu twee objecten van de klasse Product.
```

**Fout:**
```markdown
In deze module gaan we werken met objecten.
We gebruiken type annotaties vanaf nu.
We hebben nu twee objecten van de klasse Product.
```

**Regel:** Gebruik consequent "je/jij", nooit "we/wij". De student doet het, niet "wij samen".

### 2. Vermijd docentenperspectief en meta-uitleg

**VERBODEN PATRONEN:**

❌ **"In dit deel leer je..." introducties**
```markdown
In dit deel leer je hoe je SQL injection voorkomt en errors afhandelt.
In deze sectie gaan we kijken naar...
```

✅ **Direct beginnen met inhoud**
```markdown
SQL injection is één van de meest voorkomende en gevaarlijkste beveiligingslekken.
```

❌ **"Voordelen voor deze cursus" lijsten**
```markdown
Voordelen van SQLite voor deze cursus:
- Eenvoudig te gebruiken
- Geen server nodig
- Perfect voor development

Waarom is Flask een goede keuze?
- Lichtgewicht framework
- Gemakkelijk te leren
```

✅ **Gewoon de feiten**
```markdown
SQLite is een lichtgewicht database die als een enkel bestand werkt en built-in bij Python zit. Geen server setup nodig.

Flask is een webframework, het is een Python-module waarmee op eenvoudige wijze webapplicaties ontwikkeld kunnen worden.
```

❌ **Vergelijkingstabellen "oud vs nieuw"**
```markdown
| Taak | pip/venv (oud) | uv (modern) |
|------|----------------|-------------|
| Package installeren | pip install flask | uv add flask |
```

✅ **Direct de moderne aanpak tonen**
```markdown
Installeer Flask met uv:
\```console
uv add flask
\```
```

❌ **"Later/Straks leer je..." forward references**
```markdown
Later leer je SQLAlchemy voor database operaties.
Straks zie je hoe templates werken.
In Week 6 gebruik je dit met SQLAlchemy.
```

✅ **Neutrale verwijzingen**
```markdown
Met SQLAlchemy wordt dit nog makkelijker - dat zie je in Week 6.
Met templates scheid je HTML van Python.
```

**REGEL:**
- Geen cursus-meta-uitleg ("dit vak leert je...", "voordelen voor de cursus...")
- Geen weeknummers als motivatie
- Geen vergelijkingstabellen tenzij technisch absoluut noodzakelijk
- Geen "leer je" taal - de inhoud spreekt voor zich
- Begin direct met de inhoud, niet met aankondigingen wat komt

### 3. Geen onbekende termen als motivatie

**Goed:**
```markdown
Type annotaties zijn nieuw voor je, maar hebben drie grote voordelen:
1. Je ziet direct wat een functie verwacht
2. Je editor helpt je met autocompletion
3. Later (bij databases en webapplicaties) zijn ze vereist
```

**Fout:**
```markdown
Type annotaties zijn belangrijk omdat:
1. Je code wordt duidelijker
2. Je editor kan helpen
3. SQLAlchemy 2.0 vereist ze
```

**Regel:** Motiveer niet met termen die studenten nog niet kennen (SQLAlchemy, ORM, etc.). Gebruik algemene begrippen (databases, webapplicaties).

### 4. Direct en praktisch

**Goed:**
```markdown
Met `class` definieer je een nieuwe klasse.
Methoden kunnen ook berekeningen doen:
```

**Fout:**
```markdown
Laten we eens kijken hoe we een klasse definiëren.
Het interessante van methoden is dat ze ook berekeningen kunnen doen:
```

**Regel:** Kom snel to the point. Geen omslachtige introducties of "laten we..." constructies.

### 5. Natuurlijk Nederlands

**Goed:**
- klassen, objecten, methoden, attributen
- "geeft terug" in plaats van "returnt"
- "Deze methode geeft True terug"

**Fout:**
- classes, objects, methods, attributes
- "returnt" in plaats van "geeft terug"
- "Deze method returnt True"

**Uitzonderingen** (Engels blijft):
- Technische termen zonder goede NL vertaling: constructor, docstring
- Code keywords: `class`, `def`, `return`, `self`
- Framework termen: Flask, SQLAlchemy
- Gangbare jargon: routes, templates, flash (Flask specifiek)

### 6. Geen AI tells

**Vermijd:**
- Emoji (✅ ❌ 🎯 etc.) - alleen in AGENTS.md zelf toegestaan voor voorbeelden
- **"Oude stijl vs nieuwe stijl" vergelijkingstabellen** - studenten kennen de "oude stijl" niet
- **"Voordelen:" opsommingen** bij nieuwe tools/technieken - klinkt als marketing
- Over-enthusiaste taal ("Super!", "Geweldig!", "Perfect!")
- Kunstmatige structuren ("Stap 1, Stap 2, Stap 3...") - alleen als pedagogisch nodig
- **"Waarom [technologie]?" secties** - de inhoud moet voor zich spreken
- **Em dash (—)** als leesteken in lopende tekst: is ongebruikelijk in Nederlands en een veelzeggend AI-kenmerk. Gebruik in plaats daarvan een komma, dubbele punt of herschrijf de zin.
- **Leestijd** ("Leestijd: ~20 minuten" e.d.) bovenaan pagina's: niet toevoegen.

**Gebruik:**
- Natuurlijke, professionele docenttaal
- Heldere uitleg zonder overdrijving
- Praktische voorbeelden
- Direct to the point - geen marketing-achtige taal

## Didactische Principes

### 1. Gecontroleerde conceptintroductie

**Probleem:** Studenten worden overspoeld wanneer te veel nieuwe concepten tegelijk worden geïntroduceerd.

**Regel:** Introduceer maximaal 1-2 nieuwe concepten per sectie. Leg nieuwe syntax altijd uit voordat je het gebruikt.

**Voorbeelden:**

**@dataclass decorator - GOED:**
```markdown
## Dataclasses

Python heeft een handige manier om klassen te maken die vooral data bevatten: **dataclasses**.

Je gebruikt de `@dataclass` decorator (een speciale aanduiding boven de klasse) om aan te geven dat dit een dataclass is:

\```python
from dataclasses import dataclass

@dataclass
class Product:
    naam: str
    prijs: float
\```

De `@dataclass` zorgt ervoor dat Python automatisch een `__init__` methode maakt...
```

**@dataclass decorator - FOUT:**
```markdown
## Dataclasses

\```python
from dataclasses import dataclass

@dataclass  # Geen uitleg wat @ is
class Product:
    naam: str
    prijs: float
\```
```

**Volg deze volgorde:**
1. Leg uit WAAROM (voordeel/doel)
2. Leg uit WAT (nieuwe syntax/concept)
3. Toon HOE (code voorbeeld)
4. Voorkom stapeling (niet: decorators + type hints + dataclasses + field() tegelijk)

### 2. Syntax uitleg bij eerste gebruik

**Verplichte uitleg voor:**
- **Decorators** (`@dataclass`, `@app.route`, `@staticmethod`)
- **Special methods** (`__init__`, `__str__`, `__repr__`)
- **Type syntax** (`list[Product]`, `Optional[str]`, `dict[str, int]`)
- **Imports** waarom je iets importeert

**Voorbeeld - Decorator bij eerste gebruik:**
```markdown
De `@` syntax (decorator) is een manier om een klasse of functie uit te breiden met extra functionaliteit. Je hoeft nu niet precies te begrijpen hoe decorators werken - belangrijk is dat `@dataclass` ervoor zorgt dat Python automatisch code voor je schrijft.
```

**Gebruik admonitions voor syntax uitleg:**
```markdown
!!! info "Wat betekent `@dataclass`?"
    De `@` voor `dataclass` is een **decorator**. Dit is een manier om aan Python te vertellen: "behandel deze klasse speciaal". De decorator zorgt automatisch voor `__init__`, `__repr__` en meer.
```

### 3. Focus: Traditionele webapplicaties

**Deze cursus richt zich op traditionele server-side web apps**, niet op moderne API/SPA architectuur.

**Technologie stack:**
- Flask met Jinja2 templates (server-side rendering)
- HTML forms (POST requests)
- SQLAlchemy ORM
- WTForms voor formulieren

**Gebruik dus:**
- "Gestructureerde data voor templates" ✅
- "Dicts kun je in templates gebruiken" ✅
- `render_template()` voor voorbeelden ✅

**Vermijd:**
- "JSON-ready data" ❌ (tenzij je JSON echt nodig hebt)
- `jsonify()` voorbeelden ❌ (niet relevant voor deze cursus)
- "API endpoints" ❌
- "REST API" terminologie ❌

**Uitzonderingen** waar JSON wel past:
- `asdict()` voor debugging/inspectie
- Data export functionaliteit (optioneel)
- AJAX calls (indien behandeld in latere modules)

**Voorbeeld - GOED:**
```python
def bereken_totaal(self) -> dict:
    """
    Bereken totaal en geef gestructureerde data terug.

    Returns:
        dict met subtotaal, korting en totaal - handig voor templates
    """
    return {
        "subtotaal": self.subtotaal,
        "korting": self.korting,
        "totaal": self.subtotaal - self.korting
    }
```

```markdown
In een Flask route kun je deze dict doorgeven aan je template:

\```python
@app.route('/bestelling/<int:id>')
def toon_bestelling(id):
    bestelling = Bestelling.query.get(id)
    totaal_info = bestelling.bereken_totaal()
    return render_template('bestelling.html',
                         bestelling=bestelling,
                         totaal=totaal_info)
\```
```

**Voorbeeld - FOUT:**
```python
def bereken_totaal(self) -> dict:
    """Bereken totaal. Geeft JSON-ready dict terug."""  # ❌ JSON noemen
    return {...}
```

```markdown
In een Flask API endpoint:  # ❌ Geen APIs in deze cursus

\```python
@app.route('/api/bestelling/<int:id>')  # ❌
def get_bestelling(id):
    return jsonify(bestelling.bereken_totaal())  # ❌
\```
```

## Technische Principes

### 1. Moderne Python vanaf het begin

**Altijd gebruiken:**
- Type annotations voor alle parameters en return types
- Dataclasses waar relevant (data containers)
- F-strings voor formatting
- Type hints uit `typing` waar nodig (`Optional`, `list[]`, etc.)

**Vermijden:**
- Java-achtige getters/setters
- Name mangling (`__private`)
- Underscore prefix (`_protected`) tenzij echt nodig
- Oude string formatting (%, .format())

### 2. Web-ready code patterns

**Altijd:**
```python
def verkoop(self, aantal: int) -> bool:
    if self.voorraad >= aantal:
        self.voorraad -= aantal
        return True
    return False
```

**Nooit:**
```python
def verkoop(self, aantal: int) -> None:
    if self.voorraad >= aantal:
        self.voorraad -= aantal
        print("Verkocht!")  # ❌ Print in business logic
    else:
        print("Onvoldoende voorraad")  # ❌
```

**Regel:** Business logic returnt values, geen print statements. Dit is essentieel voor Flask.

### 3. Separation of concerns

Studenten moeten vanaf het begin leren dat:
- **Models/Classes**: Business logic, data, berekeningen → RETURN values
- **Routes/Controllers**: HTTP handling, user feedback → PRINT/FLASH
- **Templates**: Presentatie

## Curriculumarchitectuur

### Week 2: OOP Focus

**Doel:** Voorbereiden op SQLAlchemy en Flask, niet algemene OOP mastery.

**Wat moet:**
- Klassen en objecten begrijpen
- Type annotations gebruiken
- Inheritance basics (voor `db.Model`)
- Object relaties (voorbereiding FK's)

**Wat NIET:**
- Complexe OOP patterns
- Getters/setters
- Properties (tenzij kort)
- Abstracte base classes
- Multiple inheritance

### Rode draad

**Consistent voorbeeld:** Webshop (Product, Klant, Bestelling)

**Progressie:**
1. **Deel 1:** Basic classes met type annotations
2. **Deel 2:** Dataclasses
3. **Deel 3:** Inheritance basics
4. **Deel 4:** Object relaties

**Elk deel:**
- Preview naar SQLAlchemy/Flask waar relevant
- Praktische oefening
- Code die overdraagbaar is naar web context

## Admonitions Gebruik

MkDocs Material ondersteunt verschillende admonition types. Gebruik ze strategisch:

### `!!! info`
Voor nieuwe concepten die uitleg verdienen:
```markdown
!!! info "Waarom type annotaties?"
    Type annotaties zijn nieuw voor je, maar hebben drie grote voordelen:
    1. ...
```

### `!!! note`
Voor belangrijke details die opvallen:
```markdown
!!! note "`self` - het object zelf"
    `self` verwijst naar het object zelf. Wanneer je...
```

### `!!! warning`
Voor cruciale verschillen of waarschuwingen:
```markdown
!!! warning "Print vs Return in webapplicaties"
    De `verkoop()` methode geeft een boolean terug...
```

### `!!! tip`
Voor handige technieken:
```markdown
!!! tip "Default waarden"
    `btw_percentage: float = 21.0` is een default waarde...
```

**Regel:** Gebruik spaarzaam. Alleen voor echt belangrijke concepten die extra aandacht verdienen.

## Code Voorbeelden

### Structuur

```python
class Product:
    """Korte beschrijving."""

    def __init__(self, naam: str, prijs: float):
        self.naam = naam
        self.prijs = prijs

    def bereken_totaal(self, aantal: int) -> float:
        """Docstring met wat de methode doet."""
        return self.prijs * aantal
```

**Altijd:**
- Class docstring bovenaan
- Type annotations overal
- Methode docstrings waar functionaliteit niet obvious is
- Return types, ook voor `None`
- Betekenisvolle variabele namen

### Voorbeelddata

**Gebruik realistische waardes:**
```python
laptop = Product("Laptop", 799.99, 5)
muis = Product("Draadloze muis", 25.50, 20)
```

**Niet:**
```python
product1 = Product("Product A", 10.0, 5)
product2 = Product("Product B", 20.0, 10)
```

## Pull Request Workflow

> **Regel: commit nooit direct op `main`.** Maak altijd een feature branch vanaf `upstream/main`, werk daar op, en dien een PR in naar `hanze-hbo-ict/webtech1`. Zo kunnen collega-docenten reviewen en bepalen wanneer wijzigingen worden opgenomen.

### Branches aanmaken

```bash
# Haal upstream op
git fetch upstream

# Maak feature branch vanaf upstream/main
git checkout -b feature/oop-modernisering upstream/main

# Wijzigingen aanbrengen, dan committen
git add docs/week2/
git commit -m "Herschrijf OOP deel 1: moderne Python + type annotations"

# Push naar eigen fork
git push -u origin feature/oop-modernisering

# PR aanmaken naar upstream
gh pr create --repo hanze-hbo-ict/webtech1 --base main
```

### Branching

```
main (productie - deployed naar GitHub Pages)
  └── feature/oop-modernisering
        ├── feature/oop-deel1-herschrijven
        ├── feature/oop-deel2-dataclasses
        └── ...
```

### Commits

**Goed:**
```
Herschrijf OOP deel 1: moderne Python + type annotations

- Verwijder Java-achtige getters/setters
- Voeg type annotations toe overal
- Return values i.p.v. print statements
- Schrijfstijl: naar student toe, geen docentenperspectief
```

**Fout:**
```
Update oop-deel1.md
```

### PR's voor review

Alle wijzigingen via PR's:
- Collega-docenten kunnen reviewen
- Beslissen wanneer te mergen (dit jaar / volgend jaar)
- Discussie mogelijk over aanpak

## Technische Setup

### Dependencies

```toml
[project]
dependencies = [
    "mkdocs>=1.6.0",
    "mkdocs-material>=9.5.0",
    "pymdown-extensions>=10.11.0",
    "mknotebooks>=0.8.0",
]
```

### Development

```bash
# Setup
uv sync

# Live preview
uv run mkdocs serve

# Build
uv run mkdocs build
```

### File conventies

- Nieuwe versies: `oop-deel1-nieuw.md` (voor vergelijking)
- Na merge: hernoemen naar `oop-deel1.md`
- Oefeningen: `oefeningen/oop-oefening1.md`
- Bestanden: `bestanden/voorbeeld.py`

## Checklist voor nieuwe content

Voordat je content indient:

**Schrijfstijl:**
- [ ] Geschreven naar student toe (je/jij, geen we/wij)
- [ ] Geen docentenperspectief (weeknummers, cursusstructuur)
- [ ] **GEEN "In dit deel leer je..." introducties**
- [ ] **GEEN "Voordelen voor deze cursus" lijsten**
- [ ] **GEEN vergelijkingstabellen "oud vs nieuw"**
- [ ] **GEEN "Later/Straks leer je..." forward references**
- [ ] **GEEN "Waarom is X een goede keuze?" secties**
- [ ] Nederlandse termen waar mogelijk (klassen, methoden, objecten)
- [ ] Geen emoji of AI tells
- [ ] Admonitions alleen voor belangrijke concepten
- [ ] Realistische voorbeelddata

**Didactiek:**
- [ ] Max 1-2 nieuwe concepten per sectie
- [ ] Nieuwe syntax uitgelegd bij eerste gebruik (decorators, special methods, etc.)
- [ ] Geen te veel nieuwe concepten tegelijk gestapeld
- [ ] Logische volgorde: WAAROM → WAT → HOE

**Code:**
- [ ] Type annotations overal in code voorbeelden
- [ ] Return values in plaats van print in business logic
- [ ] Docstrings in code voorbeelden
- [ ] Code is web-ready (separation of concerns)

**Flask context:**
- [ ] Focus op traditionele web apps (niet API's/JSON)
- [ ] "Template-ready" niet "JSON-ready" (tenzij JSON echt nodig is)
- [ ] `render_template()` voorbeelden, niet `jsonify()` (tenzij API relevant is)
- [ ] Link naar SQLAlchemy/Flask waar relevant (zonder jargon)

## Flask Terminologie

Wanneer je over Flask schrijft:

**Blijft Engels:**
- routes (gangbaar in NL)
- templates (gangbaar)
- flash (Flask functie)
- request, response

**Wordt Nederlands:**
- models → **modellen**
- forms → **formulieren**
- views → **weergaven** (of houd "views" als gangbaar?)

**Nog te bepalen:** Consistente keuzes maken bij verdere materialen.

## Vragen?

Bij twijfel over stijlkeuzes:
1. Lees voorbeelden in deze guide
2. Bekijk bestaande herschreven materialen
3. Vraag in PR comments

**Kerndoel:** Studenten voorbereiden op moderne Flask development met helder, natuurlijk Nederlands lesmateriaal.
