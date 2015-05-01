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
import generate as Gen
from copy import deepcopy
#<COMMON_DATA>
N_DIM = 9
rows = ['a','b','c','d','e','f','g','h','i']
cols = [n for n in range(1,N_DIM+1)]
blocks=[]
for r in [rows[0:3],rows[3:6],rows[6:9]]:
  for c in [cols[0:3],cols[3:6],cols[6:9]]:
    blocks.append([rr+str(cc) for rr in r for cc in c])
squares = [row+str(col) for row in rows for col in cols]
unit_mates = {} # key = square, val = unit members
for s in squares:
    # for each square specify squares in the same block, row, and col
    unit_mates[s] = [os for os in [b for b in blocks if b.__contains__(s)][0] if os!=s]
    unit_mates[s]+= [os for os in squares if not unit_mates[s].__contains__(os)\
                    and (os[0]==s[0] or os[1]==s[1]) and os!=s]

#</COMMON_DATA>


#<COMMON_CODE>

# init_state is a 1xN_DIM**2 array containing values 1:N_DIM+1 values.
# the order must correspond to that of the square index (i.e. 'a1')
def initialize_cand(init_state):
  # this is the true representation of a specific state
  candidates = {} # key = square, val = vals [1,9]

  # all squares start with all possible vals
  for ii in range(0,N_DIM**2): candidates[squares[ii]] = [n for n in range(1,N_DIM+1)]

  # for each init_state value, if non-zero init_stzate val,
  # eliminate all other possible vals from other squares
  for ii in range(0,N_DIM**2):
    if init_state[ii] != 0:
      candidates[squares[ii]]=[init_state[ii]]
      # eliminate init_state val from cand_list of other sqaures in same row,col,block
      for s in unit_mates[squares[ii]]:
        cand_list = candidates[s]
        if cand_list.__contains__(init_state[ii]):
          del cand_list[cand_list.index(init_state[ii])]

  return candidates

def DESCRIBE_STATE(candidates):
  # Produces a textual description of a state.
  txt="each square's potential values\n"
  jj=0
  for s in squares: # print candidate values per square
    if(jj+1)%3==0: # show block separation (horizontal)
      if(jj+1)%9 != 0: # start next row after 9th square
        for el in candidates[s]: txt+=str(el)
        for ii in range(0,9-len(candidates[s])): txt+=" "
        txt+=' | '
      else:
        for el in candidates[s]: txt+=str(el)
        for ii in range(0,9-len(candidates[s])): txt+=" "
        txt+='\n'
    else:
      for el in candidates[s]: txt+=str(el)
      for ii in range(0,9-len(candidates[s])): txt+=" "
      txt+='/' # show square separation

    if(jj+1)%27==0 and s[0]!='i': # show block separation (vertical)
      txt+="------------------------------+"+\
        "-------------------------------+"+\
        "------------------------------\n" # 27+3 dashes
    jj+=1

  return txt

def DEEP_EQUALS(cand1,cand2):
  'Tests equality for each corresponding number of candidates per \
  square between two states, single false --> unequal'
  equals = [ equal_lists(cand1[s],cand2[s]) for s in squares ]
  return not equals.__contains__(False)

def equal_lists(list1,list2):
  if len(list1) == len(list2):
    for ii in range(0,len(list1)): # check element equality
      if list1[ii]!=list2[ii]: return False
  else: return False
  return True

def HASHCODE(cand):
  '''The result should be an immutable object such as a string
  that is unique for the state s.'''
  hash = ''
  for s in squares: # keep track of number of possible values for each square
    for el in cand[s]: hash+=str(el)
    hash+='|'

  return hash

def goal_test(cand):
  '''If all cand_lists are of length 1, then s is a goal state.'''
  assigned_vals = [cand[s][0] for s in cand if len(cand[s]) < 2] # get single valued squares
  if len(assigned_vals) < N_DIM**2: return False
  # check for redundant vals in blocks
  for ii in range(0,N_DIM):
    distinct_vals=set(cand[s][0] for s in blocks[ii])
    if len(distinct_vals) < 9: return False
  return True


#puzzle0
def goal_message(s):
  return "The Sudoku Puzzle is Complete!"

def copy_state(cand):
  # Performs an appropriately deep copy of a state,
  # for use by operators in creating new states.
  return deepcopy(cand)

s2assign="";v2assign=0
def can_assign_square(cand,sq):
  '''Returns true only if square has more than one candidate and
  if the value is not assined to a unit_mate (square in same row,col,block).'''
  global s2assign,v2assign

  try:
    if len(cand[sq]) < 2: return False # square is already
    for v in cand[sq]:
      # get squares in units with only 1 val, add them to assigned_vals
      assigned_vals = []; assigned_vals += [cand[s][0] for s in unit_mates[sq] if len(cand[s]) < 2]
      if assigned_vals.__contains__(v): del cand[sq][cand[sq].index(v)]; return False # remove assigned val
      else: s2assign=sq;v2assign=v ;return True
  except (Exception) as e:
    print(e)

