# Flask – Project Setup met uv

**uv** is een Python package en project manager waarmee je packages installeert en je projectomgeving beheert.

## uv installeren

=== "macOS"
    Via Homebrew:
    ```console
    brew install uv
    ```
    Of via de standalone installer:
    ```console
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
=== "Linux"
    ```console
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
=== "Windows"
    ```console
    winget install -e --id astral-sh.uv
    ```
    Of via PowerShell:
    ```console
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

Zie [uv documentatie](https://docs.astral.sh/uv/getting-started/installation/) voor meer opties.

Controleer of uv correct is geïnstalleerd:

```console
uv --version
```

Je zou een versienummer moeten zien (bijv. `uv 0.4.30`).

## Flask project aanmaken

### Stap 1: Project directory maken

Maak een nieuwe directory voor je Flask project:

```console
mkdir mijn-flask-app
cd mijn-flask-app
```

### Stap 2: Python project initialiseren

Initialiseer een nieuw Python project met uv:

```console
uv init
```

Dit maakt automatisch:

- `pyproject.toml` - Project configuratie en dependencies
- `.python-version` - Python versie voor dit project
- `main.py` - Een voorbeeld bestand (kun je verwijderen)

### Stap 3: Flask installeren

Installeer Flask met uv:

```console
uv add flask
```

Dit doet automatisch:

- Installeert Flask
- Maakt een virtual environment (`.venv/`)
- Update `pyproject.toml` met Flask dependency
- Maakt `uv.lock` voor reproduceerbare builds

Je `pyproject.toml` ziet er nu ongeveer zo uit:

```toml
[project]
name = "mijn-flask-app"
version = "0.1.0"
description = "Een Flask webapplicatie"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "flask>=3.1.0",
]
```

!!! info "Virtual environment"
    uv maakt automatisch een virtual environment in `.venv/`. Deze wordt automatisch gebruikt wanneer je `uv run` gebruikt - je hoeft niets te activeren!

## Je eerste Flask app

### Stap 4: Maak app.py

Verwijder het voorbeeld bestand en maak een nieuwe `app.py`:

```console
rm main.py
```

Maak `app.py` met deze inhoud:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index() -> str:
    """Homepage route."""
    return "<h1>Welkom bij mijn Flask app!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
```

### Stap 5: Flask app runnen

Run je app met uv:

```console
uv run python app.py
```

Of korter (uv zoekt automatisch naar Python bestanden):

```console
uv run app.py
```

Je ziet output zoals:

```console
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

Open je browser en ga naar [http://127.0.0.1:5000](http://127.0.0.1:5000) - je ziet je eerste Flask pagina!

!!! tip "Flask development server"
    Met `debug=True` herstart de server automatisch bij code wijzigingen. Perfect voor development!

## Project structuur

Je project ziet er nu zo uit:

```text
mijn-flask-app/
├── .python-version      # Python versie (bijv. 3.12)
├── .venv/               # Virtual environment (automatisch)
├── pyproject.toml       # Project configuratie
├── uv.lock              # Dependency lock file
└── app.py               # Je Flask applicatie
```

## Werken met uv commands

### Dependencies toevoegen

Voeg packages toe met `uv add`:

```console
# Voeg requests toe
uv add requests

# Voeg development dependencies toe (bijv. pytest)
uv add --dev pytest
```

### Dependencies verwijderen

```console
uv remove requests
```

### Python commando's runnen

Gebruik `uv run` voor alle Python commando's:

```console
# Run Python bestand
uv run app.py

# Run Python module
uv run -m flask --version

# Open Python REPL
uv run python
```

### Dependencies installeren (nieuwe machine)

Als je het project op een nieuwe machine kloont:

```console
git clone <repo>
cd mijn-flask-app
uv sync
```

Dit installeert automatisch alle dependencies uit `uv.lock`.

## Flask development mode

Voor development is het handig om Flask in development mode te runnen met de Flask CLI:

```console
uv run flask --app app run --debug
```

Of korter, maak een `run.sh` (macOS/Linux) of `run.bat` (Windows):

**run.sh:**

```bash
#!/bin/bash
uv run flask --app app run --debug
```

**run.bat:**

```batch
@echo off
uv run flask --app app run --debug
```

Maak executable (macOS/Linux):

```console
chmod +x run.sh
./run.sh
```

## Veelvoorkomende workflows

### Development workflow

```console
# 1. Project maken
mkdir mijn-app && cd mijn-app
uv init

# 2. Dependencies toevoegen
uv add flask

# 3. Code schrijven (app.py)

# 4. Runnen
uv run app.py

# 5. Nieuwe package nodig?
uv add requests

# 6. Tests runnen (later)
uv add --dev pytest
uv run pytest
```

### Project delen (Git)

In je `.gitignore`:

```text
.venv/
__pycache__/
*.pyc
.DS_Store
```

Commit deze bestanden WEL:

```text
pyproject.toml
uv.lock
.python-version
```

Anderen kunnen dan je project gebruiken met:

```console
git clone <repo>
cd <repo>
uv sync
uv run app.py
```

## Troubleshooting

### "uv: command not found"

Volg de installatie-instructies bovenaan deze pagina voor jouw besturingssysteem.

### "Python version mismatch"

Check je Python versie:

```console
python --version
uv python list
```

Installeer een specifieke Python versie met uv:

```console
uv python install 3.12
```

### "Package conflict"

Sync dependencies opnieuw:

```console
uv sync --refresh
```

### Virtual environment handmatig activeren (soms nodig voor editors)

```console
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.\.venv\Scripts\activate.bat
```

Deactiveren:

```console
deactivate
```

Maar normaal gesproken gebruik je gewoon `uv run` en hoef je niets te activeren!

## Samenvatting

Je hebt geleerd:

- **uv installeren** via Homebrew (macOS) of de standalone installer voor jouw platform
- **Flask project maken** met `uv init` en `uv add flask`
- **Flask app runnen** met `uv run app.py`
- **Project structuur** met `pyproject.toml` en `uv.lock`
- **Development workflow** zonder handmatige virtual environment activatie

**Volgende stap:** [Deel 3](flask-deel3.md) - Routes en dynamische URLs.
