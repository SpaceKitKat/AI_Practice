#!/usr/bin/python3.4
# montyHall.py
# Bilkit Githinji,1263465, CSE 415, Spring 2015, University of Washington
# Instructor:  S. Tanimoto.
# Ver 0.1, May 13, 2015.

import sys
from random import randint
import queue as Q
from copy import deepcopy

if len(sys.argv) != 3:
  ValueError("Incorrect number of arguments passed")
else:
  NGAMES = sys.argv[1]; POLICY = sys.argv[2]

WINS=0; LOSES=0
MAX_PRIORITY=Q.PriorityQueue()


def main():
  print("\nWelcome to the Montyhall Problem. Starting games...\n")
  report_game_summary(play_n_rounds())
  return

def play_n_rounds():
  rounds = int(NGAMES)
  stats = [0,0] # 0 --> losses, 1--> wins
  while rounds > 0:
    if play_game(): stats[1]+=1
    else: stats[0]+=1
    rounds-=1
  # print(stats) #DEBUG#
  return stats

def play_game():
  curr_state=create_init_state();
  print(describe_state(curr_state),end='')
  next_state=[]
  while is_game_over(next_state) == False:
    for ii in range(3):
      # print(OPERATORS[ii][0]);print(OPERATORS[ii][1](curr_state)); #DEBUG#
      if OPERATORS[ii][1](curr_state): next_state=OPERATORS[ii][2](curr_state)

    print(", "+describe_state(next_state),end='')
    curr_state=next_state
  print()
  selected=[d for d in curr_state if d[0]=='>' and d[1].isupper()]
  # print("prize: "+str(selected)) #DEBUG#
  return selected[0][1].lower() == 'c'

def report_game_summary(stats):
  losses=stats[0]
  wins=stats[1]
  perc_loss = losses/int(NGAMES)
  perc_wins = wins/int(NGAMES)

  sum_vars = [NGAMES,POLICY,losses,wins,perc_loss,perc_wins]
  summary = "\nGame Summary:\n\tgames played\t{:s}\tplayer policy\t{:s}\n\t"+\
            "total losses\t{:d}\ttotal wins\t{:d}\n\t"+\
            "\t\t{:.2%}\t\t\t{:.2%}"
  print(summary.format(*sum_vars))
  return

def create_init_state():
  doors = {}
  for ii in range(3):
    doors[ii] = randint(1,1000)
    MAX_PRIORITY.put(doors[ii])
  val_car = MAX_PRIORITY.get()
  for d in doors:
    if doors[d] == val_car: doors[d] = 'c'
    else: doors[d] = 'g'
  return [['',doors[0]],['',doors[1]],['',doors[2]]]

def deep_equals(s1,s2):
  return s1.__contains__(s2[0]) and s1.__contains__(s2[1]) and s1.__contains__(s2[2])

def deep_copy(s):
  return deepcopy(s)

def describe_state(state):
  return "["+state[0][0]+state[0][1]+","+state[1][0]+state[1][1]+","+state[2][0]+state[2][1]+"]"

MOVE=[]
def can_move(state,d):
  'Pass state (list) and door index'
  global MOVE
  selected=None; opened=[]; dgoat=[]
  #analyze state for selected door and prize door
  for door in state:
    dinx = state.index(door)
    if door[0] == '>': selected = dinx
    if door[1].isupper(): opened.append(dinx)
    if door[1] == 'g': dgoat.append(dinx)

  if len(opened) == 0:
    #player select - nothing selected and d not opened
    if selected==None:
      MOVE = ["p_sel"]
      # print("\tplayer can select") #DEBUG#
      return True
    #host open - d not selected, d not opened, d not prize
    if d in dgoat:
      MOVE = ["h_open"]
      # if d != selected: print("\thost can open") #DEBUG#
      return d != selected
  else:
    # if len(opened) > 1: return False # game has already ended
    if d in opened: return False # ignore opened doors
    #check for switch or reveal prize
    if POLICY.lower()=="switch":
      toSwap = [state.index(s) for s in state if state.index(s) != selected and state.index(s) not in opened]
      MOVE = ["p_swap",toSwap[0]]
      # if d == selected and toSwap != selected: print("\tplayer can swap") #DEBUG#
      return d == selected
    if d == selected:
      MOVE = ["h_open"]
      # print("\thost can reveal prize") #DEBUG#
      return True
  return False

def move(state,d):
  global MOVE

  # print(describe_state(state)+'\nDoor:'+str(d)+"\tmove: "+str(MOVE))

  newstate = deep_copy(state)
  if "p_sel" in MOVE[0]: newstate[randint(0,2)][0]='>' # player select random
  elif "h_open" in MOVE[0]: newstate[d][1]=newstate[d][1].capitalize() # host open d
  elif "p_swap" in MOVE[0]: newstate[d][0]=''; newstate[MOVE[1]][0]='>';\
      newstate[MOVE[1]][1]=newstate[MOVE[1]][1].capitalize() # switch doors
  else: print("no possible move")

  return newstate

def is_game_over(state):
  if state==[]: return False
  opened_doors = [s for s in state if s[1].isupper()]
  return len(opened_doors) > 1


swap = [(ii,jj) for ii in range(3) for jj in range(3) if ii!=jj and ii<jj]
OPERATORS = [["operating on door "+str(d),\
             lambda s,d=d: can_move(s,d),\
             lambda s,d=d: move(s,d)]
             for d in range(3)]
def test():
  # state=create_init_state()
  # state[0][0]='>'
  # state[1][1]=state[1][1].capitalize()
  # state[2][1]=state[2][1].capitalize()
  # for ii in range(3):
    # print( describe_state(state) )
    # print( str(OPERATORS[ii][0])+"\n"+\
    #        str(OPERATORS[ii][1](state))+"\n"+\
    #        str(OPERATORS[ii][2](state)) )
  #test single game
  # play_game()
  #test multi games
  # play_n_rounds()
  # report_game_summary([0,0])
  return

# test()
main()




