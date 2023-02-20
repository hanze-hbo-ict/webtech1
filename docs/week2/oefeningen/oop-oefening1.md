# OOP Python – Oefening 1

Bekijk nogmaals het bestand [`bankrekening.py`](../bestanden/bankrekening.py).  Het programma is nog niet helemaal perfect. Kijk naar de volgende coderegels van een tweede klant, Britt:

```ipython
In [1]: run "bankrekening"

In [2]: britt = Bankrekening("Britt", 800)
Bankrekening aangemaakt voor Britt

In [3]: 
   ...: britt.storten(100)
Saldo bedraagt 900
Saldo bedraagt 900

In [4]: britt.opnemen(200)
Saldo bedraagt 700

In [5]: britt.toon_transacties()
100 gestort op 2021-01-10 14:04:54
200 opgenomen op 2021-01-10 14:04:54
``` 

Er is iets duidelijk niet goed gegaan. De eerste transactie, het storten van 800 euro is niet in de transactielijst te zien. Graag een oplossing hiervoor.