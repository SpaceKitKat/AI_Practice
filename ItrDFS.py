#!/usr/bin/python3.4
# ItrDFS.py
# Ver 0.2, April 15, 2015.
# Iterative Depth-First Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowersOfHanoi.py example file for details.
# Examples of Usage:
# python3 ItrDFS.py TowersOfHanoi
# python3 ItrDFS.py EightPuzzle

import sys

if sys.argv==[''] or len(sys.argv)<2:
  import sudoku as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1]) # import TOH


print("\nWelcome to ItrDFS")
COUNT = None
BACKLINKS = {}

def runDFS():
  initial_state = Problem.CREATE_INITIAL_STATE(1) # no 1
  state0=Problem.CREATE_INITIAL_STATE(0) # none filled
  state2=Problem.CREATE_INITIAL_STATE(2) # no 1 or 2
  state3=Problem.CREATE_INITIAL_STATE(3) # all filled
  state4=Problem.CREATE_INITIAL_STATE(4) # no row 0 and 3

  state=state4

  # DEBUG GENERAL #
  # print("Initial State:")
  # print(Problem.DESCRIBE_STATE(initial_state))
  # print("State 2:\n"+Problem.DESCRIBE_STATE(state2))
  # print("State 4:\n"+Problem.DESCRIBE_STATE(state4))
  # print( "deep_equals(s1,s1): "+str(Problem.DEEP_EQUALS(initial_state,\
  #                               initial_state)) )
  # print( "deep_equals(s1,empty): "+str(Problem.DEEP_EQUALS(initial_state,\
  #                               state0)) )
  # print( "goal_test(s1): "+str(Problem.goal_test(initial_state)) )
  # print( "goal_test(s2): "+str(Problem.goal_test(state2)) )
  # DEBUG OPS #
  # cnt=0
  # for op in Problem.OPERATORS:
  #       #Optionally uncomment the following when debugging
  #       ## DEBUG ##
  #       # print( "Trying operator: "+op.name+' can operate? '+str(op.precond(state2)) )
  #       if op.precond(state):
  #         new_state = op.state_transf(state)
  #         print("new state "+str(cnt)+":\n"+Problem.DESCRIBE_STATE(new_state)); cnt+=1
  #         state=new_state
  # print("final_state:\n"+Problem.DESCRIBE_STATE(state))
  # print("goal_test = "+str(Problem.goal_test(state)))

  global COUNT, BACKLINKS
  COUNT = 0
  BACKLINKS = {}
  IterativeDFS(state)
  print(str(COUNT)+" states examined.")

def IterativeDFS(initial_state):
  global COUNT, BACKLINKS

  OPEN = [initial_state]
  CLOSED = []
  BACKLINKS[Problem.HASHCODE(initial_state)] = -1

  while OPEN != []:
    S = OPEN[0]
    del OPEN[0]
    CLOSED.append(S)

    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      backtrace(S)
      return
    # print count if it is very large
    COUNT += 1
    if (COUNT % 32)==0:
       print(".",end="")
       if (COUNT % 128)==0:
         print("COUNT = "+str(COUNT))
         print("len(OPEN)="+str(len(OPEN)))
         print("len(CLOSED)="+str(len(CLOSED)))
    L = []
    for op in Problem.OPERATORS:
      #Optionally uncomment the following when debugging
      ## DEBUG ##
      # print("Trying operator: "+op.name+' can operate? '+str(op.is_applicable(S)))
      if op.precond(S):
        new_state = op.state_transf(S)
        if not occurs_in(new_state, CLOSED):
          L.append(new_state)
          BACKLINKS[Problem.HASHCODE(new_state)] = S
          ## DEBUG ##
          print("Trying operator: "+op.name+'\n')
          # print(Problem.DESCRIBE_STATE(new_state))

    print("OPEN: "+str(len(OPEN)))
    # print("L: "+str(len(L)))


    for s2 in L:
      for i in range(len(OPEN)):
        if Problem.DEEP_EQUALS(s2, OPEN[i]):
          del OPEN[i]; break

    OPEN = L + OPEN
    #DEBUG#

def backtrace(S):
  global BACKLINKS

  path = []
  while not S == -1:
    path.append(S)
    S = BACKLINKS[Problem.HASHCODE(S)]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(Problem.DESCRIBE_STATE(s))
  return path


def occurs_in(s1, lst):
  for s2 in lst:
    if Problem.DEEP_EQUALS(s1, s2): return True
  return False

if __name__=='__main__':
  runDFS()
