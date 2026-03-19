from dimacs import loadGraph, isVC, edgeList
from time import time
from twoaprox import twoaprox, optimized_twoaprox
from lognaprox import lognaprox, optimized_lognaprox
from simulatedannealing import simulated_annealing

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
("k330_d"),
("k330_e"),
("k330_f"),
("f30"),
("f35"),
("f40"),
("f56"),
("m20"),
("m30"),
("m40"),
("m50"),
("m100"),
("p20"),
("p35"),
("p60"),
("p150"),
("p200"),
("r30_01"),
("r30_05"),
("r50_001"),
("r50_01"),
("r50_05"),
("r100_005"),
("r100_01"),
("r200_001"),
("r200_005")
]

functions = [
    ("2-aprox", twoaprox),
    ("optimized 2-aprox", optimized_twoaprox),
    ("logn-aprox", lognaprox),
    ("optimized logn-aprox", optimized_lognaprox),
   ("simulated annealing", simulated_annealing)
]

for gname in graphs:
    G = loadGraph("graph/" + gname)
    edges = edgeList(G)
    print(f"graph: {gname}")

    for fname, function in functions: 
        start = time()
        cover = function(G)
        print(f"{fname}{"" if isVC(edges, cover) else " did not"} found solution in {time() - start} seconds of {len(cover)} vertices for graph of {len(edges)} vertices")
