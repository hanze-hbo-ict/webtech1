"""Database populatie script voor relaties voorbeeld.

Dit script vult de database met voorbeelddata om relaties te demonstreren:
- Een-op-een relatie: Cursist heeft één Docent
- Een-op-veel relatie: Cursist heeft meerdere Instrumenten
"""
from models import db, Cursist, Instrument, Docent

# Maak tabellen aan
with db.app.app_context():
    db.create_all()

    # Maak 2 cursisten aan
    joyce = Cursist("Joyce")
    bram = Cursist("Bram")

    # Voeg cursisten toe aan database
    db.session.add_all([joyce, bram])
    db.session.commit()

    print("=== Cursisten aangemaakt ===")
    print(db.session.execute(db.select(Cursist)).scalars().all())
    print()

    # Maak een docent aan voor Joyce (een-op-een relatie)
    david = Docent("David", joyce.id)

    # Zoek Joyce op uit de database
    joyce = db.session.execute(db.select(Cursist).filter_by(naam='Joyce')).scalar_one_or_none()

    # Geef aan welke instrumenten Joyce wil leren bespelen (een-op-veel relatie)
    instr1 = Instrument('Drums', joyce.id)
    instr2 = Instrument("Piano", joyce.id)

    # Voeg toe en leg vast
    db.session.add_all([david, instr1, instr2])
    db.session.commit()

    # Haal Joyce opnieuw op om relaties te tonen
    joyce = db.session.execute(db.select(Cursist).filter_by(naam='Joyce')).scalar_one_or_none()
    print("=== Joyce met relaties ===")
    print(joyce)
    print()

    # Toon instrumenten via relatie
    print("=== Instrumenten van Joyce ===")
    print(joyce.overzicht_instrumenten())
