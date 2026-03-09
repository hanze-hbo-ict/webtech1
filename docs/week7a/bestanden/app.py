from mijnproject import app, db
from flask import render_template, redirect, request, url_for, flash, Response
from flask_login import login_user, login_required, logout_user
from mijnproject.models import User
from mijnproject.forms import LoginForm, RegistrationForm


@app.route('/')
def home() -> str:
    """Homepage route.

    Returns:
        Gerenderde home template
    """
    return render_template('home.html')


@app.route('/welkom')
@login_required
def welkom() -> str:
    """Welkom pagina voor ingelogde gebruikers.

    Returns:
        Gerenderde welkom template
    """
    return render_template('welkom.html')


@app.route('/logout')
@login_required
def logout() -> Response:
    """Log gebruiker uit.

    Returns:
        Redirect naar home pagina
    """
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    """Login route voor gebruikers.

    Bij GET: toon login formulier
    Bij POST: valideer credentials en log in

    Returns:
        Bij GET: gerenderde login template
        Bij POST: redirect naar welkom of next pagina
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar_one_or_none()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Succesvol ingelogd.')

            # Als gebruiker een beveiligde pagina probeerde te bezoeken,
            # wordt die URL opgeslagen in 'next'
            next_page = request.args.get('next')

            # Controleer of next bestaat en veilig is (begint met /)
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('welkom')

            return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register() -> str | Response:
    """Registratie route voor nieuwe gebruikers.

    Bij GET: toon registratie formulier
    Bij POST: valideer gegevens en maak nieuwe gebruiker aan

    Returns:
        Bij GET: gerenderde register template
        Bij POST: redirect naar login pagina
    """
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )

        db.session.add(user)
        db.session.commit()
        flash('Dank voor de registratie. Er kan nu ingelogd worden!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    # Maak database tabellen aan indien nodig
    with app.app_context():
        db.create_all()

    app.run(debug=True)
