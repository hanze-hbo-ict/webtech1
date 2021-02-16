![Filmfan toont ook posters van films](imgs/filmfan.jpeg)

Op deze website worden alle gegevens vastgelegd omtrent de films uit Nederland. Van alle films is een trailer te zien, zijn er diverse overzichten beschikbaar van bezoeker, omzetgegevens en nog veel meer.

De bedoeling van deze opdracht is om hier een sterk vereenvoudigde webapplicatie aan te maken. De database zal beperkt worden tot een viertal tabellen die maar een paar attributen gaan bevatten.

Van iedere acteur hoeven maar een drietal kenmerken worden vastgelegd, een id, een voornaam en een achternaam. Dezelfde drie eigenschappen worden door iedere regisseur genoteerd, id, voor- en achternaam. Om het niet te complex te laten zijn mag je ervan uitgaan dat iedere film een enkele regisseur heeft.

Van iedere film wordt een id vastgelegd, de titel, het id van de regisseur en het jaar waarin de film werd uitgebracht.

In de tabel rol worden een viertal attributen opgegeven, id, id van de acteur, id van de film en de naam van het personage dat vertolkt wordt.

Het is mogelijk om bij deze site een account aan te maken. Ingelogde bezoekers kunnen gegevens van films aanpassen of aanvullen. Ook kunnen ze bijvoorbeeld mooie citaten uit de film aan de betreffende pagina toevoegen of onvolledigheden  of incorrectheden toevoegen (bijvoorbeeld spijkerbroeken in een film die speelt in de Romeinse tijd).

## Gevraagd
Maak deze webapplicatie om de gegevens bij te houden van acteurs, films en de gespeelde rollen. Het is een DUO-opdracht.

## Tips

- Gebruik KISS (hier Keep it Small en Simple), uitbreiden kan altijd nog.
- Kijk goed naar de al beschikbare code, het wiel hoeft niet opnieuw uitgevonden te worden.
- Zorg voor een goede planning en samenwerking!

## Planning:

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


