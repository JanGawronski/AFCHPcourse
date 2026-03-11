from dimacs import edgeList
def kernelization(G: list[list[int]], k: int) -> list[list[int]]:
    edges = edgeList(G)

    def rotation(E: list[tuple[int]], cover: list[int], k: int):
        if len(E) == 0:
            return E, cover
        
        count = {}    
        for u, v in E:
            count[u] = count.get(u, 0) + 1 
            count[v] = count.get(v, 0) + 1

        smallest = min(count, key=lambda x: count[x])
        biggest = max(count, key=lambda x: count[x])
        
        if count[smallest] == 1:
            pair = [edge for edge in E if smallest in edge][0]
            if pair[0] == smallest:
                neighbour = pair[1]
            else:
                neighbour = pair[0]
            
            return rotation([edge for edge in E if neighbour not in edge], cover + [neighbour], k - 1)
        elif count[biggest] > k:
            return rotation([edge for edge in E if biggest not in edge], cover + [biggest], k - 1)
        else:
            return E, cover

    kernel_G = []

    vertex_mapping = {}
    vertex_reverse_mapping = []
    vertices = 0
    
    (kernel_edges, cover) = rotation(edges, [], k)

    for u, v in kernel_edges:
        if u not in vertex_mapping:
            vertex_mapping[u] = vertices
            vertex_reverse_mapping.append(u)
            vertices += 1
            kernel_G.append([])
        if v not in vertex_mapping:
            vertex_mapping[v] = vertices
            vertex_reverse_mapping.append(v)
            vertices += 1
            kernel_G.append([])
        
        kernel_G[vertex_mapping[u]].append(vertex_mapping[v])
        kernel_G[vertex_mapping[v]].append(vertex_mapping[u])

    return kernel_G, cover, vertex_reverse_mapping
