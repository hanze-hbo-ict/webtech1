"""
Webshop Application Entry Point (Week 7b).

Dit is het entry point voor de webshop applicatie.
We gebruiken de Application Factory pattern uit webshop_app/__init__.py.

Run de applicatie met:
    python app.py
"""
from webshop_app import create_app, db
from webshop_app.models import Customer, Category

# Maak app instance met factory
app = create_app()

if __name__ == "__main__":
    # Create tables and demo admin if they don't exist
    with app.app_context():
        db.create_all()

        # Check if admin exists, anders maak demo admin aan
        admin = db.session.execute(db.select(Customer).filter_by(email='admin@webshop.nl')).scalar_one_or_none()
        if not admin:
            admin = Customer(
                name='Admin',
                email='admin@webshop.nl',
                password='admin123',  # Voor demo! In productie betere wachtwoorden gebruiken
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Demo admin account aangemaakt:")
            print("   Email: admin@webshop.nl")
            print("   Wachtwoord: admin123")

    app.run(debug=True)
