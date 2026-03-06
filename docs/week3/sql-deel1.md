# SQLite in Python

In het vak Databases heb je geleerd werken met PostgreSQL. In deze module gebruik je **SQLite** - een lichtgewicht database die als een enkel bestand werkt en built-in bij Python zit. Geen server setup nodig.

## SQLite CLI (kort)

Je kunt SQLite via de command-line gebruiken (vergelijkbaar met `psql` voor PostgreSQL). Of het al beschikbaar is hangt af van je besturingssysteem:

=== "macOS en Linux"
    SQLite3 is standaard aanwezig, er is niets te installeren. Controleer met `sqlite3 --version` in de terminal.

=== "Windows"
    SQLite3 staat niet standaard op Windows. De makkelijkste manier is via **winget** (de packagemanager die standaard op Windows 10 en 11 zit). Open PowerShell en voer uit: `winget install SQLite.SQLite`. Herstart daarna je terminal.

    Werkt winget niet? Installeer dan handmatig:

    1. Download `sqlite-tools-win-x64-*.zip` van [sqlite.org/download.html](https://www.sqlite.org/download.html) (onder "Precompiled Binaries for Windows")
    2. Pak het zip-bestand uit naar een vaste map, bijv. `C:\sqlite`
    3. Voeg die map toe aan je PATH:
        - Zoek via de Windows-zoekbalk naar "omgevingsvariabelen"
        - Klik op "Omgevingsvariabelen bewerken voor uw account"
        - Selecteer `Path` onder "Gebruikersvariabelen" en klik "Bewerken"
        - Klik "Nieuw", typ `C:\sqlite` en bevestig alles met OK
    4. Herstart PowerShell en controleer met `sqlite3 --version`

Eenmaal geïnstalleerd open je een database zo:

```console
$ sqlite3 test.db
SQLite version 3.39.5
Enter ".help" for usage hints.
sqlite> .tables
sqlite> .quit
```

Handige punt-commando's (vergelijkbaar met `\d` commando's in psql):

| Commando | Betekenis |
|----------|-----------|
| `.tables` | Toon alle tabellen |
| `.schema` | Toon tabelstructuur |
| `.quit` | Afsluiten |

!!! tip "Visueel werken met DB Browser for SQLite"
    Als je liever visueel werkt (vergelijkbaar met pgAdmin voor PostgreSQL), gebruik dan [DB Browser for SQLite](https://sqlitebrowser.org/).

    **Voordelen:**

    - Tabellen visueel bekijken en bewerken
    - SQL queries uitvoeren met syntax highlighting
    - Database structuur inspecteren
    - Handig tijdens Flask development om snel data te controleren

**Volgende stap:** [Python exceptions](python-exceptions.md) - nodig voor deel 2.

## Samenvatting

In deze les heb je geleerd:

- **SQLite**: een lichtgewicht database die als één bestand werkt, zonder serverinstallatie, en standaard meegeleverd wordt met Python
- **SQLite CLI op macOS/Linux**: de `sqlite3`-tool is standaard beschikbaar en direct te starten met `sqlite3 bestandsnaam.db`
- **SQLite installeren op Windows**: via `winget install SQLite.SQLite` of handmatig downloaden en de map toevoegen aan de PATH-omgevingsvariabele
- **Database openen via de CLI**: `sqlite3 <bestandsnaam>` opent een bestaande database of maakt een nieuw bestand aan
- **Punt-commando's**: `.tables` toont alle tabellen, `.schema` toont de tabelstructuur, `.quit` sluit de CLI af
- **DB Browser for SQLite**: een grafische tool om visueel met SQLite te werken, vergelijkbaar met pgAdmin voor PostgreSQL
