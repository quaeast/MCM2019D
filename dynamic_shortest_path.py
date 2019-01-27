import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

arg = 0.25


def get_time(path):
    time = 0
    if path['is_stairs']:
        time = 1*(1+0.1*path['fre'])
    else:
        time = 0.83+0.27*path['fre']
    if path['is_fire']==6:
        time += 2
    else:
        time += 1
    return time


def show_labels(g):
    for i in g.edges():
        print(i, end = '')
        print(g[i[0]][i[1]])


def cal_s_and_ave(g):
    sum_fre = 0
    for i in g.edges():
        sum_fre += g[i[0]][i[1]]['fre']
    ave_fre = sum_fre/g.number_of_edges()

    sum_fre = 0
    for i in g.edges():
        sum_fre += (g[i[0]][i[1]]['fre']-ave_fre)**2
    sq_fre = sum_fre/g.number_of_edges()
    return ave_fre,sq_fre


def show_length(g, paths_dict):
    numbers_of_time = np.zeros(10)
    for i in paths_dict:
        cur_point = paths_dict[i]
        length = 0
        for j in range(len(cur_point)-1):
            length += g[cur_point[j]][cur_point[j+1]]['weight']
        # print(i, end=': ')
        # print(length)
        numbers_of_time[int(length/10)] += 1
    print(numbers_of_time)


def add_fire_place(g, source):
    all_path = nx.single_source_shortest_path(g, source)
    for j in all_path:
        i = all_path[j]
        if len(i)==2:
            g[i[0]][i[1]]['is_fire'] = 6
        elif len(i)==3:
            g[i[1]][i[2]]['is_fire'] = 3

def path_blocked(g, path):
    g[path[0]][path[1]]['weight'] = 1000000

# init grapg

lv = np.array(np.load('lv.npy'))
stairs = np.load('stairs.npy')
lvg = nx.Graph()
lvg.add_weighted_edges_from(lv)


add_fire_place(lvg, 328)
add_fire_place(lvg, 419)
add_fire_place(lvg, 408)



#predict


final_dict = {}

for i in lvg.edges():                   # add frequency
    lvg[i[0]][i[1]]['fre'] = 0

for i in lvg.edges():
    lvg[i[0]][i[1]]['weight'] = 1

for i in lvg.edges():
    lvg[i[0]][i[1]]['is_fire'] = 0

for i in lvg.edges():
    lvg[i[0]][i[1]]['is_stairs'] = False

for i in lvg.edges():
    lvg[i[0]][i[1]]['width'] = 0

for i in stairs:
    lvg[i[0]][i[1]]['is_stairs'] = True


for i in lvg.node():
    path100 = nx.shortest_path(lvg, source = 100, target = i)
    path1 = nx.shortest_path(lvg, source = 1, target = i)
    path2 = nx.shortest_path(lvg, source = 2, target = i)
    path3 = nx.shortest_path(lvg, source = 3, target = i)

    length100 = nx.shortest_path_length(lvg, source = 100, target = i, weight='weight')
    length1 = nx.shortest_path_length(lvg, source = 1, target = i, weight='weight')
    length2 = nx.shortest_path_length(lvg, source = 2, target = i, weight='weight')
    length3 = nx.shortest_path_length(lvg, source = 3, target = i, weight='weight')

    min_path = min(length1, length2 , length3, length100)
    if(length100 == min_path):
        final_dict[i] = path100
    elif(length1 == min_path):
        final_dict[i] = path1
    elif(length2 == min_path):
        final_dict[i] = path2
    else:
        final_dict[i] = path3

    for j in range(len(final_dict[i])-1):
        try:
            lvg[final_dict[i][j]][final_dict[i][j+1]]['weight'] = \
            get_time(lvg[final_dict[i][j]][final_dict[i][j+1]])
            lvg[final_dict[i][j]][final_dict[i][j+1]]['fre'] += 1
        except:
            lvg[final_dict[i][j]][final_dict[i][j+1]]['fre'] = 1




#sort by frequency and show


edges_dict = {}

for i in lvg.edges():
    edges_dict[i] = lvg[i[0]][i[1]]['weight']

edges_dict = sorted(edges_dict.items(), key=lambda e:e[1], reverse=True)





#show s and average


print(arg, end=': ')
print(cal_s_and_ave(lvg))


#show the length of every path


show_length(lvg, final_dict)


#get_shortest_length


final_len = {}
all_len100 = nx.single_source_shortest_path_length(lvg, 100)
all_len1 = nx.single_source_shortest_path_length(lvg, 1)
all_len2 = nx.single_source_shortest_path_length(lvg, 2)
all_len3 = nx.single_source_shortest_path_length(lvg, 3)
for i in all_len100:
    min_length = min(all_len1[i], all_len2[i], all_len3[i], all_len100[i])
    if all_len100[i] == min_length:
        final_len[i] = all_len100[i]
    elif all_len1[i] == min_length:
        final_len[i] = all_len1[i]
    elif all_len2[i] == min_length:
        final_len[i] = all_len2[i]
    else:
        final_len[i] = all_len3[i]

final_len = sorted(final_len.items(), key=lambda e:e[1], reverse=True)

numbers_of_len = np.zeros((20))
for i in final_len:
    numbers_of_len[i[1]] += 1

#show graph

#color
node_np = np.array(lvg.nodes())

# nx.draw_spring(lvg, with_labels=True, node_size=80, font_size = 6, node_color = node_np)


#show minimum spanning tree


# mst = nx.minimum_spanning_tree(lvg)
# nx.draw_spring(mst, with_labels=True, node_size=80, font_size = 6, node_color = node_np)
# plt.show()
