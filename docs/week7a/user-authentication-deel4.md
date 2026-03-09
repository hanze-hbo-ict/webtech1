# User authentication - Flask_login deel IV

Het meeste werk is achter de rug. Alleen de HTML-bestanden uit de folder `templates` blijven nog over. Er zijn nog een aantal acties waar uitleg bij nodig is maar het merendeel zou geen problemen meer moeten opleveren.

## `base.html`

Dit bestand wordt altijd gebruikt om een aantal standaardwaarden in op te nemen die vervolgens doorgegeven kunnen worden aan de andere files uit de folder `templates`:

```html
<!DOCTYPE html>
<html>
  <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title></title>
  </head>
```

Dit gedeelte is bekend en in de code zijn de benodigde linken naar Bootstrap 5.3.0 opgenomen. Let op dat Bootstrap 5 geen jQuery meer nodig heeft en dat Popper.js nu ingebouwd zit in de bundle versie.

De body vereist een kleine uitleg:

```html hl_lines="7 9 12"
<body>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('home') }}">Home</a>
        </li>
        {% if current_user.is_authenticated %}
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('logout') }}">Uitloggen</a>
        </li>
        {% else %}
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('login') }}">Inloggen</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('register') }}">Registreren</a>
        </li>
        {% endif %}
      </ul>
    </div>
  </nav>

  <div class="container mt-4">
    {% block content %}
    {% endblock %}
  </div>
</body>
</html>
```

De inhoud van de navigatiebalk, het menu wat de gebruiker te zien krijgt, wordt bepaald door de voorwaarde `if current_user.is_authenticated`.

Is de gebruiker door de selectie gekomen dan heeft hij de mogelijkheid te kunnen uitloggen, en zo niet, dan kan een gebruiker zich laten registreren of inloggen.

In Bootstrap 5 is de navigatiebalk structuur verbeterd met de `navbar` en `navbar-nav` klassen. De oude `nav` klasse is vervangen door een meer semantisch correcte structuur met een `nav` element en nested `ul` lijst.

## `home.html`

```html
{% extends "base.html" %}
{% block content %}
<div class="card">
  <div class="card-body">
    {% if current_user.is_authenticated %}
      <h5 class="card-title">Welkom terug!</h5>
      <p class="card-text">Hallo {{ current_user.username }}!</p>
    {% else %}
      <h5 class="card-title">Welkom</h5>
      <p class="card-text">Om te kunnen beginnen: log in of registreer!</p>
    {% endif %}
  </div>
</div>
{% endblock %}
```

Als de homepagina wordt aangeroepen door een ingelogde gebruiker verschijnt de tekst 'Hallo' + de naam. Is de gebruiker niet ingelogd, dan verschijnt er een aansporing om in te loggen of te registreren.

In Bootstrap 5 is de `jumbotron` component verwijderd en vervangen door `card` componenten. Cards zijn flexibeler en bieden betere responsiviteit.

## `welkom.html`

```html
{% extends "base.html" %}
{% block content %}
<div class="card">
  <div class="card-body">
    <h5 class="card-title">Gefeliciteerd!</h5>
    <p class="card-text">Inloggen gelukt!</p>
  </div>
</div>
{% endblock %}
```

## `register.html`

```html
{% extends "base.html" %}
{% block content %}
<div class="card">
  <div class="card-header">
    <h5>Registreren</h5>
  </div>
  <div class="card-body">
    <form method="POST">
      {{ form.hidden_tag() }}
      <div class="mb-3">
        {{ form.email.label(class="form-label") }}
        {{ form.email(class="form-control") }}
      </div>
      <div class="mb-3">
        {{ form.username.label(class="form-label") }}
        {{ form.username(class="form-control") }}
      </div>
      <div class="mb-3">
        {{ form.password.label(class="form-label") }}
        {{ form.password(class="form-control") }}
      </div>
      <div class="mb-3">
        {{ form.pass_confirm.label(class="form-label") }}
        {{ form.pass_confirm(class="form-control") }}
      </div>
      {{ form.submit(class="btn btn-primary") }}
    </form>
  </div>
</div>
{% endblock %}
```

