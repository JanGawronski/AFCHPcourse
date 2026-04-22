from random import choices 
from pycosat import solve
import matplotlib.pyplot as plt

def random_formula(k: int, num_variables: int, num_clauses: int) -> list[list[int]]:
    variables = list(range(1, num_variables + 1)) + [-x for x in range(1, num_variables + 1)]
    return [choices(variables, k = k) for _ in range(num_clauses)]

def random_sat(k: int, num_variables: int, tries: int, clause_range: tuple[int, int, int]) -> list[tuple[int, int]]:
    return [(num_clauses, sum(solve(random_formula(k, num_variables, num_clauses)) != u'UNSAT' for _ in range(tries))) for num_clauses in range(*clause_range)]

def plot(k: int, num_variables: int, tries: int, clause_range: tuple[int, int, int]):
    plt.figure(figsize=(9, 5))
    sat = random_sat(k, num_variables, tries, clause_range)
    plt.plot([num_clauses for (num_clauses, _) in sat], [satisfied / num_clauses for (num_clauses, satisfied) in sat])
    plt.xlabel(f"clauses ({num_variables} variables)")
    plt.ylabel("fraction satisfiable")
    plt.title(f"Satisfiability vs clause density ({k}-SAT)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("sat.png", dpi=300)


def plot_3d(ks: list[int], num_variables: int, tries: int, clause_range: tuple[int, int, int]):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    for k in ks:
        sat = random_sat(k, num_variables, tries, clause_range)
        xs = [num_clauses for num_clauses, _ in sat]
        ys = [k for _ in sat]
        zs = [num_satisfied / num_clauses for num_clauses, num_satisfied in sat]
        ax.plot(xs, ys, zs, marker="o", label=f"{k}-SAT")

    ax.set_xlabel("clauses")
    ax.set_ylabel("k")
    ax.set_zlabel("fraction satisfiable")
    ax.set_title(f"Satisfiability vs clauses and k ({num_variables} variables)")
    ax.legend()
    plt.tight_layout()
    plt.savefig("sat_3d.png", dpi=300)
    
if __name__ == "__main__":
    #print(random_sat(3, 100, 100, (100, 1000, 10)))
    plot(3, 100, 100, (100, 1000, 10))
    #plot_3d(ks=[3, 4, 5, 6, 7, 8, 9], num_variables=100, tries=100, clause_range=(100, 1000, 10))
