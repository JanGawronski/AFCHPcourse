from dimacs import loadGraph, isVC, edgeList
from time import time
from bruteforce import bruteforce
from fibonaccirecursion import fibonacci_recursion
from smarterrecursion import smarter_recursion
from smarterrecursionkernel import smarter_recursion_with_kernel

graphs = [
("e5"),
("e10"),
("e20"),
("e40"),
("e150"),
("s25"),
("s50"),
("s500"),
("b20"),
("b30"),
("b100"),
("k330_a"),
("k330_b"),
("k330_c"),
("m20"),
("m30"),
("m40"),
("m50"),
("m100"),
("p20"),
("p35"),
("p60"),
("p150"),
("r30_01"),
("r30_05"),
("r50_001"),
("r50_01"),
("r50_05"),
("r100_005"),
]
functions = [
    #("bruteforce", bruteforce)
    #("fibonacci recursion", fibonacci_recursion)
    ("smarter recursion", smarter_recursion)
    #("smarter recursion with kernel", smarter_recursion_with_kernel)
]


for gname in graphs:
    G = loadGraph("graph/" + gname)
    edges = edgeList(G)
    print(f"graph: {gname}")

    for fname, function in functions: 
        start = time()
        cover = function(G)
        print(f"{fname}{"" if isVC(edges, cover) else " did not"} found solution in {time() - start} seconds of {len(cover)} vertices for graph of {len(edges)} vertices")
        
