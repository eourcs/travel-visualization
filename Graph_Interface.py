#Graph Interface

def graph_new(size):
    return [[0]*size for i in xrange(size)]

def add_edge(G, v, w, d):
    G[v][w] = d
    G[w][v] = d

def graph_size(G):
    return len(G)

