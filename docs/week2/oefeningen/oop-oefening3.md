# OOP Python – Oefening 3

a. Pas de code van `html_doc.py` zodanig aan dat het ook mogelijk wordt een titel mee te geven aan het `Head`-object.

b. Er zijn verschillende `tags` die *geen* eind-tag en geen content hebben. Denk bijvoorbeeld aan `<img>`, `<hr>` of `<br>` – een volledige overzicht [vind je hier](https://developer.mozilla.org/en-US/docs/Glossary/empty_element). Pas de klasse `Tag` aan zodat dit tot de mogelijkheden behoort. Let op: hiervoor moet je misschien de *constructor* aanpassen, zodat deze zowel mét als zónder parameters kan werken. Maak eventueel gebruik van [optionele parameters in je functie-definitie](https://docs.python.org/3/glossary.html#term-parameter).

c. (optionele uitdaging). Zoals besproken kan een html-tag een set van *attributen* met *waarden* bevatten. Zo heeft de `img`-tag een `src`- en een `alt`-attribuut. Breid de klasse `Tag` op zo'n manier uit, dat het mogelijk is om hier een set van attributen met waarden aan toe te voegen. Maak hiervoor een methode `add_attribute(name, value)`. Zorg er ook voor dat bij het *uitprinten* van deze tag (in de methode `__str__`) deze attributen met hun waarden ook terugkomen (bijvoorbeeld `<img src="url" alt="alt-text">`).

d. (nog een optionele uitdaging). Als je goed kijkt naar de opbouw van `html_doc.py` zie je dat de klasse `Head` eigenlijk niks bijzonders doet, net zo min als de klasse `Body`: in beide gevallen zijn dit `Tag`s die zelf weer andere `Tag`s kunnen bevatten. Het lijkt erop dat je eigenlijk *alleen* de klasse `Tag` nodig hebt om alles te laten werken (en misschien een klasse `HtmlDoc`). Pas de code aan, zodat een `Tag` ook weer andere `Tag`s kan bevatten. Let er daarbij op dat *alle* tags correct worden weergegeven op het moment dat je `__str__()` aanroept (denk hierbij aan de lessen over recursie die je in het eerste kwartaal hebt gehad).

Als je dit is gelukt kun je jezelf feliciteren: je hebt nu een zogenaamde [Tree-datastructuur](https://nl.wikipedia.org/wiki/Boom_(datastructuur)) gemaakt.
