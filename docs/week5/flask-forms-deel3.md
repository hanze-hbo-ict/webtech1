# Flask en Forms - Flash-berichten

## Introductie
De titel van deze paragraaf is geen typfout. Er wordt inderdaad Flash bedoeld.
Soms is het handig de gebruiker een bericht te sturen dat niet permanent bewaard hoeft te worden op de view-pagina. Een dergelijk bericht kan naar de gebruiker ‘geflasht’ worden en vervolgens worden gesloten. Dat betekent dat het niet meer hardcoded in een view op een Python-file hoeft te worden opgenomen.

Aan het eind van deze tekst maken we [oefening 1](oefeningen/flask-forms-oefening1.md).

## Voorbeeld
Flask kan dat op een gemakkelijke manier voor elkaar krijgen.
Dit wordt nu weer besproken aan de hand van een voorbeeld. In dit voorbeeld zijn twee bestanden nodig, [`home2.html`](bestanden/home2.html) en [`flashing_messages.py`](bestanden/flashing_messages.py).

### Python gedeelte
Zoals gebruikelijk als eerste de Python-file. Het begin moet geen vragen meer oproepen.

```python hl_lines="1"
from flask import Flask, render_template, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mijngeheimesleutel'
```

Het enige bijzondere bij het importeren is dat nu ook `flash` in het rijtje wordt meegenomen.
Vervolgens wordt de applicatie weer aangemaakt en omdat er met een formulier gewerkt wordt is de geheime sleutel ook een vereiste.

#### SimpelForm
Het formulier moet ook weer aangemaakt worden:

```python
class SimpelForm(FlaskForm):
    submit = SubmitField('Klik mij!')
```

Het formulier kent slechts een enkel veld, een knop met de tekst ‘Klik mij!’.
Het idee is dat als de button geactiveerd wordt, er een melding op het scherm verschijnt.

#### View functies
Als derde actie wordt de view voor het formulier opgezet:

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SimpelForm()

    if form.validate_on_submit():
        flash("Je hebt zojuist de button geactiveerd!")

        return redirect(url_for('index'))
    return render_template('home2.html', form=form)
```

De view heeft de naam index meegekregen en er wordt een instantie van de klasse `SimpelForm` aangemaakt. Wanneer er op de knop geklikt wordt, zorgt het flash-commando ervoor dat er melding naar het scherm gestuurd wordt via het redirect-statement. Het tweede return-statement is nodig om in eerste instantie het formulier te laten zien.

#### Afsluiting python code
Om de boel te laten runnen, gebruiken we de inmiddels bekende code:

```python
if __name__ == '__main__':
    app.run(debug=True)
```


### HTML gedeelte

#### Bootstrap
Bij het opzetten van de file `home2.html `komt de opgedane kennis van Bootstrap goed van pas. De melding die naar het scherm gestuurd gaat worden krijgt een opvallende lay-out mee zodat het is duidelijk herkenbaar is.

Als er elementen van Bootstrap gebruikt gaan worden in een HTML-file is het nodig een aantal koppelingen te leggen naar Bootstrap. Deze linken worden in de ‘head’ van de HTML-file, `home2.html`, ondergebracht.

```html
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-  WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js" integrity="sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB/pTJ0euyQp0Mk8ck+5T" crossorigin="anonymous"></script>
```

Deze code is overgenomen uit [het HTML-bestand met daarin oplossing van oefening 5](../week1/oefeningen/wk1oefening5.md) uit het onderdeel HTML/CSS/Bootstrap. Hierna kan gesprongen worden naar dat gedeelte op de site van Bootstrap waar de code voor de melding gevonden kan worden. Dat gedeelte kan [hier gevonden worden](https://getbootstrap.com/docs/4.0/components/alerts/).

Voor de melding wordt als component `Alert` geselecteerd. Hiermee kunnen feedbackberichten als reactie op gebruikersacties aangemaakt worden. Van de beschikbare opties is hier gekozen voor `dismissing`.
Het onderstaande plaatje is rechtstreeks overgenomen van de Bootstrap-site.

![Alert melding code en voorbeeld op bootstrap site](imgs/alert-melding-bootstrap.png)

De button ‘Copy’ hoort er natuurlijk niet bij. Deze heeft tot doel een kopie van de code naar Clipboard te sturen.

Deze code kan natuurlijk aan `home2.html `toegevoegd worden. Voordat deze actie daadwerkelijk wordt uitgevoerd, is het nodig eerst nog twee andere stappen te verrichten:

#### Container

```html
<div class="container">
{% for mess in get_flashed_messages()  %}

    {{ mess }}

