from dimacs import edgeList, isVC

def twoaprox(G: list[list[int]]) -> list[int]:
    edges = edgeList(G)
    result = set()
    while edges:
        u, v = edges.pop()
        if u not in result and v not in result:
            result.add(u)
            result.add(v)
    return list(result)

def optimized_twoaprox(G: list[list[int]]) -> list[int]:
    edges = edgeList(G)
    result = set()
    while edges:
        u, v = edges.pop()
        if u not in result and v not in result:
            result.add(u)
            result.add(v)

    edges = edgeList(G)
    while True:
        for v in result:
            if isVC(edges, result - {v}):
                result.remove(v)
                break
        else:
            break

    return list(result)
