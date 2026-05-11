#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { DIR_N = 0, DIR_E = 1, DIR_S = 2, DIR_W = 3 };

static const int DX[4] = {0, 1, 0, -1};
static const int DY[4] = {-1, 0, 1, 0};
static const int SLASH_TURN[4] = {1, 0, 3, 2};
static const int BACK_TURN[4] = {3, 2, 1, 0};

typedef struct {
    int *a;
    int n;
    int cap;
} IntVec;

typedef struct {
    int *lit_data;
    int lit_n;
    int lit_cap;
    int *cl_off;
    int *cl_len;
    int cl_n;
    int cl_cap;
    int var_count;
    int true_var;
} CNF;

typedef struct {
    int x, y, d;
} Laser;

static void die_oom(void) {
    fprintf(stderr, "Out of memory\n");
    exit(1);
}

static void *xmalloc(size_t n) {
    void *p = malloc(n);
    if (!p) die_oom();
    return p;
}

static void *xcalloc(size_t c, size_t s) {
    void *p = calloc(c, s);
    if (!p) die_oom();
    return p;
}

static void *xrealloc(void *p, size_t n) {
    void *q = realloc(p, n);
    if (!q) die_oom();
    return q;
}

static void ivec_init(IntVec *v) {
    v->a = NULL;
    v->n = 0;
    v->cap = 0;
}

static void ivec_push(IntVec *v, int x) {
    if (v->n == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 8;
        v->a = (int *)xrealloc(v->a, (size_t)v->cap * sizeof(int));
    }
    v->a[v->n++] = x;
}

static void ivec_free(IntVec *v) {
    free(v->a);
    v->a = NULL;
    v->n = 0;
    v->cap = 0;
}

static void cnf_init(CNF *cnf) {
    memset(cnf, 0, sizeof(*cnf));
}

static int cnf_new_var(CNF *cnf) {
    cnf->var_count++;
    return cnf->var_count;
}

static void cnf_reserve_lits(CNF *cnf, int add) {
    int need = cnf->lit_n + add;
    if (need <= cnf->lit_cap) return;
    int nc = cnf->lit_cap ? cnf->lit_cap : 1024;
    while (nc < need) nc *= 2;
    cnf->lit_data = (int *)xrealloc(cnf->lit_data, (size_t)nc * sizeof(int));
    cnf->lit_cap = nc;
}

static void cnf_reserve_clauses(CNF *cnf, int add) {
    int need = cnf->cl_n + add;
    if (need <= cnf->cl_cap) return;
    int nc = cnf->cl_cap ? cnf->cl_cap : 1024;
    while (nc < need) nc *= 2;
    cnf->cl_off = (int *)xrealloc(cnf->cl_off, (size_t)nc * sizeof(int));
    cnf->cl_len = (int *)xrealloc(cnf->cl_len, (size_t)nc * sizeof(int));
    cnf->cl_cap = nc;
}

static void cnf_add_clause(CNF *cnf, const int *lits, int n) {
    cnf_reserve_clauses(cnf, 1);
    cnf_reserve_lits(cnf, n);
    cnf->cl_off[cnf->cl_n] = cnf->lit_n;
    cnf->cl_len[cnf->cl_n] = n;
    memcpy(cnf->lit_data + cnf->lit_n, lits, (size_t)n * sizeof(int));
    cnf->lit_n += n;
    cnf->cl_n++;
}

static void cnf_add1(CNF *cnf, int a) {
    int lits[1] = {a};
    cnf_add_clause(cnf, lits, 1);
}

static void cnf_add2(CNF *cnf, int a, int b) {
    int lits[2] = {a, b};
    cnf_add_clause(cnf, lits, 2);
}

static void cnf_add3(CNF *cnf, int a, int b, int c) {
    int lits[3] = {a, b, c};
    cnf_add_clause(cnf, lits, 3);
}

static void cnf_add4(CNF *cnf, int a, int b, int c, int d) {
    int lits[4] = {a, b, c, d};
    cnf_add_clause(cnf, lits, 4);
}

static int cnf_true_var(CNF *cnf) {
    if (!cnf->true_var) {
        cnf->true_var = cnf_new_var(cnf);
        cnf_add1(cnf, cnf->true_var);
    }
    return cnf->true_var;
}

