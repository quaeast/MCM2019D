import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

np = np.array([[1, 2],[3, 4],[5, 6]])
g = nx.Graph()
g.add_edges_from(np)

nx.draw(g, with_labels=True)
plt.show()
