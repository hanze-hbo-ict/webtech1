# Rubriek project webtechnologie

De laatste vier weken werken studenten in duo's aan één van vier mogelijke casus – zie de weekplanning voor de fasering per week. De uiteindelijke uitwerking hiervan wordt aan het eind van het kwartaal beoordeeld met een cijfer. Dat cijfer is gefundeerd op deze rubriek.

## Criteria

### Algemene realisatie frontend (25%)

Niveau | Score | Beschrijving
---|---|---
Onvoldoende | 0% | De site is rommelig en geeft foutmeldingen; er is maar weinig functionaliteit gerealiseerd.
Voldoende | 50% | De indeling van de site is functioneel, maar niet vloeiend; onboarding-proces werkt naar behoren; alle functionaliteit uit de opgave is gerealiseerd, maar niet meer.
Goed | 100% | Site kent een logische indeling met menu-structuur en een vloeiende interactie; onboarding proces kan volledig doorlopen worden; meer functionaliteit dan puur in de opdracht gegeven is.

### Algemene realisatie backend (25%)

Niveau | Score | Beschrijving
---|---|---
Onvoldoende | 0% | Er is maar een zeer beperkt aantal templates die voor veel te veel dingen verantwoordelijk zijn. De functies zijn rommelig, te complex en verantwoordelijk voor te veel dingen. Er is geen onderscheid in verschillende lagen.
Voldoende | 50% | De site bestaat uit verschillende templates voor verschillende onderdelen; het geheel werkt naar behoren, maar is niet onderverdeeld in verschillende lagen.
Goed | 100% | Meerdere templates met een hiërarchische structuur; onderverdeling in verschillende lagen (routering, logica en database).

### Flask-routes (20%)

Niveau | Score | Beschrijving
---|---|---
Onvoldoende | 0% | Routes zijn erg algemeen (veel verschillende functionaliteit in gematchte functie) en niet gedifferentieerd op basis van http-verbs.
Voldoende | 50% | De routes en de gematchte functies zijn specifiek.
Goed | 100% | De routes zijn specifiek en gedifferentieerd op basis van http-verbs; er wordt gebruik gemaakt van pad-variabelen.

### Aanmeldingsproces (10%)

Niveau | Score | Beschrijving
---|---|---
Onvoldoende | 0% | Aanmeldingsproces of inlogprocedure ontbreekt.
Voldoende | 50% | Aanmeldingsproces en inlogprocedure zijn aanwezig; er wordt gebruik gemaakt van session.
Goed | 100% | Er zijn routes die alleen beschikbaar zijn voor ingelogde gebruikers.

### CRUD-operaties vanaf de frontend (10%)

Niveau | Score | Beschrijving
---|---|---
Onvoldoende | 0% | Er kunnen geen of slechts een minimum aan crud-operaties worden uitgevoerd.
Voldoende | 50% | De meest belangrijke crud-operaties kunnen worden uitgevoerd; data kan worden opgevraagd, maar niet volledig bewerkt.
Goed | 100% | Alle crud-operaties goed gerealiseerd; alle data is via de front-end op te vragen en aan te passen.

### Database (5%)

Niveau | Score | Beschrijving
---|---|---
Onvoldoende | 0% | De data is nauwelijks genormaliseerd en dus (erg) redundant; er is erg veel onnodige traffic tussen de database en de logica.
Voldoende | 50% | De data is genormaliseerd; er worden meerdere tabellen gebruikt. Er zou wel meer logica in de database-laag mogen zitten.
Goed | 100% | Data correct genormaliseerd; gebruik van joins en geaggregeerde data (in views) om traffic tussen db en logica te reduceren.

### Vormgeving en interactie (5%)

Niveau | Score | Beschrijving
---|---|---
Onvoldoende | 0% | Er is nauwelijks aandacht besteed aan vormgeving of interactie-ontwerp; de site kent een wildgroei aan lettertypes en kleurstellingen.
Voldoende | 50% | De site is goed qua layout en interactie-ontwerp, maar veel aandacht is daaraan niet besteed.
Goed | 100% | Veel aandacht besteed aan presentatie en vormgeving. Kleurenpallet en interactie-ontwerp zijn doordacht en consistent.
