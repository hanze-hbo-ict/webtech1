# User authentication - Flask_login deel II

Het bestand `app.py` heeft verreweg de meeste aandacht nodig. Daarom is hier een aparte paragraaf voor. Er zijn een aantal zaken die voor het eerst voorbijkomen en een aantal dingen waar een duidelijke uitleg bij vereist is.

In dit bestand worden de views vastgelegd die nodig zijn om het loginsysteem naar verwachting te laten verlopen. Anders gezegd: de functies die de formulieren en de HTML-bestanden uit de directory `templates` met elkaar zullen gaan verbinden worden ontworpen en gecodeerd.

## Eerste opzet

Eerst worden alle imports opgegeven die nodig zijn om dit bestand goed te laten functioneren:

```python
from mijnproject import app,db
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from mijnproject.models import User
from mijnproject.forms import LoginForm, RegistrationForm
```

De eerste regel laat de app en de database ophalen. Daarna worden van flask een aantal oude bekenden geïmporteerd.

Vanaf de derde coderegel wordt het interessant. Deze regel zorgt ervoor dat de afwikkeling van het inloggen en uitloggen verzorgd worden zonder dat deze handelingen door de programmeur zelf geprogrammeerd hoeven te worden.

Het tweede item wat wordt ingeladen is `login_required`. Hiermee kan de status van een gebruiker (*user*) achterhaald worden en op basis van die status de gepaste bijbehorende inhoud getoond worden. Is een gebruiker nog niet ingelogd dan zal hem de mogelijkheid geboden worden dit te doen. Is een gebruiker ingelogd en is het zijn wens de sessie te beëindigen moet deze mogelijkheid hem worden aangeboden. Hoe dat geregeld wordt, komt zo aan bod.

Verder zijn hier de tabel `User` en de beide formulieren die in de vorige paragraaf ontworpen zijn nodig. Om er weer in te komen eerst de simpelste van de views, de `home-view`:

```python
@app.route('/')
def home() -> str:
    """Toon de homepagina.

    Returns:
        De gerenderde home.html template
    """
    return render_template('home.html')
```

Als eerste een decorator die verwijst naar de homepagina. Deze functie (*view*) krijgt de naam `home` zodat er straks met `url_for()` gemakkelijk naar verwezen kan worden. De laatste regel vertelt dat in dat geval de pagina `home.html` getoond wordt, die pas in de volgende paragraaf zijn inhoud zal krijgen.

De tweede view betreft een view die verschijnt op het moment dat de gebruiker succesvol is ingelogd. Deze view laat een welkomst-bericht tevoorschijn getoverd worden:

```python
@app.route('/welkom')
@login_required
def welkom() -> str:
    """Toon de welkomstpagina voor ingelogde gebruikers.

    Deze view is alleen toegankelijk voor geauthenticeerde gebruikers
    dankzij de @login_required decorator.

    Returns:
        De gerenderde welkom.html template
    """
    return render_template('welkom.html')
```

Wat gelijk opvalt is dat er een tweetal decorators aan het begin van dit codeblok zijn opgenomen. De eerste decorator koppelt de route `/welkom` aan het template bestand `welkom.html`. De tweede decorator controleert of de gebruiker van deze pagina daadwerkelijk is ingelogd. Is dat zo, wordt het welkomstbericht vrijgegeven. In het andere geval wordt er doorgeschakeld naar het loginformulier.

Door deze acties te importeren van `Flask_login` wordt het de ontwikkelaar weer een stuk eenvoudiger gemaakt.

## Logout-view

Nog een redelijk eenvoudige view voordat er met het betere codeerwerk begonnen kan worden. Het wordt een view met de naam `logout`. Wat daar de bedoeling van is moge duidelijk zijn.

```python
from flask import Response

@app.route('/logout')
@login_required
def logout() -> Response:
    """Log de huidige gebruiker uit.

    Deze view is alleen toegankelijk voor ingelogde gebruikers.
    Na het uitloggen wordt de gebruiker doorgestuurd naar de homepagina.

    Returns:
        Redirect naar de home view
    """
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('home'))
```

De `logout` view bevindt zich op de route `/logout`. Deze mogelijkheid wordt alleen geboden indien de gebruiker daadwerkelijk is ingelogd. Daar zorgt de decorator `login_required` voor. Het zou raar zijn uit te kunnen loggen zonder ingelogd te zijn.

Binnen de functie `logout()` zorgt de functie `logout_user()` voor de afwikkeling van het uitloggen. Ook deze functie is geïmporteerd om het leven zo aangenaam mogelijk te maken. Als er succesvol uitgelogd is verschijnt er een flitsbericht en wordt de gebruiker doorgestuurd naar de homepagina.

## Login-proces

Nu het moeilijkere gedeelte, te beginnen met `login`. De uitleg wordt in kleine stapjes gedaan om de denkwijze en uitvoer op een handiger manier duidelijk te maken.

```python
@app.route('/login', methods=['GET', 'POST'])
```

Er wordt begonnen met een decorator. En omdat er bij het inloggen een formulier nodig is, kan het niet achterwege gelaten worden de methoden `GET` en `POST` in deze coderegel op te nemen.

```python
def login() -> str | Response:
    """Handel het login-proces af.

    Returns:
        Bij GET: gerenderde login.html template met formulier
        Bij POST (success): redirect naar welkom of next pagina
        Bij POST (invalid): gerenderde login.html met foutmeldingen
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar_one_or_none()
```

