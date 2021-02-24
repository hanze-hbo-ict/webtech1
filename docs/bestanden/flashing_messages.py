from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mijngeheimesleutel'


class SimpelForm(FlaskForm):
    submit = SubmitField('Klik mij!')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SimpelForm()

    if form.validate_on_submit():
        flash("Je hebt zojuist de button geactiveerd!")

        return redirect(url_for('index'))
    return render_template('home2.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
