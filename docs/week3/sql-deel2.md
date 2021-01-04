# SQLite, basisvaardigheden

Hoewel SQL uitvoerig besproken is in het eerste kwartaal, kan het absoluut geen kwaad de belangrijkste statements nog even voor het voetlicht te halen en dan voor  SQLite3. Bovendien is dit een handige manier om SQLite3 te leren kennen.

Alles begint met het aanmaken van een database, dus ook hier. De database krijgt de passende naam ’test.db’. Om de database aan te maken moet er in de command-line ingetoetst worden: `SQLite 3 test.db`. Hiermee wordt de interactive shell geopend met de database `test`:

```
hostname:user$ sqlite3 test.db
SQLite version 3.24.0 2018-06-04 14:10:15
Enter ".help" for usage hints.
sqlite> 
```

Een bestaande database of tabel kan opgeroepen worden met het commando `.open <filename>`. Uiteraard dient op de plaats van `<filename>` de naam van de database of tabel ingevuld te worden.

Een belangrijk eerste commando om te leren is `.headers on`. Daarmee worden de kolomnamen boven de gegevens ook getoond. Laten we bij wijze van voorbeeld nu eerst een tabel maken.

```
sqlite> .headers on
sqlite> create table contacts(name text, phone integer, mail text);
sqlite> 
```


