# User authentication - Flask_login deel I

De `Flask-login` bibliotheek maakt het heel eenvoudig om gebruikersauthenticatie toe te voegen aan webapplicaties. Deze bibliotheek heeft tevens de beschikking over gemakkelijk op te vragen decorators, waarmee extra gebruikersfunctionaliteit toegevoegd kan worden.

De structuur van de inlogprocedure heeft de volgende vorm:

```text
.
├── app.py
└── mijnproject
    ├── forms.py
    ├── __init__.py
    ├── models.py
    └── templates
        ├── base.html
        ├── home.html
        ├── login.html
        ├── register.html
        └── welkom.html
```

Dit zijn alle files die nodig zijn bij dit project, met de naam `mijnproject`; [download hier de bestanden](bestanden/login.zip). Technisch gezien is de applicatie te klein om uit te kunnen splitsen in aparte onderdelen, zoals in het vorige deel beschreven is. Maar dezelfde opzet is wel aangehouden.

## `__init__.py`

De eerste actie is weer het importeren van de benodigde items:

```python hl_lines="5"
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
```

De onderste coderegel is nieuw. Waarschijnlijk zul je deze module separaat installeren door middel van `pip`.

`Flask-login` biedt gebruikerssessiebeheer voor `Flask`. Het voert de algemene taken uit van inloggen, uitloggen en het onthouden van de sessies van de gebruikers gedurende langere perioden. Hieronder staat een opsomming.

- De ID van de actieve gebruiker wordt opgeslagen in de sessie, zodat het gemakkelijker is de gebruiker aan en af te melden.
- Het laten zien van de views kan beperkt worden tot ingelogde (of uitgelogde) gebruikers.
- Het zorgt voor een handige “Remember me"-functionaliteit.
- Het helpt mee de sessiegegevens van de gebruikers te beschermen tegen diefstal door cookiedieven.

Er zijn ook een aantal zaken die niet geregeld worden door de `Loginmanager`, maar daar wordt een oplossing voor geregeld tijdens het coderen.

Zie de onderstaande code-listing voor een uitgewerkt voorbeeld:

```python hl_lines="10 11 12"
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mijngeheimesleutel'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
```

De tweede gearceerde coderegel zorgt ervoor dat de app bekend is bij de `login_manager` en met de laatste regel wordt de plek doorgegeven waar gebruikers kunnen inloggen.

## `models.py`

Vervolgens weer de coderegels waarmee de benodigde items geïmporteerd worden. Ook hier is een nieuw item aanwezig. Verder is de keuze voor hashing gevallen op `Werkzeug`.

```python
from mijnproject import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
```

In de eerste coderegel wordt vastgelegd dat uit `__init__.py`, `db` en `login_manager` nodig zijn voor een juiste werking. De tweede regel is bekend en de derde coderegel zorgt voor enige luxe. `UserMixin` wordt als superklasse gebruikt en dat betekent dat er toegang verkregen wordt tot veel ingebouwde functies. Het is dan niet meer nodig als ontwikkelaar deze zelf aan te maken. Ze kunnen gewoon aangeroepen worden.

Bijvoorbeeld:

- `is_authenticated()`
- `is active()`
- `is_anonymous()`
- `get_id()`

Nu kan de gebruikersklasse aangemaakt worden. De naam van de klasse wordt `User`, dat is hier een gangbaardere term dan `Gebruiker`. Voor iedere gebruiker wordt het ID, de gebruikersnaam, een wachtwoord en het e-mailadres vastgelegd.

De klasse `User()` erft eigenschappen van `dbModel` en `UserMixin`:

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class User(db.Model, UserMixin):
    """User model voor authenticatie.

    Erft van db.Model voor database functionaliteit en UserMixin voor
    ingebouwde Flask-Login methoden zoals is_authenticated(), is_active(),
    is_anonymous(), en get_id().
    """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(128))
