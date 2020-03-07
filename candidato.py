'''
Abstração do candidato, com informações simplificadas.
A classe só é usada durante operação do programa e não é persistida na blockchain.
'''
class Candidato:
    nome = None #Irá registrar o nome
    numero = None #Irá registrar o nome 
    votacao = 0 #O numero padrão após a instação do objeto é 0, a contagem de votos
                #Só realizada através do método incrementarVoto
    votacaoApurada = False #Status da votação

    def __init__(self, nome, numero):
        self.nome=nome
        self.numero=numero

    def incrementarVoto(self):
        self.votacao+=1
        
    def __eq__(self, other):
        if self.nome==other.nome and self.numero==other.numero:
            return True
        else:
            return False

    def __hash__(self):
        return hash(("nome", self.nome, "numero", self.numero))