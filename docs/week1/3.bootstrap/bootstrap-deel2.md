# Bootstrap – Voorbeeld

Als voorbeeld zullen we nu aan de hand van de documentatie een webpagina opbouwen. De basiscode kan aan het html-document worden toegevoegd en daar aangepast worden aan het gewenste ontwerp. Hierbij wordt een stapsgewijze opbouw gehanteerd.

!!! Info "Download de bestanden"
    De bestanden die in dit voorbeeld worden besproken zijn [via deze link te downloaden](../bestanden/bootstrap.zip).

__Stap 1:__ html-document zonder koppeling naar Bootstrap.

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Zonder</title>
    </head>
    <body>

        <h1>Hello, world!</h1>

    </body>
</html>
```

![Basispagina](imgs/bootstrap1.png)

__Stap 2:__ Toevoegen links van Bootstrap.

Ieder html-document dat gebruik wil maken van de faciliteiten die door Bootstrap aangeboden worden, dient de benodigde links in de `<head>`-sectie op te nemen. Deze links kunnen gekopieerd worden van de site <https://getbootstrap.com/>, [zoals we al besproken hebben](bootstrap-deel1.md).

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Met</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="x-ua-compatible" content="ie=edge">

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </head>
    <body>

        <h1>Hello, world!</h1>

    </body>
</html>
```

Nog een geluk dat de links gekopieerd kunnen worden.

![Met Bootstrap](imgs/bootstrap2.png)

Een duidelijk verschil. De marges en het lettertype is aangepast door de Bootstrap-instellingen.

!!! info "width en init-scale"
    Bootstrap 5 is ontworpen om te kunnen werken met mobiele apparaten. Daarvoor is een `<meta>`-tag toegevoegd. Hier geven we twee waarden aan mee. Door te stellen dat `width = device-width` wordt de breedte van de pagina hetzelfde als de schermbreedte van het apparaat (dit is afhankelijk van het apparaat); `initial-scale = 1` stelt het initiële zoomniveau in, wanneer de pagina voor het eerst wordt geladen door de browser.

__Stap3:__ Container toevoegen.

Bootstrap vereist een omvattend element om de inhoud van de site in te pakken. Hiervoor maken we een `div` aan van de classe `container` (we laten voor de overzichtelijkheid nu even al die links in de `header` weg):

```html
<body>
    <div class="container">
        <h1>Hello World!</h1>
    </div>
</body>
```

![Container](imgs/bootstrap3.png)

__Stap 4:__ Hero sectie.

In Bootstrap 5 is de jumbotron vervangen door utility classes. We kunnen een vergelijkbaar effect creëren met een `<div>` met een achtergrondkleur en padding. Dit maakt een prominente sectie om speciale inhoud of informatie te accentueren.

In deze hero sectie kan nagenoeg elke geldige HTML geplaatst worden, inclusief andere Bootstrap-elementen of -klassen.

```html
<body>
    <div class="container">
        <h1>Hello, world</h1>

        <div class="bg-light p-5 rounded">
            <h1 class="display-3">Hello, Hero!</h1>

            <p class="lead">Dit is een eenvoudige paragraaf, waarbij gebruik gemaakt wordt van een hero sectie, om extra aandacht te vragen voor dit specifieke onderdeel.</p>
        </div>
    </div>
</body>
```

![Hero sectie](imgs/bootstrap4.png)

__Stap 5:__ Knoppen toevoegen.

Bootstrap kent ook verschillende typen knoppen. Eén van de voordelen hiervan is dat door het algemene gebruik van Bootstrap de meeste mensen bekend zijn met de betekenis van de specifieke vorm van de knoppen, en de interactie met je site dus soepeler gaat lopen.

We gaan nu ook knoppen aan ons voorbeeld toevoegen. Als je de component *Buttons* [op de site van Bootstrap](https://getbootstrap.com/docs/5.3/components/buttons/) selecteert, krijg je te zien welke buttons er allemaal bestaan. Zie het voorbeeld hieronder (om het geheel overzichtelijk laten we de container met de hero sectie achterwege).

```html
<div class="container">
    <h1>Hello World!</h1>

    <button class="btn btn-success" type="button" name="button">Button</button>

    <!-- rest van de html is weggelaten -->

</div>
```

![Knoppen 1](imgs/bootstrap5.png)

Met de beschikbare informatie wordt een nog een tweede knop in de container opgenomen met de kenmerken, extra groot en niet actief (let op de waarden van het `class`-attribuut van deze tweede knop):

```html
<div class="container">
    <h1>Hello World!</h1>

    <button class="btn btn-success" type="button" name="button">Button</button>
    <button type="button" class="btn btn-lg btn-primary" disabled>Primary button</button>

    <!-- rest van de html is weggelaten -->

</div>
```

![Knoppen 2](imgs/bootstrap6.png)

Deze laatst toegevoegde knop heeft inderdaad de status inactief gekregen. Als je met je muis over deze knop gaat (*hover*), verschijnt er geen handje.

__Stap 6:__ Finishing touch.

In de html hieronder hebben we nog een paar wijzigingen aan onze geweldige site toegevoegd. De grotere knop heeft een ander uiterlijk gekregen, de tweede container heeft ook een tweede klasse gekregen, waarin een knop is opgenomen waaraan een link gekoppeld is.

```html
<body>
    <div class="container">
        <h1>Hello World!</h1>

        <button class="btn btn-success btn-lg active" type="button"       name="button">Button</button>
        <button class="btn " disabled type="button" name="button">Disabled Button</button>

        <div class="bg-light p-5 rounded mt-3">
            <h1 class="display-3">Hello, Hero!</h1>

            <p class="lead">Dit is een eenvoudige paragraaf, waarbij gebruik gemaakt wordt van een hero sectie, om extra aandacht te vragen voor dit specifieke onderdeel.</p>

            <p>We maken hier gebruik van een paragraaf, om de spatiëring een de ruimte tussen de container te regelen..</p>

            <p class="lead">
                <a class="btn btn-primary btn-lg " href="#" role="button">Learn more</a>
            </p>
        </div>
    </div>
</body>
```

![bootstap 7](imgs/bootstrap7.png)
