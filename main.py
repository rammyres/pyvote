#!/usr/bin/env python3
import colorama
from pyvote import Blockchain
from colorama import Fore, Style, Back, init

colorama.init(autoreset=True)

def menu():
    print(f"\n{Fore.BLUE}{Style.BRIGHT}Selecione a função:")
    print("01- Cadastrar candidato\n02- Listar Candidatos\n03- Votar\n04- Listar votos\n99- Sair")
    return input("Função: ")

if __name__ == '__main__':
    blockchain = Blockchain()
    

    print(f"{Style.BRIGHT}{Fore.BLUE}Bem vindo ao sistema sistema PyVote")   

    try:
        blockchain.importar("block.json")
    except IOError:
        print(f"{Back.BLUE}{Fore.WHITE}{Style.BRIGHT}Blockchain não localizada, criando o bloco Gênesis")
        blockchain.criarBlocoGenesis()        

    escolha = 0
    
    while escolha != 99:
        escolha = menu()

        if escolha == "1":
            teste = True
            while teste:
                try:
                    numero = str(int(input("Indique o numero do candidato: ")))
                    teste = False
                except ValueError:
                    print("Você deve entrar um numero inteiro")
                
            nome = input("Indique o nome do candidato: ")
            
        
            if blockchain.criarCandidato(nome, numero):
                print("Candidato incluido com sucesso")
            else:
                print(f"{Back.WHITE}Já existe candidato com o mesmo nome ou numero, inclusão recusada")
        
        elif escolha == "2":
            tCandidatos = blockchain.getCandidatos()
            
            if tCandidatos:
                for d in tCandidatos["candidatos"]:
                    print("{} - {}".format(d["numero"], d["dados"]))
            else:
                print("Não existem candidatos cadastrados")
        elif escolha == "3":
            tCandidatos = blockchain.getCandidatos()
            
            for d in tCandidatos["candidatos"]:
                print("{} - {}".format(d["numero"], d["dados"]))
            v = input("Escolha seu candidato: ")
            if blockchain.validarNumero(v):
                blockchain.votar(v)
                print("Voto computado")
                blockchain.exportar("block.json")
            else: 
                print("Candidato não localizado")
        
        elif escolha == "4":

            if len(blockchain.candidatosValidos)>0:
                blockchain.contarVotos()
                for c in blockchain.candidatosValidos:
                    print("{} - {}: {} voto(s)".format(c.numero, c.nome, c.votacao))
            else:
                print("Não existem cadidatos cadastrados")

        elif escolha == "99":
            blockchain.exportar("block.json") 
            quit()

    blockchain.exportar("block.json") 