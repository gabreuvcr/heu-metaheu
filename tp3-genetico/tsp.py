from random import randint, shuffle
from math import sqrt, inf

class Cidade:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"{self.id}"

    def _distancia_euc_2d(self, c2):
        x_d = self.x - c2.x
        y_d = self.y - c2.y
        d_c1_c2 = int(sqrt(x_d * x_d + y_d * y_d))
        return d_c1_c2

    def _distancia_att(self, c2):
        x_d = self.x - c2.x
        y_d = self.y - c2.y
        r_c1_c2 = sqrt((x_d * x_d + y_d * y_d) / 10.0)
        t_c1_c2 = int(r_c1_c2)
        if t_c1_c2 < r_c1_c2:
            return t_c1_c2 + 1
        else:
            return t_c1_c2
    
    def __eq__(self, outro):
        return self.id == outro.id and self.x == outro.x and self.y == outro.y
    
class TSP:
    def __init__(self, tipo):
        self.tipo = tipo
        self.rota = []
        self.distancia = 0

    def __repr__(self):
        string = "["
        for cidade in self.rota:
            string += f"{cidade};"
        string += "]"
        return string

    def _distancia(self, cidade_atual, cidade):
        if self.tipo == 'EUC_2D':
            return cidade_atual._distancia_euc_2d(cidade) 
        elif self.tipo == 'ATT':
            return cidade_atual._distancia_att(cidade)

    def _distancia_rota(self):
        distancia = 0
        for i in range(1, len(self.rota)):
            distancia += self._distancia(self.rota[i - 1], self.rota[i])
        distancia += self._distancia(self.rota[-1], self.rota[0])
        return distancia

    def _swap(self, i, j):
        while i < j:
            self.rota[i], self.rota[j] = self.rota[j], self.rota[i]
            i += 1
            j -= 1

    def _recalcula_rota(self, i, j):
        distancia = self.distancia
        n = len(self.rota)
        distancia -= self._distancia(self.rota[i - 1], self.rota[j])
        distancia -= self._distancia(self.rota[i], self.rota[(j + 1) % n])
        distancia += self._distancia(self.rota[i - 1], self.rota[i])
        distancia += self._distancia(self.rota[j], self.rota[(j + 1) % n])
        return distancia
    
    # def valida_crossover(self, filho, cidades):
    #     for cidade in filho.rota:
    #         if cidade in cidades:
    #             cidades.remove(cidade)  
    #     for i in range(1, len(filho.rota)):
    #         if filho.rota[i] in filho.rota[:i]:
    #             filho.rota[i] = cidades[0]
    #             cidades.remove(cidades[0])

    def copia(self, tsp):
        copia = TSP(tsp.tipo)
        copia.rota = tsp.rota.copy()
        copia.distancia = tsp.distancia
        return copia

    # def crossover(self, tsp_2, cidades):
    #     filho_1 = self.copia(self)
    #     filho_2 = self.copia(tsp_2)
    #     p_1 = randint(1, len(self.rota) - 1)
    #     p_2 = randint(1, len(self.rota) - 1)
    #     if p_1 > p_2: p_1, p_2 = p_2, p_1
    #     filho_1.rota[p_1:p_2], filho_2.rota[p_1:p_2] = filho_2.rota[p_1:p_2], filho_1.rota[p_1:p_2]

    #     self.valida_crossover(filho_1, cidades.copy())
    #     self.valida_crossover(filho_2, cidades.copy())
    #     filho_1.distancia = filho_1._distancia_rota()
    #     filho_2.distancia = filho_2._distancia_rota()
    #     return filho_1, filho_2

    def crossover(self, pai_2):
        pai_1 = self
        filho = self.copia(self)
        filho_p1, filho_p2 = [], []
        p_1 = randint(1, len(self.rota) - 1)
        p_2 = randint(1, len(self.rota) - 1)
        if p_1 > p_2: p_1, p_2 = p_2, p_1
        for i in range(p_1, p_2):
            filho_p1.append(pai_1.rota[i])
        filho_p2 = [cidade for cidade in pai_2.rota if cidade not in filho_p1]
        filho.rota = filho_p1 + filho_p2
        filho.distancia = filho._distancia_rota()
        return filho

    def mutacao(self):
        filho = self.copia(self)
        i = randint(0, len(filho.rota) - 1)
        j = randint(0, len(filho.rota) - 1)
        while i == j: j = randint(0, len(filho.rota) - 1)
        if i > j: i , j = j, i
        filho._swap(i, j)
        filho.distancia = filho._recalcula_rota(i, j)
        return filho
    
    def aleatorio(self, cidades):
        shuffle(cidades)
        self.rota = cidades.copy()
        self.distancia = self._distancia_rota()
        return self

    def construtivo(self, cidades):
        num = randint(0, len(cidades) - 1)
        cidade_inicial = cidades[num]
        cidades.remove(cidade_inicial)
        self.rota.append(cidade_inicial)
        cidade_atual = cidade_inicial
        while cidades:
            menor_distancia, menor_cidade= inf, None
            for cidade in cidades:
                nova_distancia = self._distancia(cidade_atual, cidade)
                if menor_distancia > nova_distancia:
                    menor_distancia, menor_cidade = nova_distancia, cidade
            cidade_atual = menor_cidade
            cidades.remove(cidade_atual)
            self.rota.append(cidade_atual)
        self.distancia = self._distancia_rota()
        return self

    def vnd(self, cidades):
        self.construtivo(cidades)
        # while True:
        melhora = False
        for i in range(0, len(self.rota) - 1):
            for j in range(i + 1, len(self.rota)):
                self._swap(i, j)
                nova_distancia = self._recalcula_rota(i, j)
                if nova_distancia < self.distancia:
                    melhora = True
                    self.distancia = nova_distancia
                    break
                self._swap(i, j)
            if melhora:
                break
            # if not melhora:
            #     break
        return self
