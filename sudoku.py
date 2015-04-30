import generate as Gen
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
      for c in candidates[squares[ii]]:
        if c != init_state[ii]: candidates[squares[ii]][candidates[squares[ii]].index(c)]=0
      # eliminate init_state val from cand_list of other sqaures in same row,col,block
      for s in unit_mates[squares[ii]]:
        cand_list = candidates[s]
        if cand_list.__contains__(init_state[ii]):
          # del cand_list[cand_list.index(init_state[ii])]
          cand_list[cand_list.index(init_state[ii])] = 0

  return candidates

# def DESCRIBE_STATE(state):
#   # Produces a textual description of a state.
#   # Might not be needed in normal operation with GUIs.
#   txt="";jj=0
#   for s in squares: # print square indices
#       if(jj+1)%3==0:
#           if(jj+1)%9!=0:
#             if(s==0): txt+=" |"
#             else:txt+=s+'|'
#           else:
#             if(s==0): txt+=" \n"
#             else: txt+=s+'\n'
#       else:
#         if(s==0): txt+="  "
#         else: txt+=s+' '
#       if (jj+1)%27==0 and s[0]!='i':
#           txt+="--------+--------+--------\n"
#       jj+=1
#   for s in squares: # print squares with state values
#     if(jj+1)%3==0:
#         if(jj+1)%9!=0:
#           if(state[jj]==0): txt+=" |"
#           else:txt+=str(state[jj])+'|'
#         else:
#           if(state[jj]==0): txt+=" \n"
#           else: txt+=str(state[jj])+'\n'
#     else:
#       if(state[jj]==0): txt+="  "
#       else: txt+=str(state[jj])+' '
#     if (jj+1)%27==0 and s[0]!='i':
#       txt+="-----+-----+-----\n"
#     jj+=1
def DESCRIBE_STATE(candidates):
  # Produces a textual description of a state.
  # Might not be needed in normal operation with GUIs.
  jj=0
  txt="candidates:\n"
  jj=0
  for s in squares: # print candidate values per square
    if(jj+1)%3==0: # show block separation (horizontal)
      if(jj+1)%9 != 0: # start next row after 9th square
        for el in candidates[s]:
          if(el==0): txt+=" "
          else:txt+=str(el)
        txt+=' | '
      else:
        for el in candidates[s]:
          if(el==0): txt+=" "
          else:txt+=str(el)
        txt+='\n'
    else:
      for el in candidates[s]:
        if(el==0): txt+=" "
        else:txt+=str(el)
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
  equals = [ len(cand1[s])==len(cand2[s]) for s in squares ]
  return not equals.__contains__(False)


def goal_test(cand):
  '''If all cand_lists are of length 1, then s is a goal state.'''
  has_single_value = []
  for s in cand:
    has_single_value.append(len(cand[s])==1)
  return has_single_value.__contains__(False)
#puzzle0
def goal_message(s):
  return "The Sudoku Puzzle is Complete!"

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
                  6,9,7,8,4,3,5,0,0]}


def CREATE_INITIAL_STATE(x):
  'A state is represented by a dictionary of each square and its corresponding\
  candidate values. If there is only one candidate value in a square, then it \
  is assigned to that square and removed from cand list of other squares.'
  IS = lambda x:INITIAL_STATE[x]
  return initialize_cand(IS(x))
DUMMY_STATE =  []
#</INITIAL_STATE>