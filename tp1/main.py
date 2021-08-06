from math import sqrt, inf
from random import randint
from time import time
from sys import argv

class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class TSP:
    def __init__(self, pontos, tipo):
        self.pontos = pontos
        self.tipo = tipo
        self.distancia = 0
        self.ponto_inicial = None

    def _distancia_att(self, p1, p2):
        x_d = p1.x - p2.x
        y_d = p1.y - p2.y
        r_p1_p2 = sqrt((x_d * x_d + y_d * y_d) / 10.0)
        t_p1_p2 = int(r_p1_p2)
        if t_p1_p2 < r_p1_p2:
            return t_p1_p2 + 1
        else:
            return t_p1_p2
    
    def _distancia_euc_2d(self, p1, p2):
        x_d = p1.x - p2.x
        y_d = p1.y - p2.y
        d_p1_p2 = int(sqrt(x_d * x_d + y_d * y_d))
        return d_p1_p2

    def _distancia(self, ponto_atual, ponto):
        if self.tipo == 'EUC_2D':
            return self._distancia_euc_2d(ponto_atual, ponto) 
        elif self.tipo == 'ATT':
            return self._distancia_att(ponto_atual, ponto) 

    def _executa(self):
        ponto_atual = self.ponto_inicial
        while self.pontos:
            menor_distancia = inf
            menor_ponto = None
            for ponto in pontos:
                dist = self._distancia(ponto_atual, ponto)
                if menor_distancia > dist:
                    menor_distancia = dist
                    menor_ponto = ponto
            ponto_atual = menor_ponto
            self.pontos.remove(ponto_atual)
            self.distancia += menor_distancia
        #custo da volta para o ponto de origem
        dist = self._distancia(ponto_atual, self.ponto_inicial)
        self.distancia += dist
        print(self.distancia)

    def calcula(self):
        ponto_aleatorio = randint(0, len(self.pontos) - 1)
        self.ponto_inicial = pontos[ponto_aleatorio]
        pontos.remove(pontos[ponto_aleatorio])
        self._executa()

start = time()     
nome_arquivo = argv[1]
tipo = ''
pontos = []
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
            pontos.append(Ponto(x, y))

tps = TSP(pontos, tipo)
print(f"{nome_arquivo}: ", end='')
tps.calcula()
end = time()
print(end - start)
