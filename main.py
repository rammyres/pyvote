#!/usr/bin/env python3

"""
Módulo princial do pyvote. Basicamente cria a interface com o usuário e trabalha a blockchain
a partir dos tipos abstratos delimitados nas classes Blockchain, Block e Candidato
"""
import colorama 
from colorama import Fore, Style, Back, init # Permite a colorização das saidas
from pyvote import Blockchain # Importa a classe principal 

colorama.init(autoreset=True) # Inicia o colorama com retorno as cores padrões após a impressão 

def menu():
    # Colhe a escolha do usuário

    print(f"\n{Fore.BLUE}{Style.BRIGHT}Selecione a função:")
    print("01- Cadastrar candidato\n02- Listar Candidatos\n03- Votar\n04- Listar votos\n99- Sair")
    try:
        return int(input("Função: "))
    except ValueError:
        print(f"{Fore.RED}{Style.BRIGHT}Você deve digitar o número da função desejada")

def listaCandidatos():
    if len(blockchain.candidatosValidos)>0: # Verifica se existem candidatos cadastrados
        for d in blockchain.candidatosValidos: # Itera com os candidatos válidos no sistema e imprime a lista 
            print("{} - {}".format(d.numero, d.nome)) 
        return True

    else: # Caso não existam candidatos, o usuário é informado 
        print(f"{Back.WHITE}{Fore.BLACK}Não existem candidatos cadastrados") 
        return False


if __name__ == '__main__':
    blockchain = Blockchain() # Instancia a blockchain na memória 

    print(f"{Style.BRIGHT}{Fore.BLUE}Bem vindo ao sistema sistema PyVote")   

    try:
        blockchain.importar("blockchain.json") # Tenta importar a persistência da blockchain, se existente 
    
    except IOError:
        # Caso não exista uma blockchain persistida, gera uma nova, criando o bloco genesis
        print(f"{Back.BLUE}{Fore.WHITE}{Style.BRIGHT}Blockchain não localizada, criando o bloco Gênesis")
        blockchain.criarBlocoGenesis()        

    escolha = 0
    
    while escolha != 99:
        escolha = menu()

        if escolha == 1:
            #Inicia o modo de inclusão de candidatos, somente um candidato pode ser incluido por vez

            while True:
                try:
                    numero = str(int(input("Indique o numero do candidato: "))) # Testa se a entrada é um numero e converte em
                                                                                # string, para otimizar o amarzenamento no
                                                                                # dicionário durante a exportação
                    break
                except ValueError: # Na hipótese do usuário não entrar com um inteiro o erro alerta ao usuário 
                    print(f"{Back.WHITE}{Fore.BLACK}Você deve entrar um numero inteiro") 
                
            nome = input("Indique o nome do candidato: ") # Recebe o nome do usuário 
            
        
            if blockchain.criarCandidato(nome, numero): # Cria um objeto candidato e inclui na blockchain
                print(f"{Back.WHITE}{Fore.BLACK}Candidato incluido com sucesso")
            else: # Caso o usuário tente incluir dados repetidos, a inclusão é recusada e o usuário é alertado 
                print(f"{Back.WHITE}{Fore.BLACK}Já existe candidato com o mesmo nome ou numero, inclusão recusada")
        
        elif escolha == 2:
            #Lista os candidatos existentes 
            listaCandidatos()

        elif escolha == 3:
            #Permite que o usuário escolha um candidato na lista apresentada e vote 

            if listaCandidatos(): # Se existirem candidatos validos, o usuário poderá votar 

                while True:
                    try:
                        v = str(int(input("Escolha seu candidato: "))) # Evita que o usuário informe não inteiros 
                        break
                    except ValueError:
                        print(f"{Back.WHITE}{Fore.BLACK}Você deve entrar o número do candidato")

                if blockchain.validarNumero(v): # Valida o numero recebido
                    blockchain.votar(v) # Caso positivo insere o voto na blockchain
                    
                    # Altera o status da votação do candidato que recebeu o voto, a fim de indicar que 
                    # o número de votos deverá ser atualizado 
                    for c in range(0, len(blockchain.candidatosValidos)):
                        if v == blockchain.candidatosValidos[c].numero:
                            blockchain.candidatosValidos[c].votacaoApurada == False

                    print(f"{Back.WHITE}{Fore.BLACK}Voto computado")
                    blockchain.exportar("blockchain.json") # Persiste a blockchain a fim de evitar perda dos dados 

                else: 
                    print("Candidato não localizado") # Caso o número não seja localizado, o usuário é informado 
            else:
                print(f"{Back.WHITE}{Fore.BLACK}Não existem candidatos cadastrados") # Caso não existam candidatos no sistema 
                                                                                     # o usuário e informado
        
        elif escolha == 4:
            # Atualiza a contagem de votos dos candidatos que receberam votos ainda não computados e 
            # imprime o numero de votos de cada candidato na lista 

            if len(blockchain.candidatosValidos)>0: # O processo só se inicia se existir pelo menos 1 candidato válido
                
                blockchain.contarVotos() # Atualiza os votos dos candidatos com votos ainda não computados 
                
                for c in blockchain.candidatosValidos: # Imprime a lista dos candidatos e os votos recebidos 
                    print("{} - {}: {} voto(s)".format(c.numero, c.nome, c.votacao))
            
            else:
                print(f"{Back.WHITE}{Fore.BLACK}Não existem cadidatos cadastrados") # Caso não existam candidatos no sistema, o usuário é informado

        elif escolha == 99:
            #Interrompe o programa, após a exportação da blockchain
            
            blockchain.exportar("blockchain.json") 
            quit()
        
        else:
            # Retorna ao inicio do loop 
            print(f"{Back.WHITE}{Fore.BLACK}Escolha uma opção válida") 