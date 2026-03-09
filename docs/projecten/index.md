# Casuïstiek voor het project

Liefst zo snel mogelijk, in ieder geval vanaf week vijf, werken studenten in duo's aan hun eigen project, waarbij de volgende onderdelen van belang zijn:

- Website heeft vormgeving en een koppeling met een database
- Op de site ingevulde data komt via SQLAlchemy terecht in een SQLite-database
- Website maakt gebruik van verschillende views
- Geregistreerde bezoekers kunnen op de site inloggen

Wanneer studenten zelf geen project kunnen bedenken, is het prima één van de onderstaande projecten uit te voeren:

1. [Bungalowpark Bos en Duin](bungalowpark.md)
2. [Website Filmfan](filmfan.md)
3. [Programmeerles voor gepensioneerden](programmeerles.md)
4. [Stage lopen](stage.md)

Kies één van deze casussen en laat aan je practicumdocent weten welke casus je gaat doen en met wie. Het advies is om je practicumdocent geregeld om feedback te vragen. Het kan zijn dat je practicumdocent een klassikaal moment inplant waarop elk duo hun idee en eventueel begin van de uitwerking aan de gehele groep kort presenteert.

## Uitgebreide planning

### week 1-3

Regel je IDE (ontwikkelomgeving). Inventariseer welke bestanden nodig zijn (py en html) en bedenk het ontwerp en de vormgeving van de site.

### week 4

Maak de belangrijkste bestanden `__init__py`, `models.py` en `app.py` aan.
Daarnaast kunnen `base.html` en `home.html` nu ook aangemaakt worden in de folder templates (in `base.html` wordt de navigatiebalk opgezet, denk hier goed over na).
Maak ook templates voor de andere pagina's uit je ontwerp

Test de werking en met name de interactie van de site.

### week 5-6

Maak per model (tabel) de bestanden `forms.py` en `views.py` aan.
Maak ook in de folder templates aan met de specifiek voor dat model beschikbare html-bestanden. Zorg ervoor dat de betreffende data via de website benaderd en eventueel aangepast kan worden.

### week 7-8

Zorg voor een inlogsysteem en dat specifieke onderwerpen alleen voor ingelogde bezoekers beschikbaar is.
