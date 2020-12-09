# Webtechnologie week 1 deel 2 – HTML

Omdat de server in principe platte tekst aan de browser teruggeeft, is er een structuur nodig om aan te geven wat de verschillende onderdelen uit die platte tekst betekenen. Een koptekst is immers iets anders dan een stuk broodtekst. Hiervoor gebruiken we HTML. 

HTML staat voor *HyperText Markup Language*. Het is, zogezegd, de taal waarmee de inhoud van een website *gemarkeerd* kan worden zodat de browser 'begrijpt' wat aan de bezoeker getoond moet worden. Het geeft structuur aan een gewoon tekstbestand dat de browser anders niet zou begrijpen.

HTML is in het begin van de jaren negentig van de vorige eeuw ontwikkeld door [Tim Berners-Lee](https://nl.wikipedia.org/wiki/Tim_Berners-Lee), terwijl hij werkte bij CERN in Zwitserland.

![De eerste webserver, uit 1991 bij CERN](imgs/cern-server.png)

!!! info "HTML was niet nieuw"
    Hoewel Tim Berners-Lee (of TBL) HTML bedacht en ontwikkeld heeft, wat dat in die tijd niet nieuw. Het idee van het in de tekst zélf aangeven wat de verschillende onderdelen van die tekst betekenen (en eventueel hoe die moeten worden vormgegeven) stamt al uit de jaren zestig. Technieken als de [Generalized Markup Language (GML)](https://en.wikipedia.org/wiki/Standard_Generalized_Markup_Language#History) en [COCOA](https://en.wikipedia.org/wiki/COCOA_(digital_humanities)) gingen aan HTML vooraf. 
    
    Het echt *nieuwe* van TBL was dat HTML een stuk eenvoudiger was om mee te werken, en dat de *browser* een stuk 'vergevingsgezinder' was dan de systemen die op die oudere technieken gebaseerd waren – een ontwerpbeslissing waar we ook heden ten dage nog last van hebben...




### Een voorbeeld

Hieronder staat een voorbeeld van een eenvoudige HTML-pagina. In de volgende paragraaf wordt uitgelegd wordt de code precies inhoudt:

```
<html> 
    <head> 
        <title>Muziekschool Sessions</title> 
    </head> 
    <body> 
        <h1>Over ‘Sessions’</h1> 
        <p>Muziekschool Sessions, de beste in piano en drums.</p> 
    </body> 
</html>
```

Wanneer je deze code opslaat en opent i n een browser, krijg je het onderstaande resultaat te zien:


![File in browser](imgs/file_in_browser.png# small-image)


!!! info "Gebruik van het file system"
    Normaliter maken we gebruik van een webserver om bestanden in je browser te laten zien. In deze en de volgende week gebruiken we nog gewoon het `file system` om de bestanden te laten zien – nadien zullen we gebruik maken van een server, waarbij we ook de verschillen zullen bespreken.




