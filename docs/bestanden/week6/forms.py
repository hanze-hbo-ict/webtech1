from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class VoegtoeForm(FlaskForm):

    naam = StringField('Vul de naam van de nieuwe cursist in:')
    submit = SubmitField('Voeg toe')


class VerwijderForm(FlaskForm):

    id = IntegerField('Vul het ID van de cursist in en klik op Verwijder:')
    submit = SubmitField('Verwijder')
