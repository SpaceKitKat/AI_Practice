#!/usr/bin/python3.4
'''BasicEightPuzzle.py
A QUIET Solving Tool problem formulation.
QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this
problem formulation.

CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''
#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Eight Puzzle"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Bilkit Githinji']
PROBLEM_CREATION_DATE = "20-APR-2015"
PROBLEM_DESC=\
'''This formulation of the Basic Eight Puzzle problem uses generic
Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface.
'''
#</METADATA>

#<COMMON_DATA>
N_DIM = 3
#</COMMON_DATA>

#<COMMON_CODE>
def DEEP_EQUALS(s1,s2):
  'Tests equality for each corresponding block between two states, single false --> unequal'
  equals = [ s1[ii]==s2[ii] for ii in range(0,N_DIM**2) ]
  return not equals.__contains__(False)

def DESCRIBE_STATE(state):
  # Produces a textual description of a state.
  # Might not be needed in normal operation with GUIs.
  txt = "\n"
  for ii in range(0,N_DIM**2):
    if state[ii] == 0:
      txt += "  " # empty block
      for digits in range(0,len(str(ii))):
        txt += " "
    else:
      txt += "["+str(state[ii])+"]"
    if (ii+1)%N_DIM==0: txt+="\n"
  return txt

def HASHCODE(state):
  '''The result should be an immutable object such as a string
  that is unique for the state s.'''
  return str(state)

def copy_state(state):
  # Performs an appropriately deep copy of a state,
  # for use by operators in creating new states.
  news=state[:]
  return news

def can_move(s,src,dst):
  '''Tests whether it's legal to swap a block in src position with a
   block in the dst position of state s.'''
  try:
    # # if val at dst is zero then legal move
    if src >= 0: # positions must be within board
      if dst < N_DIM**2:
        if(abs(src-dst)==1 or abs(src-dst) == N_DIM): # blocks must be neighbors
          return s[dst] == 0 or s[src] == 0 # block at destination must be 'empty'
    else:
      print('can only move to and from positive indices')

    return False
  except (Exception) as e:
    print(e)

def move(s,src,dst):
  '''Assuming it's legal to make the swap, this computes
     the new state resulting from swapping the block at
     src position with block at dst position in state s.'''
  news = copy_state(s) # start with a deep copy.
  news[dst] = s[src]; news[src] = s[dst]
  return news # return new state

def goal_test(s):
  '''If array is in row-major order, then s is a goal state.'''
  return DEEP_EQUALS(s,GOAL_STATE)
#puzzle0
def goal_message(s):
  return "The Eight Puzzle Completion is Triumphant!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

## HEURISTIC FUNCTIONS ##
def euclidean(state):
  'Returns sum of differences between each block in state and each\
  corresponding block in goal state.'
  score=0
  for b in state:
    score += abs( state.index(b) - GOAL_STATE.index(b))
  return score

def hamming(state):
  'Returns count of mismatched blocks between state and goal state'
  score=0
  for b in state:
    if state.index(b) != GOAL_STATE.index(b):
      score += 1
  return score

def manhattan(state):
  'Returns sum of row and column differences between each block in\
   state and each corresponding block in goal state.'
  global row_count
  score = 0
  for b in state:
    row_count = col_count = 0
    count_rows(abs( state.index(b) - GOAL_STATE.index(b)))
    col_count = abs(state.index(b)%N_DIM - GOAL_STATE.index(b)%N_DIM)
    # DEBUG #
    # print('block '+str(b)+' = '+str(row_count)+' drows, '+str(col_count)+' dcols')
    score+=row_count+col_count
  return score

def count_rows(idiff):
  'Recursively counts rows based on index difference between two blocks'
  global row_count
  if idiff < N_DIM:
    return
  row_count+=1
  count_rows(idiff-N_DIM) # move one row closer until in same row
## HEURISTIC FUNCTIONS ##

#</COMMON_CODE>

#<GOAL_STATE>
GOAL_STATE = [x for x in range(0,N_DIM**2)]
#<GOAL_STATE>

#<INITIAL_STATE>
INITIAL_STATE ={0:[0, 1, 2, 3, 4, 5, 6, 7, 8],\
                1:[1, 0, 2, 3, 4, 5, 6, 7, 8],\
                2:[3, 1, 2, 4, 0, 5, 6, 7, 8],\
                3:[1, 4, 2, 3, 7, 0, 6, 8, 5]}

CREATE_INITIAL_STATE = lambda x:INITIAL_STATE[x]
DUMMY_STATE =  []
#</INITIAL_STATE>

#<OPERATORS>
# swap between neighbors of blocks only: above or below --> diff of 3, or
# left or right --> diff of 1 (special case for right edges),
# and avoid redundancy of swap os
swaps = [(ii,jj) for ii in range(0,N_DIM**2) for jj in range(0,N_DIM**2)\
         if ( ((ii+1)%N_DIM!=0 and abs(ii-jj)==1) or abs(ii-jj)==N_DIM ) and ii<jj]

# swap_combinations = [('pos'+str(a),'pos'+str(b)) for (a,b) in swaps]
OPERATORS = [Operator("Swap blocks at positions "+str(p)+" and "+str(q),
                      lambda s,p=p,q=q: can_move(s,p,q),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,p=p,q=q: move(s,p,q) )
             for (p,q) in swaps]#for (p,q) in swap_combinations]
#</OPERATORS>

#</HEURISTICS>
HEURISTICS = {'h_euclidean':lambda s:euclidean(s)}
#</HEURISTICS>


#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
if 'BRYTHON' in globals():
 from EightPuzzleVisForBrython import set_up_gui as set_up_user_interface
 from EightPuzzleVisForBrython import render_state_svg_graphics as render_state
# if 'TKINTER' in globals(): from TicTacToeVisForTKINTER import set_up_gui
#</STATE_VIS>