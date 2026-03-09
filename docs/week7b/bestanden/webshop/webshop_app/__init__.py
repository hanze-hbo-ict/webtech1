"""
Webshop Application Factory (Week 7b).

Deze module implementeert het Application Factory pattern voor Flask.
In plaats van een globale app instantie maken we de app in een functie.

Voordelen:
- Makkelijker testen (kan meerdere app instances maken)
- Config kan per instantie verschillen (test vs productie)
- Blueprints kunnen geregistreerd worden in factory
- Betere code organisatie en schaalbaarheid
"""
import os
from flask import Flask, render_template

# Import extensions from models (voorkomt duplicate instances!)
from webshop_app.models import db, login_manager


def create_app(config_name='default'):
    """Application Factory voor de webshop.

    Deze functie maakt en configureert een Flask applicatie instance.

    Args:
        config_name: Configuratie naam ('default', 'testing', 'production')

    Returns:
        Geconfigureerde Flask app instance
    """
    # Bepaal basedir voor database pad
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # Maak Flask app aan
    app = Flask(__name__)

    # Flask configuratie
    app.config['SECRET_KEY'] = 'webshop-secret-key-2025'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'webshop.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions met app
    db.init_app(app)
    login_manager.init_app(app)

    # Login manager configuratie
    login_manager.login_view = "auth.login"  # LET OP: blueprint.view syntax!
    login_manager.login_message = "Log in om deze pagina te bekijken."

    # user_loader is al gedefinieerd in models.py!
    # Geen duplicate user_loader hier

    # Registreer Blueprints
    from webshop_app.products.views import products_bp
    from webshop_app.auth.views import auth_bp
    from webshop_app.admin.views import admin_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        """Custom 404 error handler."""
        return render_template("404.html"), 404

    # Custom context processor (optioneel)
    @app.context_processor
    def inject_app_name():
        """Maak app_name beschikbaar in alle templates."""
        return dict(app_name="Webshop")

    return app
