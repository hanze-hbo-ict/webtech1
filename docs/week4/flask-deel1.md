# Flask – Inleiding

Bestudeer ook [de presentatie over Flask en Jinja via deze link](https://video.hanze.nl/media/HC+webtech1%2C+deel+4A+Flask+en+Jinja/0_hl2ub9s2) (let op: je moet hiervoor wel inloggen in het Hanze-systeem)

## Wat is Flask?

Flask is een webframework, het is een Python-module waarmee op eenvoudige wijze webapplicaties ontwikkeld kunnen worden. Het heeft een kleine en gemakkelijk uit te breiden kern: het is een microframework dat geen ORM (Object Relational Manager) of dergelijke functies bevat. Het heeft wel veel coole functies, zoals url-routing en een template-engine. Het is een WSGI-webapp-framework.

Een Web Application Framework of gewoon een Web Framework vertegenwoordigt een verzameling bibliotheken en modules waarmee ontwikkelaars webtoepassingen kunnen schrijven zonder zich zorgen te hoeven maken over details op laag niveau, zoals protocol en threadbeheer.

Flask is een framework voor webtoepassingen geschreven in Python. Het is ontwikkeld door [Armin Ronacher](https://lucumr.pocoo.org/about/), die leiding gaf aan een team van internationale Python-enthousiastelingen genaamd Poocoo. Flask is gebaseerd op de [Werkzeug WSGI](https://palletsprojects.com/p/werkzeug/) toolkit en de [Jinja2 template engine](https://jinja.palletsprojects.com/en/2.11.x/).

De Web Server Gateway Interface (WSGI) wordt gebruikt als standaard voor de ontwikkeling van Python-webapplicaties. WSGI is de specificatie van een gemeenschappelijke interface tussen webservers en webapplicaties.

Werkzeug is een WSGI-toolkit die verzoeken, responsobjecten en hulpprogramma-functies implementeert. Hierdoor kan er een webframe op gebouwd worden. Het Flask-raamwerk gebruikt Werkzeug als één van de bases.

Jinja2 is een populaire sjabloonengine voor Python. Een websjabloonsysteem combineert een sjabloon met een specifieke gegevensbron om een dynamische webpagina weer te geven. Hiermee kunnen Python-variabelen doorgegeven worden aan HTML-sjablonen.

Een voorbeeld:

```html
<html>
    <head>
        <title>{{ titel }}</title>
    </head>
    <body>
        <h1>Hallo {{ gebruikersnaam }}</h1>
    </body>
</html>
```

Uit een database kunnen titel en gebruikersnaam opgevraagd worden en worden ingevoegd in een template. Deze waarden worden op het moment dat de pagina wordt opgevraagd door de template-engine gezet op de plaats van de corresponderende waarde tussen de dubbele accolades (`{` en `}`).

Flask wordt dus een microframework genoemd. Het is ontworpen om de kern van de applicatie eenvoudig en schaalbaar te houden. In plaats van een abstractielaag voor database-ondersteuning, ondersteunt Flask uitbreidingen om dergelijke mogelijkheden aan de applicatie toe te voegen.

**Volgende stap:** [Deel 2](flask-deel2.md) - Flask installeren met uv.

## Samenvatting

In deze les heb je geleerd:

- **Flask**: een Python microframework voor het bouwen van webapplicaties, met ingebouwde url-routing en een template-engine
- **Microframework**: Flask houdt de kern klein en uitbreidbaar; functionaliteit zoals database-ondersteuning wordt via extensies toegevoegd in plaats van ingebouwd te zijn
- **Web Application Framework**: een verzameling bibliotheken waarmee webapplicaties ontwikkeld worden zonder details op laag niveau zoals protocol- en threadbeheer
- **WSGI**: de Web Server Gateway Interface, de standaard interface tussen webservers en Python-webapplicaties
- **Werkzeug**: de WSGI-toolkit waarop Flask is gebouwd, die request- en response-afhandeling verzorgt
- **Jinja2**: de template-engine van Flask, waarmee Python-variabelen in HTML-sjablonen ingevoegd worden via dubbele accolades (`{{ variabele }}`)
