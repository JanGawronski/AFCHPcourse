from os import scandir
from dimacs import loadCNF
from time import time

def basic_solver(formula: list[list[int]]) -> tuple[dict[int, int] | str, int]:
    if formula == []:
        return ({}, 1)

    if formula is None:
        return (u'UNSAT', 1)

    (result1, calls1) = basic_solver(simplify_CNF(formula, {formula[0][0]: 1, -formula[0][0]: -1}))

    if result1 != u'UNSAT':
        return (result1 | {formula[0][0]: 1, -formula[0][0]: -1}, calls1 + 1)
    
    (result2, calls2) = basic_solver(simplify_CNF(formula, {formula[0][0]: -1, -formula[0][0]: 1}))

    if result2 != u'UNSAT':
        return (result2 | {formula[0][0]: -1, -formula[0][0]: 1}, calls1 + calls2 + 1)

    return (u'UNSAT', calls1 + calls2 + 1)

def simplify_clause(clause: list[int], evaluation: dict[int, int]) -> list[int]:
    return None if any(evaluation.get(literal, 0) > 0 for literal in clause) \
        else [literal for literal in clause if evaluation.get(literal, 0) == 0]

def simplify_CNF(formula: list[list[int]], evaluation: dict[int, int]) -> list[list[int]]:
    simplified = [simplify_clause(clause, evaluation) for clause in formula]
    if [] in simplified:
        return None
    return [clause for clause in simplified if clause is not None]

if __name__ == "__main__":
    for ((size, formula), filename) in sorted([(loadCNF("sat/" + file.name), file.name) for file in scandir("sat")]):
        start = time() 
        result, calls = basic_solver(formula)
        print(f"solver found that formula from {filename} is {"not " if result == u'UNSAT' else ""}satisfiable in {time() - start} seconds ({calls} calls) {"and it is true" if (result == u'UNSAT') == ("yes" not in filename) else "but it is false"}")
