"""
Flask-WTF formulieren voor de webshop.

Dit bestand bevat alle formulier definities voor de webshop applicatie.
We gebruiken Flask-WTF voor automatische CSRF-beveiliging en WTForms validators.
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    FloatField,
    IntegerField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, NumberRange, Length, Optional


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
