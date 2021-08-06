from math import sqrt, inf
from random import choice
from time import time
from sys import argv

class Cidade:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
    
class TSP:
    def __init__(self, tipo):
        self.tipo = tipo
        self.rota = []
        self.distancia = 0

    def _distancia(self, cidade_atual, cidade):
        if self.tipo == 'EUC_2D':
            return cidade_atual._distancia_euc_2d(cidade) 
        elif self.tipo == 'ATT':
            return cidade_atual._distancia_att(cidade)

    def _distancia_rota(self, rota):
        distancia = 0
        for i in range(1, len(rota)):
            distancia += self._distancia(rota[i - 1], rota[i])
        distancia += self._distancia(rota[-1], rota[0])
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

    def construtivo(self, cidades, alpha):
        self.rota = []
        cidade_inicial = cidades[0]
        cidades.remove(cidade_inicial)
        self.rota.append(cidade_inicial)
        cidade_atual = cidade_inicial
        while cidades:
            maximo, minimo = 0, inf
            cidades_possiveis = []
            for i in range(len(cidades)):
                distancia = self._distancia(cidade_atual, cidades[i])
                if distancia > maximo:
                    maximo = distancia
                if distancia < minimo:
                    minimo = distancia
            lrc_valor = minimo + (alpha * (maximo - minimo))
            for i in range(len(cidades)):
                if self._distancia(cidade_atual, cidades[i]) <= lrc_valor:
                    cidades_possiveis.append(cidades[i])
            cidade_atual = choice(cidades_possiveis)
            cidades.remove(cidade_atual)
            self.rota.append(cidade_atual)
        self.distancia = self._distancia_rota(self.rota)

    def vnd(self):
        while True:
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
            if not melhora:
                break

    def grasp(self, cidades):
        alpha = 0.01
        melhor_rota = TSP(self.tipo)
        melhor_rota.distancia = inf
        for _ in range(10):
            self.construtivo(cidades.copy(), alpha)
            self.vnd()
            if self.distancia < melhor_rota.distancia:
                melhor_rota.rota = self.rota.copy()
                melhor_rota.distancia = self.distancia
        self.distancia = melhor_rota.distancia
        self.rota = melhor_rota.rota.copy()

def arquivo(nome_arquivo):
    tipo = ''
    cidades = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha_split = linha.split()
            if not linha_split:
                continue
            elif linha_split[0].startswith('EDGE_WEIGHT_TYPE'):
                tipo = str(linha_split[-1])
            elif linha_split[0].isnumeric():
                x = float(linha_split[1])
                y = float(linha_split[2])
                cidades.append(Cidade(x, y))
    return cidades, tipo

nome_arquivo = argv[1]
cidades, tipo = arquivo(nome_arquivo)
start = time()
tsp = TSP(tipo)
tsp.grasp(cidades)
print(f"{nome_arquivo}: {tsp.distancia} - {time() - start:.3f} segundos")