De view krijgt de naam `login` mee. Als eerste wordt er een instantie aangemaakt van het `LoginForm()` dat ook meegeleverd is in het importblok.

Als er in het formulier op de Submit-knop gedrukt is, wordt nagegaan of de gebruiker bekend is in de database. Uit het formulier wordt het e-mailadres opgehaald en vergeleken met de opgeslagen e-mailadressen. Omdat er gecontroleerd is dat er geen dubbele e-mailadressen zijn ingevoerd is het voldoende het eerste gevonden record te benutten. Dit wordt ondergebracht in de variabele `user`.

```python
    if user is not None and user.check_password(form.password.data):
        login_user(user)
        flash('Succesvol ingelogd.')
```

Om succesvol te kunnen inloggen moet er aan twee condities voldaan worden. De gebruiker moet gevonden zijn in de database (daarom controleren we eerst of `user is not None`), en daarna moet het ingevulde wachtwoord van het formulier matchen met het corresponderende wachtwoord in de database. Dat regelt de functie `check_password()`. Is aan beide voorwaarden voldaan wordt de user automatisch ingelogd door de functie `login_user()` en verschijnt er een flitsbericht aan de bovenkant van het scherm. De functie `check_password()` komt mee met `User`.

Nu nog wat bijzonders:

```python
    next = request.args.get('next')

    if next is None or not next[0] == '/':
        next = url_for('welkom')

    return redirect(next)
```

Stel een gebruiker probeert een pagina te bezoeken waarvoor inloggen vereist is (zoals `welkom.html`). Dan slaat `Flask` die URL op in de variabele `next`. Vervolgens wordt de gebruiker doorgelinkt naar het inlogformulier.

Indien er succesvol is ingelogd wordt er nagegaan of de variabele `next` een waarde heeft. Is dat niet het geval wordt het welkomstbericht getoond, anders verschijnt de pagina waar nu wel toestemming voor gegeven is.

Tot slot moet van de inlogview worden bepaald wat in beeld verschijnt als de view wordt aangeroepen:

```python
    return render_template('login.html', form=form)
```

Het is natuurlijk duidelijk dat als de view `login` aangeroepen wordt, het inlogformulier getoond dient te worden.

## Registratie

Nog één view te gaan, het registreren van belangstellenden. Omdat er al veel Engelse termen gebruikt zijn krijgt deze view daarom de route `register` mee.

```python
@app.route('/register', methods=['GET', 'POST'])
```

Ook bij deze view wordt als eerste de route vastgesteld en zijn de methoden `GET` en `POST` noodzakelijk omdat gebruikers zich kunnen aanmelden door een formulier in te vullen.

```python
def register() -> str | Response:
    """Handel het registratieproces af voor nieuwe gebruikers.

    Returns:
        Bij GET: gerenderde register.html template met formulier
        Bij POST (success): redirect naar login view
        Bij POST (invalid): gerenderde register.html met foutmeldingen
    """
    form = RegistrationForm()
```

Bij het aanroepen van de view wordt een object van de klasse `RegistrationForm` aangemaakt.

```python
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Dank voor de registratie. Er kan nu ingelogd worden! ')
```

Indien het formulier met goed gevolg is ingevuld, waarbij onder meer de diverse checks zijn uitgevoerd, wordt er een nieuw object `user` aangemaakt met de ingevulde kenmerken e-mailadres, username en password.

De gegevens worden toevertrouwd aan de database en bevestigd door het `commit()`-statement uit te voeren. Een succesvolle registratie verdient uiteraard weer een flitsbericht.

```python
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
```

Wanneer de view wordt aangeroepen komt de inhoud van de pagina `register.html` in beeld en als het inloggen op een juiste wijze verlopen is wordt er doorgeschakeld naar de view login.

Nog eentje te gaan. Dit is het bestand `app.py`, het bestand waarmee de applicatie gerund wordt. Dat betekent dat de volgende twee coderegels nog nodig zijn:

```python
if __name__ == '__main__':
    app.run(debug=True)
```

Omdat er straks weer getest wordt, heeft debug de waarde `True` meegekregen zodat bij ieder foutje onmiddellijk in beeld verschijnt waar de fout gevonden kan worden. Werkt de applicatie feilloos en kan deze in productie genomen worden, mag debug zeker niet meer de status `True` hebben.

## Samenvatting

In deze les heb je geleerd:

- **`login_required`-decorator**: beveiligt een view zodat alleen ingelogde gebruikers er toegang toe hebben; niet-ingelogde gebruikers worden automatisch doorgestuurd naar de loginpagina
- **`login_user()`**: Flask-Login-functie die de gebruiker officieel inlogt en de sessiegegevens bijhoudt
- **`logout_user()`**: Flask-Login-functie die de sessie beëindigt en de gebruiker uitlogt; de view is zelf ook beveiligd met `@login_required`
- **`next`-parameter**: slaat de oorspronkelijk gevraagde URL op zodat de gebruiker na een succesvolle aanmelding automatisch teruggestuurd wordt naar de gewenste pagina
- **Login-view**: verwerkt een POST-verzoek door het e-mailadres op te zoeken in de database en het wachtwoord te controleren via `check_password()`
- **Registratie-view**: maakt na succesvolle formuliervalidatie een nieuw `User`-object aan en slaat dit op in de database, waarna de gebruiker wordt doorgestuurd naar de loginpagina
- **`flash()`-berichten**: tonen een korte melding na acties zoals inloggen, uitloggen en registreren om de gebruiker te informeren over het resultaat
