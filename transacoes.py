
from hashlib import sha256
from os import urandom
from datetime import datetime
import codecs

class Transacoes:

    aleatorio = None
    meuHash = None

    def criarTransacaoRaiz(self):
        hash = ''
        self.aleatorio = codecs.encode(urandom(32), 'hex').decode()
        dados = '{}'.format(self.aleatorio)
        hash = sha256(dados.encode()).hexdigest()
        self.meuHash = hash

class tCandidato(Transacoes):
    nome = None
    numero = None
    transacao = None
    timestamp = None

    def __init__(self, nome, numero, operacao):
        self.nome = nome
        self.numero = numero
        self.operacao = operacao
        self.timestamp = datetime.timestamp(datetime.now())

        self.aleatorio = codecs.encode(urandom(32), 'hex').decode()

        self.meuHash = self.criarHash()

    def criarHash(self):

        dados = "{}:{}:{}:{}:{}".format(self.nome, self.numero, self.transacao, self.timestamp, self.aleatorio)

        return sha256(dados.encode()).hexdigest()

class tVoto(Transacoes):
    numero = None

    def __init__(self, numero):
        self.numero = numero
        self.aleatorio = codecs.encode(urandom(32), 'hex').decode()
        self.meuHash = self.criarHash()
    
    def criarHash(self):

        dados = "{}:{}".format(self.numero, self.aleatorio)

        return sha256(dados.encode()).hexdigest()