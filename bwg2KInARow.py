#!/usr/bin/python3.4

from re import *   # Loads the regular expression module.
from random import randint
from copy import deepcopy
import FiveInARowGameType as game
# import TicTacToeGameType as game

DIM=(0,0)
SIDE=0
K_WIN=0
OP_NAME=""

metWinCond=False

def_count=-1
DEFAULT_REMARK=[]

ZOBRIST_VALS=[]
Z_HASH_TABLE={}

#list of valid start squares for a win per dir
UD=[]
LR=[]
D1=[]
D2=[]

def prepare(init_state,K,what_side,op_name):
  global ZOBRIST_VALS,DIM,K_WIN,SIDE,OP_NAME
  OP_NAME=op_name
  K_WIN=K
  # 0 --> height, 1--> width
  DIM=(len(init_state[0]),len(init_state[0][0]))
  #throw exception if k exceeds boarders
  if DIM[0] < K_WIN or DIM[1] < K_WIN:
    raise ValueError("K greater than DIM" )
    return

  if what_side.lower()=='x': SIDE=1

  init_valid_square_lists()
  # init_board=parse_state(init_state)
  init_board=init_state[0]

  ZOBRIST_VALS=[[0]*2]*(DIM[0]*DIM[1])

  init_zobrist()
  init_default_remarks()

  return True


MAX_PLY=2
NEG_INF=-100000
POS_INF=100000
def makeMove(currState, currRemark, timeLim=10000):
  global ZOBRIST_VALS,Z_HASH_TABLE,DIM,K_WIN,SIDE,OP_NAME

  newboard=[]
  newRemark=""
  mm=mini_max(currState[0],currState[1],MAX_PLY)
  newboard=mm[0]
  bestEval=mm[1]

  # DEBUG#
  print("currstate\n"+display_board(currState[0])+\
        currState[1]+" placed at "+str(get_move(currState[0],newboard))+\
        "\nnewboard\n"+display_board(newboard)+\
        "bestVal="+str(bestEval)) #DEBUG#

  return [[get_move(currState[0],newboard),\
           [newboard,get_other(currState[1])]],\
            newRemark]

#pass whoseMove= 'x' or 'o'
def mini_max(board,whoseMove,plyRemaining):
  global Z_HASH_TABLE,metWinCond

  successors=[]; newboard=[]
  # determine if max or min player
  if whoseMove.lower()=='x': who='max'
  else: who='min'

  if plyRemaining == 0: #leaf node in look ahead
    # print("ply: "+str(MAX_PLY-plyRemaining)+"\n"+display_board(board)+"staticEval="+str(staticEval(board))) #DEBUG#
    return [board,staticEval(board)]
  if who=='max':
    minimaxVal=-100000
    successors=get_successors(board,'x')
  else:
    minimaxVal=100000
    successors=get_successors(board,'o')
  #DEBUG#
  # print("ply: "+str(MAX_PLY-plyRemaining)+"\twhose turn: "+who+"\n"+display_board(board)+"get successors...")
  for s in successors:
    # no need to check the others if win condition is met
    if metWinCond: return [s,minimaxVal]

    mm=mini_max(s,get_other(whoseMove),plyRemaining-1)
    newVal=mm[1]
    # get max or min static eval score based on whose move
    if(who=='max' and newVal>minimaxVal) or (who=='min' and newVal<minimaxVal):
      minimaxVal=newVal
      newboard=deepcopy(s)
      # print("ply "+str(MAX_PLY-plyRemaining)+"--> "+str(newVal)) #DEBUG#

  return [newboard,minimaxVal]


