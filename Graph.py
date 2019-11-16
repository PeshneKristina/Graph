import collections
import csv

import community
import matplotlib.pyplot as plt
import networkx as nx
from fa2 import ForceAtlas2

g = nx.Graph()

# создание файла
# добавление ребер и узлов из файла
f1 = csv.reader(open("resources/Nodes.csv"))
next(f1)
node_labels = {}
for row in f1:
    row_string = row[0].split(";")
    g.add_node(row_string[0])
    g.nodes[row_string[0]]['label'] = row_string[1]
    g.nodes[row_string[0]]['tweetCount'] = row_string[2]
    node_labels[row_string[0]] = row_string[1] + ' , ' + row_string[2]
f2 = csv.reader(open("resources/Edges.csv"))
next(f2)
for row in f2:
    g.add_edge(row[0].split(";")[0], row[0].split(";")[1])

# настройка параметров расположения графа
forceatlas2 = ForceAtlas2(
    # Behavior alternatives
    outboundAttractionDistribution=True,  # Dissuade hubs
    linLogMode=False,  # NOT IMPLEMENTED
    adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
    edgeWeightInfluence=1.0,

    # Performance
    jitterTolerance=1.0,  # Tolerance
    barnesHutOptimize=True,
    barnesHutTheta=1.2,
    multiThreaded=False,  # NOT IMPLEMENTED

    # Tuning
    scalingRatio=2.0,
    strongGravityMode=False,
    gravity=1.0,

    # Log
    verbose=True)

positions = forceatlas2.forceatlas2_networkx_layout(g, pos=None,
                                                    iterations=100)

# отрисовка графа
plt.figure(1)
nx.draw_networkx_nodes(g, positions, node_size=40, with_labels=True,
                       node_color="blue", alpha=0.6)
nx.draw_networkx_edges(g, positions, edge_color="black", alpha=0.1,
                       with_labels=True)
# nx.draw_networkx_labels(g, positions, node_labels, font_size=3, alpha=0.5)

# отрисовка графа с клатеризацией
#  каждый кластер своим цветом
plt.figure(2)
partition = community.best_partition(g)

nx.draw_networkx_nodes(g, positions, node_size=40,
                       cmap=plt.cm.get_cmap('RdYlBu'),
                       node_color=list(partition.values()), alpha=0.6)
nx.draw_networkx_edges(g, positions, alpha=0.1)

# отрисовка графа с кластеризацией
# выделение 5 самых больших кластеров
# раскрашены только эти 5 кластеров, остальные узлы серые
plt.figure(3)
parts = community.best_partition(g)
values = [parts.get(node) for node in g.nodes()]
values1 = [parts.get(node) for node in g.nodes()]
c = collections.Counter(values)
list_d = list(c.items())
list_d.sort(key=lambda i: i[1])
color_dict = {list_d[-1][0]: 'red', list_d[-2][0]: 'blue',
              list_d[-3][0]: 'green', list_d[-4][0]: 'yellow',
              list_d[-5][0]: 'black'}
for i in range(0, len(values)):
    if values[i] in color_dict:
        values[i] = color_dict.get(values[i])
    else:
        values[i] = "grey"
nx.draw_networkx_nodes(g, positions, node_size=40,
                       node_color=list(values), alpha=0.6)
nx.draw_networkx_edges(g, positions, alpha=0.1)

# выгрузка составляющих каждого кластера в файл
filename = "graph_clust.csv"
cluster_dict = {}

f1 = csv.reader(open("resources/Nodes.csv"))
next(f1)
for row in f1:
    row_string = row[0].split(";")
    if cluster_dict.get(values1[int(row_string[0])]) == None:
        cluster_dict[values1[int(row_string[0])]] = row_string[1]
    else:
        cluster_dict.update({values1[int(row_string[0])]: cluster_dict.get(
            values1[int(row_string[0])]) + " , " + row_string[1]})

with open(filename, "w", newline="") as file:
    writer = csv.writer(file, delimiter=',')
    for key, value in cluster_dict.items():
        writer.writerow(["{0}: {1}".format(key, value)])
        writer.writerow(["cluster power: " + str(c.get(key))])


# отображение графов
plt.axis('off')
plt.show()
