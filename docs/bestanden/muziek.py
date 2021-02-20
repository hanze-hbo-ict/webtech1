class Song:
    """Klasse waarin gegevens van popsongs worden vastgelegd

    Attributen:
        title (str): De titel van de nummer.
        artist (Artist): Een object uit de klasse artist die de componist van
            het nummer is.
        duration (int): De duur van het nummer in seconden.
            Waarde nul (0) is toegestaan.
    """

    def __init__(self, title, artist, duration=0):
        self.title = title
        self.artist = artist
        self.duration = duration


class Album:
    """ Klasse waarin Aibums vastgeleg worden, met gebruik making van de bijbehorende track-list

    Attributen:
        name (str): De naam van het album.
        year (int): Het jaar waarin het album werd uitgebracht.
        artist: (Artist): De artiest verbonden aan het album. Als er geen
        artiest bekend is, dan krijgt de artist als defaultwaarde de naam
            "Various Artists".
        tracks (List[Song]):  Een lijst met de nummers van het album.

   Methods:
       add_song: Deze methode voeft een nieuw nummer (song) toe aan de track-list.
   """

    def __init__(self, name, year, artist=None):
        self.name = name
        self.year = year
        if artist is None:
            self.artist = Artist("Various Artists")
        else:
            self.artist = artist

        self.tracks = []

    def add_song(self, song, position=None):
        """Voegt een nummer toe aan de tracklijst

        Argumenten:
            song (Song): een nummer om toe te voegen.
            position (Optioneel [int]): Indien opgegeven, wordt de song op die
                positie ingevoegd in de tracklijst, anders wordt het nummer aan het einde van de lijst toegevoegd.
        """


class Artist:
    """Klasse om artiestgegevens op te slaan.
        Attributen:
            name (str): de naam van de artiest.
            albums (Lijst [Album]): een lijst met de albums van deze artiest.
                    De lijst bevat alleen die albums in deze verzameling, en is derhalve niet volledig.

        Methods:
            add_album: wordt gebruikt om een nieuw album aan de albumlijst toe te voegen..
   """

    def __init__(self, name):
        self.name = name
        self.albums = []

    def add_album(self, album):
        """Voeg een nieuw album toe aan de lijst.

            Argumenten:
             album (Album): Een object van het type Album dat aan de lijst moet worden toegevoegd.
               Als het album al aanwezig is, wordt het niet opnieuw toegevoegd
                 (hoewel dit nog niet is geïmplementeerd).
            """
        self.albums.append(album)


def find_object(field, object_list):
    """Check de'object_list' om na te gaan of de naam gelijk is aan de vorige,
    dan bestaat het al en hoeft er geen nieuw object voor aangemaakt te worden. """

    for item in object_list:
        if item.name == field:
            return item
    return None


def load_data():
    new_artist = None
    new_album = None
    artist_list = []

    with open("albums.txt", "r") as albums:
        for line in albums:
            # Getoond moeten worden (artist, album, year, song)
            artist_field, album_field, year_field, song_field = tuple(
                line.strip("\n").split("\t")
            )
            year_field = int(year_field)
            print(f"{artist_field}:{album_field}:{year_field}:{song_field}")

            if new_artist is None:
                new_artist = Artist(artist_field)
                artist_list.append(new_artist)
            elif new_artist.name != artist_field:
                # We hebben de details gelezen voor een nieuwe artiest
                # haal het artiestobject op als er een is,
                # maak anders een nieuw artiestenobject (Artist) en voeg het toe aan de artiestenlijst (artist_list).

                new_artist = find_object(artist_field, artist_list)
                if new_artist is None:
                    new_artist = Artist(artist_field)
                    artist_list.append(new_artist)
                new_album = None

            if new_album is None:
                new_album = Album(album_field, year_field, new_artist)
                new_artist.add_album(new_album)
            elif new_album.name != album_field:
                new_album = find_object(album_field, new_artist.albums)
                if new_album is None:
                    new_album = Album(album_field, year_field, new_artist)
                    new_artist.add_album(new_album)
            # Er is een nieuw album gelezen voor de huidige artiest
            # Haal het albumobject op als er een is,
            # maak anders een nieuw albumobject en sla het op in de collectie van de artiest.
            # maak een nieuw songobject en voeg het toe aan de huidige albumcollectie

            new_song = Song(song_field, new_artist)
            new_album.add_song(new_song)

    return artist_list


def create_checkfile(artist_list):
    """Creëer een checkfile om te kunnen vergelijken met het origineel"""
    with open("checkfile.txt", "w") as checkfile:
        for new_artist in artist_list:
            for new_album in new_artist.albums:
                for new_song in new_album.tracks:
                    print(
                        f"{new_artist.name}\t{new_album.name}\t{new_album.year}\t{new_song.title}",
                        file=checkfile,
                    )


if __name__ == "__main__":
    artists = load_data()
    print(f"There are {len(artists)} artists")

    create_checkfile(artists)
