# De muziek databases

Het werken met een database die bestaat uit een enkele tabel met 3 of 4 records is niet heel erg zinvol. Het gaat dan sneller om een gegeven op te zoeken dan door er een query aan te wijden. Daarom maken we vanaf nu gebruik van een andere database [`music.sqlite`](../bestanden/music.sqlite). Deze database bevat een aantal bekende tabellen die ook bij het werken met OOP aan bod zijn gekomen: artists, albums en songs. Alleen bevat deze database nog veel meer data.

Aan het eind van dit document maken we [oefening 1](oefeningen/sql-oefening1.md).

## kennismaken een aardigheidje

De database is te vinden [via deze link](../bestanden/music.sqlite). Neem de database over en bewaar deze op je laptop. Het simpelst is om deze database een plekje te geven in de directory waarin ook SQLite3 te vinden is. De database kan dan automatisch geopend worden zonder dat de directory gewijzigd hoeft te worden.

```console
hostname:user$ sqlite3 music.sqlite
SQLite version 3.24.0 2018-06-04 14:10:15
Enter ".help" for usage hints.
sqlite> .tables
albums   artists  songs
sqlite>
```

Er is nog een bijzonderheid met SQLite. Om dat te laten zien, eerst een gedeeltelijk overzicht van de tabel `artists`:

```console
sqlite> .headers on
sqlite> SELECT  * FROM artists LIMIT 195,15;
_id|name
196|Deep Purple
197|T.Rex
198|Tom Petty & The Heartbreakers
199|Thomas Tallis
200|Stevie Ray Vaughan
201|Chemical Brothers
sqlite>
```

Zoals je ziet is de maximale waarde van de kolom `_id` 201. Dit is tevens de primaire sleutel van deze tabel. Wat gebeurt er nu wanneer we een nieuwe record toevoegen?

```console
sqlite> INSERT into artists(name) VALUES ('Travis');
sqlite> SELECT  * FROM artists LIMIT 200,5;
_id|name
201|Chemical Brothers
202|Travis
sqlite>
```

SQLite vult automatisch een waarde voor de primaire sleutel in. Er hoeft niets bijzonders voor gedaan worden zoals in andere database-engines.

## Er weer even inkomen
Vraag: wat is de titel van het album met nummer 167?

```console
sqlite> SELECT name FROM albums WHERE _id=167;
name
Blurring The Edges
sqlite>
```

De records worden standaard gerangschikt op index; hier is dat op de kolom `_id`. Dat kan wel aangepast worden. Dit is het commando om de rijen uit de tabel `artists` te sorteren op naam in omgekeerde volgorde:

```console 
sqlite> SELECT * FROM artists
   ...> ORDER BY name desc;
_id|name
23|ZZ Top
179|Yngwie Malmsteen
148|Yardbirds
... (202 regels in totaal)
```

Dit is allemaal nog niet zo spectaculair en een beetje onoverzichtelijk. Om de albums te tonen met de naam van de artist zijn meerdere query’s nodig om het resultaat te kunnen achterhalen. Dat kan handiger. Uit de lessen ‘Databases 1’ uit periode 1 is hopelijk blijven hangen dat er dan met één of meerdere *joins* gewerkt moet worden.

Als eerste voorbeeld het SQL-statement dat de tracks en titels van de songs laat zien met daarachter de naam van het album waarop de song voorkomt.

```console
sqlite> select s.track, s.title, a.name
...> from songs s
...> join albums a on s.album = a._id;
track|title|name
2|I Can't Quit You Baby|BBC Sessions
1|Taking the Easy Way Out Again|Rhinos Winos and Lunatics
6|Let's Have A Party|Private Practice
7|Flaming Telepaths|Champions Of Rock
11|Yearnin'|The Big Come Up
...
... (5350 regels in totaal)
```

Volgende vraag: een overzicht van de artiesten met hun albums alfabetisch gerangschikt op de naam van de artiest.

```console hl_lines="3"
sqlite> SELECT ar.name, al.name
...> FROM artists ar JOIN albums al ON ar._id = al.artist
...> ORDER BY ar.name;
name|name
1000 Maniacs|Our Time in Eden
10cc|The Best Of The Early Years
AC DC|For Those About To Rock (We Salute You)
AC DC|If You Want Blood You've Got It
Aerosmith|Night In The Ruts
... (439 regels)
```

Nog wat ingewikkelder vraag: een overzicht met de naam van de artiest, de naam van de albums, en van de songs de track en de titel. Let op dat er hier tweemaal een join gebruikt dient te worden.

```console
sqlite> SELECT ar.name, al.name, s.track, s.title
...> FROM songs s JOIN albums al ON s.album=s._id
...> JOIN artists ar ON al.artist=ar._id
...> ORDER BY ar.name, al.name, s.title;
name|name|track|title
1000 Maniacs|Our Time in Eden|1|Backwater
1000 Maniacs|Our Time in Eden|4|Echoes In The Dark
1000 Maniacs|Our Time in Eden|1|The Diamond Overture
1000 Maniacs|Our Time in Eden|10|Walking in the Wild
10cc|The Best Of The Early Years|1|Backwater
... (1756 regels)
```

