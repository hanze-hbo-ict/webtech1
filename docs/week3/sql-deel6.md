# Exceptions

In deze paragraaf wordt het werken met een database even losgelaten en worden de ‘exceptions’  geïntroduceerd. Exceptions worden gebruikt om een onverwachte of incorrecte programma-flow te ondervangen en bijvoorbeeld een foutmelding opo het scherm te tonen. Een geschikt Nederlands woord hiervoor is 'foutafhandeling'. Hoe zorgen we ervoor dat duidelijk is wat de fout precies is?

Er zijn twee verschillende soorten fouten die gevonden kunnen worden bij de uitvoering van een programma. De eerste soort is al meerdere keren naar voren gekomen, namelijk fouten in de code. Deze fouten kunnen opgelost worden door verbeteringen aan te brengen in de code. In het volgende voorbeeld is per ongelijk een is-gelijk-teken (`=`) gebruikt in plaats van een min-teken (`-`): één toets te ver. Bij het runnen wordt geconstateerd dat er een fout in de code zit en er verschijnt een foutmelding met een aanwijzing naar de fout.

```iphython
In [1]: x = 8 = 5
  File "<ipython-input-1-6ddc385bfffb>", line 1
    x = 8 = 5
       ^
SyntaxError: can't assign to literal

In [2]: 
```

Andere onverwachte fouten, bijvoorbeeld problemen in de flow, of het willen aanmaken van een database terwijl de beschikbare ruimte op is, leveren meestal een crash van het programma op. Het doel van exceptions is dit in goede banen te leiden.

Kijk naar de volgende code:

```ipython
In [1]: y = 10

In [2]: x = y - (2*5)

In [3]: y / x
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)
<ipython-input-3-68e2f9788128> in <module>
----> 1 y / x

ZeroDivisionError: division by zero
```

En inderdaad, delen door nul (0) is niet toegestaan. Deze vorm wordt ‘unhandled exception’ genoemd. Gevolg van een dergelijke werkwijze is dat het programma onmiddellijk beëindigd wordt. Python geeft aan wat de fout is en er wordt aangeven in welke regel de fout geconstateerd is.

Python heeft de beschikking over [veel ‘Built-in Exceptions’](https://docs.python.org/3/library/exceptions.html). Deze exceptions doen het werk al voor de gebruiker door te laten zijn in hun beschrijving welke fout gesignaleerd is.

Een interessante exception is de `RecursionError`. Recursie is natuurlijk al uitgebreid behandeld in het eerste kwartaal, bijvoorbeeld wanneer we de *faculteit* van een getal `n` moesten berekenen. Bij een waarde van `n` die duizend overstijgt, geeft Python helaas aan te maken te hebben met een *stack overflow*. En daar past een mooie foutafhandeling bij...

```ipython
In [1]: def factorial(n):
   ...: #     n! kan gelezen worden als n*(n-1)!
   ...:     if n <= 1:
   ...:         return 1
   ...:     else:
   ...:         return n * factorial(n-1)
   ...: 
```


De output van 50! levert al een erg groot getal op.

```ipython
In [2]: factorial(50)
Out[2]: 30414093201713378043612608166064768844377641568960512000000000000
```


Hetzelfde nog een keer maar nu voor `n = 10_000`:

```ipython
In [4]: factorial(10_000)
---------------------------------------------------------------------------
RecursionError                            Traceback (most recent call last)

(...)

RecursionError: maximum recursion depth exceeded in comparison
```

Deze fout kunnen we netjes opvangen door gebruik te maken van een *exception*:

```ipython
In [7]: try:
   ...:     print(factorial(10_000))
   ...: except RecursionError:
   ...:     print("Dit programma kan zulke grote getallen niet handelen.")
   ...: 
   ...: print("Programma beëindigd!")
   ...: 
Dit programma kan zulke grote getallen niet handelen.
Programma beëindigd!

```

Het codeblok wat vermeld staat onder `try` wordt normaal gesproken uitgevoerd. Op het moment dat er wordt waargenomen dat er een fout is ontstaan, wordt er automatisch gesprongen naar het codeblok onder `except`. De mededeling wordt getoond en het programma gestopt.

In de foutafwikkeling van dit programma  is ervan uitgegaan dat er slechts één soort fout kan optreden. Dat hoeft natuurlijk niet het geval te zijn. Om dit te illustreren, passen we onze methode aan met een (beetje gezocht, maar goed) extra fout, namelijk een deling door nul (`0`):

```ipython
In [1]: def factorial(n):
   ...: #     n! kan gelezen worden als n*(n-1)!
   ...:     if n <= 1:
   ...:         return 1
   ...:     else:
   ...:         print(n / 0)
   ...:         return n * factorial(n-1)
   ...: 
```

Als we deze code runnen, krijgen we natuurlijk dezelfde foutmelding als in het voorbeeld hierboven te zien:

```ipython
In [2]: factorial(3)
---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)
<ipython-input-2-3fd9b1939623> in <module>
----> 1 factorial(3)

<ipython-input-1-72cc9778b48a> in factorial(n)
      4         return 1
      5     else:
----> 6         print(n / 0)
      7         return n * factorial(n-1)

ZeroDivisionError: division by zero
```

Om dit op te vangen, kunnen we de *call* wat uitbreiden met een extra exceptie:

```iphython hl_lines="5 6"
In [3]: try:
   ...:     print(factorial(800))
   ...: except RecursionError:
   ...:     print("Dit programma kan zulke grote getallen niet handelen.")
   ...: except ZeroDivisionError:
   ...:     print("Delen door het getal nul (0) is niet mogelijk!")
   ...: 
   ...: print("Programma beëindigd!")
   ...: 

Delen door het getal nul (0) is niet mogelijk!
Programma beëindigd!
```

Je ziet dat een `try` meerdere *typen* fouten (`exception`) kan opleveren. Door verschillende van dergelijke blokken te definiëren, wordt de bijhorende afhandeling uitgevoerd.

Naast een `RecursionError` kan er ook een i`OverflowError` optreden. Dat kan gebeuren als een getal te groot is voor Python om er iets zinvols mee te geven. In theorie zal dit niet vaak voorkomen, maar als voorbeeld is het wel nuttig. Dit laat zien hoe je *dezelfde* foutafhandeling kunt uitvoeren wanneer er *verschillende* excepties optreden.

```ipython
In [4]: try:
   ...:     print(factorial(1000))
   ...: except (RecursionError, OverflowError):
   ...:     print("Dit programma kan zulke grote getallen niet handelen.")
   ...: 
```

Op het moment dat één van beide uitzonderingen (`exceptions`)optreedt, verschijnt de melding die voor beide foutafhandelingen toepasselijk is. Deze methode is niet aan te bevelen voor de combinatie `RecursionError` en `ZeroDivisionError`, omdat beide een alternatieve foutmelding nodig hebben.












