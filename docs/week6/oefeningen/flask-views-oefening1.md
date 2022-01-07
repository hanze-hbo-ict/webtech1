# Flask en SQL - Oefening 1

In deze oefening wordt gevraagd de theorie van de laatste twee paragrafen te combineren. Dat zijn het [werken met meerdere tabellen](../flask-views-deel4.md) en [het opzetten van een website](../flask-views-deel5.md).

Op de Hanzehogeschool krijgt iedere student een mentor mee. Het is de bedoeling een site te bouwen waarin dit op een zeer eenvoudige wijze geregeld gaat worden. Maak daarbij heel erg gebruik van code die je al in bezit hebt.

De website heeft het volgende uiterlijk:
![uiterlijk van de website](../imgs/oefening-1-home.png)

Erg veel elementen lijken op het zojuist gegeven voorbeeld.

Dit zijn de aanpassingen die gedaan moeten worden:

- Navigatiebalk krijgt een extra item.
- Er zijn twee modellen (tabellen) nodig (docent en student). Daarbij geldt dat iedere student één mentor heeft en dat een docent mentor kan zijn van meerdere studenten.
- Een derde formulier voor het vastleggen van studentgegevens, naam + ID van docent is genoeg.
- Een extra `@app.route()` is nodig.
- Pas het overzicht aan uit het voorbeeld zodat nu docent en student getoond worden in een mentorrelatie.
- Denk om de naamgeving, een typo is zo gemaakt.
- Er mag iedere keer als er een nieuwe naam is ingevoerd een Flash-bericht getoond worden.
- Alles bij elkaar moet je hiervoor de volgende bestanden maken:
    - Een bestande waarin je gebruik maakt van `FlaskForm` uit `flask_wtf` om de drie formulieren te maken; noem dit bestand `forms.py`;
    - Een bestand met het databasemodel (zoals beschreven in de theorie) en de verschillende *routes* (zoals `@app.route('/list')` of `@app.route('/delete')`) die gebruik maakt van de formulieren uit je bestand `forms.py`; noem dit bestand `mentor_site.py`;
    - Een stuk of zes templates: `base`, waarin je de algemene vormgeving en imports doet, `home`, waarin de bezoeker kan aangeven welke actie hij wil uitvoeren, en verder templates om studenten en docenten toe te voegen of te verwijderen (twee keer twee templates).