static void cnf_free(CNF *cnf) {
    free(cnf->lit_data);
    free(cnf->cl_off);
    free(cnf->cl_len);
    memset(cnf, 0, sizeof(*cnf));
}

static void add_at_most_k(CNF *cnf, const int *lits, int n, int k) {
    if (k >= n) return;
    if (k == 0) {
        for (int i = 0; i < n; i++) cnf_add1(cnf, -lits[i]);
        return;
    }

    int cols = k + 1;
    int *svar = (int *)xcalloc((size_t)n * cols, sizeof(int));
#define S_RAW(i, j) (svar[(i) * cols + (j)])
#define S_GET(i, j) ((S_RAW((i), (j)) != 0) ? S_RAW((i), (j)) : (S_RAW((i), (j)) = cnf_new_var(cnf)))

    cnf_add2(cnf, -lits[0], S_GET(0, 1));
    for (int i = 1; i < n; i++) {
        cnf_add2(cnf, -lits[i], S_GET(i, 1));
        cnf_add2(cnf, -S_GET(i - 1, 1), S_GET(i, 1));
    }

    for (int i = 1; i < n; i++) {
        int lim = i + 1;
        if (lim > k) lim = k;
        for (int j = 2; j <= lim; j++) {
            cnf_add3(cnf, -lits[i], -S_GET(i - 1, j - 1), S_GET(i, j));
            cnf_add2(cnf, -S_GET(i - 1, j), S_GET(i, j));
        }
    }

    for (int i = k; i < n; i++) {
        cnf_add2(cnf, -lits[i], -S_GET(i - 1, k));
    }

    free(svar);
#undef S_RAW
#undef S_GET
}

static void add_lt_if(CNF *cnf, int cond_var, const int *ru, const int *rv, int bits) {
    int true_lit = cnf_true_var(cnf);
    int eq_next = true_lit;
    int *t_lits = (int *)xmalloc((size_t)bits * sizeof(int));

    for (int idx = 0; idx < bits; idx++) {
        int i = bits - 1 - idx;
        int u = ru[i];
        int v = rv[i];

        int t = cnf_new_var(cnf);
        t_lits[idx] = t;
        cnf_add2(cnf, -t, eq_next);
        cnf_add2(cnf, -t, -u);
        cnf_add2(cnf, -t, v);
        cnf_add4(cnf, -eq_next, u, -v, t);

        int eq = cnf_new_var(cnf);
        cnf_add2(cnf, -eq, eq_next);
        cnf_add3(cnf, -eq, -u, v);
        cnf_add3(cnf, -eq, u, -v);
        cnf_add4(cnf, -eq_next, -u, -v, eq);
        cnf_add4(cnf, -eq_next, u, v, eq);
        eq_next = eq;
    }

    int *final_clause = (int *)xmalloc((size_t)(bits + 1) * sizeof(int));
    final_clause[0] = -cond_var;
    for (int i = 0; i < bits; i++) final_clause[i + 1] = t_lits[i];
    cnf_add_clause(cnf, final_clause, bits + 1);

    free(final_clause);
    free(t_lits);
}

enum { END = -9, UNSAT = 0, SAT = 1, MARK = 2, IMPLIED = 6 };

typedef struct {
    int *DB, nVars, nClauses, mem_used, mem_fixed, mem_max, maxLemmas, nLemmas, *buffer, nConflicts, *model,
        *reason, *falseStack, *falselit, *first, *forced, *processed, *assigned, *next, *prev, head, res, fast, slow;
} MicroSolver;

static void ms_unassign(MicroSolver *S, int lit) { S->falselit[lit] = 0; }

static void ms_restart(MicroSolver *S) {
    while (S->assigned > S->forced) ms_unassign(S, *(--S->assigned));
    S->processed = S->forced;
}

static void ms_assign(MicroSolver *S, int *reason, int forced) {
    int lit = reason[0];
    S->falselit[-lit] = forced ? IMPLIED : 1;
    *(S->assigned++) = -lit;
    S->reason[abs(lit)] = 1 + (int)(reason - S->DB);
    S->model[abs(lit)] = (lit > 0);
}

static void ms_addWatch(MicroSolver *S, int lit, int mem) {
    S->DB[mem] = S->first[lit];
    S->first[lit] = mem;
}

