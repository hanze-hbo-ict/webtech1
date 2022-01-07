# SQL in Python

Hoogste tijd om SQL te gebruiken in Python. Het mooie van Python is dat bij de installatie automatisch SQLite3 wordt aangemaakt. In een vorige paragraaf is al kennis gemaakt met de tabel `contacts`. Bij wijze van voorbeeld zullen we deze tabel met behulp van Python opnieuw aanmaken en van een aantal records voorzien. Aansluitend zullen we vanuit een Python-programma de gegevens uit de database lezen.

## import sqlite3

Als een Python-file gekoppeld dient te worden aan een SQLite-database, moet als eerste SQLite geïmporteerd worden. De tweede stap is bekend te maken met welke database de Python-file gekoppeld gaat worden. Hieronder worden beide stappen weergegeven:


```ipython
In [1]: import sqlite3
In [2]: db = sqlite3.connect("contacts.sqlite")
```

Met dit commando wordt de database aangemaakt (als je op je filesystem kijkt, zie je dat het bestand [`contacts.sqlite`](bestanden/contacts.sqlite) is aangemaakt). Omdat de database nog geen tabellen heeft, moeten we deze eerst aanmaken. Om sql in Python uit te voeren, maken we gebruik van het commando `execute`.

```ipython
In [3]: db.execute("CREATE TABLE IF NOT EXISTS contacts(name text, phone integer, email text)")
Out[3]: <sqlite3.Cursor at 0x10bf95f10>
```

!!! Info "Checken of de tabel al bestaat"
    De toevoeging `IF NOT EXISTS` zorgt ervoor dat er geen foutmelding verschijnt op het moment dat er al een tabel met dezelfde naam is. Deze regel wordt dan door het programma genegeerd.

Nu voeren we twee records toe:

```ipython
In [4]: db.execute("INSERT INTO contacts VALUES ('Bart', 1234567, 'bart@org.nl')")
In [4]: db.execute("INSERT INTO contacts VALUES ('Henk', 7654321, 'henk@org.nl')")
```

Om er zeker van te zijn dat de gegevens zijn opgeslagen, maken we gebruik van het commando `commit`. Dit herken je, als het goed is, uit de periode 1, waar het ging over *transacties*.

```ipython
In [5]: db.commit()
```

## Cursors

Om in Python met data te kunnen werken, moeten we gebruik maken van een *cursor*.  Een database-cursor is een techniek die het mogelijk maakt om over regels in een result-set te itereren. Je kunt je een cursor voorstellen als een pijltje naar een specifieke regel in zo'n result-set. Met behulp van die pijl kun je de huidige record ophalen, aanpassen of verwijderen.

![Database cursor](imgs/cursor.png)

Om met een cursor te kunnen werken, moet je het volgende stappenplan volgen:

1. Definieer een cursor die gekoppeld is aan de database-connectie (`cursor=db.cursor()`)
2. Open die cursor en hang daar een result-set aan (`cursor.execute(...)`)
3. Haal regel voor regel de data op en gebruik dat in je lokale programmeeromgeving (`cursor.fetchone()`)
4. Sluit de cursor wanneer je hiermee klaar bent (`cursor.close()`)

We zullen dat stappenplan hieronder met voorbeelden verder toelichten.


## Opvragen van data

Na het runnen van deze regels is de database aangemaakt en zijn de records toegevoegd. Een testje is te zien of de gegevens ook daadwerkelijk zijn verwerkt. Daarvoor moeten we dus gebruik maken van een cursor:

```ipython
In [6]: cursor = db.cursor()

In [7]: cursor.execute("SELECT * FROM contacts")
Out[7]: <sqlite3.Cursor at 0x10c06bab0>
```

De opgevraagde rijen zijn nu benaderbaar via de cursor. We kunnen hier gebruik maken van een `for`-lus om deze gegevens één voor één af te drukken.

```ipython
In [8]: for row in cursor:
   ...:     print(row)

('Bart', 1234567, 'bart@org.nl')
('Henk', 7654321, 'henk@org.nl')
```

Het resultaat van de query is een tupel. Het is daarom ook mogelijk om individuele gegevens afzonderlijk naar het scherm te schrijven.

```ipython
In [9]: for name, phone, email in cursor:
   ...:     print(name  )
   ...:     print(phone)
   ...:     print(email)
   ...:     print ('---------')

Bart
1234567
bart@org.nl
---------
Henk
7654321
henk@org.nl
---------
```

Moeten de gegevens als een lijst getoond worden is daar de methode `fetchall()` voor beschikbaar.

```ipython
In [10]: cursor.fetchall()
Out[10]:
[('Bart', 1234567, 'bart@org.nl'),
 ('Henk', 7654321, 'henk@org.nl'),
```

Merk op dat het resultaat van de bovenstaande methode een *list* is: er zitten blokhaken (`[` een `]`) omheen.

!!! Info "Het resetten van de cursor"
    De bovenstaande code werkt niet zonder meer. Om het resultaat opnieuw te krijgen moeten we de cursor *resetten* of de query opnieuw uitvoeren. We gaan hieronder uitgebreid in op die cursor.

Een andere handige methode is `fetchone()`. Deze methode haalt de huidige regel op en verplaatst de cursor naar de volgende regel. Op deze manier kun je door je resultaten heen itereren totdat de methode geen resultaat meer teruggeeft:

```ipython
In [11]: cursor.fetchone()
Out[11]: ('Bart', 1234567, 'bart@org.nl')

In [12]: cursor.fetchone()
Out[12]: ('Henk', 7654321, 'henk@org.nl')

In [13]: cursor.fetchone()
```

