from random import sample, random
from tsp import TSP

class Populacao:
    def __init__(self, num_populacao, geracoes, prop_cross, prop_mut, k_torneio, elitismo):
        self.individuos = []
        self.POPULACAO = num_populacao
        self.GERACOES = geracoes
        self.PROP_CROSS = prop_cross
        self.PROP_MUT = prop_mut
        self.TORNEIO = k_torneio
        self.ELITISMO = elitismo

    def melhor_individuo(self):
        melhor = self.individuos[0]
        for ind in self.individuos:
            if ind.distancia < melhor.distancia:
                melhor = ind
        return melhor

    def pior_individuo(self):
        pior = self.individuos[0]
        for ind in self.individuos:
            if ind.distancia > pior.distancia:
                pior = ind
        return pior

    def media_individuos(self):
        soma = 0
        for ind in self.individuos:
            soma += ind.distancia
        return soma / len(self.individuos)
    
    def torneio(self):
        individuos_torneio = sample(self.individuos, self.TORNEIO)
        vencedor = individuos_torneio[0]
        for ind in individuos_torneio:
            if ind.distancia < vencedor.distancia:
                vencedor = ind
        return vencedor
    
    def nova_populacao(self):
        if self.ELITISMO:
            elite = self.melhor_individuo()
            nova_pop = [elite]
        else:
            nova_pop = []
        while len(nova_pop) < self.POPULACAO:
            vencedor_1, vencedor_2 = self.torneio(), self.torneio()
            prop_mut_1, prop_cross = random(), random()
            if self.PROP_CROSS >= prop_cross:
                filho_1 = vencedor_1.crossover(vencedor_2)
                nova_pop.append(filho_1)
                if self.PROP_MUT >= prop_mut_1:
                    filho_1 = filho_1.mutacao()
                nova_pop.append(filho_1)
        self.individuos = nova_pop

    def populacao_inicial(self, tipo, cidades):
        pop_construtivo = int(self.POPULACAO * 0.15) 
        pop_aleatorio = self.POPULACAO - pop_construtivo
        [self.individuos.append(TSP(tipo).construtivo(cidades.copy())) for _ in range(pop_construtivo)]
        [self.individuos.append(TSP(tipo).aleatorio(cidades.copy())) for _ in range(pop_aleatorio)]

    def evoluir(self, tipo, cidades):
        self.populacao_inicial(tipo, cidades.copy())
        gen = 0
        melhor, pior, media = self.melhor_individuo(), self.pior_individuo(), self.media_individuos()
        print(f"Geração {gen}:\nMelhor: {melhor.distancia}\nPior: {pior.distancia}\nMedia: {media:.2f}\n")
        while gen < self.GERACOES:
            self.nova_populacao()
            gen += 1
        melhor, pior, media = self.melhor_individuo(), self.pior_individuo(), self.media_individuos()
        print(f"Geração {gen}:\nMelhor: {melhor.distancia}\nPior: {pior.distancia}\nMedia: {media:.2f}\n")
        return melhor
