# -*-Python-*-
################################################################################
#
# File:         Gml.py
# RCS:          $Header: $
# Description:  Translate dict of dict representation of graph to nx to ml and back 
# Author:       Staal Vinterbo
# Created:      Wed Jun  8 12:01:17 2011
# Modified:     Wed Jun  8 15:30:20 2011 (Staal Vinterbo) staal@dink
# Language:     Python
# Package:      N/A
# Status:       Experimental
#
# (c) Copyright 2011, Staal Vinterbo, all rights reserved.
#
################################################################################


import networkx as nx
from operator import add
import StringIO as si

def gtoNX(G,gtype=nx.DiGraph):
    '''loads adjacency dictofdict into NX.DiGraph()'''
    nxG = gtype()
    pairs = reduce(add, ([(e,o,{'weight': G[e][o]}) for o in G[e].keys()]
                   for e in G.keys()), [])
    nxG.add_edges_from(pairs)
    return nxG

def nxtoG(G):
    '''convert nx.DiGraph to dictdict, assumes edge dicts have "weight" key'''
    dd = filter(lambda (x,y): y != {}, nx.to_dict_of_dicts(G).items())
    return dict((x,
                 dict(map(lambda (o,ad): (o,ad['weight']), y.items())))
                for (x,y) in dd)

def writeg(G, writer=nx.readwrite.write_graphml):
    '''prints adjacency dictdict bigraph to format written by writer'''
    output = si.StringIO()

    writer(gtoNX(G), output)
    contents = output.getvalue()
    output.close()
    return contents

def readg(inpt, reader=nx.readwrite.read_graphml):
    '''read graph from file object (or filename) and output dictdict'''
    return nxtoG(reader(inpt))


if __name__ == '__main__':

    testG = {'e1': {'o1': 1, 'o2': 0.8 },
             'e2': {'o2': 1, 'o3': 0.4 }}
    print(testG)
    print(readg(si.StringIO(writeg(testG)))) # to graphml and back

    
    
    
        
