from flask import Flask, render_template, redirect, url_for, session, flash

# Zorg ook voor de juiste imports

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mijngeheimesleutel'


class InfoForm(FlaskForm):
    pass
    # Zorg hier voor een input-veld waarin de voor- en achternaam 
    # ingevuld kunnen worden.


@app.route('/', methods=['GET', 'POST'])
def index():
    # Maak een object van de klasse InfoForm aan.
    # Als het formulier valide is
        # Haal de gegevens op uit het formulier.

    return render_template('home3.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
