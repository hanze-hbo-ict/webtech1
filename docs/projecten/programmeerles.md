![Programmeerles voor senioren](imgs/programmeerles.jpeg)

Een groot aantal ouderen die van hun pensioen genieten hebben toch vaak nog de behoefte iets geheel nieuws op te pakken. En programmeerles voor senioren is één van de onderwerpen waar veel vraag naar is.

Nu is het natuurlijk niet de bedoeling bij deze opdracht even een cursus uit de grond te stampen; het draait erom de gegevens van een viertal bestanden (klanten, docenten, talen en lessen) op een verantwoorde manier bij te houden.

De bedoeling van deze opdracht is om hier een sterk vereenvoudigde webapplicatie aan te maken op basis van de hier genoemde tabellen. Van iedere klant wordt vastgelegd een id, een e-mailadres, gebruikersnaam en wachtwoord. 

Voor iedere docent worden dezelfde gegevens vastgelegd. De tabel talen kent slecht een tweetal attributen, een id en de naam van de taal.

Als laatste de tabel lessen. De meest omvangrijke met 6 eigenschappen. Dat zijn achtereenvolgens, id, id van de klant, id van de docent, id van de taal, start en locatie.

Er zijn twee soorten geregistreerde bezoekers van deze site. Allereerst mensen die de programmeerlessen volgen. Zij kunnen, na inloggen, zich aanmelden, hun rooster bekijken en zich met korting aanmelden voor een andere cursus. Ten tweede zijn er administratief medewerkers die roosters kunnen maken, cursussen en talen kunnen toevoegen en docentgegevens bewerken. 

Nieuwe bezoekers, dus zij die zich nog niet geregistreerd hebben, kunnen vanzelfsprekend het aanbod bekijken en zich voor een cursus aanmelden.

## Gevraagd

Maak een sterk vereenvoudige webapplicatie waarbij deze gegevens kunnen worden geraadpleegd en bewerkt. Het is een DUO-opdracht. 

## Tips

- Gebruik KISS (hier Keep it Small en Simple), uitbreiden kan altijd nog.
- Kijk goed naar de al beschikbare code, het wiel hoeft niet opnieuw uitgevonden te worden.
- Zorg voor een goede planning en samenwerking!

## Planning

#### WC 6
Regel de IDE en de ontwikkelomgeving. Inventariseer welke bestanden nodig zijn (py en html) en bedenk het ontwerp en de vormgeving van de site. 

#### WC 7
Maak de belangrijkste bestanden `__init__py`, `models.py` en `app.py` aan.
Daarnaast kunnen `base.html` en `home.html` nu ook aangemaakt worden in de folder templates (in `base.html` wordt de navigatiebalk opgezet, denk hier goed over na).
Maak ook templates voor de andere pagina's uit je ontwerp

Test de werking en met name de interactie van de site.

#### WC 8
Maak per model (tabel) de bestanden `forms.py` en `views.py` aan.
Maak ook in de folder templates aan met de specifiek voor dat model beschikbare html-bestanden. Zorg ervoor dat de betreffende data via de website benaderd en eventueel aangepast kan worden.

#### WC 9
Zorg voor een inlogsysteem en dat specifieke onderwerpen alleen voor ingelogde bezoekers beschikbaar is.


