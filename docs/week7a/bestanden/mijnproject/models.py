from mijnproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


@login_manager.user_loader
def load_user(user_id: int):
    """Laad gebruiker op basis van ID.

    Deze functie wordt gebruikt door Flask-Login om de huidige gebruiker
    te laden en zijn/haar ID op te halen uit de sessie.

    Args:
        user_id: Het ID van de gebruiker

    Returns:
        User object of None als niet gevonden
    """
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    """Model voor gebruikers met authenticatie."""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(128))

    def __init__(self, email: str, username: str, password: str):
        """Maak nieuwe gebruiker aan.

        Args:
            email: Email adres (moet uniek zijn)
            username: Gebruikersnaam (moet uniek zijn)
            password: Wachtwoord in plain text (wordt gehashed opgeslagen)
        """
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Controleer of wachtwoord klopt.

        Args:
            password: Het te controleren wachtwoord

        Returns:
            True als wachtwoord correct is, anders False
        """
        return check_password_hash(self.password_hash, password)
