import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
######################################
#### SET UP OUR SQLite DATABASE #####
####################################

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# verbind de Flask App met de Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# De eerste tabel (model)!
# Overerven van de klasse db.Model
class Cursist(db.Model):

    # Deze regel is optioneel; wordt deze weggelaten dan krijgt de tabel de naam van de klasse
    __tablename__ = 'cursisten'

    #########################################
    ## Het vastleggen van de structuur   ####
    #########################################

    # Primary Key column, uniek voor iedere cursist
    id = db.Column(db.Integer,primary_key=True)
    # Naam van de cursist, als tekst
    naam = db.Column(db.Text)
    # Leeftijd van de cursist, als getal
    leeftijd = db.Column(db.Integer)

    # Hier wordt aangegeven wat iedere instantie meekrijgt aan het begin
    # Merk op dat de ID later automatisch voor ons wordt aangemaakt, dus we voegen deze hier niet toe!
    def __init__(self,naam,leeftijd):
        self.naam = naam
        self.leeftijd = leeftijd

    def __repr__(self):
        # Deze tekst wordt getoond als een cursist wordt aangeroepen
        return f"Cursist {self.naam} is {self.leeftijd} jaar oud"
