from dimacs import loadGraph
from pycosat import solve
from os import scandir

def is_graph_coloring_sat(num_colors: int, graph: list[set[int]]) -> String | list[int]:
    logic_variable = lambda vertex, color: (len(graph) + 1) * color + vertex
    
    sat_result = solve([[logic_variable(vertex, color) for color in range(num_colors)] for vertex in range(1, len(graph))] \
                     + [[-logic_variable(vertex, color1), -logic_variable(vertex, color2)] for color1 in range(num_colors) for color2 in range(color1 + 1, num_colors) for vertex in range(1, len(graph))] \
                     + [[-logic_variable(vertex1, color), -logic_variable(vertex2, color)] for vertex1, neighbours in enumerate(graph) for vertex2 in neighbours if vertex1 > vertex2 for color in range(num_colors)])
    
    if sat_result == u'UNSAT':
        return sat_result
    
    coloring = [0 for _ in range(len(graph))]

    for var in sat_result:
        if var > 0:
            vertex = var %  (len(graph) + 1)
            color  = var // (len(graph) + 1)
            coloring[vertex] = color
    
    return coloring

            
def is_graph_coloring_valid(graph: set[list[int]], coloring: list[int]) -> Bool:
    return all(coloring[v] != coloring[neighbour] for v, neighbours in enumerate(graph) for neighbour in neighbours)

if __name__ == "__main__":
    for file in scandir("coloring"):
        graph = loadGraph("coloring/" + file.name)
        for k in range(1, len(graph) + 1):
            coloring = is_graph_coloring_sat(k, graph)
            if coloring != u'UNSAT':
                if is_graph_coloring_valid(graph, coloring):
                    print(f"solver found coloring of {file.name} of order {k}")
                else:
                    print(f"solver returned invalid coloring of {file.name} of order {k}")
                break
