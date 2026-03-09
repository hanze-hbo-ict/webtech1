# Webtech1 - Kritieke regels (lees dit bij elke taak)

Volledig document: AGENTS.md

## Schrijfstijl - meest vergeten

- **je/jij**, nooit we/wij. De student doet het.
- Geen "In dit deel leer je..." of "In deze sectie gaan we..."  → direct beginnen met inhoud
- Geen "Voordelen van X:" opsommingen bij nieuwe tools/technieken
- Geen vergelijkingstabellen "oud vs nieuw" — studenten kennen de "oude stijl" niet
- Geen "Later leer je..." of "In Week 6 gebruik je dit" → neutrale verwijzing
- Geen emoji in cursusmateriaal (in AGENTS.md zelf wel voor voorbeelden)
- Geen em-dash (—) in lopende tekst: gebruik komma, dubbele punt, of herschrijf
- Geen leestijd bovenaan pagina's

## Nederlandse termen

- klassen, objecten, methoden, attributen (niet: classes, objects, methods)
- "geeft terug" (niet: "returnt")
- constructor, docstring → blijven Engels
- routes, templates, flash → blijven Engels (gangbaar jargon)

## Python code — stijl

- Type annotations overal (parameters én return types)
- Business logic: return values, nooit print statements
- Docstrings in code voorbeelden

## Python code — correctheid (KRITIEK)

Controleer elk codevoorbeeld vóór je het presenteert. Loop de code mentaal stap voor stap door.

**Variabelenamen:**
- Consistent door het hele voorbeeld: als je `product` introduceert, gebruik dan niet later `p` of `item`
- Consistent met de rest van het bestand/codebase — lees de bestaande code eerst
- Geen namen verzinnen die niet in de context bestaan

**Logica:**
- Klopt de volgorde van operaties?
- Worden alle gedefinieerde variabelen ook gebruikt?
- Kloppen de return types met de type annotation?
- Werkt de code ook voor edge cases die in de uitleg worden genoemd?

**Imports en API-gebruik:**
- Importeer je alles wat je gebruikt?
- Bestaan de methoden/attributen die je aanroept echt (geen hallucinated API)?
- Flask/SQLAlchemy: gebruik alleen patronen die in de cursus zijn geïntroduceerd

**Zelfcheck vóór presenteren:**
- Lees de code opnieuw als lezer, niet als schrijver
- Klopt de code met de uitleg erboven/eronder?
- Zou een student dit kunnen natikken en laten werken?

## Didactiek

- Max 1-2 nieuwe concepten per sectie
- Volgorde: WAAROM → WAT → HOE
- Nieuwe syntax altijd uitleggen vóór gebruik (decorators, special methods, type syntax)

## Workflow

- Nooit direct committen op `main` — altijd feature branch
- Commit messages: beschrijvend met bullet points, niet "Update bestand.md"
