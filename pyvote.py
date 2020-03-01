from hashlib import sha256
from erros import hashAnteriorInvalido
import random, os, codecs, json

class Block:
    index = None
    dados = None
    aleatorio = None
    nonce = None
    hash_ant = None
    meu_hash = None

    def temHashValido(self, hash):
        return hash.startswith('0000')

    def crieMeuHash(self):
        hash = ''
        self.nonce = 1
        while not self.temHashValido(hash):
            block = '{}:{}:{}:{}:{}'.format(
                self.index, self.dados, self.aleatorio, self.nonce, self.hash_ant
            )
            hash = sha256(block.encode()).hexdigest()
            self.nonce += 1
        
        self.meu_hash = hash


class Blockchain:

    def __init__(self):
        self.blocks = []

    def criarBlocoGenesis(self):
        blocoGenesis = Block()
        blocoGenesis.index = 0 
        blocoGenesis.dados = 'Bloco genesis' 
        blocoGenesis.aleatorio = codecs.encode(os.urandom(16), 'hex').decode()
        blocoGenesis.nonce = 0
        blocoGenesis.hash_ant = 0
        blocoGenesis.crieMeuHash()
        self.blocks.append(blocoGenesis)

    def criarNovoBloco(self, dados):
        novoBlock = Block()
        novoBlock.index = len(self.blocks)
        novoBlock.dados = dados
        novoBlock.aleatorio = codecs.encode(os.urandom(16), 'hex').decode()
        novoBlock.hash_ant = self.blocks[len(self.blocks)-1].meu_hash
        novoBlock.crieMeuHash()
        self.blocks.append(novoBlock)
    
    def importar(self, arquivo):
        f = open(arquivo,"r+")
        dicionarios = json.load(f)
        for d in dicionarios["block"]:
            bloco = Block()
            bloco.index = d["index"]
            bloco.dados = d["dados"]
            bloco.aleatorio = d["aleatorio"]
            bloco.nonce = d["nonce"]
            bloco.hash_ant = d["hash_ant"]
            bloco.meu_hash = d["meu_hash"]
            if len(self.blocks)==0:
                pass
            elif bloco.hash_ant != self.blocks[len(self.blocks)-1].meu_hash:
                raise hashAnteriorInvalido("O bloco atual possui um hash inválido")
            self.blocks.append(bloco)
        
    
    def exportar(self, arquivo):
        f = open(arquivo, "w+")
        dicionarios = []
        
        for b in self.blocks:
            s = {"index": b.index, "dados": b.dados,"aleatorio": b.aleatorio, "nonce": b.nonce, "hash_ant": b.hash_ant, "meu_hash": b.meu_hash}
            print(s)
            dicionarios.append(s)

        #for d in dicionarios:
        #    json.dump(d, f, indent=4)

        dicionario = {"block": dicionarios}
        json.dump(dicionario, f, indent=4)

        f.close()
        