class Foo:
    _saldo = 0
    
    def __init__(self, saldo):
        self._saldo = saldo

bar = Foo()
bar._saldo = 500
