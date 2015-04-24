#!/usr/bin/python3.4
# AStar.py
# Ver 0.2, April 15, 2015.
# Iterative Depth-First Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowersOfHanoi.py example file for details.
# Examples of Usage:
# python3 AStar.py TowersOfHanoi
# python3 AStar.py EightPuzzle

import sys
import queue as Q

if len(sys.argv)==4:
  import BasicEightPuzzle as Problem
  BEP = __import__(sys.argv[3].replace('.py',''))
  initial_state = BEP.CREATE_INITIAL_STATE
  typeh = sys.argv[2]
if sys.argv==[''] or len(sys.argv)<2:
  import BasicEightPuzzle as Problem
  initial_state = Problem.CREATE_INITIAL_STATE(3)
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1]) # import TOH


print("\nWelcome to AStar Search")
COUNT = None
BACKLINKS = {}
STATE_H = {}
inQueue = []
OPEN = Q.PriorityQueue()

def runAStar():
  print("Initial State:")
  print(Problem.DESCRIBE_STATE(initial_state))

  # DEBUG #
  # print('euclidean(s) = '+str(Problem.euclidean(initial_state)))
  # print('hamming(s) = '+str(Problem.hamming(initial_state)))
  # print('manhattan(s) = '+str(Problem.manhattan(initial_state)))

  global COUNT, BACKLINKS
  COUNT = 0
  BACKLINKS = {}
  AStar(initial_state)
  print(str(COUNT)+" states examined.")

def AStar(initial_state):
  global COUNT, BACKLINKS, OPEN
  # calc state score and put score:state in a dictionary and score in open priority queue
  h_score = Problem.CALC_H(typeh)(initial_state)
  STATE_H[h_score] = [initial_state]
  OPEN.put(h_score)
  inQueue.append(initial_state)

  CLOSED = []
  BACKLINKS[Problem.HASHCODE(initial_state)] = -1

  while OPEN.qsize() > 0:
    key = OPEN.get()
    S = STATE_H[key][0] # get state with lowest h(s
    del STATE_H[key][0]
    if S in inQueue:
      del inQueue[inQueue.index(S)]

    CLOSED.append(S)

    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      backtrace(S)
      return

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
          # print(Problem.DESCRIBE_STATE(new_state))

    for state in L:
      for i in range(len(inQueue)):
        if Problem.DEEP_EQUALS(state, inQueue[i]):
          del L[i]; break
    # throw new states in priority queue
      h_score = Problem.CALC_H(typeh)(state)
      OPEN.put(h_score)
      inQueue.append(initial_state)
      if h_score not in STATE_H:
        STATE_H[h_score] = [state] # if multiple states
      else:
        STATE_H[h_score].append(state)

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
  runAStar()
