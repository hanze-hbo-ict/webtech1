# Week 2 - Object Georiënteerd Programmeren (Verbeterd)

Deze map bevat een volledig herziene versie van week 2 met een **consistent webshop-thema** door alle delen en oefeningen heen.

## 📚 Structuur

### Lesstof (7 delen)

1. **oop-deel1.md** - Inleiding OOP
   - Klassen en objecten
   - Constructor (`__init__`)
   - Methoden
   - `Product` klasse met `verkoop()` methode
   - `__str__()` voor nette weergave

2. **oop-deel2.md** - Methoden en inkapseling
   - Private (`__`) en protected (`_`) attributen
   - `Voorraad` klasse met voorraad management
   - Tijdstempel tracking
   - `@staticmethod` decorator

3. **oop-deel3.md** - Meerdere klassen
   - `Product`, `Klant`, `Winkelwagen` klassen
   - Klassen die samenwerken
   - Docstrings voor documentatie
   - Bestellingen plaatsen

4. **oop-deel4.md** - Getters en Setters
   - `Klant` klasse met krediet en korting
   - Getters en setters
   - `@property` decorator
   - Read-only properties
   - Input validatie

5. **oop-deel5.md** - Overerving (Inheritance)
   - `FysiekProduct` (fysieke producten met verzendkosten)
   - `DigitaalProduct` (digitale downloads met licenties)
   - `Boek` als subklasse
   - `super()` voor parent class

6. **oop-deel6.md** - Overriding en Polymorfisme
   - Method overriding in subklassen
   - `DigitaalProduct.verkoop()` met licentiecheck
   - Polymorfisme met betaalmethoden (iDEAL, Creditcard, PayPal)
   - Dezelfde interface, verschillende implementaties

7. **oop-deel7.md** - Compositie
   - `Bestelling` klasse (compositie)
   - `Betaalmethode` klasse
   - "Heeft-een" vs "is-een" relaties
   - Volledige checkout flow

### Oefeningen

- **oop-oefening1.md** - Voorraad geschiedenis bug fixen
- **oop-oefening2.md** - `DigitaalProduct` en `Boek` klassen maken
- **oop-oefening3.md** - Bestelling uitbreiden (bestellingsnummer, verzendmethode, kortingscodes)

### Voorbeeldbestanden

Alle voorbeeldbestanden staan in `bestanden/webshop/`:

- `product.py` - Basis Product en FysiekProduct klassen (starter voor studenten)
- `voorraad.py` - Voorraad management met history
- `webshop.py` - Volledige webshop met Product, Klant, Winkelwagen
- `klant.py` - Klant met properties (krediet, korting)
- `main.py` - Test bestand (starter)
- `betaalmethode.py` - Betaalmethode klasse
- `bestelling.py` - Bestelling klasse (compositie voorbeeld)

## 🎯 Consistentie

**Voor:** Verschillende thema's per deel (kroketten, bankrekeningen, muziek, games, vogels, Tolkien)

**Na:** Één doorlopend webshop-thema met:
- Producten (fysiek en digitaal)
- Klanten
- Winkelwagentjes
- Bestellingen
- Betaalmethoden
- Voorraad management

## 🚀 Voor studenten

Studenten volgen nu één consistent verhaal:
1. Start met simpele `Product` klasse
2. Breidt uit met voorraad management
3. Voegt klanten en winkelwagentjes toe
4. Leert properties en validatie
5. Maakt subklassen (fysieke/digitale producten)
6. Past polymorfisme toe op betaalmethoden
7. Combineert alles in een `Bestelling` (compositie)

## 📝 Implementatie notities

- Alle voorbeelden gebruiken Nederlandse teksten (consistent met de rest van de cursus)
- Code is volledig getest en werkend
- Starter-bestanden bevatten duidelijke TODO-markers
- Oefeningen bouwen incrementeel op elkaar voort
- Realistische webshop-functionaliteit

## 🔄 Migratie van oude week2

Deze map vervangt de oude week2. Bij implementatie:

1. Backup oude week2 indien gewenst
2. Verplaats week2-improved naar week2
3. Update navigatie/links indien nodig

## 📧 Contact

Voor vragen of suggesties over deze herziening, neem contact op met de docent.
