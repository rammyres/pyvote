class Candidato:
    nome = None
    numero = None
    votacao = 0

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