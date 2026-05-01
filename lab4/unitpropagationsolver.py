from os import scandir
from dimacs import loadCNF
from time import time

def unit_propagation_solver(formula: list[list[int]]) -> tuple[dict[int, int] | str, int]:
    (formula, evaluation) = unit_propagation(formula)

    if formula == []:
        return ({}, 1)
    
    if formula is None:
        return (u'UNSAT', 1)
    
    head = formula[0]
    tail = formula[1:]
    
    evaluation |= {head[0]: 1, -head[0]: -1}

    (result, calls) = unit_propagation_solver(simplify_CNF(tail, evaluation))

    if result != u'UNSAT':
        return (result, calls + 1)
    
    full_calls = calls + 1
    
    for past_literal, literal in zip(head, head[1:]):
        evaluation[ past_literal] = -1
        evaluation[-past_literal] =  1
        evaluation[ literal] =  1
        evaluation[-literal] = -1
            
        (result, calls) = unit_propagation_solver(simplify_CNF(tail, evaluation))

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

def unit_propagation(formula: list[list[int]]) -> tuple[list[list[int]], dict[int, int]]:
    if formula is None:
        return (None, {})

    units = [clause[0] for clause in formula if len(clause) == 1]

    if len(units) > 0:
        formula, evaluation = unit_propagation(simplify_CNF(formula, {clause: 1 for clause in units} | {-clause: -1 for clause in units}))
        return (formula, evaluation | {clause: 1 for clause in units} | {-clause: -1 for clause in units})
        
    return (formula, {})

if __name__ == "__main__":
    for ((size, formula), filename) in sorted([(loadCNF("sat/" + file.name), file.name) for file in scandir("sat")]):
        start = time() 
        result, calls = unit_propagation_solver(formula)
        print(f"solver found that formula from {filename} is {"not " if result == u'UNSAT' else ""}satisfiable in {time() - start} seconds ({calls} calls) {"and it is true" if (result == u'UNSAT') == ("yes" not in filename) else "but it is false"}")
