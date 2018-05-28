"""
classe che gestisce il cluster
"""


class Cluster:
    def __init__(self, elem):
        """
        :param: elem: array di elementi per inizializzazione
        """
        self.elements = elem  # array di tuple di punti (xi, yi)
        self.centroid = self.calculate_centroid()
        self.need_recalculus = False  # ci dice se è necessario ricalcolare il centroide del cluster

    def __repr__(self):
        return str(self.calculate_centroid())

    def calculate_centroid(self):
        """
        funzione che ritorna il centroide del cluster
        """
        sum_x = 0
        sum_y = 0
        n = len(self.elements)
        for i in range(n):
            sum_x += self.elements[i][0]
            sum_y += self.elements[i][1]

        if n > 0:
            centroid = (sum_x/n, sum_y/n)
        else:
            centroid = None

        self.need_recalculus = False

        return centroid

    def add_element(self, x):
        self.elements.append(x)
        self.need_recalculus = True

    # remove element
    def remove_element(self, x):
        self.elements

    def get_elements(self):
        return self.elements

    def get_centroid(self):
        if self.need_recalculus:
            self.calculate_centroid()
        return self.centroid

    def union_cluster(self, c):
        self.elements.extend(c.get_elements())
        self.need_recalculus = True

    def __lt__(self, other):
        return self.get_centroid() < other.get_centroid()

    def __add__(self, other):
        c1 = self.get_centroid()
        c2 = other.get_centroid()
        return c1[0]+c2[0], c1[1]+c2[1]
