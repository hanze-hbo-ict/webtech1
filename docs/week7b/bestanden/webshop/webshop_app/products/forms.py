"""
Products Blueprint Forms (Week 7b).

Bevat formulieren voor de products blueprint.
Momenteel alleen ContactForm, product forms zitten in admin blueprint.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


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
