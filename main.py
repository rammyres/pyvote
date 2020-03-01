#!/usr/bin/env python3
from pyvote import Blockchain

def menu():
    print("Selecione a função:\n1- Cadastrar candidato\n2- Listar Candidatos\n3- Votar\n4- Listar votos\n99- Sair")
    return input("Função: ")



def votar():
    print("Registre seu voto: ")



if __name__ == '__main__':
    blockchain = Blockchain()

    try:
        arquivo = open("block.json")
        blockchain.importar("block.json")
    except IOError:
        blockchain.criarBlocoGenesis()        


    escolha = 0
    
    while escolha != 99:
        escolha = menu()
        if escolha == 1:
            nome = input("Indique o nome do candidato: ")
            numero = input("Indique o numero do candidato: ")
        
            blockchain.criarCandidato(nome, numero)

        

    blockchain.votar('Primeiro bloco!')
    blockchain.votar('Blockchain eh top!')
    blockchain.votar('Mais uma vez!')
    
    blockchain.exportar("block.json") 