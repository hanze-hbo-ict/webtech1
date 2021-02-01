# Flask-applicaties - Structuur

Tot nu toe zijn alle coderegels in één `app.py`-bestand ondergebracht. Voor grotere Flask-applicaties is het logischer om delen van de applicatie in hun eigen bestanden vast te leggen bijvoorbeeld in `models.py`, `forms.py` en `views.py`.
Voor nog grotere toepassingen begint het logisch te worden om de bestanden te herstructureren en componenten te scheiden zoals forms, views en templates voor elke belangrijke component. Bij de vorige oefening waren alle formulieren, views en templates in een enkel bestand of directory opgenomen.
In dit deel aandacht voor de wijze waarop de ontwikkelde applicatie van [oefening 1](../week6/oefeningen/flask-views-oefening1.md) gerefactored kan worden. Dat is een duur woord voor anders opschrijven. Daarvoor wordt de file mentor_site.py opgesplitst in afzonderlijke componenten voor de hierboven genoemde aspecten. In plaats van mentor_site.py wordt vanaf nu app.py gehanteerd.

![](imgs/structuur-flask-app.png)

De blueprints-bibliotheek kan gebruikt worden om deze afzonderlijke modulaire componenten te verbinden met het hoofdbestand app.py. 
Houd er rekening mee dat de app.py nog steeds een rol speelt, alleen verwijst het nu alleen nog naar de subcomponenten in plaats van zelf alle code te bevatten.
Tijd om de definitieve structuur aan te brengen voor deze applicatie!
En omdat het best een lang overzicht wordt is het weergegeven als één geheel op de volgende pagina.

- app.py	#main app.py-bestand dat moet worden aangeroepen om de server voor de webapp te starten
- requirements.txt # Bestand met pip install-statements
- migrations # folder waarin de migraties zijn ondergebracht
- mijn_project # belangrijkste project map, sub-componenten in aparte mappen
    - data.sqlite
    - models.py
    - __init__.py
    - docenten
        - forms.py
        - views.py
        - templates
- docenten
    - add.html
    - delete.html
    - list.html
    - studenten
        - forms.py
        - views.py
        - templates
- studenten
    - add.html
    - static  # voor de opslag van CSS, JS, afbeeldingen, lettertypen etc.
    - templates
        - base.html
        - home.html

In de volgende paragraaf wordt de applicatie die hoort bij de applicatie  van de oefening uit het deel waarin voor het eerste een website gebouwd is omgeschreven naar een meer overzichtelijke vorm.