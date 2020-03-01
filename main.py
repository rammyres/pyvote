#!/usr/bin/env python3
from pyvote import Blockchain


if __name__ == '__main__':
    blockchain = Blockchain()

    try:
        arquivo = open("block.json")
        blockchain.importar("block.json")
    except IOError:
        blockchain.criarBlocoGenesis()        

    blockchain.criarNovoBloco('Primeiro bloco!')
    blockchain.criarNovoBloco('Blockchain eh top!')
    blockchain.criarNovoBloco('Mais uma vez!')
    
    blockchain.exportar("block.json") 