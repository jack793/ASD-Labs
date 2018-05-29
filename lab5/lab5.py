import numpy as np
from hierarchical_clustering import *
from kmeans import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import itertools

if __name__ == '__main__':
    f_name = "unifiedCancerData/unifiedCancerData_111.csv"
    dataset = np.loadtxt(f_name, dtype=float, delimiter=',')

    n = len(dataset)

    number_of_clusters = 15

    x = dataset[:, 1]  # coordinate x
    y = dataset[:, 2]  # coordinate y
    pop = dataset[:, 3]  # population

    coordinates = [(x[i], y[i]) for i in range(n)]

    clusters = hierarchical_clustering(coordinates, 15)
    # clusters = kmeans(coordinates, number_of_clusters, pop, q=5)

    print(sum([len(cluster.get_elements()) for cluster in clusters]))

    img = plt.imread("./immagini/USA_Counties.png")
    fig, ax = plt.subplots()
    ax.imshow(img)
    # ax.imshow(img, extent=[0, 400, 0, 300])

    # palette = itertools.cycle(sns.color_palette())

    colors = cm.rainbow(np.linspace(0, 1, number_of_clusters))
    for cluster, c in zip(clusters, colors):
        elements = cluster.get_elements()
        for element in elements:
            # sns.pointplot(element[0], element[1], color=next(palette))
            ax.scatter(element[0], element[1], color=c)

    plt.show()

