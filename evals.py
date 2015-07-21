# -*-Python-*-
################################################################################
#
# File:         evals.py
# RCS:          $Header: $
# Description:  
# Author:       Staal Vinterbo
# Created:      Wed Jun  8 15:58:33 2011
# Modified:     Tue Jul 21 11:02:21 2015 (Staal Vinterbo) staal@mats.gateway.pace.com
# Language:     Python
# Package:      N/A
# Status:       Experimental
#
# (c) Copyright 2011, Staal Vinterbo, all rights reserved.
#
################################################################################

import sys


def value(expl, target, r, tau=0.7, eprev = lambda s: 1, gamma = lambda s: 1):
    coverage = map(lambda o: sum(map(lambda e: r(o,e)*eprev(e), expl)), target)
    covered = len(filter(lambda v : v >= tau, coverage))
    cratio = covered/float(len(target))
    return (cratio*gamma(expl), coverage)

def ddtor(dd):
    return lambda o,e: dd[e][o] if dd[e].has_key(o) else 0

def greedy(target, E, r,
           taus=[0.7, 0.5, 0.3, 0.05],
           eprev = lambda s: 1, gamma = lambda s: 1):
    avail = set(E) # still available to try
    # force any explanations that are also targets
    sol = list(set(E) & set(target))       # solution
    cval = 0
    for tau in taus:
        cval = value(sol, target, r, tau, eprev, gamma)[0]
        if cval > 0:
            break
    while avail:
        # try adding all available explanations
        beste = None
        bestv = cval
        for tau in taus:        
            for e in avail:
                #print('trying ' + str(e) + ' at ' + str(tau))
                tmpv = value(sol + [e], target, r, tau, eprev, gamma)[0]
                if tmpv > bestv:
                    bestv = tmpv
                    beste = e
            if beste != None: # improvement
                #print('exiting tau' + str(tau) + ' best e ' + str(beste))
                break
        if beste == None: # no improvement
            return (sol, cval, value(sol, target, r, 0.9, eprev, gamma)[1])
        cval = bestv
        sol.append(beste)
        avail.remove(beste)
    return (sol, cval, value(sol, target, r, 0.9, eprev, gamma)[1])
    
if __name__ == '__main__':
    from random import random, sample, randint
    from collections import defaultdict
    from pprint import pprint
    from lcs import strdiff, lenLCS
    from codd import codd_iterative
    from Gml import gtoNX
    import numpy as np
    import networkx as nx

    
    testG = eval(open('OR_G.txt').read())
    O = reduce(lambda x,y : x | set(testG[y].keys()), testG.keys(), set())
    E = set(testG.keys())
    OE = list(O | set(testG.keys()))

    # Read input symptoms, translate into observations in relationships
    print('Input Symptoms, end with empty line:')
    target = []
    Es = []
    while True:
        line = sys.stdin.readline()
        word = line.lstrip().rstrip()
        if len(word) == 0:
            break
        (s,o) = max(map(lambda w : (strdiff(word, w), w), OE))
        print('using ' + str(o) + ' for ' + word + ' (word match: ' + str(s) + ')')
        if o in E:
           Es.append(o) 
        target.append(o)
    for e in Es:
        missed = set(testG[e].keys()) - set(target)
        if len(missed) > 0:
            print('for ' + e + ', symptoms not entered:')
            print('>' + ', '.join(str(t) for t in missed))

    print('Observed :\n  ' + '\n  '.join(str(t) for t in target))


    # compute explanation using greedy
    rfunc = ddtor(testG)
    sol, cf, cov = greedy(target, testG.keys(), rfunc)
    print('\nExplained to degree by Greedy:')
    print('  ' + str(cov))
    print('by:\n  ' +
          '\n  '.join(str(t) + ' (' +
                      ','.join(str(v) for v in value([t], target, rfunc)[1]) +
                      ')' for t in sol))

    # try iterative codd

    targ = dict.fromkeys(target, 1.0)
    stages, left = codd_iterative(testG, targ, max_e = 20, lam=0.05, verbose=True)

    print 'Explained by:'
    out = []
    for s in stages:
        outs = ''
        for e in s:
            outs += '  %s ' % (e,)
            ex = []
            for t in target:
                if testG[e].has_key(t):
                    ex.append('%s:%.2f' % (t, testG[e][t]))
            outs += ','.join(ex) + '\n'
        out.append(outs)
    print 'One of:\n', 'and one of:\n'.join(out)
    print
    print 'Observations not covered:', list(left)
    print('plot explanation? (y/[n])')
    if sys.stdin.readline().lstrip().rstrip() == 'y':
        try:
            from Gplt import mpG
            mpG(
                    dict(
                        map(lambda (e,_):
                            (e,
                             dict((s,v) for (s,v) in testG[e].items()
                                  if s in target)),
                            filter(lambda (e, s) : e in sol, testG.items())
                            )
                        )
                    )
        except:
            print('Sorry, plotting failed. Are needed packages installed?')
            pass

    

    
