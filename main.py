#!/usr/bin/env python3
from transacoes import Transacoes, tCandidato, tVoto
from merkle import No, Arvore
from random import randint

if __name__ == '__main__':
    arvore = Arvore()

    tRaiz = Transacoes()
    tRaiz.criarTransacaoRaiz()

    raiz = No(tRaiz)
    t1 = tCandidato("Fulano", "10", 1)
    t2 = tCandidato("Sicrano", "20", 1)
    t3 = tCandidato("Beltrano", "30", 1)

    arvore.inserir(raiz)

    no1 = No(t1)
    no2 = No(t2)
    no3 = No(t3)

    arvore.inserir(no1)
    arvore.inserir(no2)
    arvore.inserir(no3)

    for i in range(0,20):
        x = randint(0, 3000)
        if x>0 and x<1000:
            t = tVoto("10")
        elif x>1000 and x<2000:
            t=tVoto("20")
        elif x>2000:
            t=tVoto("30")
        v=No(t)
        arvore.inserir(v)

    arvore.imprimirArvore(arvore.raiz)