import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

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
    """Model voor cursisten van de muziekschool."""

    __tablename__ = 'cursisten'

    id: Mapped[int] = mapped_column(primary_key=True)
    naam: Mapped[str | None]

    # Dit is een een-op-veel relatie
    # Een cursist kan meerdere instrumenten bespelen
    instrumenten: Mapped[list['Instrument']] = relationship(back_populates='cursist')
    # Dit is een een-op-een relatie
    # Hier geldt dat iedere cursist maar één docent heeft.
    # Voor dit voorbeeld geldt ook dat elke docent maar les geeft aan één cursist.
    docent: Mapped['Docent | None'] = relationship(back_populates='cursist')

    def __init__(self, naam: str):
        """Maak nieuwe cursist aan.

        Args:
            naam: Voor- en achternaam
        """
        # Het is verplicht voor een cursist een naam op te geven bij de initialisatie!
        self.naam = naam

    def __repr__(self) -> str:
        """String representatie."""
        if self.docent:
            return f"Cursist {self.naam} heeft {self.docent.naam} als docent"
        else:
            return f"Cursist {self.naam} heeft nog geen docent toegewezen gekregen"

    def overzicht_instrumenten(self) -> list[str]:
        """Geef lijst van instrumentnamen terug.

        Returns:
            Lijst met namen van instrumenten
        """
        return [instr.naam for instr in self.instrumenten]


class Instrument(db.Model):
    """Model voor instrumenten waarin de school lesgeeft."""

    __tablename__ = 'instrumenten'

    id: Mapped[int] = mapped_column(primary_key=True)
    naam: Mapped[str | None]
    # Dit is de relatie tussen instrument en cursist.
    # Er staat cursisten.id omdat de __tablename__='cursisten' hier gebruikt wordt!
    cursist_id: Mapped[int | None] = mapped_column(ForeignKey('cursisten.id'))
    cursist: Mapped['Cursist | None'] = relationship(back_populates='instrumenten')

    def __init__(self, naam: str, cursist_id: int):
        """Maak nieuw instrument aan.

        Args:
            naam: Naam van het instrument
            cursist_id: ID van de cursist die dit instrument bespeelt
        """
        self.naam = naam
        self.cursist_id = cursist_id


class Docent(db.Model):
    """Model voor docenten die lesgeven aan cursisten."""

    __tablename__ = 'docenten'

    id: Mapped[int] = mapped_column(primary_key=True)
    naam: Mapped[str | None]
    # Ook hier weer __tablename__='cursisten'
    cursist_id: Mapped[int | None] = mapped_column(ForeignKey('cursisten.id'))
    cursist: Mapped['Cursist | None'] = relationship(back_populates='docent')

    def __init__(self, naam: str, cursist_id: int):
        """Maak nieuwe docent aan.

        Args:
            naam: Voor- en achternaam
            cursist_id: ID van de cursist die deze docent begeleidt
        """
        self.naam = naam
        self.cursist_id = cursist_id