static int *ms_getMemory(MicroSolver *S, int mem_size) {
    if (S->mem_used + mem_size > S->mem_max) {
        return NULL;
    }
    int *store = (S->DB + S->mem_used);
    S->mem_used += mem_size;
    return store;
}

static int *ms_addClause(MicroSolver *S, int *in, int size, int irr) {
    int i, used = S->mem_used;
    int *base = ms_getMemory(S, size + 3);
    if (!base) return NULL;
    int *clause = base + 2;
    if (size > 1) {
        ms_addWatch(S, in[0], used);
        ms_addWatch(S, in[1], used + 1);
    }
    for (i = 0; i < size; i++) clause[i] = in[i];
    clause[i] = 0;
    if (irr) S->mem_fixed = S->mem_used;
    else S->nLemmas++;
    return clause;
}

static void ms_reduceDB(MicroSolver *S, int k) {
    while (S->nLemmas > S->maxLemmas) S->maxLemmas += 300;
    S->nLemmas = 0;

    for (int i = -S->nVars; i <= S->nVars; i++) {
        if (i == 0) continue;
        int *watch = &S->first[i];
        while (*watch != END)
            if (*watch < S->mem_fixed) watch = (S->DB + *watch);
            else *watch = S->DB[*watch];
    }

    int old_used = S->mem_used;
    S->mem_used = S->mem_fixed;
    for (int i = S->mem_fixed + 2; i < old_used; i += 3) {
        int count = 0, head = i;
        while (S->DB[i]) {
            int lit = S->DB[i++];
            if ((lit > 0) == S->model[abs(lit)]) count++;
        }
        if (count < k) {
            int *clause = ms_addClause(S, S->DB + head, i - head, 0);
            if (!clause) return;
        }
    }
}

static void ms_bump(MicroSolver *S, int lit) {
    if (S->falselit[lit] != IMPLIED) {
        S->falselit[lit] = MARK;
        int var = abs(lit);
        if (var != S->head) {
            S->prev[S->next[var]] = S->prev[var];
            S->next[S->prev[var]] = S->next[var];
            S->next[S->head] = var;
            S->prev[var] = S->head;
            S->head = var;
        }
    }
}

static int ms_implied(MicroSolver *S, int lit) {
    if (S->falselit[lit] > MARK) return (S->falselit[lit] & MARK);
    if (!S->reason[abs(lit)]) return 0;
    int *p = (S->DB + S->reason[abs(lit)] - 1);
    while (*(++p))
        if ((S->falselit[*p] ^ MARK) && !ms_implied(S, *p)) {
            S->falselit[lit] = IMPLIED - 1;
            return 0;
        }
    S->falselit[lit] = IMPLIED;
    return 1;
}

static int *ms_analyze(MicroSolver *S, int *clause) {
    S->res++;
    S->nConflicts++;
    while (*clause) ms_bump(S, *(clause++));
    while (S->reason[abs(*(--S->assigned))]) {
        if (S->falselit[*S->assigned] == MARK) {
            int *check = S->assigned;
            while (S->falselit[*(--check)] != MARK)
                if (!S->reason[abs(*check)]) goto build;
            clause = S->DB + S->reason[abs(*S->assigned)];
            while (*clause) ms_bump(S, *(clause++));
        }
        ms_unassign(S, *S->assigned);
    }

build:;
    int size = 0, lbd = 0, flag = 0;
    int *p = S->processed = S->assigned;
    while (p >= S->forced) {
        if ((S->falselit[*p] == MARK) && !ms_implied(S, *p)) {
            S->buffer[size++] = *p;
            flag = 1;
        }
        if (!S->reason[abs(*p)]) {
            lbd += flag;
            flag = 0;
            if (size == 1) S->processed = p;
        }
        S->falselit[*(p--)] = 1;
    }

    S->fast -= S->fast >> 5;
    S->fast += lbd << 15;
    S->slow -= S->slow >> 15;
    S->slow += lbd << 5;

    while (S->assigned > S->processed) ms_unassign(S, *(S->assigned--));
    ms_unassign(S, *S->assigned);
    S->buffer[size] = 0;
    return ms_addClause(S, S->buffer, size, 0);
}