```

Achter de variabelen `email`, `username` en `password_hash` staat een getal genoteerd (64 of 128). Dat betreft het aantal posities dat voor die variabele beschikbaar is. Verder hebben `email` en `username` het kenmerk `unique` meegekregen. Op de primary key wordt automatisch gecontroleerd dat er geen dubbele waarden van voorkomen, maar het e-mailadres en de gebruikersnaam mogen natuurlijk ook maar één keer voorkomen in de database met inloggegevens.

Nu is het weer de beurt aan `__init__()`. De volgorde waarin de coderegels worden opgenomen in de diverse bestanden heeft steeds eenzelfde stramien.

```python
def __init__(self, email: str, username: str, password: str) -> None:
    """Initialiseer een nieuwe gebruiker.

    Args:
        email: Het e-mailadres van de gebruiker
        username: De unieke gebruikersnaam
        password: Het wachtwoord in plain text (wordt automatisch gehashed)
    """
    self.email = email
    self.username = username
    self.password_hash = generate_password_hash(password)
```

Voor iedere nieuwe gebruiker wordt gevraagd om een gebruikersnaam, een e-mailadres en een wachtwoord. Van het opgegeven wachtwoord wordt onmiddellijk een hash-versie geproduceerd.

Verder is er nog een methode nodig die gaat controleren of het ingevoerde wachtwoord het juiste is. In de vorige paragraaf is deze methode uitgebreid besproken:

```python
def check_password(self, password: str) -> bool:
    """Controleer of het opgegeven wachtwoord correct is.

    Args:
        password: Het te verifiëren wachtwoord in plain text

    Returns:
        True als het wachtwoord overeenkomt, anders False
    """
    return check_password_hash(self.password_hash, password)
```

Er wordt gecontroleerd of het opgegeven password voldoet aan de hash-versie. Er wordt `True` of `False` als uitkomst geretourneerd.

Als laatste nog een nieuwe vereiste methode. Deze nieuwe functie `load_user()` wordt in de code opgenomen net voor het definiëren van de klasse `User()`:

```python
@login_manager.user_loader
def load_user(user_id: int) -> User | None:
    """Laad een gebruiker op basis van het user ID.

    Deze functie wordt gebruikt door Flask-Login om de huidige gebruiker
    te laden uit de sessie.

    Args:
        user_id: Het ID van de gebruiker om te laden

    Returns:
        De User instantie als gevonden, anders None
    """
    return db.session.get(User, int(user_id))
```

De `user_loader` decorator geeft `Flask-login` toestemming om de gegevens van de huidige gebruiker te laden en het bijbehorende ID te gebruiken. Daarmee kan de gebruiker pagina’s bekijken die bij zijn profiel horen, zoals onder andere het beheren van de eigen gegevens en eigen blogberichten. En na een succesvolle aanmelding kan de naam van de gebruiker aan een welkomstwoord gekoppeld worden.

## `forms.py`

In dit bestand worden de formulieren opgesteld. Bij het inloggen vinden er een aantal controles plaats, dus naast het importeren van de formulieropties, moeten ook de voorgeprogrammeerde validaties beschikbaar komen om die controles te kunnen uitvoeren zonder dat de ontwikkelaar ze zelf weer hoeft uit te programmeren.

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from mijnproject.models import User
```

Er moet gecontroleerd worden of velden op een formulier voldoen aan de verplichting een waarde te krijgen. Verder vindt er toezicht plaats of het opgegeven e-mailadres aan de eisen voldoet: is er bijvoorbeeld een apenstaartje (`@`) meegestuurd en dergelijke. De validator `EqualTo` is uitgerust om twee waardes met elkaar te vergelijken. Mocht er iets niet in orde dan kan er met behulp van de `ValidationError` een passende melding getoond wordt.

Nu kunnen de formulieren opgebouwd worden, te beginnen met het registratieformulier. Omdat er als veel vaker Engelse termen in de code zijn opgetekend, worden hier ook Engelse benamingen gehanteerd.

```python
class RegistrationForm(FlaskForm):
    """Formulier voor het registreren van nieuwe gebruikers."""

    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField(
        'Password',
        validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')]
    )
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Leg vast!')
```

Voor de variabele `email` zijn twee (2) validators opgenomen: `DataRequired` en `Email`: dit betekent dat het tekstveld een verplichte invulling heeft er en er tevens een controle op de inhoud zal worden toegepast.

De variabele `password` verdient ook de nodige aandacht te krijgen. Deze is van het type `PasswordField`, wat wil zeggen dat de inhoud op het scherm niet door anderen kan worden afgelezen. Het is in ieder geval een verplicht veld op het formulier. Op de tweede validator-optie komen we zo terug.

