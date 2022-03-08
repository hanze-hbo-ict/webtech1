# Oefening 1

## opgave 1
Zorg voor een koppeling tussen SQLite en de database `test.db`. Zorg voor een passende melding als het gelukt is.

## opgave 2
Maak een tabel aan met naam `bedrijf`. Deze tabel moet de volgende attributen hebben:

kolomnaam | eigenschappen 
---- | ----
`ID` | INT primaire sleutel	NOT NULL
`Naam` | Text			NOT NULL
`Plaats` | INT			NOT NULL
`Salaris` | Real			NOT NULL

Laat een melding zien als het aanmaken van de tabel gelukt is.

## opgave 3
Voeg de volgende gegevens toe:

ID | Naam | Plaats | Salaris
---|---|---|---
1 | Aad | Amsterdam | 60000
2 | Bea | Berlijn | 70000
3 | Coen | Cairo | 65000
4 | Daphne | Dortmund | 65000

Als de gegevens ingevoerd zijn een melding dat het gelukt is.

## Opgave 4

Schrijf een functie die alle gegevens uit de tabel `bedrijf` afdrukt. Gebruik deze functie om telkens de gegevens uit de tabel af te drukken nadat je de volgende wijzigingen hebt doorgevoerd:

- Wijzig het salaris van het record met ID 1. Het salaris wordt nu 90_000.
- Verwijder het record met het nummer 2.
- Wijzig de naam van record met ID 2 in 'Beatrix Ritzema.


## Opgave 5

Verbreek de connectie.



