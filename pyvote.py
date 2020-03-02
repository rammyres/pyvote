from hashlib import sha256
from erros import hashAnteriorInvalido, tipoDeBlocoInvalido
import random, os, codecs, json

class Block:
    index = None
    tipoBloco = None
    dados = None
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

class Blockchain:
    numeroCandidatos = 0

    def __init__(self):
        self.blocks = []

    def criarBlocoGenesis(self):
        blocoGenesis = Block("Genesis")
        blocoGenesis.index = 0 
        blocoGenesis.dados = 'Bloco genesis' 
        blocoGenesis.aleatorio = codecs.encode(os.urandom(16), 'hex').decode()
        blocoGenesis.nonce = 0
        blocoGenesis.hash_ant = 0
        blocoGenesis.crieMeuHash()
        self.blocks.append(blocoGenesis)

    def procurarCandidato(self, nome, numero):
        cand = self.getCandidatos()["candidatos"]
        for c in cand:
            if nome==c["dados"] and numero==c["numero"]:
                return True
    
    def validarNumero(self, numero):
        cand = self.getCandidatos()["candidatos"]
        for c in cand:
            if numero==c["numero"]:
                return True
    
    def criarCandidato(self, nome, numero):
        if not self.procurarCandidato(nome, numero):
            candidato = Block("candidato")
            candidato.index = len(self.blocks)
            candidato.dados = nome
            candidato.numero = numero
            candidato.aleatorio = codecs.encode(os.urandom(16), 'hex').decode()
            candidato.hash_ant = self.blocks[len(self.blocks)-1].meu_hash
            candidato.crieMeuHash()
            self.blocks.append(candidato)
            self.numeroCandidatos += 1
            return True
        else:
            return False

    def votar(self, dados):
        novoBlock = Block("voto")
        novoBlock.index = len(self.blocks)
        novoBlock.dados = dados
        novoBlock.numero = 0
        novoBlock.aleatorio = codecs.encode(os.urandom(16), 'hex').decode()
        novoBlock.hash_ant = self.blocks[len(self.blocks)-1].meu_hash
        novoBlock.crieMeuHash()
        self.blocks.append(novoBlock)
    
    def importar(self, arquivo):
        f = open(arquivo,"r+")
        dicionarios = json.load(f)
        for d in dicionarios["block"]:
            if d["tipoBloco"]=="Genesis":
                bloco = Block("Genesis")
            else:
                bloco = Block(d["tipoBloco"])
                if bloco.tipoBloco == "candidato":
                    self.numeroCandidatos += 1

            bloco.index = d["index"]
            bloco.dados = d["dados"]
            bloco.aleatorio = d["aleatorio"]
            bloco.nonce = d["nonce"]
            bloco.numero = d["numero"]
            bloco.hash_ant = d["hash_ant"]
            bloco.meu_hash = d["meu_hash"]

            if len(self.blocks)==0:
                pass
            elif bloco.hash_ant != self.blocks[len(self.blocks)-1].meu_hash:
                raise hashAnteriorInvalido("O bloco atual possui um hash inválido")
            self.blocks.append(bloco)

    def getCandidatos(self):
        c = []
        for b in self.blocks:
            
            if b.tipoBloco == "candidato":
                c.append({"numero": b.numero, "dados": b.dados})
        candidatos = {"candidatos": c}
    
        return candidatos
            
    
    def exportar(self, arquivo):
        f = open(arquivo, "w+")
        dicionarios = []
        
        for b in self.blocks:
            s = {"index": b.index, "tipoBloco": b.tipoBloco, "dados": b.dados,"aleatorio": b.aleatorio, 
                 "nonce": b.nonce, "numero": b.numero, "hash_ant": b.hash_ant, "meu_hash": b.meu_hash}
            #print(s)
            dicionarios.append(s)

        dicionario = {"block": dicionarios}
        json.dump(dicionario, f, indent=4)

        f.close()
        