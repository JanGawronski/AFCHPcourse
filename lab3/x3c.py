from dimacs import loadX3C
from pycosat import solve
from os import scandir

def is_x3c_sat(num_variables: int, sets: list[set[int]]) -> String | list[int]:
    variables = [[] for _ in range(num_variables)]
    for i, s in enumerate(sets):
        for v in s:
            variables[v - 1].append(i + 1)
    return solve(variables + [[-i, -j] for s in variables for i in s for j in s if i != j])

if __name__ == "__main__":
    for file in scandir("x3c"):
        sat = is_x3c_sat(*loadX3C("x3c/" + file.name))
        print(f"solver states that {file.name} is {"un" if sat == u'UNSAT' else ""}satisfiable {"and it is true" if (sat == u'UNSAT') == ("no" in file.name) else "but it is false"}")
