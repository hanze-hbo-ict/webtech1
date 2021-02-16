# User authentication - Hashing

## Inleiding

De titel van dit deel is *User Authentication*. Gelijk weer een omschrijving in het Engels. Vertaald naar normaal Nederlands levert dat het begrip gebruikersverificatie op. Hiermee wordt bedoeld dat voordat een gebruiker toegang wordt verleend op een aanvraag er een procedure wordt opgestart om te bepalen of het een rechtmatige aanvraag betreft.

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

Is Bcrypt aanwezig, is de eerste actie het importeren ervan:

```python
from flask_bcrypt import Bcrypt
```

De tweede actie is om een object van de klasse aan te maken:

```python
bcrypt = Bcrypt()
```

Het opslaan van het wachtwoord in een hash-vorm gebeurt als volgt (als wachtwoord wordt `supergeheimwachtwoord` gebruikt):

```python
hashed_pass = bcrypt.generate_password_hash('supergeheimwachtwoord')
print(hashed_pass)
```

Het wachtwoord wordt gehashed en bewaard in de variabele `hashed_pass`. Nadat het geprint is, is het echt niet meer te herleiden naar het origineel:

![de waarde van de variabele hashed_pass](imgs/hashed-pass.png)

Wordt het runnen herhaald, verschijnt er een andere hash.

Uiteraard nu weer een test naar de werking.

```python
fout_check = bcrypt.check_password_hash(hashed_pass, 'verkeerdwachtwoord')
print(fout_check)
goed_check = bcrypt.check_password_hash(hashed_pass, 'supergeheimwachtwoord')
print(goed_check)
```

Het effect:

![de uitkomst van de hash test](imgs/hash-test-bcrypt.png)

Precies in de lijn der verwachting.

### Werkzeug

Dit kan een stuk sneller gedaan worden. Het is weer meer van hetzelfde.

```python
from werkzeug.security import generate_password_hash,check_password_hash

hashed_pass = generate_password_hash('supergeheimwachtwoord')
print(hashed_pass)
fout_check = check_password_hash(hashed_pass,'verkeerdwachtwoord')
print(fout_check)
goed_check = check_password_hash(hashed_pass,'supergeheimwachtwoord')
print(goed_check)
```


En het effect:


![de output van bovenstaande code](imgs/werkzeug-hash-test.png)

Het verschil tussen beiden is dat bij Werkzeug exact de juiste methoden binnengehaald worden en bij Bcrypt moet er soms een beetje over nagedacht worden. De keuze tussen deze pakketten is vrij aan de ontwikkelaar.




