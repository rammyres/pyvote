from erros import hashAnteriorInvalido, tipoDeBlocoInvalido
from hashlib import sha256

class Block:
    index = None #Indice do bloco
    tipoBloco = None #Definição do tipo de bloco
    dados = None #dados contidos no bloco
    aleatorio = None
    nonce = None
    numero = None
    hash_ant = None
    meu_hash = None

    def __init__(self, tipo):
        if tipo == "Genesis" or tipo == "candidato" or tipo == "voto":
            self.tipoBloco = tipo
        else:
            raise tipoDeBlocoInvalido("Tipo de bloco deve ser candidato ou voto")

    def temHashValido(self, hash):
        return hash.startswith('0000')

    def crieMeuHash(self):
        hash = ''
        self.nonce = 1
        while not self.temHashValido(hash):
            block = '{}:{}:{}:{}:{}:{}'.format(
                self.index, self.dados, self.aleatorio, self.nonce, self.numero, self.hash_ant
            )
            hash = sha256(block.encode()).hexdigest()
            self.nonce += 1
        
        self.meu_hash = hash