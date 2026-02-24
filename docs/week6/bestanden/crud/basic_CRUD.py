"""CRUD operaties demonstratie met SQLAlchemy.

Dit script demonstreert alle CRUD (Create, Read, Update, Delete) operaties:
- CREATE: Nieuwe cursist toevoegen
- READ: Cursisten opvragen (all, get, filter)
- UPDATE: Leeftijd van cursist wijzigen
- DELETE: Cursist verwijderen

Voer eerst setup_database.py uit om de database aan te maken.
"""
from basic_model_app import app, db, Cursist

with app.app_context():
    ###########################
    ###### CREATE ############
    ###########################
    print("=== CREATE: Nieuwe cursist toevoegen ===")
    elsje = Cursist('Elsje', 19)
    db.session.add(elsje)
    db.session.commit()
    print("Elsje toegevoegd\n")

    ###########################
    ###### READ ##############
    ###########################
    print("=== READ: Alle cursisten ===")
    alle_cursisten = db.session.execute(db.select(Cursist)).scalars().all()
    print(*alle_cursisten, sep='\n')
    print()

    # Zoeken op ID
    print("=== READ: Cursist met ID 2 ===")
    cursist_twee = db.session.get(Cursist, 2)
    print(cursist_twee)
    print(f"Leeftijd: {cursist_twee.leeftijd}")
    print()

    # Filteren op naam
    print("=== READ: Filter op naam 'Elsje' ===")
    cursist_elsje = db.session.execute(
        db.select(Cursist).filter_by(naam='Elsje')
    ).scalar_one_or_none()
    print(cursist_elsje)
    print()

    ###########################
    ###### UPDATE ############
    ###########################
    print("=== UPDATE: Leeftijd wijzigen ===")
    cursist_joyce = db.session.get(Cursist, 1)
    print(f"Oude leeftijd Joyce: {cursist_joyce.leeftijd}")
    cursist_joyce.leeftijd = 40
    db.session.add(cursist_joyce)
    db.session.commit()
    print(f"Nieuwe leeftijd Joyce: {cursist_joyce.leeftijd}")
    print()

    ###########################
    ###### DELETE ############
    ###########################
    print("=== DELETE: Cursist verwijderen ===")
    cursist_elsje = db.session.get(Cursist, 3)
    print(f"Te verwijderen: {cursist_elsje}")
    db.session.delete(cursist_elsje)
    db.session.commit()
    print("Elsje verwijderd")
    print()

    # Overzicht na alle aanpassingen
    print("=== FINAL: Overzicht na CRUD operaties ===")
    alle_cursisten = db.session.execute(db.select(Cursist)).scalars().all()
    print(*alle_cursisten, sep='\n')
