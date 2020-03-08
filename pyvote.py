'''
Classe principal, que a abstrai a blockchain pyvote e suas principais ferramentas
'''

from block import Block
from erros import hashAnteriorInvalido
from candidato import Candidato
import random, os, codecs, json

class Blockchain:

    def __init__(self):
        self.blocks = [] # A blockchain é uma cadeia de blocos, que será abstraido na execução por uma lista
        self.candidatosValidos = [] # Para acesso simplificado e controle nas votações, utilizamos uma lista
                                    # com os candidatos, seus números e a votação (iniciada em 0 por padrão)

    def criarBlocoGenesis(self):
        # Cria o bloco Gênesis. O bloco gênesis, em versões posteriores o bloco conterá dados necessários a 
        # execução e controle da blockchain. Por hora provê uma "ancôra" para a blockchain. 
        blocoGenesis = Block(0, "Genesis", 0, "Bloco genesis", 0, 0) # Instância um bloco como gênesis
        self.blocks.append(blocoGenesis) # Inclui o o bloco genêsis na lista de blocos 

    def criarCandidato(self, nome, numero):
        # Cria um candidato com os dados recebidos como parâmetro (nome e número)
        if not self.validarNome(nome): # Caso já exista outro candidato com o mesmo nome a inclusão é recusada 
            if not self.validarNumero(numero): # Caso já exista outro candidato com o mesmo número a inclusão é recusada
                
                # Cria um candidato temporário, que será anexado ao bloco 
                tCandidato = Block(0, "candidato", len(self.blocks), nome, self.blocks[len(self.blocks)-1].meu_hash, numero)
                self.blocks.append(tCandidato)

                # Para facilitar o trabalho de contagem de voto e acesso aos dados, eles são registrados em uma lista de 
                # candidatos temporários, que não são persistidos, mas existem na memória durante a execução. 
                d = Candidato(nome, numero)
                self.candidatosValidos.append(d)

                # Persiste os dados atuais da blockchain
                self.exportar("blockchain.json")

                # Caso tudo ocorra ok
                return True

            else:
                return False
        else:
            return False

    def votar(self, dados):
        # Função base de votação, recebe o número votado e persiste o mesmo na blockchain

        voto = Block(0, "voto", len(self.blocks), dados, self.blocks[len(self.blocks)-1].meu_hash)
        self.blocks.append(voto)
        self.exportar("blockchain.json")

    def procurarCandidato(self, nome, numero):
        # Permite a busca pelo nome e número do candidato, caso ele exista retorna verdadeiro e interrompe a busca
        for c in self.candidatosValidos:
            if nome==c.nome and numero==c.numero:
                return True
            else:
                return False
    
    def validarNumero(self, numero):
        # Procura o número do candidato na blockchain, caso seja localizado retorna verdadeiro e interrompe a busca 
        for c in self.candidatosValidos:
            if numero==c.numero:
                return True
        return False
    
    def validarNome(self, nome):
        # Procura o nome do candidato na blockchain, caso seja localizado retorna verdadeiro e interrompe a busca 
        for c in self.candidatosValidos:
            if nome==c.nome:
                return True
            else:
                return False
    
    def importar(self, arquivo):
        # Importa o arquivo persistido da blockchain, em formato json
        
        f = open(arquivo,"r")
        
        dicionarios = json.load(f) # O arquivo aberto é carregado como uma lista de dicionários aninhados,
                                   # onde cada dicionário representa um bloco
        
        for d in dicionarios["blockchain"]: #O dicionário raiz tem como dados "blockchain" como identificador
            
            # Os dicionários brutos são importados individualmente
            bloco = Block(1, d["tipoBloco"], d["index"], d["dados"], d["hash_ant"], d["numero"], d["aleatorio"],  d["nonce"], d["meu_hash"])

            # No bloco genesis não há teste do hash
            if len(self.blocks) == 0:
                pass

            # Para os demais blocos há o teste de validação do bloco, caso o bloco atual possua um registro
            # diferente do bloco anterior o programa é interrompido por erro 
            elif bloco.tipoBloco != "Genesis" and bloco.hash_ant != self.blocks[len(self.blocks)-1].meu_hash:
                raise hashAnteriorInvalido

            # O bloco é anexado a blocochain
            self.blocks.append(bloco)

            # Caso os dados importados na iteração atual seja referente a um candidato, os dados são carregados
            # na lista de candidatos atualmente existentes 
            if d["tipoBloco"]=="candidato":
                c = Candidato(d["dados"], d["numero"])
                c.votacaoApurada = False
                self.candidatosValidos.append(c)

    def getCandidatos(self):
        # Retorna os dados brutos dos candidatos, na forma de uma lista de dicionários aninhados 
        c = []
        for b in self.blocks:
            
            if b.tipoBloco == "candidato":
                c.append({"numero": b.numero, "dados": b.dados})

        if len(c)>0:
            return {"candidatos": c}
        else:
            return None

    def getVotos(self):
        # Retorna os dados brutos dos votos, na forma de uma lista de dicionários aninhados 
        v = []
        for b in self.blocks:
            if b.tipoBloco=="voto":
                v.append({"voto": b.dados})
        return {"votos": v}

    def getNumeros(self):
        # Retora uma lista contendo os numeros dos candidatos 
        tCandidatos = self.getCandidatos()
        numeros = []
                
        for n in tCandidatos["candidatos"]:
            numeros.append(int(n["numero"]))
    
        return numeros
            

    def contarVotos(self):
        # Efetua a atualização da votação dos candidtados. Cada objeto Candidaato possui um atributo votacao e um
        # votacaoApurada. O primeiro registra os votos recebidos, o segundo se os votos já foram apurados 
        votacao = self.getVotos()["votos"] #recebe os votos como uma lista de dicionários aninhados 
        
        for x in range(0, len(self.candidatosValidos)): # Apesar do loop for no python conseguir iterar em lista 
                                                        # sem necessidade de contagem pelo indice, o método não é
                                                        # o mais adequado, pois causa um bug que só permite a 
                                                        # apuração do primeiro item da lista. 

            if not self.candidatosValidos[x].votacaoApurada: # Caso o candidato ainda não tenha os votos apurados, os votos existentes 
                                                             # são comparados com os candidatos e, em caso positivo, o numero é atualizado
                for b in votacao:
                    if b["voto"]==str(self.candidatosValidos[x].numero):
                        self.candidatosValidos[x].votacao += 1

        for x in range(0, len(self.candidatosValidos)): # 'Reseta' o estado da apuração nas votações de todos os cadidatos
            self.candidatosValidos[x].votacaoApurada = True 
                    
    def exportar(self, arquivo):
        # Exposta o estado atual da blockchain, coletada como uma lista de dicionários aninhados e salva como um arquivo json, com
        # o nome recebido como parametro
        f = open(arquivo, "w+")
        dicionarios = [] # Cria a lista de dicionários aninhados 
        
        for b in self.blocks: # Todos os dicionáios (blocos) são anexados a lista
            s = {"index": b.index, "tipoBloco": b.tipoBloco, "dados": b.dados,"aleatorio": b.aleatorio, 
                 "nonce": b.nonce, "numero": b.numero, "hash_ant": b.hash_ant, "meu_hash": b.meu_hash}
            dicionarios.append(s)
    
        dicionario = {"blockchain": dicionarios} # Os dicionários são identificado em um dicionário contendo
                                                 # os dicionários aninhados 
        json.dump(dicionario, f, indent=4) # Os dicionários (blocos) são exportados como um arquivo json identado

        f.close()
        