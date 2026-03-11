from itertools import combinations
from dimacs import edgeList, isVC

def bruteforce(G: list[list[int]]):
    all_edges = edgeList(G)
    for k in range(1, len(G) + 1):
        for subset in combinations(range(len(G)), k):
            if isVC(all_edges, subset):
                return subset
