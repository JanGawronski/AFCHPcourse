# Lab 5 Problem SAT (część 3: VertexCover i funkcja progowa)

W ramach laboratorium należy:

1.  Wykonać podstawową część redukcji Vertex Cover do SAT
2.  Wypróbować różne sposoby realizacji funkcji progowej

Grafy do testów należy wziąć z wcześniejszych laboratoriów.

## Szczegóły techniczne

Wszystkie programy powinny być implementowane w języku Python (wersja 3.x.y). Mogą Państwo (i powinni) korzystać z poniższych programów:

- [dimacs.py](dimacs.py) - mikrobiblioteka pozwalająca na wczytywanie grafów, nagrywanie wyników, najbardziej podstawowe operacje na grafach, oraz nagrywanie formuł logicznych CNF w formacie DIMACS ascii (z którego korzystają solwery SAT)
    
- [sortnet.py](sortnet.py) - mikrobiblioteka pozwalająca tworzyć formuły CNF implementujące sieci sortujące
    
- Biblioteka [pycoSAT](https://pypi.org/project/pycosat/)
    
- Solwery [glucose](http://www.labri.fr/perso/lsimon/glucose/) lub [maple](https://sites.google.com/a/gsd.uwaterloo.ca/maplesat/).
    

## Zadanie 1: VertexCover (podstawa redukcji)

Proszę zrealizować redukcję problemu VertexCover do SAT. Najpierw zajmiemy się elementarną częścią redukcji, a potem zrealizujemy funkcję progową.

### Redukcja SAT

Mamy graf _G = (V,E)_, gdzie _V = { v1, …, vn }_ oraz pytamy, czy istnieje pokrycie wierzchołkowe wykorzystujące _k_ wierzchołków. Dla każdego wierzchołka _vi_ tworzymy zmienną _xi_, której wartość interpretujemy następująco:

- _xi_ = prawda – wierzchołek _vi_ należy do pokrycia,
- _xi_ = fałsz – wierzchołek _vi_ nie należy do pokrycia.

Każda krawędź musi być pokryta przez jakiś wierzchołek. Stąd dla każdej krawędzi _{ vi,vj }_ tworzymy klauzulę wymagającą, że co najmniej jeden z jej końców został wybrany:

_( xi ∨ xj )_

Taka redukcja wystarcza, żeby solwer SAT znalazł _jakieś_ pokrycie wierzchołkowe, ale nic go nie zmusza do minimalizacji liczby użytych wierzchołków.

## Zadanie 2: Implementacja funkcji progowej

Trudniejszą częścią redukcji VertexCover do SAT jest wymuszenie, że najwyżej _k_ zmiennych spośród _x1, …, xn_ może mieć wartość `prawda`.

### Rozwiązanie a’la programowanie dynamiczne

W pierwszym podejściu tworzymy zmienne _yi,j_, które interpretujemy następująco:

- _yi,j_ = prawda – wśród zmiennych _x1, … ,xi_, co najmniej j ma wartość `prawda`,
- _yi,j_ = fałsz – powyższe nie zachodzi.

Wymuszamy poprawną wartość zmiennych następująco. Przede wszystkim zmienne _yi,0_ są prawdziwe dla wszystkich _i_, a zmienne _y0,j_ są fałszywe dla wszystkich _j_ > 0:

_( y0,0 ) ∧ ( y1,0 ) ∧ … ∧ ( yn,0 ) ∧ (-y0,1 ) ∧ ( -y0,2 ) ∧ … ∧ ( -y0,n )_

Następnie dla każdej pary wartości _0 < i,j ≤ n_ dodajemy następujące implikacje (każda z nich może być zapisana jako pojedyncza klauzula):

_( yi-1,j ⇒ yi,j ) ∧ ( ( yi-1,j-1 ∧ xi ) ⇒ yi,j )_

Na samym końcu dodajemy pojedynczą klauzulę:

_( -yn,k+1 )_

która wymusza, że nie używamy więcej niż _k_ wierzchołków do pokrycia.

### Indeksowanie zmiennych

W tym zadaniu należy odróżnić zmienne _xi_ od zmiennych _yi,j_. Niestety pycoSAT (oraz inne solwery) stosują prostą numerację zmiennych. W związku z tym konieczne jest tłumaczenie numerów “dwuwymiarowych” na jednowymiarowe. W tym celu przydatna może być poniższa funkcja, która zamienia parę indeksów _i, j_ na jedną, jednoznacznie określoną, liczbę naturalną:

```
def index( i, j ):
  return (i+j)*(i+j+1)/2+i
```

### Testowanie redukcji

Jako dane testowe proszę wykorzystać zestaw grafów z [poprzedniego laboratorium](../lab2): [graph/](graph/)

## Zadanie 2: Funkcja progowa zbudowana na sieci sortującej

Alternatywne rozwiązanie polega na zastosowaniu sieci sortujące. Sieć sortującą zrealizujemy w oparciu o clasę `sorterNet`:

```

class sorterNet:
    def __init__( self, start, lines, equiv ):
      # stwórz sieć sortującą
      # start -- numer pierwszej dostępnej zmiennej
      # lines -- tablica numerów zmiennych, które są sortowane
      # equiv -- czy komparatory mają być realizowane jako równoważności,
                 czy jako implikacje

        
    def comp( self, i, j ):
      # dodaj komparator między liniami i oraz j
      # większa wartość wędruje do linii o niższym numerze


    def getCNF( self )
      # odczytaj formułę realizującą zadane komparatory
      
    def getLines( self ):
      # odczytaj obecne numery zmiennych przechowujących kolejne linie
```

### Elementarny test

Sprawdź, czy powyższa klasa działa poprawnie. Stwórz formułę, która zmiennym 1, 2 i 3 przypisuje—na przykład—wartości False, True, False, stwórz obiekt `sorterNet` dla `lines = [1,2,3]` (oraz używającej równoważności) i dodaj komparatory (1,2), (2,3), (1,2). Przekonaj się, że połączenie Twojej formuły oraz tej, którą zwraca `sorterNet` poprawnie sortuje zmienne 1,2,3 (żeby to sprawdzić, musisz wywołać `getLines` po dodaniu komparatorów, żeby wiedzieć jaka zmienna realizuje jaką linię).

### Sieci sortujące

Najprostszą siecią sortującą jest sieć realizująca sortowanie przez wstawianie. W powyższym zadaniu stworzyliśmy taką sieć dla trzech linii. Można to łatwo uogólnić do sieci dla dowolnej liczby linii.

Wykład 6 zawiera także opis sieci opartej o MergeSort.

### Użycie sieci sortującej w redukcji VertexCover

Proszę połączyć sieci sortujące z poprzedniego punktu z redukcją z VertexCover. Najpierw wykonujemy elementarną część redukcji, która używa zmiennych od _1_ do _n_ do opisu wykorzystania wierzchołków. Następnie dodajemy sieć sortującą, która traktuje te zmienne jako linie wejściowe. Na koniec wymuszamy, że _k+1_\-sza linia ma wartość _False_

### Lepsze kodowanie funkcji progowej

Przedstawione metody kodowania warunku liczności nie są optymalne. Istnieje wiele lepszych metod, z których jedna jest opisana w pracy:
- M. Karpiński, M. Piotrów, Encoding cardinality constraints using multiway merge selection networks, Constraints, Vol. 24, str. 234–251, 2019. [PDF](https://link.springer.com/article/10.1007/s10601-019-09302-0)
