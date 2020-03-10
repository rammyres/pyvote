import codecs
from os import urandom
from transacoes import Transacoes, tCandidato, tVoto

class No:

    numero = None
    transacao = None
    noDireito = None
    noEsquerdo = None
    hashNoDireito = ''
    hashNoEsquerdo = ''
    

    def __init__(self, _transacao = None):
        if _transacao != None:
            self.transacao = _transacao

    def transacaoParaDict(self):
        if isinstance(self.transacao, tVoto):
            hashNoDireito = ''
            hashNoEsquerdo = ''
            if self.noDireito:
                hashNoDireito = self.noDireito.transacao.meuHash
            if self.noEsquerdo:
                hashNoEsquerdo = self.noEsquerdo.transacao.meuHash
            return {"tipo": "voto", "numero": self.transacao.numero, "aleatorio": self.transacao.aleatorio, "hash": self.transacao.meuHash,
                    "hashNoEsquerdo": hashNoEsquerdo, "hashNoDireito": hashNoDireito}
        
        elif isinstance(self.transacao, tCandidato):
            hashNoDireito = ''
            hashNoEsquerdo = ''
            if self.noDireito:
                hashNoDireito = self.noDireito.transacao.meuHash
            if self.noEsquerdo:
                hashNoEsquerdo = self.noEsquerdo.transacao.meuHash
            return {"tipo": "voto", "nome": self.transacao.nome, "numero": self.transacao.numero, "operacao": self.transacao.operacao, 
                    "timestamp": self.transacao.timestamp, "aleatorio": self.transacao.aleatorio, "hash": self.transacao.meuHash,
                    "hashNoEsquerdo": hashNoEsquerdo, "hashNoDireito": hashNoDireito}
        
        elif isinstance(self.transacao, Transacoes):
            hashNoDireito = ''
            hashNoEsquerdo = ''
            if self.noDireito:
                hashNoDireito = self.noDireito.transacao.meuHash
            if self.noEsquerdo:
                hashNoEsquerdo = self.noEsquerdo.transacao.meuHash
            return {"tipo": "raiz", "aleatorio": self.transacao.aleatorio, "hash": self.transacao.meuHash,
                    "hashNoEsquerdo": hashNoEsquerdo, "hashNoDireito": hashNoDireito}
        
        else: 
            return False

class Arvore:
    raiz = None

    def inserir(self, _no):
        if self.raiz == None:
            self.raiz = _no
        else:
            self._inserir(self.raiz, _no)

    def _inserir(self, _raiz, _no):

        if(_no.transacao.aleatorio < _raiz.transacao.aleatorio):
            if(_raiz.noEsquerdo != None):
                self._inserir(_raiz.noEsquerdo, _no)
            else:
                _raiz.noEsquerdo = _no
        else:
            if(_raiz.noDireito != None):
                self._inserir(_raiz.noDireito, _no)
            else:
                _raiz.noDireito = _no

    def imprimirArvore(self, _no):
        if _no.transacaoParaDict():
            print(_no.transacaoParaDict())
        if _no.noEsquerdo != None:
            self.imprimirArvore(_no.noEsquerdo)
        if _no.noDireito != None:
            self.imprimirArvore(_no.noDireito)
