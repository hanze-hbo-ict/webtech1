from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mijngeheimesleutel'


class InfoForm(FlaskForm):

    instrument = StringField('Welk instrument wil je graag leren bespelen?')
    submit = SubmitField('Verzend')


@app.route('/', methods=['GET', 'POST'])
def index():

    instrument = False
    # Maak een object van de klasse InfoForm aan.
    form = InfoForm()
    # Als het formulier valide is
    if form.validate_on_submit():
        # Haal de data voor het instrument op uit het formulier.
        instrument = form.instrument.data
        # Zet de waarde voor instrument weer op False
        form.instrument.data = ''
    return render_template('home.html', form=form, instrument=instrument)


if __name__ == '__main__':
    app.run(debug=True)
