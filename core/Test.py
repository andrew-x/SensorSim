import pygraphviz as pgv
from pygraphviz import *

# with open('graph.dot','w') as out:
#     out.write('}\n')

G=pgv.AGraph()
ndlist = [1,2,3]
for node in ndlist:
    G.add_node(node)
    label = "Label #" + str(node)
    G.get_node(node).attr['label'] = label
    G.get_node(node).attr['pos'] = '10,10!'
G.layout()
G.draw('example.png', format='png')

#d_usr = d_usr.text((105,280), "Travis L.",(0,0,0), font=usr_font)