from sklearn import tree
import numpy as np
import csv
import graphviz
import pydotplus

import os     
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


data = {}
numColsIncludingY = 22

with open('ForTreeFinal.csv', 'r') as f:
    rows = list(csv.reader(f, delimiter=','))
    dataArray = np.array(rows[1:], dtype=np.float)
    data['featureNames'] = rows[0][:numColsIncludingY - 1]
    data['X'] = dataArray[:, 0:numColsIncludingY - 1]
    data['Y'] = dataArray[:, numColsIncludingY - 1]

#print(dataArray)
print(data['featureNames'])
#print(data['X'])
#print(data['Y'])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(data['X'], data['Y'])



#dot_data = tree.export_graphviz(clf, out_file=None, 
#                      feature_names=data['featureNames'], 
#                      filled=True, rounded=True,  
#                      special_characters=True) 
#graph = graphviz.Source(dot_data) 
#graph



#dot_data = tree.export_graphviz(clf, out_file='treeResult') 
#graph = graphviz.Source(dot_data) 
#graph.render("iris") 


dot_data = tree.export_graphviz(clf,
                                feature_names=data['featureNames'],
                                out_file=None,
                                filled=True,
                                rounded=True)
graph = pydotplus.graph_from_dot_data(dot_data)


#colors = ('turquoise', 'orange')
#edges = collections.defaultdict(list)

#for edge in graph.get_edge_list():
#    edges[edge.get_source()].append(int(edge.get_destination()))
#
#for edge in edges:
#    edges[edge].sort()    
#    for i in range(2):
#        dest = graph.get_node(str(edges[edge][i]))[0]
#        dest.set_fillcolor(colors[i])

graph.write_png('tree.png')





