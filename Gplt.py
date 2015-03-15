# -*-Python-*-
################################################################################
#
# File:         Gplt.py
# RCS:          $Header: $
# Description:  plot dictdict 
# Author:       Staal Vinterbo
# Created:      Wed Jun  8 12:24:33 2011
# Modified:     Sun Mar 15 11:49:16 2015 (Staal Vinterbo) staal@mats.gateway.pace.com
# Language:     Python
# Package:      N/A
# Status:       Experimental
#
# (c) Copyright 2011, Staal Vinterbo, all rights reserved.
#
################################################################################

import matplotlib
matplotlib.use('TkAgg')  # make it work on mac os x
import matplotlib.pyplot as plt
import networkx as nx
from Gml import gtoNX
from operator import add
from random import random
from collections import defaultdict

def mpG(G, labs = True):
    '''generate mathplot plot of dictdict'''
    E = sorted(G.keys())
    O = sorted(reduce(lambda x,y : x | set(y),
                      (G[e].keys() for e in G.keys()), set()))
    ne = len(E)
    no = len(O)

    labs = dict(
        reduce(add, ([((e,o), G[e][o]) for o in G[e].keys()] for e in G.keys()),
               []))

    # hack to get nicer ordering for the o's and the e's
    es = map(lambda e: len(G[e].keys()), E)
    E = map(lambda (e,v):e,sorted(zip(E, es),key=lambda (e,v):v,reverse=False))
    # Eleft = map(lambda (i, e): e, filter(lambda (i,e): i % 2, enumerate(E)))
    # Eright = map(lambda (i, e): e, filter(lambda (i,e): i % 2 == 0,
    #                                        enumerate(E)))
    # E = list(reversed(Eleft)) + Eright
    od = defaultdict(list)
    for (i, e) in enumerate(E):
        for o in G[e].keys():
            od[o].append(i)
    ave = lambda v : 0 if len(v) == 0 else sum(v)/float(len(v))
    os = map(lambda o : ave(od[o]), O)
    O = map(lambda (o,v) : o, sorted(zip(O, os), key = lambda (o,v) : v))

    pos=dict(zip(E,zip(range(ne),[1]*ne))) # upper nodes
    pos.update(dict(zip(O,zip(range(no),[0]*no)))) # lower nodes
    #print(pos)
    #print(labs)
    nxG = gtoNX(G)
    nx.draw(nxG,pos=pos, with_labels=True)

    if labs:
        for (e,o),w in labs.items():
            ex, ey = pos[e]
            ox, oy = pos[o]
            x=(ex+ox) * 0.5
            y=(ey+oy) * (0.5 + (0.1 if (ex > ox) else (ex != ox)*-0.1))
            plt.text(x,y,"%(w).02f" % {'w': w})

    plt.draw()
    plt.show()

if __name__ == '__main__':

    testG = {'e1': {'o1': 1.1, 'o2': 1.2 },
             'e2': {'o1': 2.1, 'o2': 2.2 , 'o3': 2.3},
             'e4': {'o1': 4.1, 'o2': 4.2 , 'o3': 4.3},             
             'e3': {'o1': 3.1, 'o3': 3.3 , 'o4': 3.4}}
    mpG(testG)

