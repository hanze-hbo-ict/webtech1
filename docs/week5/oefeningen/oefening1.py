from flask import Flask, render_template, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField)
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mijngeheimesleutel'


class InfoForm(FlaskForm):
    voornaam = StringField('Wat is je voornaam?', validators=[DataRequired()])
    achternaam = StringField('Wat is je achternaam?', validators=[DataRequired()])
    submit = SubmitField('Verstuur')


@app.route('/', methods=['GET', 'POST'])
def index():
    # Maak een object van de klasse InfoForm aan.
    # Als het formulier valide is
        # Haal de gegevens op uit het formulier.

    return render_template('home3.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