{% endfor %}
```

Alle bedrijvigheden worden bij elkaar gehouden door ze in een container te stoppen. Het ziet er misschien wat vreemd uit dat er een `for` is opgenomen in de code. Het is natuurlijk mogelijk dat er meerdere berichten geflitst gaan worden. De `for` verstuurt ze dan tegelijkertijd. Voor de code maakt het niet uit of het er één is of meerdere.

Daarna kan de Bootstrap-code worden ingeladen:

```html
{% for mess in get_flashed_messages()  %}
<div class="alert alert-warning alert-dismissible fade show" role="alert">
    {{ mess }}
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
</div>
{% endfor %}
```
Wat gebeurt er nu precies wanneer de boodschap verstuurd wordt? Of anders gezegd, wat staat er nu precies?

#### get_flashed_messages()
Als het flash-commando afgaat dan worden de meldingen naar de template gestuurd die in de view is opgenomen. Dat gaat in de vorm van de methode `get_flashed_messages()`. Hierin worden alle berichten ondergebracht en deze worden als het er meer zijn, na elkaar afgespeeld.

#### fade show
De aanroep naar de Bootstrap-klasse zorgt ervoor dat de gebruiker de mogelijkheid krijgt het bericht weer te laten verdwijnen door op het kruisje rechtsboven te klikken. De property `fade show` geeft aan dat de melding gaat vervagen totdat deze niet meer zichtbaar is.

#### button
De regel die begint met `<button type….> `is nodig om het kruisje rechtsboven in weer te geven, en dat een klik op dat kruisje het bericht afsluit.

#### aria-label
Het `aria-label` attribuut wordt gebruikt om een string te definiëren die het huidige element labelt. Het wordt vaak gebruikt als er geen tekstlabel zichtbaar is. Door `aria-hidden = "true"` aan een element toe te voegen, worden dat element en al zijn onderliggende elementen verwijderd en is daarna niet langer beschikbaar.

#### afsluiting html code
Om deze code af te maken moet het formulier nog worden ontworpen en de container beëindigd:

```html
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.submit() }}
    </form>
</div>
```

Tenslotte is het niet zo heel erg netjes om een tekst als ‘Holy guacamole’ als boodschap te flashen. Omdat de melding al in de view is opgenomen kan deze regel geschrapt worden.

#### volledige html code
De gehele code wordt dan (zonder de head-sectie):

```html
<div class="container">

    {% for mess in get_flashed_messages()  %}
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
        {{ mess }}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    {% endfor %}

    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.submit() }}
    </form>
</div>
```


### Runnen van de applicatie

Wanneer we de code testen door de python file te runnen krijgen we het volgende:

![Een button met de tekst 'Klik mij!'](imgs/Button-met-klik-mij-tekst.png)


En na de klik:
![De pagina nadat er op de button is geklikt. Een bericht wordt geflasht](imgs/button-met-melding.png)

Tenslotte de test wat er gebeurt wanneer er op het kruisje geklikt wordt:

![Het bericht is verdwenen](imgs/Button-met-klik-mij-tekst.png)

Maak nu [oefening 1](oefeningen/flask-forms-oefening1.md).