# OOP Python – Oefening 2

Maak binnen de file `product.py` een nieuwe klasse aan, `DigitaalProduct`, die een subklasse is van `Product`.

Digitale producten hebben geen verzendkosten maar wel een bestandsgrootte. Geef digitale producten een standaard voorraad van 999 (want ze zijn bijna onbeperkt beschikbaar) en voeg een attribuut `_bestandsgrootte` toe (in MB).

Test de klasse door een tweetal instanties aan te maken en hun details te tonen. Goede voorbeelden zijn software zoals "Photoshop" en "Microsoft Office".

Test verder of de methode `verkoop()` naar behoren werkt. Dat is ook nog niet getest voor de objecten uit de klasse `FysiekProduct`. Is hier een mooie gelegenheid voor. Mocht blijken dat de test nog een probleem laat zien, graag een oplossing ervoor.

Ook kunnen fysieke producten weer onderverdeeld worden. De bekendste groepen zijn *Boek* en *Elektronica*. Alleen de klasse `Boek` wordt hier aangemaakt als voorbeeld. Een boek heeft een naam, prijs en voorraad nodig, plus een aantal extra eigenschappen zoals auteur en ISBN. Boeken krijgen standaard 0.5 kg als gewicht.

```python
class Boek(FysiekProduct):

    def __init__(self, naam, prijs, voorraad, auteur, isbn):
        super().__init__(naam, prijs, voorraad, gewicht=0.5)
        self._auteur = auteur
        self._isbn = isbn

    def __str__(self):
        basis = super().__str__()
        return f"{basis}, Auteur: {self._auteur}, ISBN: {self._isbn}"
```

Een bekend boek is 'Python Crash Course' van Eric Matthes. Dat wordt het object uit deze klasse dat aangemaakt wordt.

```python
from product import Product, FysiekProduct, DigitaalProduct, Boek

python_boek = Boek("Python Crash Course", 34.95, 8, "Eric Matthes", "978-1593279288")
print(python_boek)
python_boek.verkoop(3)
print(python_boek)
```

Maak nu de klasse `Software` aan (als subklasse van `DigitaalProduct`) met zelfgekozen eigenschappen zoals versienummer en besturingssysteem, en test deze door een instantie aan te maken en deze verschillende hoeveelheden verkopen toe te passen.

**Extra uitdaging:** Voeg een methode `download()` toe aan de klasse `DigitaalProduct` die een downloadlink genereert en de voorraad automatisch met 1 vermindert. Bij fysieke producten zou dit een error moeten geven.