De tabel `contacts` bestaat uit drie kolommen: `name`, `phone en `mail`. Er gebeurt verder niets. Maar geen nieuws is hier goed nieuws: zolang er geen meldingen getoond worden werkt alles naar behoren. 

!!! Info "Telefoonnummer in tekst"
    Normaal gezien is het beter een telefoonnummer het type tekst mee te geven, omdat zo'n nummer in de regel begint met een nul (0). Om het voorbeeld duidelijker te maken, houden we het hier echter op een integer.

Een tabel zonder rijen heeft geen zin. Op de bekende wijze kunnen records toegevoegd worden (`INSERT …  INTO … `):

```
sqlite> insert into contacts(name, phone, mail) values ('Bart',123456, 'bart@org.nl');
sqlite> 
```

Kijken of het toevoegen gelukt is. Voor het opvragen van gegevens gebruiken we zoals altijd `SELECT`. Vanaf nu worden de gereserveerde woorden met een hoofdletter weergegeven. Het maakt voor SQLite niet uit, maar het staat netter.

```
sqlite> SELECT * FROM contacts;
name|phone|mail
Bart|123456|bart@org.nl
sqlite> 
```

!!! Info "Afsluiten met een puntkomma"
    Zoals je ziet moet je commando's in SQLite afsluiten met een puntkomma (`;`). Als je dit niet doet, geeft SQLite een nieuwe regel met `...>`. Dit biedt je de mogelijkheid om het commando op de volgende regel af te ronden. 

    Deze optie is heel prettig omdat het nu mogelijk is ieder SQL-statement van een goede opbouw te voorzien door de onderdelen netjes aan het begin van een regel op te nemen. Dit komt de leesbaarheid ten goede.

Nog een tweede record toevoegen:

```
sqlite> INSERT INTO Contacts VALUES ('Henk', 76543232, 'henk@org.nl');
sqlite> 
```

Deze schrijfwijze wijkt af van het vorige INSERT-commando. Het gaat wel goed maar alleen als de juiste waarden *in de juiste volgorde* aan de tabel worden aangeboden. Als je voor niet alle kolommen een waarde hebt, *moet* je de kolommen in het `INSERT`-statement opnemen. De volgorde van de waarden moet verder overeenkomen met de kolommen. Zie het onderstaande voorbeeld:

```
sqlite> INSERT INTO Contacts VALUES ('Kobus', 543219);
Error: table contacts has 3 columns but 2 values were supplied
sqlite> INSERT INTO Contacts (phone, name) VALUES (543219, 'Kobus');
sqlite> select * from contacts;
name|phone|mail
Bart|123456|bart@org.nl
Henk|76543232|henk@org.nl
Kobus|543219|
sqlite> 
```

Nog een poging een record in te voegen:

```
sqlite> insert into contacts values ('Ilse','06-205 389', 'ilse@org.nl');
sqlite> 
```

Verbazingwekkend, geen foutmelding. En dat terwijl we toch de tweede kolom (`phone`) gedefinieerd hebben als `integer`. De rij is netjes onder aan de tabel ingevoegd. Dit werkt bij geen enkel andere SQL-variant. Daarom is het heel belangrijk een juist datatype te kiezen bij het ontwerpen van de database.

SQLite mist een handig commando dat de andere varianten wel kennen, namelijk `ALTER TABLE`. Met dit commando kan de structuur van een tabel aangepast worden. Bij SQLite dient er een nieuwe tabel aangemaakt te worden ter vervanging van de oude. Daarom nogmaals, denk heel goed na over het ontwerp van de database.

Invoegen is al aan de beurt geweest, wijzigen (`UPDATE`) wordt nu besproken. Belangrijk is altijd om van tevoren een backup te maken voor het geval dat de database is het honderd loopt. Daar heeft SQLite een specifiek commando voor, `.backup`. De backup krijgt de naam `testbackup`.

```
sqlite> .backup testbackup
sqlite> 
```

Omdat het een SQLite-commando is en geen SQL-statement hoeft er geen `;` achter genoteerd worden, alleen een punt (`.`) om het commando mee te beginnen.

De email van Kobus ontbreekt nog en die wordt nu toegevoegd.

```
sqlite> UPDATE contacts SET mail='kobus@org.nl' WHERE name='Kobus';
sqlite> SELECT * FROM contacts;
name|phone|mail
Bart|123456|bart@org.nl
Henk|76543232|henk@org.nl
Kobus|543219|kobus@org.nl
Ilse|06-205 389|ilse@org.nl
sqlite> 
```

Denk erom een `WHERE`-clausule toe te voegen om te voorkomen dat iedereen hetzelfde e-mailadres krijgt. 

De enige nog niet besproken optie is het verwijderen van gegevens (`DELETE`). De gegevens van Kobus worden uit de tabel contacts verwijderd. Let er ook hier op een `WHERE`-clausule te gebruiken omdat anders alle records gewist worden.

```
sqlite> DELETE FROM contacts WHERE name='kobus';
sqlite> SELECT * FROM contacts;
name|phone|mail
Bart|123456|bart@org.nl
Henk|76543232|henk@org.nl
Kobus|543219|kobus@org.nl
Ilse|06-205 389|ilse@org.nl
sqlite> 
```

Het kan af en toe voorkomen dat er gestopt moet worden en dat SQLite moet worden afgesloten. Daar is het commando `.quit` (kleine letters) voor beschikbaar. SQLite kan weer opgestart worden door in de command-line `SQLite3` in te geven. En met `.open <filename>` kan de database weer geactiveerd worden.

```
sqlite> .quit
hostname:user$  
hostname:user$  sqlite3
SQLite version 3.24.0 2018-06-04 14:10:15
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open test.db;
sqlite> 
```

## Nog een paar handige commando's

SQLite kent een flink aantal zogenoemde *punt-commando's* (*dot-commands). Hieronder staat een aantal van deze commando's; [hier kun je ze allemaal terugvinden](https://sqlite.org/cli.html#special_commands_to_sqlite3_dot_commands_):

Commando | Omschrijving 
-----|-----
`.tables` | geeft een overzicht van alle tabellen die in de database zijn opgenomen
`.schema` |  laat de structuur zien van alle tabellen uit de database
`.dump`  |  geeft een overzicht van alle records uit een tabel (dit kun je gebruiken om andere tabel mee te vullen)

```
sqlite> .open test.db
sqlite> .tables
contacts
sqlite> .schema
CREATE TABLE contacts(name text, phone integer, mail text);
sqlite> .dump
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE contacts(name text, phone integer, mail text);
INSERT INTO contacts VALUES('Bart',123456,'bart@org.nl');
INSERT INTO contacts VALUES('Henk',76543232,'henk@org.nl');
INSERT INTO contacts VALUES('Kobus',543219,'kobus@org.nl');
INSERT INTO contacts VALUES('Ilse','06-205 389','ilse@org.nl');
COMMIT;
sqlite> 
```




