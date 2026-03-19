from dimacs import edgeList, isVC
from random import random, shuffle

def simulated_annealing(G: list[list[int]]) -> list[int]:
    all_vertices = [i for i in range(len(G))]
    edges = edgeList(G)

    def get_first_viable_vertex(vertices: set[int]) -> set[int]:
        nonlocal all_vertices, edges
        shuffle(all_vertices)
        for v in all_vertices:
            if v in vertices:
                if isVC(edges, vertices - {v}):
                    return vertices - {v}
            else:
                return vertices | {v}
        
    result = set(all_vertices)
    for i in range(10000):
        neighbour = get_first_viable_vertex(result)
        if len(neighbour) < len(result):
            result = neighbour
        else:
            if (1 - 1 / (len(all_vertices) - len(result)))**i >= random():
                result = neighbour
    
    return list(result)
