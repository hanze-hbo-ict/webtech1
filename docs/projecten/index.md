# Casuïsiek voor het project

Vanaf week vijf werken studenten in duo's aan hun eigen project, waarbij de volgende onderdelen van belang zijn:

- Website heeft vormgeving en een koppeling met een database
- Op de site ingevulde data komt door sqlalchemy terecht in een sqlite-database
- Website maakt gebruik van verschillende views
- Geregistreerde bezoekers kunnen op de site inloggen

Wanneer studenten zelf geen project kunnen bedenken, is het prima één van de onderstaande projecten uit te voeren:

1. [Bungalowpark Bos en Duin](bungalowpark.md)
2. [Website Filmfan](filmfan.md)
3. [Programmeerles voor gepensioneerden](programmeerles.md)
4. [Stage lopen](stage.md)

Kies één van deze casus en laat aan je practicumdocent weten welke casus je gaat doen en met wie. In weken 3, 5, 6 en 8 zijn er toetsmomenten ingepland waarop je het werk tot dan toe aan de practicumdocent laat zien en toelicht. De algemene planning hiervoor is als volgt:

weeknummer | onderdelen van de website
---|---
3 | Website heeft vormgeving
5 | Website biedt basale interactie
6 | Website maakt gebruik van verschillende views en op de site ingevulde data komt terecht in een sqlite-database
8 | Geregistreerde bezoekers kunnen op de site inloggen

## Uitgebreide planning

### week 3
Regel de IDE en de ontwikkelomgeving. Inventariseer welke bestanden nodig zijn (py en html) en bedenk het ontwerp en de vormgeving van de site. 

### week 5
Maak de belangrijkste bestanden `__init__py`, `models.py` en `app.py` aan.
Daarnaast kunnen `base.html` en `home.html` nu ook aangemaakt worden in de folder templates (in `base.html` wordt de navigatiebalk opgezet, denk hier goed over na).
Maak ook templates voor de andere pagina's uit je ontwerp

Test de werking en met name de interactie van de site.

### week 6
Maak per model (tabel) de bestanden `forms.py` en `views.py` aan.
Maak ook in de folder templates aan met de specifiek voor dat model beschikbare html-bestanden. Zorg ervoor dat de betreffende data via de website benaderd en eventueel aangepast kan worden.

### week 8
Zorg voor een inlogsysteem en dat specifieke onderwerpen alleen voor ingelogde bezoekers beschikbaar is.

## Requirements
