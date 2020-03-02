#!/usr/bin/env python3
from pyvote import Blockchain

def menu():
    print("Selecione a função:\n01- Cadastrar candidato\n02- Listar Candidatos\n03- Votar\n04- Listar votos\n99- Sair")
    return input("Função: ")

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

        if escolha == "1":
            nome = input("Indique o nome do candidato: ")
            numero = input("Indique o numero do candidato: ")
        
            if blockchain.criarCandidato(nome, numero):
                print("Candidato incluido com sucesso")
            else:
                print("Já existe candidato com o mesmo nome e numero, inclusão recusada")
        
        elif escolha == "2":
            candidatos = blockchain.getCandidatos()
            
            for d in candidatos["candidatos"]:
                print("{} - {}".format(d["numero"], d["dados"]))
        elif escolha == "3":
            candidatos = blockchain.getCandidatos()
            
            for d in candidatos["candidatos"]:
                print("{} - {}".format(d["numero"], d["dados"]))
            v = input("Escolha seu candidato: ")
            if blockchain.validarNumero(v):
                blockchain.votar(v)
                print("Voto computado")
                blockchain.exportar("block.json")
            else: 
                print("Candidato não localizado")

        elif escolha == "99":
            blockchain.exportar("block.json") 
            quit()

    blockchain.exportar("block.json") 