class Erros(Exception):

    pass

class tipoDeBlocoInvalido(Erros):
    def __init__(self, message):
        self.message = message

class hashAnteriorInvalido(Erros):
    def __init__(self, message):
        self.message = message