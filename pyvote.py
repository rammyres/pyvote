#from hashlib import sha256
from block import Block
from erros import hashAnteriorInvalido
from candidato import Candidato
import random, os, codecs, json

class Blockchain:

    def __init__(self):
        self.blocks = []
        self.candidatosValidos = []

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
        for c in self.candidatosValidos:
            if nome==c.nome and numero==c.numero:
                return True
            else:
                return False
    
    def validarNumero(self, numero):
        for c in self.candidatosValidos:
            if numero==c.numero:
                return True
            else:
                return False
    
    def validarNome(self, nome):
        for c in self.candidatosValidos:
            if nome==c.nome:
                return True
            else:
                return False
    
    def criarCandidato(self, nome, numero):
        if not self.validarNome(nome):
            if not self.validarNumero(numero):
                tCandidato = Block("candidato")
                tCandidato.index = len(self.blocks)
                tCandidato.dados = nome
                tCandidato.numero = numero
                tCandidato.aleatorio = codecs.encode(os.urandom(16), 'hex').decode()
                tCandidato.hash_ant = self.blocks[len(self.blocks)-1].meu_hash
                tCandidato.crieMeuHash()
                self.blocks.append(tCandidato)

                d = Candidato(nome, numero)
                self.candidatosValidos.append(d)

                return True

            else:
                return False
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
                raise hashAnteriorInvalido("Não foi possível validar o hash do bloco anterior no bloco atual")
            self.blocks.append(bloco)
            
            if d["tipoBloco"]=="candidato":
                c = Candidato(d["dados"], d["numero"])
                self.candidatosValidos.append(c)

    def getCandidatos(self):
        c = []
        for b in self.blocks:
            
            if b.tipoBloco == "candidato":
                c.append({"numero": b.numero, "dados": b.dados})

        if len(c)>0:
            return {"candidatos": c}
        else:
            return None

    def getVotos(self):
        v = []
        for b in self.blocks:
            if b.tipoBloco=="voto":
                v.append({"voto": b.dados})
        return {"votos": v}

#criar metodo para procurar os votos nas chaves 
#completar o metodo contarVotos

    def getNumeros(self):
        tCandidatos = self.getCandidatos()
        numeros = []
                
        for n in tCandidatos["candidatos"]:
            numeros.append(int(n["numero"]))
    
        return numeros
            

    def contarVotos(self):
        votacao = self.getVotos()
        
        for b in votacao["votos"]:
            for c in self.candidatosValidos:
                if b["voto"]==c.numero:
                    c.incrementarVoto()
                
    
    def exportar(self, arquivo):
        f = open(arquivo, "w+")
        dicionarios = []
        
        for b in self.blocks:
            s = {"index": b.index, "tipoBloco": b.tipoBloco, "dados": b.dados,"aleatorio": b.aleatorio, 
                 "nonce": b.nonce, "numero": b.numero, "hash_ant": b.hash_ant, "meu_hash": b.meu_hash}
            dicionarios.append(s)

        dicionario = {"block": dicionarios}
        json.dump(dicionario, f, indent=4)

        f.close()
        