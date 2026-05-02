

class sorterNet:
    def __init__( self, start, lines, equiv ):
        self.start   = start        # first available variable
        self.current = start        # current variable ready to be used
        self.lines   = lines.copy() # current variables for the input lines
        self.equiv   = equiv        # generate equivalences (if true), or implications (if false)
        self.CNF     = []           # current formula


        
    def comp( self, i, j ):
        """add a comparator between lines i and j"""
        (i,j) = (max(i,j), min(i,j))
        # print("comp", i,j)
        oldi = self.lines[i]
        oldj = self.lines[j]
        newi = self.lines[i] = self.current
        newj = self.lines[j] = self.current+1
        self.current += 2

        self.CNF += [[-oldi,-oldj, newi],
                     [-oldi,newj], [-oldj, newj] ]

        if self.equiv:
            self.CNF += [[-newi, oldi], [-newi, oldj],
                         [-newj, oldi, oldj] ]


    def getCNF( self )  : return self.CNF
    def getLines( self ): return self.lines
        

