# Flask – Inleiding

## Wat is Flask?

Flask is een webframework, het is een Python-module waarmee op eenvoudige wijze webapplicaties ontwikkeld kunnen worden. Het heeft een kleine en gemakkelijk uit te breiden kern: het is een microframework dat geen ORM (Object Relational Manager) of dergelijke functies bevat. Het heeft veel coole functies, zoals url-routing, template-engine. Het is een WSGI-webapp-framework.

Een Web Application Framework of gewoon een Web Framework vertegenwoordigt een verzameling bibliotheken en modules waarmee ontwikkelaars webtoepassingen kunnen schrijven zonder zich zorgen te hoeven maken over details op laag niveau, zoals protocol en threadbeheer.

Flask is een framework voor webtoepassingen geschreven in Python. Het is ontwikkeld door [Armin Ronacher](https://lucumr.pocoo.org/about/), die leiding gaf aan een team van internationale Python-enthousiastelingen genaamd Poocoo. Flask is gebaseerd op de [Werkzeug WSGI](https://palletsprojects.com/p/werkzeug/) toolkit en de [Jinja2 template engine](https://jinja.palletsprojects.com/en/2.11.x/).

De Web Server Gateway Interface (WSGI) wordt gebruikt als standaard voor de ontwikkeling van Python-webapplicaties. WSGI is de specificatie van een gemeenschappelijke interface tussen webservers en webapplicaties.

Werkzeug is een WSGI-toolkit die verzoeken, responsobjecten en hulpprogramma-functies implementeert. Hierdoor kan er een webframe op gebouwd worden. Het Flask-raamwerk gebruikt Werkzeug als één van de bases.

Jinja2 is een populaire sjabloonengine voor Python. Een websjabloonsysteem combineert een sjabloon met een specifieke gegevensbron om een dynamische webpagina weer te geven. Hiermee kunnen Python-variabelen doorgegeven worden aan HTML-sjablonen.

Een voorbeeld:

```html
<html>
    <head>
        <title> {{titel}} </title>
    </head>
    <body>
        <h1> Hallo {{gebruikersnaam}} </h1>
    </body>
</html>
```

Uit een database kunnen titel en gebruikersnaam opgevraagd worden en worden ingevoegd in een template. Deze waarden worden op het moment dat de pagina wordt opgevraagd door de template-engine gezet op de plaats van de corresponderende waarde tussen de accolades (`{` en `}`).

Flask wordt dus een microframework genoemd. Het is ontworpen om de kern van de applicatie eenvoudig en schaalbaar te houden. In plaats van een abstractielaag voor database-ondersteuning, ondersteunt Flask uitbreidingen om dergelijke mogelijkheden aan de applicatie toe te voegen.

## Waarom is Flask een goede keuze voor een webframework?

Flask is specifiek voor Python gebouwd. Verder is het gemakkelijk om met Flask aan de slag te gaan, omdat het geen enorme leercurve heeft. Bovendien is het erg expliciet, wat de leesbaarheid vergroot. Er zijn slechts een aantal coderegels nodig om een "Hello World" -app te creëren. Daarover zometeen meer.

Het wordt dus een microframework genoemd, maar dat betekent niet dat de gehele app in één enkel Python-bestand ondergebracht hoeft te worden. Vaak is het gewenst en nodig meerdere bestanden te gebruiken voor grote en complexe programma’s.

Flask is één van de meest populaire webframeworks; het is up-to-date en modern. Bovendien is de functionaliteit op eenvoudige wijze uit te breiden.

Maar voordat er met ontwikkelen begonnen kan worden, is het nodig Flask te installeren omdat het niet standaard als module wordt meegenomen bij het installeren van Python.

