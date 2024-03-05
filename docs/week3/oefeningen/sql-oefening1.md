# Oefening 1

## Opgave 1

Maak gebruik van sqlite om de database `test.sqlite` te maken. 

## Opgave 2

Maak een tabel aan met naam `bedrijf`. Deze tabel moet de volgende attributen hebben:

kolomnaam | eigenschappen 
---- | ----
`ID` | Integer primary key NOT NULL
`Naam` | Text NOT NULL
`Plaats` | Text NOT NULL
`Salaris` | Real NOT NULL


## Opgave 3

Voeg de volgende gegevens toe:

ID | Naam | Plaats | Salaris
---|---|---|---
1 | Aad | Amsterdam | 60000
2 | Bea | Berlijn | 70000
3 | Coen | Cairo | 65000
4 | Daphne | Dortmund | 65000


## Opgave 4

Schrijf een query die alle gegevens uit de tabel `bedrijf` afdrukt. Gebruik deze query om telkens de gegevens uit de tabel af te drukken nadat je de volgende wijzigingen hebt doorgevoerd:

- Wijzig het salaris van het record met ID 1. Het salaris wordt nu 90000.
- Wijzig de naam van record met ID 2 in Beatrix.
- Verwijder het record met het nummer 2.


## Opgave 5

Sluit sqlite weer af. Merk op dat er nu een bestand `demo.sqlite` op je filesystem is aangemaakt.


