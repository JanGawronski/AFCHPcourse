# Lab 3: Problem SAT (część 1)

W ramach laboratorium należy:

1. Wykonać zadanie pierwsze: przejście fazowe SAT
2. Wykonać redukcję z problemu X3C do SAT
3. Wykonać redukcję problemu kolorowania grafów do SAT

## Szczegóły techniczne

Wszystkie programy powinny być implementowane w języku Python (wersja 3.x.y). Mogą Państwo (i powinni) korzystać z poniższych programów:

- [dimacs.py](dimacs.py) - mikrobiblioteka pozwalająca na wczytywanie grafów, nagrywanie wyników, najbardziej podstawowe operacje na grafach, oraz nagrywanie formuł logicznych CNF w formacie DIMACS ascii (z którego korzystają solwery SAT)
    
- Biblioteka [pycoSAT](https://pypi.org/project/pycosat/)
    
- Solwery [glucose](http://www.labri.fr/perso/lsimon/glucose/) lub [maple](https://sites.google.com/a/gsd.uwaterloo.ca/maplesat/).
### pycoSAT

Biblioteka pycoSAT tworzy interface do solwera [PicoSAT](http://fmv.jku.at/picosat/) dla języka Python (PicoSAT odnosił sukcesy na turniejach rozwiązywania instancji SAT—[SAT Competition](http://www.satcompetition.org/)—ok. roku 2007; dzięki wygodnemu interface’owi będzie świetnym narzędziem na początek)

**Instalacja pycoSAT**. Należy zainstalować pakiet `pycosat` wykonując polecenie `pip install pycosat` (w niektórych systemach `pip3` zamiast `pip`)

**Reprezentacja formuł**. pycoSAT reprezentuje formuły jako listy klauzul, gdzie każda klauzula to lista numerów zmiennych, które w niej występują. Wartość ujemna oznacza zanegowanie danej zmiennej. Na przykład lista:

```
cnf = [ [-1,2,3], [2,-3], [1,-2,-3] ]
```

reprezentuje formułę ( -x1 ∨ x2 ∨ x3 ) ∧ ( x2 ∨ -x3 ) ∧ ( x1 ∨ -x2 ∨ -x3 ). Zmienna o numerze 0 nie istnieje.

**Szukanie rozwiązania**. Aby sprawdzić czy formuła jest spełnialna i znaleźć odpowiednie wartościowanie należy wykonać funkcję `solve( cnf )`. Poniższy kod pokazuje przykład:

```
import pycosat
cnf = [ [-1,2,3], [2,-3], [1,-2,-3] ]
sol = pycosat.solve( cnf )
print( sol )
```

Ten kod jako wyjście wypisze `[-1, 2, -3]`, co oznacza, że formuła jest spełnialna i świadczy o tym wartościowanie:

- _x1_ = `fałsz`,
- _x2_ = `prawda`,
- _x3_ = `fałsz`.

Formalnie, funkcja `solve` zwraca następujące wartości:

- napis `u'UNSAT'` jeśli formuła jest niespełnialna
- listę numerów zmiennych, gdzie zmienna występuje jako ujemna jeśli w rozwiązaniu ma logiczną wartość `fałsz` oraz dodatnią jeśli w rozwiązaniu ma wartość `prawda`.

### dimacs.py

Tę mikrobibliotekę znają Państwo z [Laboratorium 1: VertexCover](../lab1). W ramach tego laboratorium pojawiły się dwie nowe funkcja:

```
saveCNF( name, cnf ) 
```

która nagrywa formułę ze zmiennej `cnf` (reprezentowaną jako lista klauzul) do pliku o nazwie `name` w formacie DIMACS ascii. Taki plik można bezpośrednio przekazać do zewnętrznego solwera. Druga nowa funkcja to:

```
loadX3C( name )
```

która wczytuje instancję problemu X3C (jest omówiona przy redukcji X3C do SAT).

### glucose i maple

Solwerami zewnętrznymi należy zająć się po zakończeniu wszystkich innych prac

glucose i maple to dwa solwery SAT (wywodzące się z tej samej bazy kodu), które odnosiły sukcesy w ostatnich turniejach SAT. Po ściągnięciu ich źródeł należy je skompilować.

Odpowiednie instrukcje znajdują się w pliku README. Sprowadza się to do wykonania poleceń:

```
cd simp
make rs
```

W przypadku glucose może być konieczna podmiana opcji kompilatora w pliku `mtl/template.mk` (zmiana linii zaczynającej się od `CFLAGS` na `CFLAGS ?= -Wall -Wno-parentheses -std=c++0x`).

_Wywołanie solwera_. Jeśli solwer ma nazwę `solver` oraz mamy plik `cnf` z zapisaną formułą, to należy wykonać polecenie:

```
solver cnf
```

## Zadanie 1: Przejście fazowe SAT

W ramach tego zadania należy sporządzić wykres, który pokazuje prawdopodobieństwo, że losowo wygenerowana formuła w formacie k-CNF (k literałów na klauzulę) jest spełnialna, w zależności od ilorazu liczby klauzul i liczby zmiennych.

**Generowanie losowej klauzuli.** Załóżmy, że mamy _n_ zmiennych do dyspozycji (o numerach _1, …, n_). Losowa klauzula rozmiaru _k_ składa się z losowo wybranych _k_ zmiennych (z powtarzaniem), z których każda jest zanegowana/niezanegowana z prawdopodobieństwem 1/2.

Od strony technicznej przydatny mozę być następuący fragment kodu:

```
import random         # biblioteka liczb pseudolosowych
n = 5
S = [1,-1]            # lista +/-
V = range(1,n+1)      # lista zmiennych 1...n
x = random.choice(V)*random.choice(S)  # losowo wybrana zmienna z losowym negowaniem     
print( x )
```

**Wykonanie eksperymentu.** Ustalmy _k=3_, czyli problem 3CNF-SAT. Proszę ustalić pewną liczbę zmiennych _n_ (np. 10, 50, 100) oraz pewną liczbę powtórzeń _T_ (np. _T = 100_). Następnie, dla wartości _a_ z przedziału 1 do 10 (np. z krokiem 0.1) proszę:

- Wygenerować _T_ formuł zawierających po _n_ zmiennych oraz _a \* n_ klauzul.
- Dla każdej wygenerowanej formuły sprawdzić, czy jest spełnialna.
- Zapisać liczbę _S_ spełnialnych formuł.
- Wypisać wartość _a_ oraz iloraz _S/T_.

Następnie proszę wygenerować wykres funkcji _S/T_ w zależności od _a_.

Proszę powtórzyć eksperyment dla kilku wartości _n_ oraz dla innej wartości _k_.

### Rysowanie wykresu

Jeśli dane są w pliku tekstowym `dane`, np. o treści:

```
1 0.1
2 0.4
3 0.8
4 0.16
5 0.32
```

to można zrobić ich wykres przy pomocy narzędzia `gnuplot`, wpisując w jego konsoli:

```
set yrange [-0.1:1.1]
plot "dane" using 1:2 with lines
```

**Alternatywa:** Wykorzystanie pakietu OpenOffice lub Google Sheets.

## Zadanie 2: Exact Cover by 3-Sets (X3C)

W tym zadaniu należy zaimplementować redukcję pewnego wariantu problemu X3C do SAT oraz wykorzystać solwer SAT do rozwiązywania przykładowych instancji X3C.

W problemie X3C mamy dany zbiór elementów _N = {1, …, 3k}_ oraz rodzinę zbiorów _S = {S1, …, Sm}_ gdzie _m <= 3k_. Każdy zbiór _Si_ zawiera trzy elementy ze zbioru _N_ a każdy element z _N_ występuje najwyżej w trzech zbiorach z rodziny _S_. Pytanie brzmi czy da się wybrać _k_ zbiorów tak, że każdy element zbioru _N_ należy do dokładnie jednego wybranego zbioru.

### Redukcja do SAT

Pomysł redukcji polega na tym, że dla każdego zbioru _Si_ tworzymy zmienną logiczną _xi_, której wartość interpretujemy następująco:

- jeśli _xi_ = 1 to zbiór \*Si należy do rozwiązania,
- jeśli _xi_ = 0 to zbiór \*Si nie należy do rozwiązania.

Następnie tworzymy następujące klauzule. Dla każdego elementu _j_ ze zbioru _N_ tworzymy klauzulę, która składa się ze zmiennych odpowiadających zbiorom, do których należy _j_. Na przykład, jeśli element _1_ należy do zbiorów _S6_, _S9_ oraz _S11_ to tworzymy klauzulę:

_( (x6 ∨ x9 ∨ x11) )_

która wymusza, że co najmniej jeden z tych zbiorów jest wybrany. Następnie dla każdej takiej klauzuli należy zapewnić, że żadne dwa zbiory zawierające ten sam element nie są wybrane jednocześnie. Dla powyższego przykładu wystarczy dodać trzy klauzule:

_( (-x6 ∨ -x9) ∧ (-x6 ∨ -x11) ∧ (-x9 ∨ -x11) )_

Każda z powyższych klauzul mówi, że spośród dwóch zbiorów co najwyżej jeden może być wybrany.

### Testowanie redukcji

Jako dane testowe proszę wykorzystać instancje X3C z katalogu [x3c/](x3c/). Nazwa pliku mówi, czy instancja ma rozwiązanie czy nie, oraz daje pogląd na temat rozmiaru danych (np. plik 10.yes.x3c ma rozwiązanie i zawiera zbiór N składający się z 3\*10 elementów). Instancje z tego pliku można wczytać przy pomocy funkcji

```
loadX3C( name )
```

która wczytuje instancję z pliku _name_ i zwraca parę _n, sets_, gdzie _n_ to liczba elementów do pokrycia (numerowanych od _1_ do _n_) a _sets_ to lista zbiorów, gdzie każdy zbiór jest listą trzyelementową. N

## Zadanie 3: Kolorowanie grafów

W tym zadaniu rozważamy problem kolorowania grafów, zdefiniowany następująco:

- Wejście: Graf nieskierowany _G_, liczba naturalna _k_.
- Pytanie: Czy da się przypisać każdemu z wierzchołków jeden z _k_ kolorów tak, żeby żadne dwa wierzchołki połączone krawędzią nie miały tego samego koloru.

W ramach zadania proszę napisać program, który wczytuje graf oraz dostaje liczbę _k_ dopuszczalnych kolorów, oblicza formułę logiczną, która jest spełnialna wtedy i tylko wtedy gdy graf posiada odpowiednie kolorowanie, sprawdza spełnialność tej formuły (i w przypadku spełnialności wypisuje numery kolorów przypisanych wierzchołkom).

### Redukcja do SAT

Można wykorzystać następującą redukcję do SAT. Mamy graf _G = (V,E)_, gdzie _V = {v1, …, vn}_ oraz _k_ kolorów do wykorzystania. Dla każdego wierzchołka _vi_ oraz koloru _j_ tworzymy zmienną _xi,j_, której wartość interepretujemy następująco:

- _xi,j_ = prawda – wierzchołek _vi_ ma kolor _j_,
- _xi,j_ = fałsz – wierzchołek _vi_ nie ma koloru _j_.

Dla każdego wierzchołka _xi_ tworzymy serię klauzul, które mówią, że ten wierzchołek ma dokładnie jeden kolor:

_( xi,1 ∨ xi,2 ∨ … ∨ xi,k ) ∧ ( -xi,1 ∨ -xi,2 ) ∧ ( -xi,1 ∨ -xi,3 ) ∧… ∧ ( -xi,1 ∨ -xi,k ) ∧ ( -xi,2 ∨ -xi,3 ) ∧ ( -xi,2 ∨ -xi,4 ) ∧ … ∧ ( -xi,2 ∨ -xi,k ) ∧ … ∧ ( -xi,k-1 ∨ -xi,k )_

Dla każdej krawędzi _{ vi,vt }_ i dla każdego koloru _j_ tworzymy klauzulę, która mówi, że oba wierzchołki nie mogą mieć jednocześnie koloru _j_:

_( -xi,j ∨ -xt,j )_

### Testowanie redukcji

Jako dane testowe proszę wykorzystać [zestaw grafów](coloring/) pochodzący ze zbioru benchmarków Graph Coloring Benchmarks ( [wygasły link](https://sites.google.com/site/graphcoloring/vertex-coloring)). Proszę pamiętać o odczytaniu kolorów wierzchołków z wartościowania formuły oraz zrobienia wewnętrznego testu w programie, sprawdzającego czy kolorowanie jest poprawne.

### Zewnętrzne solwery

Jeśli `pycoSAT` okaże się za wolny, można próbować nagrywać formułę na dysk (`saveCNF`) oraz uruchamiać solwery `glucose` lub `maple`.
