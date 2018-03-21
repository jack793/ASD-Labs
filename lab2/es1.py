# -*- coding: utf-8 -*-
import numpy as np
import random
import matplotlib.pyplot as plt
from enum import Enum

class Color(Enum):
    WHITE = 0
    GREY = 1
    BLACK = 2


class Graph:
    def __init__(self, V, E):
        self.numNodes = len(V)
        self.adj_list = self.create_adj_list_from_graph(V, E)
        self.color = {}

    def create_adj_list_from_graph(self, V, E):
        adj_list = {}
        for v in V:
            adj_list[v] = []

        for e in E:
            if e[0] != e[1]:  # evita cappi
                if e[1] not in adj_list[e[0]]:
                    adj_list[e[0]].append(e[1])
                    adj_list[e[1]].append(e[0])

        return adj_list

    def remove_node_from_graph(self):
        to_remove = random.choice(list(self.adj_list.keys()))
        to_sanitize = self.adj_list.pop(to_remove)
        # print("NODO SCELTO", to_remove)

        for i in to_sanitize: # pulendo la lista
            for index, value in enumerate(self.adj_list[i]):
                if value == to_remove:
                    self.adj_list[i].pop(index)


    def DFS_Visited(self, u, visited):
        self.color[u] = Color.BLACK
        visited.append(u)
        for v in self.adj_list[u]:
            if self.color[v] == Color.WHITE:
                visited = self.DFS_Visited(v, visited)

        return visited

    def connected_components(self):
        V = list(self.adj_list.keys())
        for v in V:
            self.color[v] = Color.WHITE
        CC = []
        for v in V:
            if self.color[v] == Color.WHITE:
                visited = []
                # calcola le comp connesse partendo partendo da v
                comp = self.DFS_Visited(v, visited)
                CC.append(comp)

        return CC


    def get_resiliences(self):
        resiliences = []
        for i in range(n):
            self.remove_node_from_graph()
            CC = self.connected_components()
            # print("CC", CC)
            #compute_resilience non è metodo della classe
            resilience = compute_resilience(CC)
            # print("Resilienza", resilience)
            resiliences.append(resilience)
        return resiliences

class UPATrial:
    def __init__(self, m):
        self.numNodes = m  # numero iniziale di nodi
        self.nodeNumbers = []  # lista di 111122223333444455...

        for i in range(m):
            for j in range(m):
                self.nodeNumbers.append(i)

    def run_trial(self, m):
        V = set()

        for i in range(m):  # estrae m nodi sempre
            u = random.choice(self.nodeNumbers) # estratto a caso
            V.add(u)  # contiene tutti i nodi estratti in questo turno

        for i in range(len(V)+1):  # len(V) può essere diverso da m perchè posso estrarre più volte lo stesso nodo
            self.nodeNumbers.append(self.numNodes)

        self.nodeNumbers.extend(V)  # aumentiamo la probabilità degli altri
        self.numNodes += 1

        return V


def UPA(n, m):
    V = [x for x in range(m)]
    E = [(i, j) for i in V for j in V if i != j]

    trial = UPATrial(m)

    for u in range(m, n):
        V_1 = trial.run_trial(m)  # nodi estratti da trial
        V.append(u)
        for v in V_1:
            E.append((u, v))
    return V, E

def compute_resilience(CC):
    max = 0
    for i in CC:
        if len(i) > max:
            max = len(i)

    return max


def ER(n,p):
    V = [x for x in range(n)]
    E = []
    for i in V:
        for j in V:
            a = random.uniform(0, 1)
            if a < p and i != j:
                E.append((i, j))
    return V, E


if __name__ == '__main__':
    data = np.loadtxt("./as19991212.txt", dtype=int)
    coda = data[:,0]
    testa = data[:,1]
    x = set(coda)
    y = set(testa)
    z = x.union(y)
    n = len(z)  # numero di nodi

    G_NET = Graph(z, data)
    adj_list_net = G_NET.adj_list
    degrees = [len(adj_list_net[i]) for i in z]
    mean = int(np.average(degrees))

    print("NODI NET:", n)
    print("ARCHI NET:", int(sum([len(adj_list_net[i]) for i in z])/2))  # /2 perchè ci sono 2 archi

    m=int(mean/2)
    V_UPA, E_UPA = UPA(n, m) # rich get richer va bene
    G_UPA = Graph(V_UPA, E_UPA)
    print("NODI UPA:", len(V_UPA))
    print("ARCHI UPA:", len(E_UPA))

    p=0.0014
    V_ER, E_ER = ER(n, p)
    G_ER = Graph(V_ER, E_ER)
    print("NODI ER:", len(V_ER))
    print("ARCHI ER:", len(E_ER))

    res_NET = G_NET.get_resiliences()
    res_ER = G_ER.get_resiliences()
    res_UPA = G_UPA.get_resiliences()

    plt.plot(np.arange(0, len(res_NET)), res_NET, label="Resilienza NET")
    plt.plot(np.arange(0, len(res_ER)), res_ER, label="Resilienza ER")
    plt.plot(np.arange(0, len(res_UPA)), res_UPA, label="Resilienza UPA")
    plt.legend()
    plt.xlabel("Nodi disabilitati")
    plt.ylabel("Massima componente connessa")
    plt.title("Resilienza delle reti")

    plt.text(0, 0, 'I valori scelti sono p='+str(p)+', m='+str(m))
    plt.savefig("lab2-es1.png")

    plt.show()
