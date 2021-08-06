from populacao import Populacao
from tsp import Cidade
from time import time
from sys import argv

POPULACAO = 250
GERACOES = 300
CROSS = 0.99
MUT = 0.35
TORNEIO = 7
ELITISMO = True

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
                id = int(linha_split[0]) - 1
                x = float(linha_split[1])
                y = float(linha_split[2])
                cidades.append(Cidade(id, x, y))
    return cidades, tipo

nome_arquivo = argv[1]
CIDADES, tipo = arquivo(nome_arquivo)
start = time()
pop = Populacao(POPULACAO, GERACOES, CROSS, MUT, TORNEIO, ELITISMO)
melhor = pop.evoluir(tipo, CIDADES)
print(f"\n{nome_arquivo[7:]}: {melhor.distancia} {time() - start:.3f} segundos")
