# Webtechnologie 1

In deze module maken we kennis met webtechnologie. We bespreken html en css, en gebruiken het [Bootstrap-framework](https://getbootstrap.com/) om de vormgeving van onze site eenvoudig professioneel te maken. Vervolgens gebruiken we de [python-library Flask](https://flask.palletsprojects.com/en/2.0.x/) om websites interactief te maken en aan te sluiten op een [sqlite-database](https://sqlite.org/index.html).

Zoals altijd hebben we ook in deze module te maken met versies van de afhankelijkheden. Alle voorbeelden en opdrachten zijn getest en uitgewerkt met speciekeke versies, maar in de tussentijd kunnen deze natuurlijk zijn aangepast. [Download hier het requirements-bestand](bestanden/requirements.txt) om de exacte versies van deze *dependencies* te krijgen.

De module is onderdeel van de propedeuse van de opleiding HBO-ICT en is daarom bewust breed van ondiep van opzet: we bespreken alle facetten en alle lagen waar webtechnologie mee te maken heeft, maar gaan nergens echt de diepte in. Het web is een complex apparaat waarin veel verschillende technieken samenwerken en het is binnen het tijdsbestek van tien weken niet mogelijk om die allemaal uit ten treure te behandelen. Voor deze propedeutische fase is het voldoende wanneer deelnemers aan het eind voldoende <i>working knowledge</i> van dit alles hebben. Bij de opleiding Software Engineering komt het web nog uitgebreid aan de orde in semester vier.

## Opzet van het thema

Elke week staat een specifiek onderdeel van het web centraal. Dit onderwerp wordt ondersteund door een vooraf opgenomen theorieles die studenten in hun eigen tijd kunnen doornemen. Hiernaast zijn er werkcolleges, waarin studenten werken aan oefeningen die het onderwerp van die week via een meer praktische weg over het voetlicht brengen. Vanaf week vijf werken studenten in duo’s aan hun eigen project, op basis waarvan de beoordeling plaatsvindt.

Elke klas heeft twee werkcolleges per week. Bij dit werkcollege wordt de theoretische opzet nog een keer praktisch uitgebreid toegelicht. Per week zijn er ook oefeningen gegeven waar studenten individueel of met hun projectduopartner aan kunnen werken. De werkcolleges zijn verder natuurlijk bedoeld om te werken aan het project; de practiumdocent is dan aanwezig om vragen te stellen of te beantwoorden.

## Weekplanning

In de tabel hieronder staan de onderwerpen per week.

P-weeknummer | Onderwerpen
---|---
1 | [Front-end, html en css](week1/1.html/html-deel1.md)
2 | [Python OOP](week2/oop-deel1.md)
3 | *voorjaarsvakantie*
4 | [Python en databases](week3/sql-deel1.md)
5 | [Flask en Jinja-templates](week4/flask-deel1.md)
6 | [Flask en formulieren](week5/flask-forms-deel1.md)
7 | [Flask en databases (ORM)](week6/flask-views-deel1.md)
8 | [Inloggen](week7a/user-authentication-deel1.md) en evt. [Refactoring](week7b/flask-applicaties-deel1.md)

## Toetsing

Liefst zo snel mogelijk, in ieder geval vanaf week vijf, werken studenten in duo's aan hun eigen project, waarbij de volgende onderdelen van belang zijn:

- Website heeft vormgeving en een koppeling met een database
- Op de site ingevulde data komt door sqlalchemy terecht in een sqlite-database
- Website maakt gebruik van verschillende views
- Geregistreerde bezoekers kunnen op de site inloggen

Als studenten geen project hebben of kunnen bedenken, is het ook prima om één van [de vier voorgestelde projecten](projecten/index.md) uit te werken.

Hulpmiddel bij de beoordeling van het project kan een kort assessment met de betreffende practicumdocent zijn. Tijdens dit gesprek van zo'n 10 minuten laten de student-duo's hun uitwerking zien en worden ze bevraagd over de technische en niet-technische aspecten van hun realisatie. Ten behoeve van deze gesprekken wordt een extra lange laatste les in de laatste lesweek ingeroosterd - de docenten maken daarbinnen een separaat rooster voor de duo's.

Basis voor de uiteindelijke beoordeling is [de beoordelings-rubric](rubrics_webtech.html). Mocht het project aan het eind van het blok nog onvoldoende blijken te zijn, dan worden door de betreffende practicumdocent individuele reparatieafspraken (inclusief deadline) gemaakt. In dat geval wordt de onvoldoende wel in Osiris geregistreerd en gelden de herstelwerkzaamheden als herkansing.

Deadlines zijn te vinden in [de BrightSpace-course van dit vak](https://brightspace.hanze.nl/d2l/home/13207).

## Bron

Deze module is in grote lijnen gebaseerd op de cursus [Python and Flask Bootcamp van Udemy](https://www.udemy.com/course/python-and-flask-bootcamp-create-websites-using-flask/). Om deze cursus voor de opleiding geschikt te maken hebben we de programmacode gemoderniseerd en vertaald naar het Nederlandse domein, specifieke methoden en technieken (die voor deze fase te ver gingen) verwijderd en het geheel van uitgebreide tekstuele toelichting voorzien.
