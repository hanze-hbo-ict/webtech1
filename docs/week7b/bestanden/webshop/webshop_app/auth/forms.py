"""
Auth Blueprint Forms (Week 7b).

Bevat formulieren voor authentication: login en registratie.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from webshop_app.models import db, Customer


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

    def validate_email(self, field):
        """Valideer dat het e-mailadres nog niet in gebruik is.

        WTForms roept validate_<fieldname> automatisch aan!

        Args:
            field: Het email veld uit het formulier

        Raises:
            ValidationError: Als het e-mailadres al geregistreerd is
        """
        if db.session.execute(db.select(Customer).filter_by(email=field.data)).scalar_one_or_none():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')
