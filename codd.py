# -*-Python-*-
################################################################################
#
# File:         codd.py
# RCS:          $Header: $
# Description:  Differential diagnosis as an optimization problem
# Author:       Staal Vinterbo
# Created:      Sat Mar 14 20:54:31 2015
# Modified:     Sun Mar 15 14:34:25 2015 (Staal Vinterbo) staal@mats.gateway.pace.com
# Language:     Python
# Package:      N/A
# Status:       Experimental
#
# (c) Copyright 2015, Staal Vinterbo, all rights reserved.
#
################################################################################

'''
codd: Convex Optimization for Differential Diagnosis

---
title: Convex Optimization for Differential Diagnosis
author: Staal A. Vinterbo
---

Assume there are $m$ possible observations, and $n$ possible explanations.
We can formulate the problem of finding a set of explanations that explain
our set of observations as an optimization problem.

Let 

* $M = [m_{ij}]$ -- be an $m \\times n$ matrix with entries from
  $[-1, 1]$, where $m_{ij}$ gives the association strength between
  observation $i$ and explanation $j$. 
* $o \in [0,1]^m$ be vector of observations

A possible interpretation of observation and association values 
can be: 0 means not known, or neutral, the while absolute value 
represents strenght of presence (positive) or absence (negative).


The problem can now be formulated as: find $y \in {0,1}^n$ that minimizes
$$
\|o - M y^t\|_p + \lambda \|y\|_1,
$$
where $p \in \{1,2,\infty\}$ determines the wanted norm, and $\lambda$ 
represents the weight we place on sparse solutions. 

The above mixed integer program can be *relaxed* so that we only require
$e \in [0, 1]^n$. 

The top scoring explanations can be kept, and if there are observations
that are not explained by these, a next iteration can be performed for just
these.



'''


__all__ = ['codd', 'rround']

import cvxpy as cy
import numpy as np
import sys

def codd(o, M, p = 2, lam = 0.1, verbose = False):
    '''compute d that minimizes ||o - Md^t||_p + ||d||_1'''

    if verbose:
        print >> sys.stderr, 'codd(): M.shape:', M.shape
        print >> sys.stderr, 'codd(): p:', p
        print >> sys.stderr, 'codd(): lam:', lam


    n = M.shape[1]
    m = M.shape[0]
    d = cy.Variable(n)
    x = cy.Variable(m) 

    obj = cy.Minimize(cy.norm(o - x, p) + lam*cy.norm(d, 1))
    cons = [ 0 <= d, d <= 1, M*d == x]
    prob = cy.Problem(obj, cons)
    prob.solve()
    if verbose:
        print >> sys.stderr, 'codd(): problem value = ', prob.value
        print >> sys.stderr, 'codd(): problem status = ', prob.status
    return np.array(d.value.flat)


def codd_iterative(ed, target, lam = 0.1, max_e = 10, verbose = False):
    '''iteratively apply codd to cover target dict keys

    input: 
    ed     -- dict so that ed[explanation][observation] contains strength
    target -- dict so that target[observation] contains strength
    lam    -- sparcity parameter passed to codd
    max_e  -- max number of top explanations to keep for each iteration

    Output: (stages, left)
    where
    stages -- list of list of explanations such that each element in 
              itertools.product(stages) is an explanation
    left   -- set of unexplained observations
    '''

    E = ed.keys()
    O = reduce(lambda x,y : x + ed[y].keys(), E, [])
    
    M = np.zeros((len(O), len(E)))
    oidx = dict((n, i) for (i, n) in enumerate(O))
    for i, e in enumerate(E):
        for j, o in enumerate(O):
            if ed[e].has_key(o):
                M[j,i] = ed[e][o]

    if verbose:
        print >> sys.stderr, 'codd_iterative(): target:', target.keys()
        print >> sys.stderr, 'codd_iterative(): max_e:', max_e

    obs = np.zeros(len(O))
    for n,v in target.items():
        obs[oidx[n]] = v

    left = set(target.keys())
    stages = []
    while left:
        if verbose:
            print >> sys.stderr, 'codd_iterative(): left', left
        exp = codd(obs, M, verbose=verbose, lam=lam)
        ordr = sorted(range(len(exp)), key=lambda i: exp[i], reverse=True)
        top = E[ordr[0]]
        hit = dict()
        left_s = sorted(left)
        for o in left_s:
            if ed[top].has_key(o):
                hit[o] = ed[top][o]
        if not hit:
            break

        # don't look for these again
        for o in hit.keys():
            obs[oidx[o]] = 0.0
        left -= set(hit.keys())

        stage = []
        # get the max_e equally valid for this stage
        for i in xrange(max_e):
            keep = True
            for o in hit.keys():
                j = ordr[i]
                if ed[E[j]].has_key(o):
                    if ed[E[j]][o] < hit[o]:
                        keep = False
                        break
                else:
                    keep = False
                    break
            if keep:
                stage.append(E[ordr[i]])
        stages.append(stage)
    return stages, left
            
            
            
        
    
        

    



if __name__ == "__main__":

    lam = 0.1

    if len(sys.argv) > 1:
        v = sys.argv[1]
        if v[0:4] == '-doc':
            print __doc__
            sys.exit(0)
        try:
            lam = float(v)
        except:
            print >> sys.stderr, 'usage %s [-doc|FLOAT]'
            sys.exit(1)

    M = -1 + 2*np.array(np.random.random(30)).reshape((5, 6))
    o = np.array(np.random.random(5))
    d = codd(o, M, lam = 0.01, verbose=True)

    print 'M:'
    print np.round(M, 2)
    print
    print 'o       :', np.round(o, 2)
    print 'solution:', np.round(d, 2)
    print 'rounded :', rround(d)

    

