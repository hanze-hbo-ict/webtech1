from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from mijnproject.models import User
from mijnproject import db
from sqlalchemy import select


class LoginForm(FlaskForm):
    """Formulier voor gebruikers login."""

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    """Formulier voor nieuwe gebruikers registratie."""

    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Registreer!')

    def check_email(self, field):
        """Valideer dat email nog niet in gebruik is.

        Args:
            field: Het email veld uit het formulier

        Raises:
            ValidationError: Als email al bestaat in database
        """
        if db.session.execute(select(User).filter_by(email=field.data)).scalar_one_or_none():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')

    def check_username(self, field):
        """Valideer dat gebruikersnaam nog niet in gebruik is.

        Args:
            field: Het username veld uit het formulier

        Raises:
            ValidationError: Als username al bestaat in database
        """
        if db.session.execute(select(User).filter_by(username=field.data)).scalar_one_or_none():
            raise ValidationError('Deze gebruikersnaam is al vergeven, kies een andere naam!')
