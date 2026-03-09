import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Maak een object LoginManager() aan
login_manager = LoginManager()

app = Flask(__name__)

# Vaak worden deze coderegels in een apart config.py-bestand ondergebracht
app.config['SECRET_KEY'] = 'mijngeheimesleutel'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

# De app wordt bekend gemaakt bij de Loginmanager
login_manager.init_app(app)

# Hier wordt duidelijk gemaakt welke view verantwoordelijk is voor het inloggen
login_manager.login_view = "login"
