"""Database setup script voor basic model app.

Dit script maakt de database tabellen aan en vult deze met initiële data.
Moet uitgevoerd worden voordat basic_CRUD.py gebruikt kan worden.
"""
from basic_model_app import db, Cursist

# Maak de tabel(len) aan in de database
with db.app.app_context():
    db.create_all()

    # Twee nieuwe cursisten
    joyce = Cursist('Joyce', 36)
    bram = Cursist('Bram', 24)

    # De ID's worden automatisch gecreëerd als de cursisten worden aangemaakt
    db.session.add_all([joyce, bram])

    # Vastleggen in de database
    db.session.commit()

    # Check of de ID's zijn toegevoegd
    print(f"Joyce ID: {joyce.id}")
    print(f"Bram ID: {bram.id}")
