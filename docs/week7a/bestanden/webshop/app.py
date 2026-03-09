"""
Webshop Flask Applicatie met SQLAlchemy ORM en Authentication (Week 7a).

Deze versie bouwt voort op Week 6 en voegt toe:
- Flask-Login voor user authentication
- Login/Register/Logout routes
- Admin vs Customer roles
- Protected admin routes met @login_required
- Welcome page voor ingelogde gebruikers
"""
import os
from flask import Flask, render_template, abort, redirect, url_for, flash, request, Response
from flask_login import login_user, login_required, logout_user, current_user
from functools import wraps
from models import db, login_manager, Category, Product, Customer, Order, OrderItem
from forms import AddProductForm, EditProductForm, ContactForm, LoginForm, RegistrationForm

# Bepaal database pad
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Flask configuratie
app.config['SECRET_KEY'] = 'webshop-secret-key-2025'

# SQLAlchemy configuratie
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'webshop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect naar login pagina als niet ingelogd
login_manager.login_message = "Log in om deze pagina te bekijken."


def admin_required(f):
    """Decorator om routes te beschermen voor alleen admins.

    Gebruik dit naast @login_required om te controleren of de ingelogde
    gebruiker admin rechten heeft.

    Args:
        f: De view functie om te beschermen

    Returns:
        Wrapped functie die admin rechten controleert
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Log in om deze pagina te bekijken.', 'warning')
            return redirect(url_for('login'))
        if not current_user.is_admin:
            flash('Deze pagina is alleen toegankelijk voor admins.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ===== AUTHENTICATION ROUTES =====

@app.route("/login", methods=['GET', 'POST'])
def login() -> str | Response:
    """Handel het login-proces af.

    Returns:
        Bij GET: gerenderde login.html template met formulier
        Bij POST (success): redirect naar welkom of next pagina
        Bij POST (invalid): gerenderde login.html met foutmeldingen
    """
    # Al ingelogde gebruikers redirecten
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))

    form = LoginForm()

    if form.validate_on_submit():
        # Zoek gebruiker op email
        user = db.session.execute(db.select(Customer).filter_by(email=form.email.data)).scalar_one_or_none()

        # Check of gebruiker bestaat en wachtwoord klopt
        if user is not None and user.check_password(form.password.data):
            # Log gebruiker in
            login_user(user)
            flash(f'Welkom terug, {user.name}!', 'success')

            # Redirect naar 'next' parameter of naar welcome
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('welcome')

            return redirect(next_page)
        else:
            flash('Ongeldig e-mailadres of wachtwoord. Probeer het opnieuw.', 'danger')

    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register() -> str | Response:
    """Handel het registratieproces af voor nieuwe gebruikers.

    Returns:
        Bij GET: gerenderde register.html template met formulier
        Bij POST (success): redirect naar login view
        Bij POST (invalid): gerenderde register.html met foutmeldingen
    """
    # Al ingelogde gebruikers redirecten
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Maak nieuwe Customer aan (is_admin=False standaard)
        new_customer = Customer(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            is_admin=False  # Nieuwe gebruikers zijn geen admin
        )

        # Opslaan in database
        db.session.add(new_customer)
        db.session.commit()

        flash(f'Account aangemaakt voor {form.name.data}! Je kunt nu inloggen.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout() -> Response:
    """Log de huidige gebruiker uit.

    Deze view is alleen toegankelijk voor ingelogde gebruikers.
    Na het uitloggen wordt de gebruiker doorgestuurd naar de homepagina.

    Returns:
        Redirect naar de home view
    """
    logout_user()
    flash('Je bent succesvol uitgelogd.', 'info')
    return redirect(url_for('index'))


@app.route("/welcome")
@login_required
def welcome() -> str:
    """Toon de welkomstpagina voor ingelogde gebruikers.

    Deze view is alleen toegankelijk voor geauthenticeerde gebruikers
    dankzij de @login_required decorator.

    Returns:
        De gerenderde welcome.html template
    """
    return render_template('welcome.html')


# ===== PUBLIC ROUTES (Catalog) =====

@app.route("/")
def index() -> str:
    """Homepage met overzicht van alle categorieën.

    Returns:
        Rendered HTML template
    """
    # ORM Query: SELECT * FROM categories
    categories = db.session.execute(db.select(Category)).scalars().all()
    return render_template("index.html", categories=categories)


@app.route("/category/<int:category_id>")
def category(category_id: int) -> str:
    """Categorie overzicht met alle producten.

    Args:
        category_id: ID van de categorie

    Returns:
        Rendered HTML template

    Raises:
        404: Als categorie niet bestaat
    """
    # ORM Query: SELECT * FROM categories WHERE id = ?
    category_info = db.get_or_404(Category, category_id)

    # ORM Query: SELECT * FROM products WHERE category_id = ?
    products = db.session.execute(db.select(Product).filter_by(category_id=category_id)).scalars().all()

    return render_template(
        "category.html",
        category=category_info,
        products=products
    )


@app.route("/product/<int:product_id>")
def product(product_id: int) -> str:
    """Product detail pagina.

    Args:
        product_id: ID van het product

    Returns:
        Rendered HTML template

    Raises:
        404: Als product niet bestaat
    """
    # ORM Query: SELECT * FROM products WHERE id = ?
    product_info = db.get_or_404(Product, product_id)

    return render_template("product.html", product=product_info)


# ===== ADMIN ROUTES (Protected) =====

@app.route("/admin/products")
@admin_required
def admin_products() -> str:
    """Admin overzicht van alle producten.

    Alleen toegankelijk voor admins.

    Returns:
        Rendered HTML template met product lijst
    """
    # ORM Query: SELECT * FROM products JOIN categories
    products = db.session.execute(db.select(Product).join(Category)).scalars().all()
    return render_template("admin_products.html", products=products)


@app.route("/admin/product/add", methods=['GET', 'POST'])
@admin_required
def admin_add_product() -> str | Response:
    """Admin formulier om een nieuw product toe te voegen.

    Alleen toegankelijk voor admins.

    Returns:
        Rendered HTML template of redirect

    Methods:
        GET: Toon formulier
        POST: Verwerk formulier en voeg product toe
    """
    form = AddProductForm()

    # Populate category choices
    form.category_id.choices = [(c.id, c.name) for c in db.session.execute(db.select(Category)).scalars().all()]

    if form.validate_on_submit():
        # Create new product instance
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data,
            description=form.description.data
        )

        # Save to database
        db.session.add(new_product)
        db.session.commit()

        flash(f'Product "{new_product.name}" succesvol toegevoegd!', 'success')
        return redirect(url_for('product', product_id=new_product.id))

    return render_template("add_product.html", form=form)


@app.route("/admin/product/edit/<int:product_id>", methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id: int) -> str | Response:
    """Admin formulier om een bestaand product te bewerken.

    Alleen toegankelijk voor admins.

    Args:
        product_id: ID van het product om te bewerken

    Returns:
        Rendered HTML template of redirect

    Methods:
        GET: Toon formulier met huidige product data
        POST: Verwerk formulier en update product

    Raises:
        404: Als product niet bestaat
    """
    # Get product or 404
    product_info = db.get_or_404(Product, product_id)

    form = EditProductForm()

    # Populate category choices
    form.category_id.choices = [(c.id, c.name) for c in db.session.execute(db.select(Category)).scalars().all()]

    if form.validate_on_submit():
        # Update product attributes
        product_info.name = form.name.data
        product_info.price = form.price.data
        product_info.stock = form.stock.data
        product_info.category_id = form.category_id.data
        product_info.description = form.description.data

        # Save changes
        db.session.commit()

        flash(f'Product "{product_info.name}" succesvol gewijzigd!', 'success')
        return redirect(url_for('product', product_id=product_id))

    # Pre-fill form met huidige product data (bij GET request)
    elif not form.is_submitted():
        form.name.data = product_info.name
        form.price.data = product_info.price
        form.stock.data = product_info.stock
        form.description.data = product_info.description
        form.category_id.data = product_info.category_id

    return render_template(
        "edit_product.html",
        form=form,
        product=product_info
    )


@app.route("/admin/product/delete/<int:product_id>", methods=['POST'])
@admin_required
def admin_delete_product(product_id: int) -> Response:
    """Admin route om een product te verwijderen.

    Alleen toegankelijk voor admins.

    Args:
        product_id: ID van het product om te verwijderen

    Returns:
        Redirect naar admin products overzicht

    Methods:
        POST: Verwijder product (alleen via POST voor veiligheid)

    Raises:
        404: Als product niet bestaat
    """
    # Get product or 404
    product_info = db.get_or_404(Product, product_id)

    product_name = product_info.name

    # Delete product
    db.session.delete(product_info)
    db.session.commit()

    flash(f'Product "{product_name}" succesvol verwijderd.', 'success')
    return redirect(url_for('admin_products'))


# ===== OTHER ROUTES =====

@app.route("/contact", methods=['GET', 'POST'])
def contact() -> str | Response:
    """Contact formulier voor klanten.

    Returns:
        Rendered HTML template

    Methods:
        GET: Toon formulier
        POST: Verwerk formulier (toon bevestiging)
    """
    form = ContactForm()

    if form.validate_on_submit():
        flash(
            f'Bedankt voor je bericht, {form.name.data}! '
            f'We nemen zo snel mogelijk contact met je op.',
            'success'
        )
        return redirect(url_for('index'))

    return render_template("contact.html", form=form)


@app.errorhandler(404)
def page_not_found(error) -> tuple[str, int]:
    """Custom 404 error handler.

    Args:
        error: Error object

    Returns:
        Tuple van (HTML, status_code)
    """
    return render_template("404.html"), 404


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
