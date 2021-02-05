# OOP Python – Compositie

In deze laatste paragraaf aandacht voor nog OOP-techniek, compositie (*composition*) (*composition*). Compositie wil zeggen dat een object *samengesteld* wordt aan de hand van verschillende andere objecten. Het samengesteld object kan op die manier taken delegeren aan die samenstellende objecten. Op zich lijkt compositie wel wat op overerving, maar waar overerving *impliciet* is, is compositie *expliciet* (en daarmee ook schaalbaarder, testbaarder en overdraagbaarder).

Compositie biedt een superieure manier om delegatie te beheren, aangezien het selectief de toegang kan delegeren, zelfs sommige attributen of methoden kan maskeren, terwijl overerving dat niet kan. 

Aan het eind van deze paragraaf maken we [oefening 3](oefeningen/oop-oefening3.md).

## Een gevleugeld voorbeeld

Als voorbeeld wordt hier een klasse `Vleugel` toegevoegd aan de file met de eend en de pinguin. Deze klassee krijgt behalve de constructor (`__init__`) de methode `vliegen()`. Deze laatste krijgt als parameter `ratio` mee, die de verhouding tussen vleugels en lichaamsgewicht aangeeft. Deze verhouding bepaalt de wijze of een vogel al dan niet makkelijk kan opstijgen. 

```python
class Vleugel:

    def __init__(self, ratio):
        self.ratio = ratio

    def vliegen(self):
          if self.ratio > 1:
               print("Wauwwww, dit is fun")
          elif self.ratio == 1:
               print("Pff, hard werken, maar ik vlieg tenminste")
          else:
               print("Ik denk dat ik maar weer gewoon ga waggelen")
```

De volgende stap is om de klasse `Duck` van een constructor te voorzien en bovendien een methode `vliegen()` toe te voegen die verwijst naar de klasse `Vleugel`.

```python
class Duck:

    def __init__(self):
        self._vleugel = Vleugel(1.8)
        
    def vliegen(self):
        self._vleugel.vliegen()
```

Eenden hebben nu een vleugel en een methode om te vliegen. Kijken of Donald de lucht in wil.

```python
if __name__ == '__main__':
   donald = Duck()
   donald.vliegen()
```

Resultaat:

```shell
Wauwwww, dit is fun
```

Wat is er nu gebeurd? In de klasse `Duck` is een nieuw object gecreëerd van de klasse `Vleugel`. Vervolgens is er een methode `vliegen()` aangemaakt, waarbij een object uit de klasse `Duck` gebruik maakt van zijn eigen instantie van de klasse `Vleugel` om de methode `vliegen()` daarop aan te roepen. 

De klasse `Duck` bestaat nu (voor het merendeel) uit eigen methoden, maar er wordt ook een deel van de functionaliteit gedelegeerd naar objecten van een ander type (namelijk `Vleugel`). De eend is dus een *samengestelde klasse* geworden.

## Een wat realistischer voorbeeld
Daarom nu een meer realistisch voorbeeld. Basis hiervoor is een nieuwe Python-file, getiteld [`html_doc.py`](../bestanden/html_doc.py).

Een HTML-pagina moet minstens drie elementen bevatten:

- een verwijzing naar het doctype
- een header
- een body

Als opfrisser, een kort overzicht van de basisstructuur van een HTML-pagina.

```html
<!DOCTYPE html>
<html>
	<head>
	</head>

	<body>
	</body>
</html> 
```

HTML wordt voornamelijk opgebouwd door gebruik te maken van tags, dus als eerste wordt er een klasse `Tag` gecreëerd, met een constructor. 

```python
class Tag:

    def __init__(self, name, contents):
        self.start_tag = '<{}>'.format(name)
        self.end_tag = '</{}>'.format(name)
        self.contents = contents
```

De volgende stap is de tags en de inhoud naar het scherm te schrijven. Met 'inhoud' wordt hier bedoeld de tekens die tussen de begin- en eind tag zijn opgenomen.

```python
def __str__(self):
    return "{0.start_tag}{0.contents}{0.end_tag}".format(self)

def display(self, file=None):
    print(self, file=file)
```

De basisstructuur laat zien dat er nog drie andere klassen nodig zijn. De eerste daarvan is `Doctype`. Hierin wordt vastgelegd met welke versie van HTML er gewerkt wordt. Daar wordt een nieuwe klasse voor ontwikkeld.

```python 
class DocType(Tag):

    def __init__(self):
        super().__init__('!DOCTYPE HTML', '')
        self.end_tag = ''   # DOCTYPE heeft geen endtag
```