static int ms_propagate(MicroSolver *S) {
    int forced = S->reason[abs(*S->processed)];
    while (S->processed < S->assigned) {
        int lit = *(S->processed++);
        int *watch = &S->first[lit];
        while (*watch != END) {
            int i, unit = 1;
            int *clause = (S->DB + *watch + 1);
            if (clause[-2] == 0) clause++;
            if (clause[0] == lit) clause[0] = clause[1];
            for (i = 2; unit && clause[i]; i++)
                if (!S->falselit[clause[i]]) {
                    clause[1] = clause[i];
                    clause[i] = lit;
                    int store = *watch;
                    unit = 0;
                    *watch = S->DB[*watch];
                    ms_addWatch(S, clause[1], store);
                }
            if (unit) {
                clause[1] = lit;
                watch = (S->DB + *watch);
                if (S->falselit[-clause[0]]) continue;
                if (!S->falselit[clause[0]]) {
                    ms_assign(S, clause, forced);
                } else {
                    if (forced) return UNSAT;
                    int *lemma = ms_analyze(S, clause);
                    if (!lemma) return UNSAT;
                    if (!lemma[1]) forced = 1;
                    ms_assign(S, lemma, forced);
                    break;
                }
            }
        }
    }
    if (forced) S->forced = S->processed;
    return SAT;
}

static int ms_solve(MicroSolver *S) {
    int decision = S->head;
    S->res = 0;
    for (;;) {
        int old_nLemmas = S->nLemmas;
        if (ms_propagate(S) == UNSAT) return UNSAT;

        if (S->nLemmas > old_nLemmas) {
            decision = S->head;
            if (S->fast > (S->slow / 100) * 125) {
                S->res = 0;
                S->fast = (S->slow / 100) * 125;
                ms_restart(S);
                if (S->nLemmas > S->maxLemmas) ms_reduceDB(S, 6);
            }
        }

        while (S->falselit[decision] || S->falselit[-decision]) {
            decision = S->prev[decision];
        }
        if (decision == 0) return SAT;

        decision = S->model[decision] ? decision : -decision;
        S->falselit[-decision] = 1;
        *(S->assigned++) = -decision;
        decision = abs(decision);
        S->reason[decision] = 0;
    }
}

static int ms_init(MicroSolver *S, int n, int m, int mem_max) {
    if (n < 1) n = 1;
    if (mem_max < 1024) mem_max = 1024;

    S->nVars = n;
    S->nClauses = m;
    S->mem_max = mem_max;
    S->mem_used = 0;
    S->nLemmas = 0;
    S->nConflicts = 0;
    S->maxLemmas = 2000;
    S->fast = S->slow = 1 << 24;

    S->DB = (int *)malloc((size_t)S->mem_max * sizeof(int));
    if (!S->DB) return 0;

    S->model = ms_getMemory(S, n + 1);
    S->next = ms_getMemory(S, n + 1);
    S->prev = ms_getMemory(S, n + 1);
    S->buffer = ms_getMemory(S, n);
    S->reason = ms_getMemory(S, n + 1);
    S->falseStack = ms_getMemory(S, n + 1);
    S->forced = S->falseStack;
    S->processed = S->falseStack;
    S->assigned = S->falseStack;
    S->falselit = ms_getMemory(S, 2 * n + 1);
    S->first = ms_getMemory(S, 2 * n + 1);
    if (!S->model || !S->next || !S->prev || !S->buffer || !S->reason || !S->falseStack || !S->falselit || !S->first) {
        free(S->DB);
        return 0;
    }

    S->falselit += n;
    S->first += n;
    S->DB[S->mem_used++] = 0;

    for (int i = 1; i <= n; i++) {
        S->prev[i] = i - 1;
        S->next[i - 1] = i;
        S->model[i] = S->falselit[-i] = S->falselit[i] = 0;
        S->first[i] = S->first[-i] = END;
    }
    S->head = n;
    return 1;
}

