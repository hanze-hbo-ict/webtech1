# OOP Python – Oefening 1

In deze oefening ga je een `Klant` klasse maken voor de webshop. Je past toe wat je in deel 1 hebt geleerd: klassen, type annotations, methoden en return values.

## Opdracht

Maak een bestand `klant.py` met een `Klant` klasse die het volgende kan:

### a. Basis klasse opzetten

De klasse moet deze attributen hebben:

- `naam` (str): De naam van de klant
- `email` (str): Het emailadres
- `korting_percentage` (float): Het kortingspercentage (default: 0.0)

**Gebruik type annotations bij alle attributen!**

### b. Methoden implementeren

Voeg de volgende methoden toe:

1. **`bereken_korting(bedrag: float) -> float`**
   - Berekent de korting op een bepaald bedrag
   - Geeft het kortingsbedrag terug

2. **`bereken_prijs_na_korting(bedrag: float) -> float`**
   - Berekent de prijs na aftrek van korting
   - Geeft de uiteindelijke prijs terug

3. **`__str__() -> str`**
   - Geeft een nette string representatie van de klant
   - Formaat: `"Klant: Jan Jansen (jan@email.nl) - 10% korting"`

!!! warning "Return values, geen prints"
    Je methoden moeten waarden **teruggeven**, niet printen. De aanroepende code beslist wat er met de waarde gebeurt.

### c. Testen

Test je klasse met deze code:

```python
# Maak klanten aan
jan = Klant("Jan Jansen", "jan@email.nl", 10.0)
marie = Klant("Marie Peters", "marie@email.nl")  # Geen korting

# Bereken prijzen
prijs = 100.0

print(jan)
print(f"Korting op €{prijs:.2f}: €{jan.bereken_korting(prijs):.2f}")
print(f"Prijs na korting: €{jan.bereken_prijs_na_korting(prijs):.2f}")
print()

print(marie)
print(f"Korting op €{prijs:.2f}: €{marie.bereken_korting(prijs):.2f}")
print(f"Prijs na korting: €{marie.bereken_prijs_na_korting(prijs):.2f}")
```

**Verwachte output:**

```text
Klant: Jan Jansen (jan@email.nl) - 10.0% korting
Korting op €100.00: €10.00
Prijs na korting: €90.00

Klant: Marie Peters (marie@email.nl) - 0.0% korting
Korting op €100.00: €0.00
Prijs na korting: €100.00
```

## Extra uitdaging (optioneel)

Voeg een methode `verhoog_korting(extra_percentage: float) -> None` toe die het kortingspercentage verhoogt. Beperk de maximale korting tot 50%.

```python
jan.verhoog_korting(5.0)  # Nu 15% korting
print(jan)
# Output: Klant: Jan Jansen (jan@email.nl) - 15.0% korting

jan.verhoog_korting(40.0)  # Zou 55% worden, maar max is 50%
print(jan)
# Output: Klant: Jan Jansen (jan@email.nl) - 50.0% korting
```

## Checklist

Controleer voordat je klaar bent:

- [ ] Type annotations bij alle parameters en return types
- [ ] Methoden geven waarden terug (return), geen print statements
- [ ] `__str__` methode geïmplementeerd
- [ ] Default waarde voor `korting_percentage`
- [ ] Code werkt met de testcode
- [ ] Docstrings bij alle methoden

## Tips

- Gebruik `self.attribuut` om attributen van het object te benaderen
- Type annotatie voor return value: `-> float`, `-> str`, of `-> None`
- F-strings zijn handig voor de `__str__` methode: `f"Tekst {variabele}"`
- Een percentage van 10% bereken je als: `bedrag * (percentage / 100)`
