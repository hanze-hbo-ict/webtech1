"""
Auth Blueprint - Authentication views (Week 7b).

Deze blueprint bevat alle authentication routes:
- Login
- Register
- Logout
- Welcome (account overzicht)

Deze blueprint wordt geregistreerd met url_prefix='/auth'.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from webshop_app.models import db, Customer
from webshop_app.auth.forms import LoginForm, RegistrationForm

# Maak blueprint aan
auth_bp = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    """Handel het login-proces af.

    Route: /auth/login

    Returns:
        Bij GET: gerenderde login.html template met formulier
        Bij POST (success): redirect naar welkom of next pagina
        Bij POST (invalid): gerenderde login.html met foutmeldingen
    """
    # Al ingelogd? Redirect naar welcome
    if current_user.is_authenticated:
        return redirect(url_for('auth.welcome'))

    form = LoginForm()

    if form.validate_on_submit():
        # Zoek user op email
        user = db.session.execute(db.select(Customer).filter_by(email=form.email.data)).scalar_one_or_none()

        # Check wachtwoord
        if user is not None and user.check_password(form.password.data):
            # Log user in
            login_user(user)
            flash(f'Welkom terug, {user.name}!', 'success')

            # Redirect naar 'next' parameter of naar welcome
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('auth.welcome')

            return redirect(next_page)
        else:
            flash('Ongeldig e-mailadres of wachtwoord. Probeer het opnieuw.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    """Handel het registratieproces af voor nieuwe gebruikers.

    Route: /auth/register

    Returns:
        Bij GET: gerenderde register.html template met formulier
        Bij POST (success): redirect naar login view
        Bij POST (invalid): gerenderde register.html met foutmeldingen
    """
    # Al ingelogd? Redirect naar welcome
    if current_user.is_authenticated:
        return redirect(url_for('auth.welcome'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Maak nieuwe Customer aan (is_admin=False standaard)
        new_customer = Customer(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            is_admin=False
        )

        # Opslaan in database
        db.session.add(new_customer)
        db.session.commit()

        flash(f'Account aangemaakt voor {form.name.data}! Je kunt nu inloggen.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """Log de huidige gebruiker uit.

    Route: /auth/logout

    Deze view is alleen toegankelijk voor ingelogde gebruikers.
    Na het uitloggen wordt de gebruiker doorgestuurd naar de homepagina.

    Returns:
        Redirect naar de home view
    """
    logout_user()
    flash('Je bent succesvol uitgelogd.', 'info')
    return redirect(url_for('products.index'))


@auth_bp.route("/welcome")
@login_required
def welcome():
    """Toon de welkomstpagina voor ingelogde gebruikers.

    Route: /auth/welcome

    Deze view is alleen toegankelijk voor geauthenticeerde gebruikers
    dankzij de @login_required decorator.

    Returns:
        De gerenderde welcome.html template
    """
    return render_template('auth/welcome.html')