Bij een registratie is het heel gebruikelijk te vragen om het wachtwoord nog een keer op te voeren om na te kunnen gaan of de gebruiker geen typo heeft gemaakt. Zo ook hier. De user voert een tweede keer het wachtwoord in dat wordt opgeslagen in de variabele `pass_confirm`.

Nu weer terug naar het veld waar voor de eerste keer het wachtwoord wordt ingevuld. De tweede validator hier is `EqualTo`. Hierbij wordt nu vergeleken of de beide opgegeven wachtwoorden aan elkaar gelijk zijn.

Aan dit formulier worden nog een tweetal methoden verbonden:

```python
def validate_email(self, field) -> None:
    """Valideer dat het e-mailadres nog niet in gebruik is.

    Args:
        field: Het email veld uit het formulier

    Raises:
        ValidationError: Als het e-mailadres al geregistreerd is
    """
    if db.session.execute(db.select(User).filter_by(email=field.data)).scalar_one_or_none():
        raise ValidationError('Dit e-mailadres staat al geregistreerd!')
```

De melding is al duidelijk genoeg, maar toch nog wat extra uitleg. Er wordt gecontroleerd of het opgegeven e-mailadres gevonden kan worden door de waarde ervan op te geven in `db.session.execute(db.select(User).filter_by(email=field.data)).scalar_one_or_none()`. Geeft dit resultaat niet `None`, dan is er al een e-mailadres met een gelijke inhoud in de database te vinden, en dat mag niet. Er moet dan een melding getoond worden, hetgeen hier dus via de `ValidationError` geregeld is.

De tweede methode is nagenoeg gelijk aan de eerste. Alleen moet er nu nagegaan worden of de gebruikersnaam al in de database voorkomt.

```python
def validate_username(self, field) -> None:
    """Valideer dat de gebruikersnaam nog niet in gebruik is.

    Args:
        field: Het username veld uit het formulier

    Raises:
        ValidationError: Als de gebruikersnaam al bestaat
    """
    if db.session.execute(db.select(User).filter_by(username=field.data)).scalar_one_or_none():
        raise ValidationError('Deze gebruikersnaam is al vergeven, probeer een ander naam!')
```

## Het inlogformulier

Nu het registratieformulier ontwikkeld is, is de volgende logische stap het aanmaken van een inlogformulier:

```python
class LoginForm(FlaskForm):
    """Formulier voor het inloggen van bestaande gebruikers."""

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Inloggen')
```

Ook hier geldt dat het inlogformulier eigenschappen overneemt van `FlaskForm`. Verder is er niet zo veel bijzonders bij dit formulier te vermelden. Zoals al wel vaker gezegd, meer van hetzelfde.

Het formulier kent twee velden, eentje om de gebruikersnaam in te geven en het tweede veld is beschikbaar voor het wachtwoord. Tenslotte kan het inloggen worden afgesloten door op de knop met het opschrift 'Inloggen' te klikken.

## Samenvatting

In deze les heb je geleerd:

- **Flask-Login**: een bibliotheek die sessie- en gebruikersbeheer verzorgt, waaronder inloggen, uitloggen en het onthouden van gebruikerssessies
- **LoginManager**: het centrale object uit Flask-Login dat via `init_app()` aan de app gekoppeld wordt en via `login_view` aangeeft waar gebruikers kunnen inloggen
- **UserMixin**: een superklasse die de `User`-klasse standaardmethoden geeft zoals `is_authenticated()`, `is_active()`, `is_anonymous()` en `get_id()`
- **Wachtwoord hashing in het model**: het wachtwoord wordt bij het aanmaken van een gebruiker direct gehashed opgeslagen; de plain-text variant wordt nergens bewaard
- **`check_password()`-methode**: controleert bij het inloggen of het ingevoerde wachtwoord overeenkomt met de opgeslagen hash
- **`user_loader`-decorator**: laadt de huidige gebruiker op basis van het sessie-ID, zodat Flask-Login de ingelogde gebruiker bij elke aanvraag automatisch kan opzoeken
- **`RegistrationForm`**: een WTForms-formulier met validaties voor uniek e-mailadres, unieke gebruikersnaam en wachtwoordbevestiging via `EqualTo`
- **`LoginForm`**: een eenvoudig formulier met een e-mailadres- en wachtwoordveld voor bestaande gebruikers