def staticEval(board):
  global K_WIN,DIM,SIDE,UD,LR,D2,D2,metWinCond
  'calculates hs for state 1xNXM'
  count=[]; hs=0
  for ii in range(DIM[0]):
    for jj in range(DIM[1]):
      sq=board[ii][jj]
      # print('square ('+str(ii)+','+str(jj)+')='+str(sq)) #DEBUG#
      if sq != '-': # check if forbidden
        if (ii,jj) in UD:
          count= count_in_line([board[ii+n][jj] for n in range(K_WIN)])
          if count[SIDE] == K_WIN: metWinCond=True
          if count[1]>0: hs+=10**(count[1]-1) #add player's count
          if count[0]>0: hs-=10**(count[0]-1) #subtract opponent's count
          # print("ud window:\t"+str([state[ii+n][jj] for n in range(K_WIN)])) #DEBUG#
          # print("count:\t"+str(count))
        if (ii,jj) in LR:
          count= count_in_line([board[ii][jj+n] for n in range(K_WIN)])
          if count[SIDE] == K_WIN: metWinCond=True
          if count[1]>0: hs+=10**(count[1]-1) #add player's count
          if count[0]>0: hs-=10**(count[0]-1) #subtract opponent's count
          # print("lr window:\t"+str([state[ii][jj+n] for n in range(K_WIN)])) #DEBUG#
          # print("count:\t"+str(count))
        if (ii,jj) in D1:
          count= count_in_line([board[ii+n][jj-n] for n in range(K_WIN)])
          if count[SIDE] == K_WIN: metWinCond=True
          if count[1]>0: hs+=10**(count[1]-1) #add player's count
          if count[0]>0: hs-=10**(count[0]-1) #subtract opponent's count
          # print("d1 window:\t"+str([state[ii+n][jj-n] for n in range(K_WIN)])) #DEBUG#
          # print("count:\t"+str(count))
        if (ii,jj) in D2:
          count= count_in_line([board[ii+n][jj+n] for n in range(K_WIN)])
          if count[SIDE] == K_WIN: metWinCond=True
          if count[1]>0: hs+=10**(count[1]-1) #add player's count
          if count[0]>0: hs-=10**(count[0]-1) #subtract opponent's count
          # print("d2 window:\t"+str([state[ii+n][jj+n] for n in range(K_WIN)])) #DEBUG#
          # print("count:\t"+str(count))

  return hs

def get_successors(state,who):
  global DIM
  ''' who is either 'x' or 'o' '''
  successors=[];
  for ii in range(DIM[0]):
    for jj in range(DIM[1]):

      newState=deepcopy(state)

      if newState[ii][jj] == ' ':
        newState[ii][jj] = who
        successors.append(newState)
        # print("newstate \t"+str(newState)) #DEBUG#

  return successors

def get_other(whoseMove):
  if whoseMove.lower() == 'x': return 'o'
  else: return 'x'

def get_move(b1,b2):
  for ii in range(DIM[0]):
    for jj in range(DIM[1]):
      if b1[ii][jj] != b2[ii][jj]: return(ii,jj)
  return None


def count_in_line(list):
  '''list of characters containing x's,o'x,spaces,or dashes. This function counts
   either x's and o's contained in the list'''
  ox_count=[0,0] # 0--> O, 1--> X
  # count x's
  if '-' in list or 'o' in list: #x is blocked
    ox_count[1]=0
  else:
    for el in list:
      if el.lower() == 'x': ox_count[1]+=1
  # count o's
  if '-' in list or 'x' in list: #o is blocked
    ox_count[0]=0
  else:
    for el in list:
      if el.lower() == 'o': ox_count[0]+=1

  return ox_count

def init_valid_square_lists():
  global K_WIN,DIM,UD,LR,D1,D2

  K=K_WIN
  UD=[(ii,jj) for ii in range(DIM[0]-K+1) for jj in range(DIM[1])]
  LR=[(ii,jj) for ii in range(DIM[0]) for jj in range(DIM[1]-K+1)]
  D1=[(ii,jj) for ii in range(DIM[0]-K+1) for jj in range(K-1,DIM[1])]
  D2=[(ii,jj) for ii in range(DIM[0]-K+1) for jj in range(DIM[1]-K+1)]
  #DEBUG#
  # print("valid start quares for a win per dir")
  # print("up-down: "); print(str(UD))
  # print("LR: "); print(str(LR))
  # print("D1: "); print(str(D1))
  # print("D2: "); print(str(D2))

  return

