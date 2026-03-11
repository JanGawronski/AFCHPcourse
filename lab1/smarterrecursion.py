from dimacs import edgeList
def smarter_recursion(G: list[list[int]]):
    edges = edgeList(G)

    def VC(E: list[tuple[int]], cover: list[int], k: int):
        if k < 0:
            return None
        if len(E) == 0:
            return cover
        if k == 0:
            return None

        count = {}
        
        for u, v in E:
            count[u] = count.get(u, 0) + 1 
            count[v] = count.get(v, 0) + 1

        chosen = max(count, key = lambda x: count[x])

        if count[chosen] <= 2:
            smallest = min(count, key = lambda x: count[x])
            chosen_edge = [edge for edge in E if smallest in edge][0]
            if count[chosen_edge[0]] == 1:
                neighbour = chosen_edge[1]
            else:
                neighbour = chosen_edge[0]
                
            return VC([edge for edge in E if neighbour not in edge], cover + [chosen], k - 1)
            
        res = VC([edge for edge in E if chosen not in edge], cover + [chosen], k - 1)

        if res is not None:
            return res

        neighbours = [u if u != chosen else v for (u, v) in E if chosen in (u, v)]
        
        return VC([(u, v) for (u, v) in E if u not in neighbours or v not in neighbours], cover + neighbours, k - len(neighbours))

    for k in range(1, len(G)):
        res = VC(edges, [], k)
        if res is not None:
            return res
        
