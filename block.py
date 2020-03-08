"""
Abstrai os blocos, permintindo sua instaciação como objeto da blockchain 
e permite operações básicas do seu funcionamento, como a criação de 
assinaturas (hashs) e 
"""

from erros import erroGenericoGenesis, vatoNaoPodeConterNumero, tipoDeBlocoInvalido, modoDeInclusaoInvalido
from hashlib import sha256
import os, codecs

class Block:
    index = None #Indice do bloco
    tipoBloco = None #Definição do tipo de bloco
    dados = None #dados contidos no bloco
    aleatorio = None #Numero aleatório unico para cada bloco, gerado na criação do mesmo
                     #uma das ideias é evitar a probabilidade de colisão, já que exige 
                     # um elemento aleatório na formação dos dados 
    nonce = None #Número único na blockchain 
    numero = None #Usado exclusivamente para instâncias "Candidato" dos blocos
    hash_ant = None #Hash do bloco anterior ao atual
    meu_hash = None #Hash do bloco atual

    def __init__(self, modo, tipo, index, dados, hash_anterior, numero = None, aleatorio = None, nonce = None, meuhash = None):
        # O construtor dessa classe é sobrecarregado, permitindo instanciar em modo de inclusão (modo == 0) ou modo de importação
        # (modo == 1). No caso do instanciamento em modo de importação, todos os dados devem ser recebidos e a classe faz poucas
        # validações (basicamente dos tipo de bloco em importação). Uma das sobrecargas permite que omita-se o numero, para a 
        # inclusão de blocos de votos
        if modo == 1: # Instanciamento em modo de importação
            if tipo == "Genesis" or tipo == "candidato" or tipo == "voto":
                # Caso o bloco tenha um tipo valido ele é importado integralmente 
                self.index = index
                self.tipoBloco = tipo
                self.dados = dados 
                self.aleatorio = aleatorio
                self.nonce = nonce
                self.numero = numero
                self.hash_ant = hash_anterior
                self.meu_hash = meuhash

            else:
                # Caso não tenha um tipo valido de bloco levanta um erro 
                raise tipoDeBlocoInvalido
        
        elif modo == 0:
            # No modo de inclusão de bloco, dados gerados aleatoriamente (aleatorio e nonce)
            # e a assinatura (meu_hash) são gerados pelo método crieMeuHash().

            if aleatorio != None or nonce != None or meuhash != None:
                raise modoDeInclusaoInvalido # Caso haja instanciamento em metodo de inclusão, com
                                             # parametros aleatórios passados ao construtor o erro
                                             # modoDeInclusaoInvalido é levantado
            if tipo == "Genesis" or tipo == "candidato" or tipo == "voto": # Valida o tipo de bloco gerado
                self.index = index 
                self.tipoBloco = tipo
                self.dados = dados
                
                if tipo == "voto":
                    if tipo == "voto" and numero != None: # Valida se o construtor recebeu um numero, caso o bloco 
                                                          # seja um voto
                        raise vatoNaoPodeConterNumero
                    else:
                        self.numero = "0"

                else:
                    self.numero = numero # Para inclusão e candidato, o numero é recebido no construtor
                
                self.hash_ant = hash_anterior
                self.aleatorio = codecs.encode(os.urandom(32), 'hex').decode() # Gera um hexadecimal aleatório, aumentando a dificuldade
                                                                               # para quebra da assinatura dos blocos
                self.crieMeuHash() # Gera o número único (nonce) e a assinatura (hash) do bloco

            else:
                raise tipoDeBlocoInvalido


        #No constutor da classe somente os tipos candidato, voto e genesis são aceitos

        if tipo == "Genesis" and dados!="Bloco genesis": # Verifica se o bloco Genesis foi bem formado 
            raise erroGenericoGenesis


    def temHashValido(self, hash):
        #Basicamente define a dificuldade da blockchain. 
        #No calculo do bloco somente quando o nonce calculado permitir que o 
        #hash do bloco atual começar com '0000' ele poderá ser adicionado. 
        return hash.startswith('0000')


    def crieMeuHash(self):
        #Utiliza os dados do bloco atual para gerar seu hash
        #Caso o número único (nonce) não gere um hash com a dificuldade apresentada
        #ele é incrementado e o procedimento desta função é refeito
        hash = '' #Define a variável hash
        self.nonce = 1 #Inicializa o nonce com 1
        while not self.temHashValido(hash):
            block = '{}:{}:{}:{}:{}:{}'.format(
                self.index, self.dados, self.aleatorio, self.nonce, self.numero, self.hash_ant 
            ) #Utiliza os dados do bloco como uma string contendo os numeros em sequência
            hash = sha256(block.encode()).hexdigest() #e gera um hash sha256 hexadecimal 
            self.nonce += 1 #incrementa o nonce antes do próximo teste

        self.meu_hash = hash #Caso o hash produzido atenda ao critério de dificuldade o hash é gerado