static int solve_cnf_microsat(const CNF *cnf, signed char *assign_out) {
    MicroSolver S;
    memset(&S, 0, sizeof(S));

    long long base = (long long)cnf->lit_n + 3LL * cnf->cl_n + 32LL * cnf->var_count + 1024;
    long long mem_max_ll = base * 8;
    if (mem_max_ll < (1LL << 20)) mem_max_ll = (1LL << 20);
    if (mem_max_ll > 1200000000LL) mem_max_ll = 1200000000LL;
    int mem_max = (int)mem_max_ll;

    if (!ms_init(&S, cnf->var_count, cnf->cl_n, mem_max)) {
        return UNSAT;
    }

    for (int ci = 0; ci < cnf->cl_n; ci++) {
        int off = cnf->cl_off[ci];
        int len = cnf->cl_len[ci];
        for (int k = 0; k < len; k++) {
            S.buffer[k] = cnf->lit_data[off + k];
        }
        int *clause = ms_addClause(&S, S.buffer, len, 1);
        if (!clause) {
            free(S.DB);
            return UNSAT;
        }
        if (!len || ((len == 1) && S.falselit[clause[0]])) {
            free(S.DB);
            return UNSAT;
        }
        if ((len == 1) && !S.falselit[-clause[0]]) {
            ms_assign(&S, clause, 1);
        }
    }

    int res = ms_solve(&S);
    if (res == SAT) {
        for (int v = 1; v <= cnf->var_count; v++) {
            assign_out[v] = S.model[v] ? 1 : -1;
        }
    }
    free(S.DB);
    return res;
}

