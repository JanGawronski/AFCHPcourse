#!/usr/bin/python3

from copy import deepcopy
import sys

RERAISE = False




def problem( s ):
  raise Exception( s )




def readBoard( fname ):
  f=open(fname)
  W,H,M = f.readline().strip('\n').split()
  W = int(W)
  H = int(H)
  M = int(M)
  board = []
  for i in range(H):
    line = f.readline().strip()
    line = [ d for d in line ]
    if len( line ) != W: raise Exception("Zla dlugosc wiersza w opisie planszy")
    board += [line]
    
  return W,H,M, board


def matchingBoards( iboard, oboard, M ):
  err = "Plansza z wejscia nie pasuje do planszy z wyjscia"  
  iH = len(iboard)
  iW = len(iboard[0])
  oH = len(oboard)
  oW = len(oboard[0])
  if iH != oH or iW != oW:
    problem( err + ": niezgodne rozmiary")

  for y in range(oH):
    for x in range(oW):
      if oboard[y][x] == "M": M-=1
      if oboard[y][x] in ["/","\\"] and iboard[y][x] != ".":
        problem(err + ": lustro w miejscu innego elementu")
      if oboard[y][x] not in ["/","\\"] and oboard[y][x] != iboard[y][x]:
        problem(err + ": niezgodne obiekty na planaszach")
  if M < 0:
    problem(err + ": uzyto zbyt wielu luster")
  return True
    
    



def drawBoard( board ):
  for line in board:
    print( "".join(line))
  print()




def raytrace( board, x,y, dx, dy, bound=None ):
  step = 0
  H = len(board)
  W = len(board[0])
  while True:
    if y < 0 or x < 0 or y >= H or x >= W: break
  
    if board[y][x] == ".":
      if dx != 0: board[y][x] = "="
      if dy != 0: board[y][x] = "I"
    if (board[y][x] == "=" and dy != 0) or (board[y][x] == "I" and dx != 0):
      board[y][x] = "+"
    if board[y][x] == "O":
      board[y][x] = "X"
    if board[y][x] == "#":
      break
    if board[y][x] == "/":
      dx,dy = -dy,-dx
    if board[y][x] == "\\":
      dx,dy = dy,dx
    x += dx
    y += dy
    step += 1
    if bound and step > bound: return
        

def alltrace( board ):
  H = len(board)
  W = len(board[0])
  B = W*H*2
  for y in range(H):
    for x in range(W):
      if board[y][x] == "A":
        raytrace( board, x,y, 0,-1, B)
      if board[y][x] == "V":
        raytrace( board, x,y, 0, 1, B)
      if board[y][x] == "<":
        raytrace( board, x,y,-1, 0, B)
      if board[y][x] == ">":
        raytrace( board, x,y, 1, 0, B)


def check( board ):
  H = len(iboard)
  W = len(iboard[0])
  for y in range(H):
    for x in range(W):
      if board[y][x] == "O": return False
  return True


    

  





if __name__=="__main__":
  if len(sys.argv)<3:
    print("Wywołanie:\n   judge.py <infile> <outfile> [-v]")
  else:
    view = len(sys.argv)==4 and sys.argv[3]=='-v'

    try:
      
      iW,iH,iM,iboard = readBoard(sys.argv[1])
      oW,oH,oM,oboard = readBoard(sys.argv[2])
      matchingBoards( iboard, oboard, iM )
      
      if view: drawBoard( iboard )
      alltrace( oboard )
      if view: drawBoard( oboard )

      if check( oboard ):
        print('OK')
        exit(0)
      else:
        problem("Koty pozostaly nieoswiecone. Kot Imperator jest rozczarowany.")
        exit(1)
            
    except Exception as e:
      print("WRONG")
      print(e)
      if RERAISE: raise e
      exit(1)
