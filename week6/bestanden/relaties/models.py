import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Het opzetten van de database

# Geef de basis-directory op
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Koppel de Flask App met de database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


class Cursist(db.Model):
    __tablename__ = 'cursisten'

    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.Text)
    # Dit is een een-op-veel relatie
    # Een cursist kan meerdere instrumenten bespelen
    instrumenten = db.relationship('Instrument', backref='cursist', lazy='dynamic')
    # Dit is een een-op-een relatie
    # Hier geldt dat iedere cursist maar één docent heeft.
    # De waarde van uselist is daarom False.
    # Voor dit voorbeeld geldt ook dat elke docent maar les geeft aan één cursist.
    docent = db.relationship('Docent', backref='cursist', uselist=False)

    def __init__(self, naam):
        # Het is verplicht voor een cursist een naam op te geven bij de initialisatie!
        self.naam = naam

    def __repr__(self):
        if self.docent:
            return f"Cursist {self.naam} heeft {self.docent.naam} als docent"
        else:
            return f"Cursist {self.naam} heeft nog geen docent toegewezen gekregen"

    def overzicht_instrumenten(self):
        print("Mijn instrumenten:")
        for instr in self.instrumenten:
            print(instr.naam)


class Instrument(db.Model):
    __tablename__ = 'instrumenten'

    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.Text)
    # Dit is de relatie tussen instrument en cursist.
    # Er staat cursisten.id omdat de __tablename__='cursisten' hier gebruikt wordt!
    cursist_id = db.Column(db.Integer, db.ForeignKey('cursisten.id'))

    def __init__(self, naam, cursist_id):
        self.naam = naam
        self.cursist_id = cursist_id


class Docent(db.Model):
    __tablename__ = 'docenten'

    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.Text)
    # Ook hier weer __tablename__='cursisten'
    cursist_id = db.Column(db.Integer, db.ForeignKey('cursisten.id'))

    def __init__(self, naam, cursist_id):
        self.naam = naam
        self.cursist_id = cursist_id
