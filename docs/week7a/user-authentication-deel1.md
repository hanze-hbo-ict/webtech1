# User authentication - Hashing

## Inleiding

De titel van dit deel is *User Authentication*. Gelijk weer een omschrijving in het Engels... Vertaald naar normaal Nederlands levert dat het begrip gebruikersauthenticatie op. Hiermee wordt bedoeld dat voordat een gebruiker toegang wordt verleend op een aanvraag er een procedure wordt opgestart om te bepalen of het een rechtmatige aanvraag betreft.

Kortweg, het draait om het inloggen.

Tot nu toe heeft iedereen toegang tot elke pagina van de ontwikkelde webapplicaties. Vaak is het wenselijk de toegang te beperken tot alleen geregistreerde gebruikers. Het gaat in dit deel om de autorisatie en authenticatie van de gebruikers.

De onderwerpen die we gaan behandelen zijn:

- Password hashing
- De `Flask-Login` library

## Password hashing

Als een website gebruikersverificatie kent, zijn wachtwoorden en gebruikersnamen opgeslagen in een database. Om veiligheidsredenen zal nooit de letterlijke inhoud van het wachtwoord worden opgeslagen. Dat zou te gemakkelijk te achterhalen zijn voor hackers, en bovendien is het niet netjes wanneer een database-administrator gewoon beschikking zou hebben over wachtwoorden.

Een hashfunctie brengt hierbij uitkomst. Het is een algoritme dat een wachtwoord kan omtoveren naar een veilig alternatief. En met veilig wordt bedoeld dat een buitenstaander uit de hash niet kan achterhalen wat het originele wachtwoord is.

In de praktijk werkt dat als volgt: als een gebruiker een wachtwoord invoert, kan dit eenvoudig vergeleken worden met de opgeslagen hash. De hash is het enige wat opgeslagen wordt, en het is niet mogelijk (of in ieder geval erg moeilijk) om het wachtwoord te reconstrueren op basis van die hash.

Voor het werken met die hashes kan uit een tweetal beschikbare bibliotheken gekozen worden:

- [`Bcrypt`](https://flask-bcrypt.readthedocs.io/en/latest/)
- [`Werkzeug`](https://techmonger.github.io/4/secure-passwords-werkzeug/)

Beiden kunnen zeer goed gebruikt worden in een Flask-applicatie om te kunnen achterhalen of er een juist wachtwoord is ingevoerd. Van beide pakketten wordt een voorbeeld gegeven hoe het gebruikt kan worden.

`Bcrypt` en `Werkzeug` komen vaak mee als `Flask` geïnstalleerd wordt. Is dat niet het geval kunnen de pakketten [op de bekende wijze](../week5/flask-forms-deel1.md) opgehaald worden.

### Bcrypt

Is Bcrypt aanwezig, is de eerste actie het importeren ervan. Daarna maken we een object aan van het type `BCrypt()` en gebruiken dat object om het wachtwoord te hashen:

```ipython

In [1]: from flask_bcrypt import Bcrypt

In [2]: bcrypt = Bcrypt()

In [3]: hashed_pass = bcrypt.generate_password_hash('supergeheimwachtwoord')
```

Het wachtwoord wordt gehashed en bewaard in de variabele `hashed_pass`. Nadat het geprint is, is het echt niet meer te herleiden naar het origineel:

```ipython
In [4]: print(hashed_pass)
b'$2b$12$rFOT5/VUiUpjODpcCn/0UONrhkQ2h224c7Srz3jk2qJOAUw2.xvyG'
```

Wordt het runnen herhaald, verschijnt er een andere hash.

Uiteraard nu weer een test naar de werking.

```ipython
In [5]: bcrypt.check_password_hash(hashed_pass, 'verkeerdwachtwoord')
Out[5]: False

In [6]: bcrypt.check_password_hash(hashed_pass, 'supergeheimwachtwoord')
Out[6]: True
```

Precies in de lijn der verwachting.

### Werkzeug

Je kunt hetzelfde bereiken met Werkzeug, waarbij de syntax en de check zelfs nog iets simpeler is:

```ipython
In [1]: from werkzeug.security import generate_password_hash,check_password_hash

In [2]: hashed_pass = generate_password_hash('supergeheimwachtwoord')

In [3]: print (hashed_pass)
pbkdf2:sha256:150000$hUiH149n$af71be7ff46588f9c5d93b4ec9f46ef1a64801d02434ee2057ca81b8bb2939cb

In [4]: check_password_hash(hashed_pass,'verkeerdwachtwoord')
Out[4]: False

In [5]: check_password_hash(hashed_pass,'supergeheimwachtwoord')
Out[5]: True
```

Het verschil tussen beiden is dat bij Werkzeug exact de juiste methoden binnengehaald worden en bij Bcrypt moet er soms een beetje over nagedacht worden. De keuze tussen deze pakketten is vrij arbitrair en ligt een beetje aan de voorkeuren van de ontwikkelaar.

## Samenvatting

In deze les heb je geleerd:

- **Authenticatie**: het proces van het controleren of een gebruiker rechtmatig toegang heeft tot een webapplicatie, in de volksmond het inloggen
- **Wachtwoord hashing**: een hashfunctie zet een wachtwoord om naar een onleesbare reeks tekens die niet terug te leiden is naar het origineel
- **Opslag van hashes**: de database bewaart uitsluitend de gehashte versie van een wachtwoord, nooit de plain-text variant
- **Wachtwoord verificatie**: bij het inloggen wordt het ingevoerde wachtwoord vergeleken met de opgeslagen hash via een controlemethode, zonder het origineel te hoeven kennen
- **Bcrypt**: een bibliotheek die `generate_password_hash()` en `check_password_hash()` aanbiedt voor het hashen en controleren van wachtwoorden
- **Werkzeug**: een alternatieve bibliotheek met een iets eenvoudigere importstructuur voor hetzelfde doel
- **Herhaalbaarheid**: elke aanroep van de hashfunctie levert een andere hash op voor hetzelfde wachtwoord, wat de beveiliging verder versterkt