int main(void) {
    int W, H, L;
    if (scanf("%d %d %d", &W, &H, &L) != 3) return 0;
    if (W <= 0 || H <= 0) return 0;

    int N = W * H;
    char *board = (char *)xmalloc((size_t)N);
    char *line = (char *)xmalloc((size_t)W + 5);

    int *slash_var = (int *)xcalloc((size_t)N, sizeof(int));
    int *back_var = (int *)xcalloc((size_t)N, sizeof(int));
    IntVec mirror_lits;
    ivec_init(&mirror_lits);

    Laser *lasers = (Laser *)xmalloc((size_t)N * sizeof(Laser));
    int laser_count = 0;
    int *cat_idx = (int *)xmalloc((size_t)N * sizeof(int));
    int cat_count = 0;

    for (int y = 0; y < H; y++) {
        if (scanf("%s", line) != 1) return 0;
        for (int x = 0; x < W; x++) {
            char c = line[x];
            int idx = y * W + x;
            board[idx] = c;
            if (c == 'A' || c == 'V' || c == '<' || c == '>') {
                int d = (c == 'A') ? DIR_N : (c == '>') ? DIR_E : (c == 'V') ? DIR_S : DIR_W;
                lasers[laser_count].x = x;
                lasers[laser_count].y = y;
                lasers[laser_count].d = d;
                laser_count++;
            } else if (c == 'O') {
                cat_idx[cat_count++] = idx;
            }
        }
    }
    free(line);

    CNF cnf;
    cnf_init(&cnf);

    for (int idx = 0; idx < N; idx++) {
        if (board[idx] != '.') continue;
        int s = cnf_new_var(&cnf);
        int b = cnf_new_var(&cnf);
        slash_var[idx] = s;
        back_var[idx] = b;
        ivec_push(&mirror_lits, s);
        ivec_push(&mirror_lits, b);
        cnf_add2(&cnf, -s, -b);
    }

    add_at_most_k(&cnf, mirror_lits.a, mirror_lits.n, L);

    int *cell_base = (int *)xmalloc((size_t)N * sizeof(int));
    int states = 0;
    for (int idx = 0; idx < N; idx++) {
        if (board[idx] == '#') cell_base[idx] = -1;
        else {
            cell_base[idx] = states;
            states += 4;
        }
    }

    int *x_state = (int *)xmalloc((size_t)states * sizeof(int));
    for (int i = 0; i < states; i++) x_state[i] = cnf_new_var(&cnf);

    unsigned char *is_source = (unsigned char *)xcalloc((size_t)states, 1);
    for (int i = 0; i < laser_count; i++) {
        int idx = lasers[i].y * W + lasers[i].x;
        int sid = cell_base[idx] + lasers[i].d;
        is_source[sid] = 1;
        cnf_add1(&cnf, x_state[sid]);
    }

    int rank_bits = 1;
    while ((1 << rank_bits) < (states + 1) && rank_bits < 30) rank_bits++;
    if (rank_bits < 1) rank_bits = 1;

    int *rank = (int *)xmalloc((size_t)states * rank_bits * sizeof(int));
    for (int s = 0; s < states; s++) {
        for (int b = 0; b < rank_bits; b++) {
            rank[s * rank_bits + b] = cnf_new_var(&cnf);
        }
    }

    IntVec *incoming = (IntVec *)xmalloc((size_t)states * sizeof(IntVec));
    for (int i = 0; i < states; i++) ivec_init(&incoming[i]);

    for (int y = 0; y < H; y++) {
        for (int x = 0; x < W; x++) {
            int idx = y * W + x;
            if (board[idx] == '#') continue;
            int base = cell_base[idx];

            for (int d = 0; d < 4; d++) {
                int u = base + d;
                int mode_nd[3];
                int mode_cond_len[3];
                int mode_cond_a[3];
                int mode_cond_b[3];
                int mode_count = 0;

                if (board[idx] == '.') {
                    mode_nd[mode_count] = d;
                    mode_cond_len[mode_count] = 2;
                    mode_cond_a[mode_count] = -slash_var[idx];
                    mode_cond_b[mode_count] = -back_var[idx];
                    mode_count++;

                    mode_nd[mode_count] = SLASH_TURN[d];
                    mode_cond_len[mode_count] = 1;
                    mode_cond_a[mode_count] = slash_var[idx];
                    mode_count++;

                    mode_nd[mode_count] = BACK_TURN[d];
                    mode_cond_len[mode_count] = 1;
                    mode_cond_a[mode_count] = back_var[idx];
                    mode_count++;
                } else {
                    mode_nd[mode_count] = d;
                    mode_cond_len[mode_count] = 0;
                    mode_count++;
                }

                for (int m = 0; m < mode_count; m++) {
                    int nd = mode_nd[m];
                    int nx = x + DX[nd];
                    int ny = y + DY[nd];
                    if (nx < 0 || nx >= W || ny < 0 || ny >= H) continue;
                    int nidx = ny * W + nx;
                    if (board[nidx] == '#') continue;

                    int v = cell_base[nidx] + nd;
                    int p = cnf_new_var(&cnf);
                    ivec_push(&incoming[v], p);

                    cnf_add2(&cnf, -p, x_state[u]);
                    cnf_add2(&cnf, -p, x_state[v]);
                    if (mode_cond_len[m] >= 1) cnf_add2(&cnf, -p, mode_cond_a[m]);
                    if (mode_cond_len[m] >= 2) cnf_add2(&cnf, -p, mode_cond_b[m]);

                    add_lt_if(&cnf, p, &rank[u * rank_bits], &rank[v * rank_bits], rank_bits);
                }
            }
        }
    }

    for (int s = 0; s < states; s++) {
        if (is_source[s]) continue;
        if (incoming[s].n == 0) {
            cnf_add1(&cnf, -x_state[s]);
        } else {
            int len = incoming[s].n + 1;
            int *cl = (int *)xmalloc((size_t)len * sizeof(int));
            cl[0] = -x_state[s];
            for (int i = 0; i < incoming[s].n; i++) cl[i + 1] = incoming[s].a[i];
            cnf_add_clause(&cnf, cl, len);
            free(cl);
        }
    }

    for (int ci = 0; ci < cat_count; ci++) {
        int idx = cat_idx[ci];
        int b = cell_base[idx];
        int cl[4] = {x_state[b], x_state[b + 1], x_state[b + 2], x_state[b + 3]};
        cnf_add_clause(&cnf, cl, 4);
    }

    signed char *assignment = (signed char *)xcalloc((size_t)cnf.var_count + 1, sizeof(signed char));
    int sat = solve_cnf_microsat(&cnf, assignment);

    char *out = (char *)xmalloc((size_t)N);
    memcpy(out, board, (size_t)N);
    if (sat == SAT) {
        for (int idx = 0; idx < N; idx++) {
            if (board[idx] != '.') continue;
            int s = slash_var[idx];
            int b = back_var[idx];
            if (s > 0 && assignment[s] == 1) out[idx] = '/';
            else if (b > 0 && assignment[b] == 1) out[idx] = '\\';
        }
    }

    printf("%d %d %d\n", W, H, L);
    for (int y = 0; y < H; y++) {
        for (int x = 0; x < W; x++) putchar(out[y * W + x]);
        putchar('\n');
    }

    free(out);
    free(assignment);
    for (int i = 0; i < states; i++) ivec_free(&incoming[i]);
    free(incoming);
    free(rank);
    free(is_source);
    free(x_state);
    free(cell_base);
    ivec_free(&mirror_lits);
    free(cat_idx);
    free(lasers);
    free(back_var);
    free(slash_var);
    free(board);
    cnf_free(&cnf);
    return 0;
}
