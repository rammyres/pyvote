import codecs
from os import urandom
from transacoes import Transacoes, tCandidato, tVoto
class No:

    numero = None
    transacao = None
    pai = None
    noDireito = None
    noEsquerdo = None

    def __init__(self, _transacao = None):
        if _transacao != None:
            self.transacao = _transacao

        self.numero = codecs.encode(urandom(32), 'hex').decode()

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
            return {"tipo": "voto", "nome": self.transacao.nome, "numero": self.transacao.numero, "transcao": self.transacao.transacao, 
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
        if _no.noEsquerdo != None:
            self.imprimirArvore(_no.noEsquerdo)
        if _no.transacaoParaDict():
            print(_no.transacaoParaDict())
        if _no.noDireito != None:
            print(_no.noDireito)
            self.imprimirArvore(_no.noDireito)

    def imprimirBFS(self, _no = No):
        """In BFS the Node Values at each level of the Tree are traversed before going to next level"""

        visitados = []
        if _no:
            visitados.append(_no)
            print(_no.transacaoParaDict())
        atual = _no
        while atual:
            if atual.noEsquerdo:
                print(_no.noEsquerdo.transacaoParaDict())
                visitados.append(atual.noEsquerdo)
            if atual.noDireito:
                print(_no.noDireito.transacaoParaDict())
                visitados.append(_no.noDireito)
            visitados.pop(0)
            if not visitados:
                break
            atual = visitados[0]
            input()