Wanneer de view `register` wordt opgeroepen, wordt het registratieformulier getoond. Ook wordt er gecontroleerd op een typo bij het invullen van het wachtwoord.

In Bootstrap 5 is de formulier styling aangepast. De klasse `form-group` is vervangen door `mb-3` (margin-bottom) en formulier labels gebruiken nu de `form-label` klasse.

## `login.html`

```html
{% extends "base.html" %}
{% block content %}
<div class="card">
  <div class="card-header">
    <h5>Inloggen</h5>
  </div>
  <div class="card-body">
    <form method="POST">
      {{ form.hidden_tag() }}
      <div class="mb-3">
        {{ form.email.label(class="form-label") }}
        {{ form.email(class="form-control") }}
      </div>
      <div class="mb-3">
        {{ form.password.label(class="form-label") }}
        {{ form.password(class="form-control") }}
      </div>
      {{ form.submit(class="btn btn-primary") }}
    </form>
  </div>
</div>
{% endblock %}
```

Ook hier is een formulier nodig om een gebruiker toestemming te verlenen de pagina's van de site te kunnen inspecteren.

## Testen

Tot zover alle code die nodig is om een inlogsysteem op te zetten. Nu komt weer het spannendste deel, het testen.

Na het runnen van `app.py`:

> **Verwacht resultaat:** Een kaart met een welkomstbericht en knoppen/links om in te loggen of te registreren.

Registreren ('<joyce@sessions.com>' en het wachtwoord 'geheim'):

> **Verwacht resultaat:** Een registratieformulier met velden voor e-mailadres, gebruikersnaam, wachtwoord en wachtwoordbevestiging.

Inloggen:

> **Verwacht resultaat:** Een inlogformulier met velden voor e-mailadres en wachtwoord.

Na inloggen:
> **Verwacht resultaat:** Een welkomstpagina met de melding "Gefeliciteerd! Inloggen gelukt!"

Een klik op Home:

> **Verwacht resultaat:** De homepagina toont een gepersonaliseerde begroeting met de gebruikersnaam en een optie om uit te loggen in de navigatiebalk.

Tot zover het testen. Er kunnen nog veel meer opties bekeken worden op hun gedrag, maar voor nu is dit even voldoende.

## Samenvatting

Je hebt nu een compleet user authentication systeem gebouwd met Flask-Login. De belangrijkste onderdelen die je hebt geleerd zijn:

### Beveiliging

- **Password hashing** met Werkzeug - wachtwoorden worden nooit in plain text opgeslagen
- **CSRF protection** via Flask-WTF - automatische beveiliging tegen cross-site request forgery
- **Session management** - Flask-Login beheert automatisch de ingelogde status

### Functionaliteit

- **Registratie** - nieuwe gebruikers kunnen zich aanmelden
- **Login** - gebruikers kunnen inloggen met email en wachtwoord
- **Logout** - veilig uitloggen met sessie cleanup
- **Protected routes** - pagina's die alleen toegankelijk zijn voor ingelogde gebruikers

### Flask-Login Features

- `UserMixin` - standaard implementatie van user methoden
- `@login_required` decorator - beveilig routes automatisch
- `current_user` - altijd beschikbaar in templates en views
- `user_loader` - automatisch laden van users uit database

Dit authentication systeem vormt de basis voor grotere applicaties waar gebruikers persoonlijke data hebben of verschillende toegangsniveaus nodig zijn (bijvoorbeeld admin vs reguliere gebruiker).

!!! tip "Volgende stappen"
    Met deze kennis kun je verder met:
    - **Role-based access control** - Admin vs normale gebruikers
    - **Password reset** - Gebruikers kunnen wachtwoord vergeten link gebruiken
    - **Email verificatie** - Bevestig email adressen bij registratie
    - **Two-factor authentication** - Extra beveiligingslaag toevoegen
    - **OAuth integration** - Login met Google, GitHub, etc.

Veel succes met het bouwen van je eigen beveiligde webapplicaties!