def assign_square(cand):
  '''Assuming it's legal to assign, this computes
     the new state resulting from making the assignment.'''
  global s2assign,v2assign

  news = copy_state(cand) # start with a deep copy.
  news[s2assign]=[v2assign] # assign val to square
  unassinged_squares=[s for s in unit_mates[s2assign] if len(news[s]) > 1 and news[s].__contains__(v2assign)]
  for us in unassinged_squares: del news[us][news[us].index(v2assign)] # remove v from mates with v
  return news # return new state


class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf


  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

#<COMMON_CODE>





#<INITIAL_STATE>
# give square id and value
INITIAL_STATE ={0:[0]*81,\
                1:[0,3,6,2,5,9,7,4,8,\
                  7,2,5,4,0,8,9,3,6,\
                  4,8,9,3,6,7,0,5,2,\
                  3,6,4,7,8,5,2,0,9,\
                  5,0,8,6,9,2,3,7,4,\
                  9,7,2,0,3,4,6,8,5,\
                  2,4,0,5,7,6,8,9,3,\
                  8,5,3,9,2,0,4,6,7,\
                  6,9,7,8,4,3,5,2,0],
                2:[0,3,6,0,5,9,7,4,8,\
                  7,0,5,4,0,8,9,3,6,\
                  4,8,9,3,6,7,0,5,0,\
                  3,6,4,7,8,5,0,0,9,\
                  5,0,8,6,9,0,3,7,4,\
                  9,7,0,0,3,4,6,8,5,\
                  0,4,0,5,7,6,8,9,3,\
                  8,5,3,9,0,0,4,6,7,\
                  6,9,7,8,4,3,5,0,0],
                3:[1,3,6,2,5,9,7,4,8,\
                  7,2,5,4,1,8,9,3,6,\
                  4,8,9,3,6,7,1,5,2,\
                  3,6,4,7,8,5,2,1,9,\
                  5,1,8,6,9,2,3,7,4,\
                  9,7,2,1,3,4,6,8,5,\
                  2,4,1,5,7,6,8,9,3,\
                  8,5,3,9,2,1,4,6,7,\
                  6,9,7,8,4,3,5,2,1],
                4:[0,0,0,0,0,0,0,0,0,\
                  7,2,5,4,1,8,9,3,6,\
                  4,8,9,3,6,7,1,5,2,\
                  0,0,0,0,0,0,0,0,0,\
                  5,1,8,6,9,2,3,7,4,\
                  9,7,2,1,3,4,6,8,5,\
                  2,4,1,5,7,6,8,9,3,\
                  8,5,3,9,2,1,4,6,7,\
                  6,9,7,8,4,3,5,2,1]}


def CREATE_INITIAL_STATE(x):
  'A state is represented by a dictionary of each square and its corresponding\
  candidate values. If there is only one candidate value in a square, then it \
  is assigned to that square and removed from cand list of other squares.'
  IS = lambda x:INITIAL_STATE[x]
  print( "initializing state "+str(x)+": \n"+init_to_string(IS(x)) )
  return initialize_cand(IS(x))
DUMMY_STATE =  []

def init_to_string(state):
  # Produces a textual description of a state.
  txt='';jj=0
  for s in squares: # print squares with state values
    if(jj+1)%3==0:
        if(jj+1)%9!=0:
          if(state[jj]==0): txt+=" |"
          else:txt+=str(state[jj])+'|'
        else:
          if(state[jj]==0): txt+=" \n"
          else: txt+=str(state[jj])+'\n'
    else:
      if(state[jj]==0): txt+="  "
      else: txt+=str(state[jj])+' '
    if (jj+1)%27==0 and s[0]!='i':
      txt+="-----+-----+-----\n"
    jj+=1
  return txt
#</INITIAL_STATE>


# <OPERATORS>
# Transform:
# remove all -- except assigned val -- elements from cand_list of square
# remove assigned val from all unit_mate squares' cand_list
# Precond:
# return false if length of cand_list is less than 1
# for every val in cand_list
#   return false if single valued unit_mates have this value

# s is the candidates dictionary for a particular state
OPERATORS = [Operator("Assign value to "+str(sq),
                      lambda s,sq=sq: can_assign_square(s,sq),
                      lambda s: assign_square(s) )
             for sq in squares]#for (p,q) in swap_combinations]
# </OPERATORS>






#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
