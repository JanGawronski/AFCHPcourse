from dimacs import edgeList
def fibonacci_recursion(G: list[list[int]]):
    edges = edgeList(G)

    def VC(E: list[tuple[int]], cover: list[int], k: int):
        if k < 0:
            return None
        if len(E) == 0:
            return cover
        if k == 0:
            return None

        chosen = E[0][0]

        if [edge for edge in E[1:] for chosen in edge] != []:
            res = VC([edge for edge in E if chosen not in edge], cover + [chosen], k - 1)
            if res is not None:
                return res
        
        neighbours = [u if u != chosen else v for (u, v) in E if chosen in (u, v)]
        
        return VC([(u, v) for (u, v) in E if u not in neighbours and v not in neighbours], cover + neighbours, k - len(neighbours))

    for k in range(1, len(G)):
        res = VC(edges, [], k)
        if res is not None:
            return res
        
