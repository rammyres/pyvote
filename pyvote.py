'''
Classe principal, que a abstrai a blockchain pyvote e suas principais ferramentas
'''

from block import Block
from erros import hashAnteriorInvalido
from candidato import Candidato
import random, os, codecs, json

class Blockchain:

    def __init__(self):
        self.blocks = [] #A blockchain é uma cadeia de blocos, que será abstraido na execução por uma lista
        self.candidatosValidos = [] #Para acesso simplificado e controle nas votações, utilizamos uma lista
                                    #com os candidatos, seus números e a votação (iniciada em 0 por padrão)

    def criarBlocoGenesis(self):
        #Cria o bloco Gênesis. O bloco gênesis, em versões posteriores o bloco conterá dados necessários a 
        #execução e controle da blockchain. Por hora provê uma "ancôra" para a blockchain. 
        blocoGenesis = Block(0, "Genesis", 0, "Bloco genesis", 0, 0) #Instância um bloco como gênesis
        self.blocks.append(blocoGenesis) #Inclui o o bloco genêsis na lista de blocos 

    def criarCandidato(self, nome, numero):
        if not self.validarNome(nome):
            if not self.validarNumero(numero):
                
                tCandidato = Block(0, "candidato", len(self.blocks), nome, self.blocks[len(self.blocks)-1].meu_hash, numero)
                self.blocks.append(tCandidato)

                d = Candidato(nome, numero)
                self.candidatosValidos.append(d)

                self.exportar("block.json")

                return True

            else:
                return False
        else:
            return False

    def votar(self, dados):
        novoBlock = Block(0, "voto", len(self.blocks), dados, self.blocks[len(self.blocks)-1].meu_hash)
        self.blocks.append(novoBlock)

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
        return False
    
    def validarNome(self, nome):
        for c in self.candidatosValidos:
            if nome==c.nome:
                return True
            else:
                return False
    
    def importar(self, arquivo):
        f = open(arquivo,"r+")
        dicionarios = json.load(f)
        for d in dicionarios["block"]:
            
            if d["tipoBloco"]=="Genesis":
                bloco = Block(1, "Genesis", 0, "Bloco genesis", d["hash_ant"], d["numero"], d["aleatorio"],  d["nonce"], d["meu_hash"])
            else:
                bloco = Block(1, d["tipoBloco"], d["index"], d["dados"], d["hash_ant"], d["numero"], d["aleatorio"],  d["nonce"], d["meu_hash"])

            if len(self.blocks) == 0:
                pass
            elif bloco.tipoBloco == "Genesis" and bloco.hash_ant != self.blocks[len(self.blocks)-1].meu_hash:
                raise hashAnteriorInvalido
            self.blocks.append(bloco)

            if d["tipoBloco"]=="candidato":
                c = Candidato(d["dados"], d["numero"])
                c.votacaoApurada = False
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
        votacao = self.getVotos()["votos"]
        
        for x in range(0, len(self.candidatosValidos)):
            if not self.candidatosValidos[x].votacaoApurada: 
                for b in votacao:
                    if b["voto"]==str(self.candidatosValidos[x].numero):
                        self.candidatosValidos[x].votacao += 1

        for x in range(0, len(self.candidatosValidos)):
            self.candidatosValidos[x].votacaoApurada = True
                    
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
        