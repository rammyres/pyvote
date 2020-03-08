'''
Abstração dos erros esperados, não especificados no Python

'''

class Erros(Exception):
    #Erro base
    pass

class erroGenericoGenesis(Erros):
    # Caso a criação do bloco gênesis receba um número maior que 0 como parâmetro
    
    def __init__(self):
        self.message = "O bloco genesis deve conter dados \'Bloco genesis\' e demais variáveis iguais a 0"

class tipoDeBlocoInvalido(Erros):
    # Especifica o erro no caso da inclusão de um tipo de bloco inválido na bloco

    def __init__(self):
        self.message = "O tipo de bloco deve ser \'Genesis\', \'voto\' ou \'candidato\'"

class hashAnteriorInvalido(Erros):
    # Erro de importação, no caso de conflito de bloco, no caso dele não conter
    # um hash válido referente ao último bloco carregado
    
    def __init__(self):
        self.message = "O bloco atual não contém um hash válido para o bloco anterior"

class vatoNaoPodeConterNumero(Erros):
    # Erro de importação de blocos de voto, caso os mesmos contenham os dados no 
    # campo número, ao invés do campo dados. 

    def __init__(self):
        self.message = "O voto não pode contar número"

class modoDeInclusaoInvalido(Erros):
    # Caso haja instanciamento em modo inclusão

    def __init__(self):
        self.message = "No instanciamento de novos blocos não pode haver a inclusão de nonce, hash ou aleatorio"