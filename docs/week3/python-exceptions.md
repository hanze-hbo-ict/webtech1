# Python exceptions

Je kent ze al: rode foutmeldingen in je terminal.

```text
ValueError: invalid literal for int() with base 10: 'abc'
TypeError: unsupported operand type(s) for +: 'int' and 'str'
IndexError: list index out of range
```

Elke foutmelding is een **exception** - een object dat Python aanmaakt als er iets misgaat tijdens het uitvoeren van je code. Tot nu toe stopte je programma altijd zodra zo'n exception optrad. Met `try/except` bepaal je zelf wat er dan gebeurt.

## try/except

```python
# Zonder try/except: programma crasht
getal = int("geen getal")  # ValueError, programma stopt

# Met try/except: jij bepaalt wat er gebeurt
try:
    getal = int("geen getal")
    print(f"Getal: {getal}")
except ValueError:
    print("Dat is geen geldig getal")
```

De code in het `try`-blok wordt uitgevoerd. Als er een exception optreedt:

1. Python stopt direct met de rest van het `try`-blok
2. Python springt naar het bijpassende `except`-blok
3. Het programma gaat daarna verder - het crasht niet meer

## Exceptions die je al kent

Alle foutmeldingen die je eerder hebt gezien zijn exceptions:

| Exception | Wanneer |
|-----------|---------|
| `TypeError` | Verkeerd type, bijv. `"a" + 1` |
| `ValueError` | Ongeldige waarde, bijv. `int("abc")` |
| `NameError` | Variabele bestaat niet |
| `IndexError` | Lijstindex buiten bereik |
| `KeyError` | Dictionary-sleutel bestaat niet |
| `AttributeError` | Methode of attribuut bestaat niet op het object |
| `ZeroDivisionError` | Delen door nul |

## Meerdere except-blokken

Je kunt verschillende soorten exceptions apart afhandelen:

```python
def lees_getal(tekst: str) -> int | None:
    """Zet tekst om naar int. Geeft None terug bij fout."""
    try:
        return int(tekst)
    except ValueError:
        print(f"'{tekst}' is geen geldig geheel getal")
        return None
    except TypeError:
        print("Verwachtte een string als invoer")
        return None
```

## De foutmelding opvragen

Met `as` sla je de exception zelf op als variabele:

```python
try:
    getal = int("abc")
except ValueError as fout:
    print(f"Fout: {fout}")
# Uitvoer: Fout: invalid literal for int() with base 10: 'abc'
```

## Exceptions zijn klassen

Exceptions zijn gewone Python-klassen - ze erven van `Exception`. Dat is ook waarom je het type aangeeft in `except`: je controleert welke klasse de exception heeft.

```python
# ValueError is een klasse, net als Product of Klant
except ValueError:    # opvangen van ValueError-objecten
except TypeError:     # opvangen van TypeError-objecten
```

Je ziet dit patroon ook bij databases: `sqlite3.IntegrityError` is een exception-klasse specifiek voor database-fouten - die zie je in deel 2.

**Volgende stap:** [Deel 2](sql-deel2.md) - SQLite vanuit Python.
