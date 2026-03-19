from dimacs import edgeList, isVC

def lognaprox(G: list[list[int]]) -> list[int]:
    G = {v: set(neighbours) for v, neighbours in enumerate(G) if neighbours}
    result = []
    while G:
        chosen = max(G, key = lambda x: len(G[x]))
        neighbours = G.pop(chosen)
        result.append(chosen)

        for v in neighbours:
            G[v].remove(chosen)
            if not G[v]:
                G.pop(v)
            
    return result

def optimized_lognaprox(G: list[list[int]]) -> list[int]:
    edges = edgeList(G)
    G = {v: set(neighbours) for v, neighbours in enumerate(G) if neighbours}
    result = []
    
    while G:
        chosen = min(G, key = lambda x: len(G[x]))
        if len(G[chosen]) == 1:
            chosen = next(iter(G[chosen]))
        else:    
            chosen = max(G, key = lambda x: len(G[x]))

        neighbours = G.pop(chosen)
        result.append(chosen)

        for v in neighbours:
            G[v].remove(chosen)
            if not G[v]:
                G.pop(v)

    result = set(result)
    while True:
        for v in result:
            if isVC(edges, result - {v}):
                result.remove(v)
                break
        else:
            break

    return list(result)