!!! Info "Is DOCTYPE echt een html-element?"
    De declaratie `DOCTYPE` is niet echt een html-tag. Hij behoort tot de zogenaamde *preambule* van de pagina, en vertelt browsers dat de tekst die gaat volgen bestaat uit html; je zou dus kunnen zeggen dat deze tag *voorafgaat* aan de html en er dus geen onderdeel van uitmaakt. [Zoals gewoonlijk is er veel over te vertellen](https://html.spec.whatwg.org/multipage/syntax.html#the-doctype), maar voor het voorbeeld houden we het er hier op dat `DOCTYPE` een subklasse is van `Tag`.

De tweede is de klasse `Head`, de derde is de klasse `Body`:

```python
class Head(Tag):

  def __init__(self, title=None):
        super().__init__('head', '')

class Body(Tag):

    def __init__(self):
        super().__init__('body', '')   # De inhoud van de body wordt apart opgebouwd
        self._body_contents = []

    def add_tag(self, name, contents):
        new_tag = Tag(name, contents)
        self._body_contents.append(new_tag)

    def display(self, file=None):
        for tag in self._body_contents:
            self.contents += str(tag)

        super().display(file=file)
```

De methode `__init__()` plaatst de begintag op de juiste plaats. De inhoud van de body is nog leeg. Dat is echter wel de plek waarop de inhoud van HTML-document getoond wordt. De methode `add_tag()` bouwt de inhoud langzaam op en de methode `display()` laat de inhoud verschijnen.

Uiteraard had dezelfde inhoud ook bij de klasse `Head` ondergebracht kunnen worden omdat daar ook de nodige tags aan toegevoegd zouden kunnen worden. Het is hier een voorbeeld en niet het bouwen van een professionele site, dus een versimpeling van de werkelijkheid.

Alle klassen zijn nu aangemaakt en nu kan het daadwerkelijke document opgebouwd worden.

## Een html-document

Alle klassen zijn nu aangemaakt en nu kan het daadwerkelijke document opgebouwd worden.

```python
class HtmlDoc(object):

      def __init__(self, title=None):
           self._doc_type = DocType()
           self._head = Head()
           self._body = Body()
```

Als eerste worden nieuwe objecten aangemaakt voor doctype, head en body. De klasse `HtmlDoc` is dus opgebouwd (*samengesteld*, *gecomponeerd*) vanuit drie andere klassen. Dit object kent geen attributen van zichzelf, maar wordt opgebouwd uit elementen van andere klassen.

```python
def add_tag(self, name, contents):
    self._body.add_tag(name, contents)
```
Voor iedere object uit de klasse `HtmlDoc` wordt de inhoud apart opgebouwd. De tags worden aan object gekoppeld en deze roept de methode van de klasse `Body` aan om de inhoud op te bouwen. Dat lukt dus omdat er een nieuw object `Body` is aangemaakt.

De inhoud van de pagina kan vervolgens opgebouwd worden. Daarvoor voegen we de methode `display()` toe aan de klasse `HtmlDoc`:

```python
def display(self, file=None):
    self._doc_type.display(file=file)
    print('<html>', file=file)
    self._head.display(file=file)
    self._body.display(file=file)
    print('</html>', file=file)
```

Het enige werk dat de methode zelf moet uitvoeren is het aanmaken van de begin- en eind tag `html` en drie keer een methode van een andere klasse aanroepen.

Tijd voor een test!

```python
if __name__ == '__main__':
    demo_page = HtmlDoc('Demo HTML Document')
    demo_page.add_tag('h1', 'Muziekschool Session')
    demo_page.add_tag('h2', 'de specialist in drums en piano')
    demo_page.add_tag('p', 'verdere informatie staat in deze paragraaf')
    demo_page.display()
```

Het resultaat is er, maar wordt niet echt flitsend afgebeeld. Is dat gewenst dat kan op de gebruikelijke manier weer de parameter `file=file` na de diverse display’s toegevoegd worden. 

Het is momenteel gewenst dus een aantal kleine aanpassingen zijn gedaan. Nog een test om te kijken of een browserpagina geopend kan worden met de aangemaakte inhoud.

```python
if __name__ == '__main__':
    my_page.add_tag('h1', 'Muziekschool Session')
    my_page.add_tag('h2', 'de specialist in drums en piano')
    my_page.add_tag('p', 'verdere informatie staat in deze paragraaf')
    with open('test.html', 'w') as test_doc:
            my_page.display(file=test.html)
```

Er is een bestand test.html zichtbaar in het rijtje bestanden dat behoort bij dit project. 

![Directory listing met het html-bestand erbij](imgs/directory_listing.png)

Activeer `test.html` en open dit bestand in een zelfgekozen browser. Geef daarvoor een rechterklik op de bestandsnaam, kies voor ‘Open in Browser’ en selecteer de gewenste browser.

![Het resultaat van het script](imgs/test.png)

Wat is nu het belangrijkste verschil tussen overerving en compositie? Een overerving kent een *is-een* relatie (*is-a relationship*): iedere subklasse heeft de kenmerken van de superklasse en is er een uitbreiding op. Compositie kent een *heeft-een* relatie (*has-a relationship*: een klasse is samengesteld uit meerdere klassen.

Maak nu [oefening 3](oefeningen/oop-oefening3.md).


