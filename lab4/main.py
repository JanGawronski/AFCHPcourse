from sys import argv
from os import scandir
from time import time
from dimacs import loadCNF

from basicsolver import basic_solver
from betterbacktracksolver import better_backtrack_solver
from unitpropagationsolver import unit_propagation_solver
from fixedsigneliminationsolver import fixed_sign_elimination_solver
from setordersolver import set_order_solver 
from twocnfsolver import two_cnf_solver

solvers = {
    "basic": basic_solver,
    "betterbacktrack": better_backtrack_solver,
    "unitpropagation": unit_propagation_solver,
    "fixedsignelimination": fixed_sign_elimination_solver,
    "setorder": set_order_solver,
    "twocnf": two_cnf_solver
}

if __name__ == "__main__":
    if argv[1] not in solvers:
        print(f"{argv[1]} is not valid solver name")
        print("Known solvers:", *list(solvers.keys()))
        exit(code=1)

    files = argv[2:] if len(argv) > 2 else ["sat/" + file.name for file in scandir("sat")] 
    for ((size, formula), filename) in sorted([(loadCNF(file), file) for file in files]):
        start = time() 
        result, calls = solvers[argv[1]](formula)
        print(f"{argv[1]} solver found that formula from {filename} is {"not " if result == u'UNSAT' else ""}satisfiable in {time() - start} seconds ({calls} calls) {"and it is true" if (result == u'UNSAT') == ("yes" not in filename) else "but it is false"}")
        