!!! Info "Een betere teksteditor"
    Het is best een uitgebreid SQL-statement dat is ingevoerd bij SQLite. De kans op fouten is daarbij erg groot, met als gevolg dat het commando opnieuw ingetoetst moet worden. De code kan ook in een teksteditor (bijvoorbeeld Notepad++ of VS Code) getypt worden en later gekopieerd worden naar SQLite om uitgevoerd te worden. Scheelt vaak een hoop tijd en ergernis.


Gevraagd: een overzicht met de naam van de artiest, de naam van de albums, en van de songs de track en de titel, alleen nu met de voorwaarde erbij dat het woord 'doctor' in de titel van de song moet voorkomen.


```console
sqlite> SELECT ar.name, al.name, s.track, s.title
...> FROM songs s JOIN albums al ON s.album=al._id
...> JOIN artists ar ON al.artist=ar._id
...> WHERE s.title LIKE '%doctor%'
...> ORDER BY ar.name, al.name, s.title;
name|name|track|title
Black Sabbath|Technical Ecstasy|6|Rock 'N' Roll Doctor
Dr Feelgood|Malpractice|11|You Shouldn't Call The Doctor (If You Can't Afford The Bills)
Dr Feelgood|Private Practice|1|Down At The Doctors
Fleetwood Mac|The Best of|11|Doctor Brown
Hawkwind|25 Years On|5|Flying Doctor
... (13 regels)
```

## Views

Het laatste onderwerp voordat SQLite gekoppeld gaat worden met Python zijn de views. Een view is niets meer dan een virtuele tabel, waarin gegevens afgeschermd kunnen worden voor buitenstaanders. Stel er is een tabel `medewerkers`. Niet iedereen hoeft alle gegevens van iedere werknemer te kunnen bekijken. Een kolom als `salaris` zou niet zonder meer beschikbaar moeten zijn. Daarom kan er een view aangemaakt worden die gevoelige informatie verbergt voor onbevoegden.

Om de werking van een view te demonstreren wordt nu van het laatst besproken SQL-statement een view aangemaakt, zonder de `WHERE`-clausule, met de naam `vArtistList`. De kleine letter `v` aan het begin van de naam van de view is een prefix om aan te geven dat het hier een view betreft.

```console
sqlite> create view vArtistsList AS
...> SELECT ar.name, al.name, s.track, s.title
...> FROM songs s JOIN albums al ON s.album=al._id
...> JOIN artists ar ON al.artist=ar._id
...> WHERE s.title LIKE '%doctor%'
...> ORDER BY ar.name, al.name, s.title;
sqlite>
sqlite> .schema
CREATE TABLE songs (_id INTEGER PRIMARY KEY, track INTEGER, title TEXT NOT NULL, album INTEGER);
CREATE TABLE albums (_id INTEGER PRIMARY KEY, name TEXT NOT NULL, artist INTEGER);
CREATE TABLE artists (_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE VIEW vArtistsList as Select ar.name, al.name, s.track, s.title from songs s join albums al on s.album=al._id join artists ar on al.artist=ar._id where s.title like '%doctor%' order by ar.name, al.name, s.title
/* vAristsList(name,"name:1",track,title) */;
sqlite>
```

Het is nu een klein kunstje om de gegevens van de view te tonen. Dat gaat weer lukken met een `SELECT`-statement:

```console
sqlite> SELECT *
...> FROM vArtistsList;
name|name:1|track|title
Black Sabbath|Technical Ecstasy|6|Rock 'N' Roll Doctor
Dr Feelgood|Malpractice|11|You Shouldn't Call The Doctor (If You Can't Afford The Bills)
Dr Feelgood|Private Practice|1|Down At The Doctors
Fleetwood Mac|The Best of|11|Doctor Brown
... (diezelfde 13 regels)
```

Nu worden alle gegevens getoond met `SELECT * from vArtistList`. Het is nog mooier als er op kolomnaam gezocht kan worden of dat de kolommen een duidelijke koptekst hebben. Daarvoor is een kleine aanpassing nodig. De view wordt eerst verwijderd en daarna opnieuw lichtelijk gewijzigd, aangemaakt.

```console
sqlite> drop view vAristsList;
sqlite> create view vArtistsList AS
...> SELECT ar.name as artist, al.name as album, s.track as track, s.title as title
...> FROM songs s JOIN albums al ON s.album=al._id
...> JOIN artists ar ON al.artist=ar._id
...> WHERE s.title LIKE '%doctor%'
...> ORDER BY ar.name, al.name, s.title;
```

En deze aanpassing heeft tot gevolg dat het opvragen van gegevens uit de view ook anders gaat. De aangepaste kolomnamen moeten nu gebruikt worden om resultaat te kunnen zien.

```console
sqlite> SELECT * FROM vArtistsList
...> WHERE artist LIKE '%feelgood%';
artist|album|track|title
Dr Feelgood|Malpractice|11|You Shouldn't Call The Doctor (If You Can't Afford The Bills)
Dr Feelgood|Private Practice|1|Down At The Doctors
sqlite>
```

Het kan gebeuren dat er een aantal zaken misgaan bij het uitvoeren van SQL-statements, zoals het verwijderen van een grote hoeveelheid records uit de tabellen. SQLite heeft daar een prima oplossing voor ingebouwd, het commando `.restore`. Hiermee wordt de inhoud van de database teruggezet naar de laatste versie die in het bestand is opgeslagen.

Maak nu [oefening 1](oefeningen/sql-oefening1.md).


