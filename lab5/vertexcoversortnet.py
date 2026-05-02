from os import scandir
from time import time
from pycosat import solve
from dimacs import loadGraph
import sortnet

def vertex_cover_sortnet(graph: list[set[int]], k: int) -> list[int] | str:
    clauses = [[v, neighbour] for v, neighbours in enumerate(graph) for neighbour in neighbours if neighbour > v]

    net = sortnet.sorterNet(len(graph), list(range(1, len(graph))), True)

    for i in range(1, len(graph) - 1):
        for j in range(i, 0, -1):
            net.comp(j - 1, j)

    clauses.extend(net.getCNF())

    if k < len(graph) - 1:
        clauses.append([-net.getLines()[k]])

    result = solve(clauses)
    
    return [v for v in result if 0 < v < len(graph)] if result != u'UNSAT' else u'UNSAT'


if __name__ == '__main__':
    for (size, graph, filename) in sorted([(len(loadGraph("graph/" + file.name)), loadGraph("graph/" + file.name), file.name) for file in scandir("graph")]):
        start = time()
        for k in range(size + 1):
            result = vertex_cover_sortnet(graph, k)
            if result != 'UNSAT':
                print(f"solver found that graph from {filename} has vertex cover of {k} in {time() - start}s")
                break
   
