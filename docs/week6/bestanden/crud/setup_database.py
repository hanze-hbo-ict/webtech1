# Dit is een heel eenvoudig script om te laten zien hoe een database in te stellen

# Importeer database info
from basic_model_app import db, Cursist

# Maak de tabel(len) aan in de database
db.create_all()

# Twee nieuwe cursisten
joyce = Cursist('Joyce',36)
bram = Cursist('Bram',24)

# De ID's worden automatisch gecreëerd als de cursisten worden aangemaakt in de database
db.session.add_all([joyce, bram])

# Vastleggen in de database
db.session.commit()

# Checken of de ID's zijn toegevoegd.
print(joyce.id)
print(bram.id)
