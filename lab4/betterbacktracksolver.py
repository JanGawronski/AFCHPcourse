from os import scandir
from dimacs import loadCNF
from time import time

def better_backtrack_solver(formula: list[list[int]]) -> tuple[dict[int, int] | str, int]:
    if formula == []:
        return ({}, 1)
    
    if formula is None:
        return (u'UNSAT', 1)
    
    head = formula[0]
    tail = formula[1:]
    
    evaluation = {head[0]: 1, -head[0]: -1}

    (result, calls) = better_backtrack_solver(simplify_CNF(tail, evaluation))

    if result != u'UNSAT':
        return (result, calls + 1)
    
    full_calls = calls + 1
    
    for past_literal, literal in zip(head, head[1:]):
        evaluation[ past_literal] = -1
        evaluation[-past_literal] =  1
        evaluation[ literal] =  1
        evaluation[-literal] = -1
            
        (result, calls) = better_backtrack_solver(simplify_CNF(tail, evaluation))

        full_calls += calls
        
        if result != u'UNSAT':
            return (result | evaluation, full_calls)

    return (u'UNSAT', full_calls)
    
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
        result, calls = better_backtrack_solver(formula)
        print(f"solver found that formula from {filename} is {"not " if result == u'UNSAT' else ""}satisfiable in {time() - start} seconds ({calls} calls) {"and it is true" if (result == u'UNSAT') == ("yes" not in filename) else "but it is false"}")
