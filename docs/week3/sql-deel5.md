# SQL-injectie

Aan het eind van deze tekst maken we [oefening nummer 2](oefeningen/sql-oefening2.md).

In de vorige paragraaf is er kennis opgedaan omtrent met wijzigen van gegevens uit een database door SQL-statements uit te voeren binnen een Python-file. Dat is gedaan door het e-mailadres hardcoded in te voeren gevolgd door een voorwaarde (`WHERE...`). Het zou meer in de lijn der verwachting liggen om gebruikt te maken van variabelen en de waarde van een variabele te gebruiken bij het wijzigen van een record.

Dat zou er zo uit kunnen zien:

```ipython
In [1]: new_email = 'anotherupdate@update.com'
In [2]: phone = 1234567
In [3]: update_sql = "UPDATE contacts SET email = '{}'
...: WHERE phone = {}".format(new_email, phone)
```

Dit werkt allemaal prima, zoals we hiervoor al gezien hebben. Maar wat gebeurt er nu als we een gebruiker in staat stellen zelf zijn telefoonnummer in te toetsen?

```ipython hl_lines="2"
In [4]: phone = input('Voer uw nummer in ')
Voer uw nummer in 123456

In [5]: update_sql = "UPDATE contacts SET email = '{}'
...: WHERE phone = {}".format(new_email, phone)

In [6]: update_sql
Out[6]: "UPDATE contacts SET email = 'anotherupdate@update.com' WHERE phone =  123456"
```

Ook dit zal het gewenste resultaat opleveren.

## Meerdere regels updaten

Python is heel pienter in de omgang met SQL en stelt gebruikers in staat meerdere SQL-statements na elkaar te laten uitvoeren. Daarvoor kan het commando `executescript()` uitgevoerd worden. Een aantal wijzigingen in de code:

```ipython hl_lines="4 10 11"
In [7]: new_email = 'newemail@update.com'
In [8]: phone = input("Please enter your phone number")

Please enter your phone number 12345; drop table contacts;

In [9]: update_sql = "UPDATE contacts SET email = '{}'
...: WHERE phone = {}".format(new_email, phone)

In [10]: update_sql
Out[10]: "UPDATE contacts SET email = 'newemail@update.com'
   WHERE phone =  12345; drop table contacts;"

In [11]: update_cursor = db.cursor()
In [12]: update_cursor.executescript(update_sql)

---------------------------------------------------------------------------
OperationalError                          Traceback (most recent call last)
<ipython-input-12-431cdd50b1d0> in <module>
      1 update_cursor = db.cursor()
----> 2 update_cursor.executescript(update_sql)

OperationalError: no such table: contacts

```

Omdat de methode `executescript()` een gebruiker dus in staat stelt meerdere SQL-statements uit de laten voeren is het mogelijk een dusdanig commando op te geven dat de hele tabel is verdwenen. En dat kan heel vervelende consequenties hebben voor een organisatie, bijvoorbeeld wanneer de gehele orderportefeuille gewist wordt. Gelukkig bestaat de file `contacts.py` nog en kan de tabel zonder al te veel moeite weer in ere hersteld worden.

Wat er nu net gedemonstreerd is, staat bekend als een *SQL-injectie* aanval. Een aanvaller injecteert dan een statement in de ‘gewone’ SQL-code. Vroeger was het zo eenvoudig als hier net getoond is, maar tegenwoordig moet er meer moeite voor gedaan worden.

Zoals gezegd, administrators en programmeurs zijn zich bewust van dit probleem en dus bestaat het fenomeen nog steeds, maar er veel meer specialistische kennis nodig van SQL en database om een succesvolle aanval in te kunnen zetten.

Ook hier is het in scène gezet (`executescript()`) om duidelijk te maken hoe de SQL-injection kan plaatsvinden. De methode `executescript()` wordt weer terug geschaald naar de methode `execute()`. Het volgende voorbeeld maakt dit duidelijk:

```ipython
In [1]: new_email = 'newmail@update.com'
In [2]: phone = input("Voer uw nummer in: ")

Voer uw nummer in: 1234; drop table contacts;

In [3]: update_sql = "UPDATE contacts SET email = '{}' WHERE phone = {}".format(new_email, phone)
In [4]: update_cursor = db.cursor()
In [5]: update_cursor.execute(update_sql)

---------------------------------------------------------------------------
Warning                                   Traceback (most recent call last)
<ipython-input-4-9d2f5feb0b58> in <module>
      1 update_sql = "UPDATE contacts SET email = '{}' WHERE phone = {}".format(new_email, phone)
      2 update_cursor = db.cursor()
----> 3 update_cursor.execute(update_sql)

Warning: You can only execute one statement at a time.
```

De tabel bestaat nog en er verschijnt alleen een waarschuwing dat het niet mogelijk is meerdere SQL-statements na elkaar uit te voeren.

## Placeholders

Het verwijderen van de tabel is weliswaar tegengegaan, maar er is wel een foutmelding ontstaan waardoor de wijziging niet is doorgevoerd. Hoe kan dit beter? Door gebruik te maken van *placeholders*  en *parameter substitution*.

Een voorbeeld om dit duidelijk te maken.

```ipython
In [6]: new_email = "newemail@update.com"
In [7]: phone = input("Voer uw nummer in: ")

Voer uw nummer in: 1234; drop table contact;

In [8]: update_sql = "UPDATE contacts SET email = ? WHERE phone = ?"

In [9]: update_sql
Out[9]: 'UPDATE contacts SET email = ? WHERE phone = ?'

In [10]: update_cursor = db.cursor()
In [11]: update_cursor.execute(update_sql, (new_email, phone))
In [12]: print("{} rows updated".format(update_cursor.rowcount))

0 rows updated
```

In het `UPDATE`-statement zijn de waarde van de kolommen `email` en `phone` vervangen door een vraagteken. Dat zijn de *placeholders*. Bij het uitvoeren van de wijziging worden de variabelen als parameters opgevoerd. De methode `execute()` krijgt nu als tweede parameter een tupel mee waarin de waarden zitten waardoor de vraagtekens vervangen moeten worden. Tijdens deze vervanging worden alle bijzonder tekens, zoals een puntkomma, *geëscaped*: dat wil zeggen dat ze onschadelijk worden gemaakt, zodat ze niet meer als database-commando worden gezien, maar gewoon als tekst.

Feitelijk betekent dit dat het update statement er na het invoeren van de kwalijke waarde (`1234;drop table contacts`) als volgt uit komt te zien:

```text
UPDATE contacts SET email='newmail@update.com'
WHERE phone='1234\;drop table contacts\;';
```

Dat resulteert in een update van nul regels, want er is niemand in de database die zo'n raar telefoonnummer heeft.

Maak nu [oefening nummer 2](oefeningen/sql-oefening2.md).



