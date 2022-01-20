!!! Warning "Begin met één van de projecten"

    Vanaf deze week moet je als duo aan [één van de vier voorgestelde projecten](../projecten/) gaan werken. Tijdens de practica heb je gelegenheid om hierover vragen te stellen aan je practicumdocent, maar hou er rekening mee dat het practicum daar niet per se voor bedoeld is. In principe zou je in staat moeten zijn op basis van de oefeningen en de theorielessen het project zelfstandig uit te voeren.

    Bekijk [de omschrijving de beoordeling](../index.md#toetsing) om je een goed beeld te vormen van het hoe of wat van deze projecten en de daarbij horende beoordeling.


# Flask en Forms - een basis Flask formulier

Flask biedt ook de mogelijkheid om eenvoudig HTML-formulieren te genereren. In dit deel ligt de focus op de modules [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) en [WTForms](https://wtforms.readthedocs.io/en/2.3.x/) en op welke wijze waarop deze gebruikt kunnen worden om snel formulieren te maken op basis van de Flask-Python-scripts.

## Componenten
Maar als eerste een bespreking van de belangrijkste componenten voor het maken van een formulier.
Dat zijn de volgende onderdelen:

- Configureer een secret key voor de beveiliging.
- Maak een WTForm-klasse aan.
    - Ontwerp velden voor alle onderdelen op het formulier.
- Stel een View Function in (weergavefunctie).
    - Voeg methoden toe ([`GET`, `POST`]).
    - Maak een instantie van Form Class aan.
    - Verwerk het formulier.

## Voorbeeld
Om deze materie te kunnen begrijpen volgt nu een uitgebreid voorbeeld. Dit voorbeeld bestaat uit een Python-file ([`basis_flask_form.py`](bestanden/basis_flask_form.py)) en een enkel HTML-bestand, getiteld [`home.html`](bestanden/home.html). Dit HTML-bestand wordt weer opgenomen in de folder ‘templates’.

### Python gedeelte
Als eerste de Python-file. Er moeten nu meerdere zaken worden geïmporteerd, zie onderstaand kader.

```python
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
```

Even een korte uitleg. `FlaskForm` is een klasse waarvan overerft wordt om onze eigen formulieren te kunnen maken. De daaropvolgende regel geeft aan welke velden er gebruikt worden op de formulieren. Voor het basisformulier wordt hier aangegeven dat er Stringfields en SubmitFields gebruik gaan worden. De laatste regel zorgt er weer voor dat de applicatie gecreëerd wordt.

### Installatie van Flask-WTF en WTForms

Het kan zijn dat de modules `flask_wtf` (Flask-WTF) en `wtforms` (WTForms) nog niet geïnstalleerd zijn. Let natuurlijk op dat de Python virtuele omgeving is geactiveerd en controleer met `pip` welke modules al geïnstalleerd zijn:

```console
(webtech)~ $> pip list
Package      Version
------------ -------
click        7.1.2
Flask        1.1.2
itsdangerous 1.1.0
Jinja2       2.11.3
MarkupSafe   1.1.1
pip          21.0.1
setuptools   47.1.0
Werkzeug     1.0.1
```

Helaas, geen Flask-WTF of WTForms... Dat kan snel worden verholpen, op dezelfde manier zoals je eerder Flask hebt geïnstalleerd:

```console
(webtech)~ $> pip install Flask-WTF
```

Als je nu nogmaals `pip` een overzicht van modules vraagt zal je zien dat ze nu geïnstalleerd zijn:

```console hl_lines="6 13"
(webtech)~ $> pip list
Package      Version
------------ -------
click        7.1.2
Flask        1.1.2
Flask-WTF    0.14.3
itsdangerous 1.1.0
Jinja2       2.11.3
MarkupSafe   1.1.1
pip          21.0.1
setuptools   47.1.0
Werkzeug     1.0.1
WTForms      2.3.3
```

!!! notice "Afhankelijkheden"
    Met `pip install Flask-WTF` is tegelijkertijd ook WTForms geïnstalleerd zonder dat je dit hebt opgegeven! Dit komt omdat Flask-WTF aangeeft dat het afhankelijk is van WTForms en `pip` slim genoeg is om vervolgens ook deze module direct op te halen en te installeren.

#### De geheime sleutel
Nadat de installatie van de applicatie is afgerond is de volgende stap het configureren van een geheime `SECRET_KEY`. Hier is het ter demonstratie, maar later wordt er echt veel meer aandacht aan besteed en zullen er betere manieren aangeleerd worden om dit te doen.

```python
app.config['SECRET_KEY'] = 'mijngeheimesleutel'
```

#### InfoForm
De volgende stap is het aanmaken van een klasse `InfoForm`, een subklasse van `FlaskForm`.

```python
class InfoForm(FlaskForm):
```

Op het formulier komen een tweetal velden te staan: een `StringField` genaamd instrument, en een `SubmitField`, een knop met het opschrift ‘Verzend’.

```python
class InfoForm(FlaskForm):

    instrument = StringField('Welk instrument wil je graag leren bespelen?')
    submit = SubmitField('Verzend')
```

#### View functie
Wanneer alle voorbereidingen zijn getroffen, kan de viewfunctie aangemaakt worden. Standaard wordt de eerste view doorgelinkt naar de indexpagina.

```python
@app.route('/', methods=['GET', 'POST'])
def index():
```

Aan de functie worden de parametermethoden `GET` en `POST `meegegeven. Deze zorgen ervoor dat het mogelijk wordt om de ingevoerde gegevens door te geven aan een template, in dit geval `home.html`.
De waarde van de variabele `instrument` krijgt de status `False` mee, omdat deze aan het begin van het programma nog geen waarde heeft meegekregen. Dat gaat veranderen wanneer het formulier is ingevuld.

```python
instrument = False
# Maak een object van de klasse InfoForm aan.
form = InfoForm()
# Als het formulier valide is
if form.validate_on_submit():
    # Haal de data voor instrument op uit het formulier.
    instrument = form.instrument.data
    # Zet de waarde voor de variabele instrument op het formulier weer op False
    form.instrument.data = ''
    return render_template('home.html', form=form, instrument=instrument)
```
Op het valide zijn wordt nog nader ingegaan.

En tot slot natuurlijk weer:

```python
if __name__ == '__main__':
    app.run(debug=True)
```

### HTML gedeelte: home.html
in `home.html` moet natuurlijk ook code staan. Eerst de bovenste helft:

```html
<p>
{% if instrument %}
    Het instrument van jouw keuze is {{ instrument }}.
    <br>De keuze kan gewijzigd worden in onderstaand formulier:
{% else %}
    Geef de naam van een instrument op in dit formulier:
{% endif %}
</p>
```

Als `home.html` wordt aangeroepen heeft de variabele `instrument` nog altijd de waarde `False`. De voorwaarde achter de `if` is dan niet waar en er wordt overgegaan naar het `else`-blok, waar gevraagd wordt om de naam van een instrument in te geven.

De tweede helft ziet er als volgt uit:

```html
<form method="POST">
    {{ form.hidden_tag() }}
    {{ form.instrument.label }} {{ form.instrument() }}
    {{ form.submit() }}
</form>
```

### Runnen van de applicatie

Bij het runnen van de applicatie wordt het volgende scherm zichtbaar:

![home.html met formulier](imgs/formulier-1-html.png)

Conform de basisinstellingen van de klasse InfoForm heeft `instrument` de waarde `False`. Bij een klik op de button ‘Verzend’ wordt `home.html` aangeroepen. Voor die tijd is als instrument ‘Gitaar’ ingevuld. Bij de aanroep worden het formulier als ook de opgegeven waarde voor `instrument `meegestuurd.

![home.html met ingevuld formulier](imgs/formulier-2-html.png)

Het bovenste gedeelte van de code van `home.html` draagt zorg voor de eerste twee regels van de output. De onderste helft stelt het formulier nogmaals ter beschikking om een ander instrument te kiezen.

Wanneer er geen `SECRET_KEY` wordt opgenomen in de Python-file ontstaat er bij het runnen een foutmelding. Deze is dus vereist evenals de hidden tag.
