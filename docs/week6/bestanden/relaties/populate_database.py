from models import db, Cursist, Instrument, Docent

db.create_all()

# Maak 2 cursisten aan
joyce = Cursist("Joyce")
bram = Cursist("Bram")

# Voeg de cursisten toe aan de database
db.session.add_all([joyce, bram])
db.session.commit()

# Maak een docent aan voor Joyce
david = Docent("David", joyce.id)

# Laat een query uitvoeren om alle gegevens van de cursisten te laten zien!
print(Cursist.query.all())

# Zoek alle cursisten met de naam Joyce op uit de database
joyce = Cursist.query.filter_by(naam='Joyce').all()[0]

# Geef aan welke instrumenten Joyce wil leren bespelen.
instr1 = Instrument('Drums', joyce.id)
instr2 = Instrument("Piano", joyce.id)

# Voeg toe en leg vast in de database
db.session.add_all([david, instr1, instr2])
db.session.commit()

# Nu nogmaals de gegevens van Joyce ophalen (de eerste en enige)
joyce = Cursist.query.filter_by(naam='Joyce').first()
print(joyce)

# Toon de instrummenten
(joyce.overzicht_instrumenten())
