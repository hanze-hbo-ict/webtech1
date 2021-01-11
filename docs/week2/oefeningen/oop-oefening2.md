# OOP Python – Oefening 2

Maak binnen de file `aardman.py` een nieuwe klasse aan, `Uruk_Hai`, die een subklasse is van `Aardman`. 

Uruk-Hai’s hebben drie (3) levens en 12 hit points.

Test de klasse door een tweetal instanties aan te maken en hun details te tonen. Bekende Uruk_Hai namen zijn Lurtz en Ugluk.

Test verder of de methode `schade()` naar behoren werkt. Dat is ook nog niet getest voor de objecten uit de klasse `Ork`. Is hier een mooie gelegenheid voor. Mocht blijken dat de test nog een probleem laat zien, graag een oplossing ervoor.

Ook kunnen Orks weer onderverdeeld worden. De bekendste groepen zijn *Mordor* en *Saruman*. Alleen de klasse `Mordor` wordt hier aangemaakt als voorbeeld. Een ork van het type Mordor dient een naam te hebben en krijgt 140 hit points om mee te beginnen. Als een ork van Mordor vier (4) keer geraakt wordt kost het één (1) punt.

```python
class Mordor(Ork):

    def __init__(self, name):
        super().__init__(name)
        self._hit_points = 140

    def schade(self, geraakt):
        super().schade(geraakt // 4)    
```

Een ork uit de Mordor-groep is ‘Gothmog’. Dat wordt het object uit deze klasse dat aangemaakt wordt.

```python
from aardman import Aardman, Ork, Uruk_Hai, Mordor

gothmog = Mordor("Gothmog")
print(gothmog)
gothmog.schade(12)
print(gothmog)
```