def init_zobrist():
  global ZOBRIST_VALS,DIM
  for ii in range(len(ZOBRIST_VALS)): # generate mxnx2 random ints in table
    for jj in range(2):
      ZOBRIST_VALS[ii][jj]=randint(0,4294967296)
      # print("z "+str(ii)+','+str(jj)+"="+str(ZOBRIST_VALS[ii][jj]))
  return

def init_default_remarks():
  global OP_NAME
  DEFAULT_REMARK=["Come again, "+OP_NAME+"?",
                  OP_NAME+", "+OP_NAME+", "+OP_NAME+"... less talk, more play.",
                  ""]

def z_hash_code(board):
  global ZOBRIST_VALS

  val=0; side=None
  for ii in range(len(board)): #for each square, xor val with rand number from table
    for jj in range(len(board[0])):
      if board[ii][jj].lower()=='x': side=1
      if board[ii][jj].lower()=='o': side=0
      if side!=None: val ^= ZOBRIST_VALS[ii*DIM[1]+jj][side]

  return val

def display_board(b):
  global DIM

  txt="+"+3*DIM[1]*"-"+"+"+"\n"
  for row in b:
      txt+="|"
      for item in row:
          txt+=" "+item+" "
      txt+="|\n"
  txt+="+"+3*DIM[1]*"-"+"+"+"\n"
  return txt

def introduce():
  return """Hello, my name is (player name). Developed by Bilkit and David,
            I am a master of K-in-row. So, you had better watch out!"""

def nickname():
  return "player1"

#<REMARK>#
def retort(remark):
  global def_count
  wordlist = split(' ',remove_punctuation(remark))
  # undo any initial capitalization
  wordlist[0]=wordlist[0].lower()
  # change nouns from second to first person
  mapped_wordlist = you_me_map(wordlist)
  mapped_wordlist[0]=mapped_wordlist[0].capitalize()

  if verbp(wordlist[0]):
        return(" " +\
              stringify(mapped_wordlist) + '?')
  if dpred(wordlist[0]):
      return(" " +\
            stringify(mapped_wordlist) + '?')
  if wpred(wordlist[0]):
    return(" " +\
          stringify(mapped_wordlist) + '?')

  def_count+=1
  return DEFAULT_REMARK[def_count]

def stringify(wordlist):
  'Create a string from wordlist, but with spaces between words.'
  return ' '.join(wordlist)

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")

# This function returns string s with first character in lowercase
lowerFirstChar = lambda s: s[:1].lower()+s[1:] if s else ""

def remove_punctuation(text):
  'Returns a string without any punctuation.'
  return sub(punctuation_pattern,'', text)

def wpred(w):
  'Returns True if w is one of the question words.'
  return (w in ['when','why','where','how'])

def dpred(w):
  'Returns True if w is an auxiliary verb.'
  return (w in ['do','can','should','would'])
def verbp(w):
  'Returns True if w is one of these known verbs.'
  return (w in ['go', 'have', 'be', 'try', 'play', 'take', 'help',
                'make', 'get', 'type', 'fill',
                'put', 'turn', 'compute'])

CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'Ol\' Gramps',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are'}

def you_me(w):
  'Changes a word from 1st to 2nd person or vice-versa.'
  try:
      result = CASE_MAP[w]
  except KeyError:
      result = w
  return result

def you_me_map(wordlist):
  'Applies YOU-ME to a whole sentence or phrase.'
  return [you_me(   w) for w in wordlist]

#<REMARK>#

#<TEST>#
def test():
  state=game.INITIAL_STATE
  state[1]='o'

  prepare(state,game.K,state[1],"noname")
  # print("hash init state= "+str(z_hash_code( state[0] )))
  # print("staticE="+str(staticEval(state[0])))
  # print("successors:\n"+str(len(get_successors(state[0],'x'))))
  # print("minimax for x: "+str(mini_max(state[0],state[1],2)))
  makeMove(state, "")
  # print("minimax for o: "+str(mini_max(state[0],'o',2)))
  # print("other for x: "+get_other('x'))
  # print("other for o: "+get_other('o'))
  # state[0][1]='x'; state[0][2]='o'
  # print("hash state= "+str(z_hash_code( state )))
#<TEST>#

test()