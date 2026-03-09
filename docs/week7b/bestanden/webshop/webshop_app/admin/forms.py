"""
Admin Blueprint Forms (Week 7b).

Bevat formulieren voor product management in admin panel.
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
