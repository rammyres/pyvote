#!/usr/bin/env python3
from transacoes import Transacoes, tCandidato, tVoto
from merkle import No, Arvore

if __name__ == '__main__':
    arvore = Arvore()

    tRaiz = Transacoes()
    tRaiz.criarTransacaoRaiz()

    raiz = No(tRaiz)
    t1 = tCandidato("Fulano", "10", 1)
    t2 = tCandidato("Sicrano", "20", 1)
    t3 = tCandidato("Beltrano", "30", 1)
    t4 = tVoto("10")

    arvore.inserir(raiz)

    no1 = No(t1)
    no2 = No(t2)
    no3 = No(t3)
    no4 = No(t4)

    arvore.inserir(no1)
    arvore.inserir(no2)
    arvore.inserir(no3)
    arvore.inserir(no4)

    arvore.imprimirArvore(arvore.raiz)
    #arvore.imprimirBFS(arvore.raiz)