# OOP Python – Oefening 1

Bekijk nogmaals het bestand [`voorraad.py`](../bestanden/webshop/voorraad.py). Het programma is nog niet helemaal perfect. Kijk naar de volgende coderegels voor een nieuw product, een muis:

```ipython
In [1]: run "voorraad"

In [2]: muis_voorraad = Voorraad("Draadloze muis", 50)
Voorraad aangemaakt voor Draadloze muis

In [3]: muis_voorraad.bijbestellen(20)
Voorraad Draadloze muis bedraagt 70

In [4]: muis_voorraad.verkoop(15)
Voorraad Draadloze muis bedraagt 55

In [5]: muis_voorraad.toon_mutaties()
Mutatie-geschiedenis voor Draadloze muis:
  2026-01-31 14:23:15: 20 bijbesteld
  2026-01-31 14:23:15: 15 verkocht
```

Er is iets nog niet helemaal goed gegaan. De eerste mutatie, het beginvoorraad van 50 stuks, is niet in de mutatielijst te zien. Graag een oplossing hiervoor.
