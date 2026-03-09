"""Eenvoudig SQLite3 voorbeeld met contacts database.

Dit script demonstreert basis SQLite3 operaties:
- Database connectie maken
- Tabel aanmaken
- Records toevoegen
- Records ophalen met cursor
"""
import sqlite3

# Maak connectie met database (wordt aangemaakt als niet bestaat)
db = sqlite3.connect("contacts.sqlite")

# Maak tabel aan
db.execute("CREATE TABLE IF NOT EXISTS contacts(name text, phone integer, email text)")

# Voeg twee contacten toe
db.execute("INSERT INTO contacts VALUES ('Bart', 1234567, 'bart@org.nl')")
db.execute("INSERT INTO contacts VALUES ('Henk', 7654321, 'henk@org.nl')")

# Maak cursor om resultaten op te halen
cursor = db.cursor()
cursor.execute("SELECT * FROM contacts")

# Haal records één voor één op met fetchone()
# Let op: cursor is een iterator die vooruit beweegt
print(cursor.fetchone())  # ('Bart', 1234567, 'bart@org.nl')
print(cursor.fetchone())  # ('Henk', 7654321, 'henk@org.nl')
print(cursor.fetchone())  # None (geen records meer)

# Sluit cursor en database
cursor.close()
db.commit()
db.close()
