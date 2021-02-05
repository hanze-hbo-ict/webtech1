
import datetime

class Bankrekening:

    def _current_time():
        now = datetime.datetime.now()
        return (now.strftime("%Y-%m-%d %H:%M:%S"))


    def __init__(self, naam, saldo):
        self._name = naam
        self.__saldo = saldo
        self._transactie_overzicht = []
        print("Bankrekening aangemaakt voor " + self._name)

        

    def storten(self, bedrag):
        if bedrag > 0:
            self.__saldo += bedrag
            self.toon_saldo()
            self._transactie_overzicht.append( (Bankrekening._current_time(), bedrag) )
        self.toon_saldo()

    def opnemen(self, bedrag):
        if 0 < bedrag <= self.__saldo:
            self.__saldo -= bedrag
            self._transactie_overzicht.append(((Bankrekening._current_time(), -bedrag)))
        else:
            print("Het bedrag dient groter dan nul (0) en maximaal gelijk aan het saldo te zijn")
        self.toon_saldo()

  
    def toon_saldo(self):
        print ("Saldo bedraagt {}".format(self.__saldo))

    def toon_transacties(self):
        for date, bedrag in self._transactie_overzicht:
            if bedrag > 0:
                trans_type = "gestort"
            else:
                trans_type = "opgenomen"
                bedrag *= -1
            print("{} {} op {}".format(bedrag, trans_type, (Bankrekening._current_time())))




