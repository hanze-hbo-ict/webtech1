import os
from forms import VoegtoeForm, VerwijderForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import Mapped, mapped_column

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
    """Model voor cursisten van de muziekschool."""

    __tablename__ = 'cursisten'

    id: Mapped[int] = mapped_column(primary_key=True)
    naam: Mapped[str | None]

    def __init__(self, naam: str):
        """Maak nieuwe cursist aan.

        Args:
            naam: Voor- en achternaam
        """
        self.naam = naam

    def __repr__(self) -> str:
        """String representatie."""
        return f"Naam van de cursist: {self.naam}"


# VIEWS met FORMS

@app.route('/')
def index() -> str:
    """Homepage route.

    Returns:
        Gerenderde home template
    """
    return render_template('home.html')


@app.route('/add', methods=['GET', 'POST'])
def add_cur() -> str:
    """Voeg nieuwe cursist toe.

    Returns:
        Bij GET: formulier template
        Bij POST: redirect naar cursisten lijst
    """
    form = VoegtoeForm()

    if form.validate_on_submit():
        naam = form.naam.data

        # Voeg nieuwe cursist toe aan database
        new_cur = Cursist(naam)
        db.session.add(new_cur)
        db.session.commit()

        return redirect(url_for('list_cur'))

    return render_template('voegtoe_cur.html', form=form)


@app.route('/list')
def list_cur() -> str:
    """Toon alle cursisten.

    Returns:
        Template met lijst van cursisten
    """
    # Selecteer alle cursisten uit de database met een query
    cursisten = db.session.execute(db.select(Cursist)).scalars().all()
    return render_template('toon_cur.html', cursisten=cursisten)


@app.route('/delete', methods=['GET', 'POST'])
def del_cur() -> str:
    """Verwijder cursist op basis van ID.

    Returns:
        Bij GET: formulier template
        Bij POST: redirect naar cursisten lijst
    """
    form = VerwijderForm()

    if form.validate_on_submit():
        id = form.id.data
        cur = db.session.get(Cursist, id)
        db.session.delete(cur)
        db.session.commit()

        return redirect(url_for('list_cur'))
    return render_template('verwijder_cur.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
