import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

arg = 1.1


#build the graph


lv = np.array(np.load('lv.npy'))
lvg = nx.Graph()
lvg.add_weighted_edges_from(lv)


#predict


path100 = nx.shortest_path(lvg, source = 100)
path1 = nx.shortest_path(lvg, source = 1)
path2 = nx.shortest_path(lvg, source = 2)
path3 = nx.shortest_path(lvg, source = 3)

length100 = nx.shortest_path_length(lvg, source = 100, weight='weight')
length1 = nx.shortest_path_length(lvg, source = 1, weight='weight')
length2 = nx.shortest_path_length(lvg, source = 2, weight='weight')
length3 = nx.shortest_path_length(lvg, source = 3, weight='weight')

final_dict = {}


# calculate shortest path


for i in lvg.node():
    min_path = min(length1[i], length2[i] , length3[i], length100[i])
    if(length100[i] == min_path):
        final_dict[i] = path100[i]
    elif(length1 == min_path):
        final_dict[i] = path1[i]
    elif(length2 == min_path):
        final_dict[i] = path2[i]
    else:
        final_dict[i] = path3[i]


for i in final_dict:
    if len(final_dict[i])>0:
        for j in range(len(final_dict[i])-1):
            try:
                lvg[final_dict[i][j]][final_dict[i][j+1]]['fre'] += 1
            except:
                lvg[final_dict[i][j]][final_dict[i][j+1]]['fre'] = 1

def show_labels(g):
    for i in g.edges():
        print(g[i[0]][i[1]])




show_labels(lvg)
# print(lvg[133][134]['fre'])


# nx.draw(lvg, with_labels=True)
mst = nx.minimum_spanning_tree(lvg)
# nx.draw(mst, with_labels=True)
# plt.show()
