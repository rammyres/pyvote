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
        arquivo = open("block.json")
        blockchain.importar("block.json")
    except IOError:
        blockchain.criarBlocoGenesis()        

    escolha = 0
    
    while escolha != 99:
        escolha = menu()

        if escolha == "1":
            nome = input("Indique o nome do candidato: ")
            numero = input("Indique o numero do candidato: ")
        
            if blockchain.criarCandidato(nome, numero):
                print("Candidato incluido com sucesso")
            else:
                print("Já existe candidato com o mesmo nome e numero, inclusão recusada")
        
        elif escolha == "2":
            tCandidatos = blockchain.getCandidatos()
            
            for d in tCandidatos["candidatos"]:
                print("{} - {}".format(d["numero"], d["dados"]))
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
            blockchain.contarVotos()
            for c in blockchain.candidatosValidos:
                
                print("{} - {}: {} voto(s)".format(c.numero, c.nome, c.votacao))

        elif escolha == "99":
            blockchain.exportar("block.json") 
            quit()

    blockchain.exportar("block.json") 