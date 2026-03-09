"""
Flask-WTF formulieren voor de webshop met authentication (Week 7a).

Dit bestand bevat alle formulier definities voor de webshop applicatie.
We gebruiken Flask-WTF voor automatische CSRF-beveiliging en WTForms validators.

Week 7a toevoegingen:
- LoginForm voor inloggen
- RegistrationForm voor nieuwe gebruikers
- Custom validators voor email en username duplicaten
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    FloatField,
    IntegerField,
    SelectField,
    PasswordField,
    SubmitField
)
from wtforms.validators import DataRequired, NumberRange, Length, Optional, Email, EqualTo, ValidationError
from models import db, Customer


class LoginForm(FlaskForm):
    """Formulier voor het inloggen van bestaande gebruikers."""

    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is verplicht"),
            Email(message="Voer een geldig e-mailadres in")
        ]
    )

    password = PasswordField(
        'Wachtwoord',
        validators=[DataRequired(message="Wachtwoord is verplicht")]
    )

    submit = SubmitField('Inloggen')


class RegistrationForm(FlaskForm):
    """Formulier voor het registreren van nieuwe gebruikers."""

    name = StringField(
        'Naam',
        validators=[
            DataRequired(message="Naam is verplicht"),
            Length(min=2, max=100, message="Naam moet tussen 2 en 100 karakters zijn")
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is verplicht"),
            Email(message="Voer een geldig e-mailadres in")
        ]
    )

    password = PasswordField(
        'Wachtwoord',
        validators=[
            DataRequired(message="Wachtwoord is verplicht"),
            Length(min=6, message="Wachtwoord moet minimaal 6 karakters zijn"),
            EqualTo('password_confirm', message='Wachtwoorden moeten overeenkomen!')
        ]
    )

    password_confirm = PasswordField(
        'Bevestig Wachtwoord',
        validators=[DataRequired(message="Bevestig je wachtwoord")]
    )

    submit = SubmitField('Registreren')

    def validate_email(self, field) -> None:
        """Valideer dat het e-mailadres nog niet in gebruik is.

        Args:
            field: Het email veld uit het formulier

        Raises:
            ValidationError: Als het e-mailadres al geregistreerd is
        """
        if db.session.execute(db.select(Customer).filter_by(email=field.data)).scalar_one_or_none():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')


class AddProductForm(FlaskForm):
    """Formulier om een nieuw product toe te voegen.

    Dit formulier wordt gebruikt door admins om producten
    aan de database toe te voegen.
    """

    name = StringField(
        'Product Naam',
        validators=[
            DataRequired(message="Product naam is verplicht"),
            Length(min=2, max=200, message="Naam moet tussen 2 en 200 karakters zijn")
        ]
    )

    price = FloatField(
        'Prijs (€)',
        validators=[
            DataRequired(message="Prijs is verplicht"),
            NumberRange(min=0.01, max=999999.99, message="Prijs moet tussen €0.01 en €999999.99 zijn")
        ]
    )

    stock = IntegerField(
        'Voorraad',
        validators=[
            DataRequired(message="Voorraad is verplicht"),
            NumberRange(min=0, max=999999, message="Voorraad moet tussen 0 en 999999 zijn")
        ]
    )

    description = TextAreaField(
        'Beschrijving',
        validators=[
            Optional(),
            Length(max=1000, message="Beschrijving mag maximaal 1000 karakters zijn")
        ]
    )

    category_id = SelectField(
        'Categorie',
        validators=[DataRequired(message="Categorie is verplicht")],
        coerce=int
    )

    submit = SubmitField('Product Toevoegen')


class EditProductForm(FlaskForm):
    """Formulier om een bestaand product te bewerken.

    Dit formulier is vergelijkbaar met AddProductForm maar
    wordt gebruikt voor het wijzigen van bestaande producten.
    """

    name = StringField(
        'Product Naam',
        validators=[
            DataRequired(message="Product naam is verplicht"),
            Length(min=2, max=200, message="Naam moet tussen 2 en 200 karakters zijn")
        ]
    )

    price = FloatField(
        'Prijs (€)',
        validators=[
            DataRequired(message="Prijs is verplicht"),
            NumberRange(min=0.01, max=999999.99, message="Prijs moet tussen €0.01 en €999999.99 zijn")
        ]
    )

    stock = IntegerField(
        'Voorraad',
        validators=[
            DataRequired(message="Voorraad is verplicht"),
            NumberRange(min=0, max=999999, message="Voorraad moet tussen 0 en 999999 zijn")
        ]
    )

    description = TextAreaField(
        'Beschrijving',
        validators=[
            Optional(),
            Length(max=1000, message="Beschrijving mag maximaal 1000 karakters zijn")
        ]
    )

    category_id = SelectField(
        'Categorie',
        validators=[DataRequired(message="Categorie is verplicht")],
        coerce=int
    )

    submit = SubmitField('Wijzigingen Opslaan')


class ContactForm(FlaskForm):
    """Formulier voor klanten om contact op te nemen.

    Dit is een eenvoudig contactformulier dat later kan worden
    uitgebreid met email functionaliteit.
    """

    name = StringField(
        'Naam',
        validators=[
            DataRequired(message="Naam is verplicht"),
            Length(min=2, max=100, message="Naam moet tussen 2 en 100 karakters zijn")
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is verplicht"),
            Length(max=120, message="Email mag maximaal 120 karakters zijn")
        ]
    )

    subject = StringField(
        'Onderwerp',
        validators=[
            DataRequired(message="Onderwerp is verplicht"),
            Length(min=3, max=200, message="Onderwerp moet tussen 3 en 200 karakters zijn")
        ]
    )

    message = TextAreaField(
        'Bericht',
        validators=[
            DataRequired(message="Bericht is verplicht"),
            Length(min=10, max=2000, message="Bericht moet tussen 10 en 2000 karakters zijn")
        ]
    )

    submit = SubmitField('Verzenden')
