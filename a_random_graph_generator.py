import random
from itertools import combinations
from math import factorial
from collections import Counter

MIN_DEGREE = 1
MAX_DEGREE = 5
assert MIN_DEGREE > 0 and MAX_DEGREE > MIN_DEGREE, "Minimum and/or maximum degrees have a wrong value!"

"""
# node class
class Node:
    def __init__(self, id):
        self.id = id
"""

# amount of vertices/degrees
n = 10

# create a sequence of random nonnegative degrees of size n
d = [random.randint(MIN_DEGREE, MAX_DEGREE) for i in range(n)]

# ensure that the sum of degrees is even
if sum(d) % 2 == 1:
    d[0] += 1

m = int(sum(d) / 2) # amount of edges

# create a sequence of nodes of size n
V = [i for i in range(n)]

def proc_A():
    # -- step 1 --
    E = set() # set of edges
    d_res = d.copy() # sequence of residual degrees (i.e. degrees yet to receive edges)
    P = 1 # product of probabilities of edges
    N = 0 # output number

    # initiate the possible edges and their amount
    E_space = list(combinations(V, 2))
    c = Counter(E_space)
    E_space_size = sum(v for k, v in c.items())

    # -- step 2 & 3 --
    # there have to be at least 2 available vertices to construct an edge
    while E_space_size > 0:

        # construct a distribution for the new, random edge
        E_p = [d_res[edge[0]] * d_res[edge[1]] * (1 - (d[edge[0]] * d[edge[1]]) / (4 * m)) for edge in E_space] # corresponding probabilities
        corr = 1 / sum(E_p)
        E_p = [corr * prob for prob in E_p] # correct the probabilities so that sum = 1

        # generate the new edge based on the constructed distribution and add it to E
        tmp = random.choices([i for i in range(E_space_size)], E_p)
        E_new_index = tmp[0]

        # multiply P by the probability of the edge
        P *= E_p[E_new_index]

        # add the new edge to E, remove it from E_space
        E_new = E_space[E_new_index] # the new edge
        E.add(E_new)
        E_space.remove(E_new)
        E_space_size -= 1

        # reduce the residual degrees by 1; check if the vertices are still 'available'
        # note: E_new[0] and E_new[1] are the vertices/nodes
        d_res[E_new[0]] -= 1
        if d_res[E_new[0]] == 0:
            E_space = [edge for edge in E_space if E_new[0] not in edge]
            c = Counter(E_space)
            E_space_size = sum(v for k, v in c.items())
        d_res[E_new[1]] -= 1
        if d_res[E_new[1]] == 0:
            E_space = [edge for edge in E_space if E_new[1] not in edge]
            c = Counter(E_space)
            E_space_size = sum(v for k, v in c.items())

    # -- step 4 --
    if len(E) < m: # failure
        raise Exception("Procedure A did not produce enough edges!")
        return N
    else: # success
        G = (V, E)
        N = pow(factorial(m) * P, -1)
        return G, N

def main():
    graph, N = proc_A()
    print(N)
    for edge in graph[1]:
        print(edge, end=" | ")

if __name__ == '__main__':
    main()
