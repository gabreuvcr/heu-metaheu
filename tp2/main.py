from math import sqrt, inf
from time import time
from sys import argv

class Ponto:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"{self.id}"

    def _distancia_euc_2d(self, p2):
        x_d = self.x - p2.x
        y_d = self.y - p2.y
        d_p1_p2 = int(sqrt(x_d * x_d + y_d * y_d))
        return d_p1_p2

    def _distancia_att(self, p2):
        x_d = self.x - p2.x
        y_d = self.y - p2.y
        r_p1_p2 = sqrt((x_d * x_d + y_d * y_d) / 10.0)
        t_p1_p2 = int(r_p1_p2)
        if t_p1_p2 < r_p1_p2:
            return t_p1_p2 + 1
        else:
            return t_p1_p2
    
class TSP:
    def __init__(self, tipo):
        self.tipo = tipo
        self.rota = []
        self.distancia = 0
        self.ponto_inicial = None

    def _distancia(self, ponto_atual, ponto):
        if self.tipo == 'EUC_2D':
            return ponto_atual._distancia_euc_2d(ponto) 
        elif self.tipo == 'ATT':
            return ponto_atual._distancia_att(ponto)

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

    def _executa_construtivo(self, pontos):
        self.ponto_inicial = pontos[0]
        pontos.remove(self.ponto_inicial)
        self.rota.append(self.ponto_inicial)
        ponto_atual = self.ponto_inicial
        while pontos:
            menor_distancia, menor_ponto= inf, None
            for ponto in pontos:
                nova_distancia = self._distancia(ponto_atual, ponto)
                if menor_distancia > nova_distancia:
                    menor_distancia, menor_ponto = nova_distancia, ponto
            ponto_atual = menor_ponto
            pontos.remove(ponto_atual)
            self.rota.append(ponto_atual)
        self.distancia = self._distancia_rota(self.rota)
        print(f"Construtivo: {self.distancia}")

    def _executa_vnd(self):
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
        print(f"VND: {self.distancia}") 

    def calcula(self, pontos):
        self._executa_construtivo(pontos)
        self._executa_vnd()

def arquivo(nome_arquivo):
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
                id = int(linha_split[0])
                x = float(linha_split[1])
                y = float(linha_split[2])
                pontos.append(Ponto(id, x, y))
    return pontos, tipo

nome_arquivo = argv[1]
pontos, tipo = arquivo(nome_arquivo)
start = time()
tsp = TSP(tipo)
tsp.calcula(pontos)
print(tsp.rota)
print(f"\n{nome_arquivo[7:]}: {tsp.distancia} - {time() - start:.3f} segundos")
