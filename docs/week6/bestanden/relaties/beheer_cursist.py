import os
from forms import VoegtoeForm, VerwijderForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Sleutel opgeven voor het gebruik van Forms
app.config['SECRET_KEY'] = 'mysecretkey'

# DATABASE en MODELS

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


class Cursist(db.Model):
    __tablename__ = 'cursisten'
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.Text)

    def __init__(self, naam):
        self.naam = naam

    def __repr__(self):
        return f"Naam van de cursist: {self.naam}"


# VIEWS met FORMS

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/add', methods=['GET', 'POST'])
def add_cur():
    form = VoegtoeForm()

    if form.validate_on_submit():
        naam = form.naam.data

        # Add new Puppy to database
        new_cur = Cursist(naam)
        db.session.add(new_cur)
        db.session.commit()

        return redirect(url_for('list_cur'))

    return render_template('voegtoe_cur.html', form=form)


@app.route('/list')
def list_cur():
    # Selecteer alle cursisten uit de database met een query.
    cursisten = Cursist.query.all()
    return render_template('toon_cur.html', cursisten=cursisten)


@app.route('/delete', methods=['GET', 'POST'])
def del_cur():
    form = VerwijderForm()

    if form.validate_on_submit():
        id = form.id.data
        cur = Cursist.query.get(id)
        db.session.delete(cur)
        db.session.commit()

        return redirect(url_for('list_cur'))
    return render_template('verwijder_cur.html', form=form)


db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
