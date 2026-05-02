from os import scandir
from time import time
from pycosat import solve
from dimacs import loadGraph

def is_vertex_cover_sat(graph: list[set[int]], k: int) -> list[int] | String:
    index = lambda i, j: (i + j) * (i + j + 1) // 2 + i + len(graph) + 1
    
    result = solve([[v, neighbour] for v, neighbours in enumerate(graph) for neighbour in neighbours if neighbour > v]
                 + [[ index(i, 0)] for i in range(len(graph) + 1)]
                 + [[-index(0, j)] for j in range(1, len(graph) + 1)]
                 + [[-index(i - 1, j), index(i, j)] for i in range(1, len(graph) + 1) for j in range(1, len(graph) + 1)]
                 + [[-index(i - 1, j - 1), -i, index(i, j)] for i in range(1, len(graph) + 1) for j in range(1, len(graph) + 1)]
                 + [[-index(len(graph), k + 1)]])
    
    return [vertex for vertex in result if 0 < vertex < len(graph)] if result != u'UNSAT' else u'UNSAT'

if __name__ == "__main__":
    for (size, graph, filename) in sorted([(len(loadGraph("graph/" + file.name)), loadGraph("graph/" + file.name), file.name) for file in scandir("graph")]):
        start = time()
        for k in range(len(graph) + 1):
            result = is_vertex_cover_sat(graph, k)
            if result != u'UNSAT':
                print(f"solver found that graph from {filename} has vertex cover of {k} in {time() - start}s")
                break
        
