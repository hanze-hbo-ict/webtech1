import sqlite3

db = sqlite3.connect("contacts.sqlite")
db.execute("CREATE TABLE IF NOT EXISTS contacts(name text, phone integer, email text)")
db.execute("INSERT INTO contacts VALUES ('Bart', 1234567, 'bart@org.nl')")
db.execute("INSERT INTO contacts VALUES ('Henk', 7654321, 'henk@org.nl')")

cursor = db.cursor()
cursor.execute("SELECT * FROM contacts")

# for row in cursor:
#     print(row)
# print(cursor.fetchall())

print(cursor.fetchone())
print(cursor.fetchone())
print(cursor.fetchone())

cursor.close()
db.commit()
db.close()

