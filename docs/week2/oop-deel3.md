# OOP Python - Meerdere klassen

Het is belangrijk om commentaar op te nemen binnen codeblokken. Het is dan voor iemand die de code niet ontwikkeld heeft en deze moet refactoren, duidelijk wat de bedoeling is. Gaan we hier ook doen.

Als voorbeeld wordt hier een applicatie opgebouwd, waarbij gegevens vanuit drie klassen aangeroepen zullen worden. Die klassen zijn `Song`, `Artist` en `Album`. De naamgeving is hier in het Engels omdat deze bestanden later gekoppeld zullen worden aan een databestand waarin alle gegevens onder de Engelse notaties staan opgeslagen. De code is te vinden in het bestand [muziek.py](../../bestanden/muziek.py). 

De eerste klasse is `Song`. In het commentaar van deze klasse zetten we een korte beschrijving van de klasse, gevolgd door een omschrijving van de attributen die van objecten deze klasse worden bijgehouden. Na dit commentaar volgt de *constructor*, die we ook voorzien van een korte beschrijving.

```python
class Song:
    """Klasse waarin gegevens van popsongs worden vastgelegd

    Attributen:
        title (str): De titel van de nummer.
        artist (Artist): Een object uit de klasse artist die de componist van het nummer is.
        duration (int): De duur van het nummer in seconden.  Waarde nul (0) is toegestaan.
    """ 

   def __init__(self, title, artist, duration=0):
        self.title = title
        self.artist = artist
        self.duration = duration

``` 

In hetzelfde bestand maken we nu een tweede klasse: `Album`. Aan deze klasse kunnen Songs aan worden toegevoegd.

```python
class Album:
   
    """ Klasse waarin Aibums vastgelegd worden, met gebruikmaking van de bijbehorende track-list

   Attributen:
       name (str): De naam van het album.
       year (int): Het jaar waarin het album werd uitgebracht.
       artist: (Artist): De artiest verbonden aan het album. Als er geen artiest bekend is, dan
       krijgt de artist als defaultwaarde de naam "Various Artists".
       tracks (List[Song]):  Een lijst met de nummers van het album.

   Methods:
       add_song: Deze methode voert een nieuw nummer (song) toe aan de track-list.   """

    def __init__(self, name, year, artist=None):
        self.name = name
        self.year = year
        if artist is None:
            self.artist = Artist("Various Artists")
        else:
            self.artist = artist

        self.tracks = []
```

Het is hier allemaal een beetje overdone, maar het idee is duidelijk.

Aan deze klasse wordt nog een methode aan toegevoegd om de songs aan een album toe te kunnen voegen. 

```python
def add_song(self, song, position=None):
    """Voegt een nummer toe aan de tracklijst

    Argumenten:
        song (Song): een nummer om toe te voegen.
        position (Optioneel [int]): Indien opgegeven, wordt de song op die positie ingevoegd
       in de tracklijst, anders wordt het nummer aan het einde van de lijst toegevoegd.
    """
    if position is None:
        self.tracks.append(song)
    else:
        self.tracks.insert(position, song)
```

Er is al verwezen naar de klasse Artist, maar die bestaat op dit moment nog niet. Daar gaat nu verandering in komen.

```python
class Artist:
    """Klasse om artiestgegevens op te slaan.
    Attributen:
        name (str): de naam van de artiest.
        albums (Lijst [Album]): een lijst met de albums van deze artiest.
                De lijst bevat alleen die albums in deze verzameling, en is derhalve niet volledig.

    Methods:
        add_album: wordt gebruikt om een nieuw album aan de albumlijst toe te voegen..   """
    def __init__(self, name):
        self.name = name
        self.albums = []
```

Ook deze klasse moet de mogelijkheid hebben een album aan de lijst van een artiest toe te voegen. Bijzondere aandacht voor het feit dat een album niet meerdere keren toegevoegd kan worden.

```python
def add_album(self, album):
    """Voeg een nieuw album toe aan de lijst.

     Argumenten:
         album (Album): Een object van het type Album dat aan de lijst moet worden toegevoegd.
             Als het album al aanwezig is, wordt het niet opnieuw toegevoegd 
             (hoewel dit nog niet is geïmplementeerd).
     """
    self.albums.append(album)
```

Qua ontwerp is het allemaal nog niet zo optimaal, maar daar kijken we later wel naar. 

Tijd om gegevens te tonen. Het is niet de bedoeling ongelofelijk veel typewerk te verrichten, maar er wordt gebruik gemaakt van de file `albums.txt`. De gegevens worden met behulp van een methode weer ingeladen.

```python
def load_data():
      new_artist = None
      new_album = None
      artist_list = []
```

Deze methode valt buiten een klasse. Hierin wordt een nieuw object van een artist en een album aangemaakt, maar deze krijgen de waarde ‘None’ mee. Tevens wordt er een lijst aangemaakt waarin de artiesten opgeslagen worden.

```python
with open("albums.txt", "r") as albums:
    for line in albums:
        # data row should consist of (artist, album, year, song)
        artist_field, album_field, year_field, song_field = tuple(line.strip('\n').split('\t'))
        year_field = int(year_field)
        print("{}:{}:{}:{}".format(artist_field, album_field, year_field, song_field))
```

Van iedere regel uit het bestand `albums.txt` wordt de artiest, album, jaar en song getoond.

Het fragment `with open(“albums.txt”,”r”)` wil zeggen dat er gezocht wordt naar de file `albums.txt` en als deze gevonden is, wordt de inhoud gelezen (`r` = read) en toevertrouwd aan de lokale variabele `albums`.

Nu nog het aanroepen van de methode, wat feitelijk het startpunt is van onze hele applicatie:

```python
if __name__=='__main__':
    load_data()
```

Er zijn te veel gegevens om allemaal te tonen; hier een klein stukje van het einde van de verzameling:

```
... (680 regels)

ZZ Top:Mescalero:2003:Que Lastima
ZZ Top:Mescalero:2003:Tramp
ZZ Top:Mescalero:2003:Crunchy
ZZ Top:Mescalero:2003:Dusted
ZZ Top:Mescalero:2003:Liquor
There are 28 artists 
```


