#!/usr/bin/python3.4
#############
#Problem 1.1#
#############
def cube(x):
  return x**3
#This function returns the output for the function 6*n^3 + 5
def six_x_cubed_plus_5(n):
  return 6*cube(n)+5
#############
#Problem 1.2#
#############
#This function takes a coded message and an integer then returns
#a decoded message.
def mystery_code(encoded,num):
  if isinstance(num,float):
    num = int(num)                          # make sure number is valid
  if num < 0:                               # non-negative and integer
    num = abs(num)
  asciiIn = [ord(char) for char in encoded] # transform input msg to ascii
  asciiOut = [val^num for val in asciiIn]   # decode message
  decoded = [chr(val) for val in asciiOut]  # convert ascii to chars
  return ''.join(decoded)
#############
#Problem 1.3#
#############
#This function takes a single list and returns a nested list with
#as many sublists of length 4 as possible.
def quadruples(l):
  # determine number of sublists
  if(len(l)%4 == 0):
    nSubLists = int(len(l)/4)
  else:
    nSubLists = int(len(l)/4) + 1
  lastSubList = nSubLists-1
  newL = nSubLists*[0]
  # create n-1 sublists since they will be guaranteed to be length 4
  for i in range(0,lastSubList):
    newL[i] = [ x for x in l[4*i:4*(i+1)] ]
  # create last sublist which may not be length 4
  newL[lastSubList] = l[4*lastSubList:]
  return newL
#############
#Problem 1.4#
#############
# dictionary of special case verbs
specialCases = {'to have':'had','to be':'were','to eat':'ate','to go':'went',\
  'have':'had','be':'were','eat':'ate','go':'went'}
vowels       = {'a','e','i','o','u'}
def isVowel(c):
  return c.lower() in vowels
def isCons(c):
  caseInSens = c.lower()
  return caseInSens.isalpha() and not isVowel(caseInSens)
def isSpecialCase(w):
  wSpecial = [x for x in specialCases]
  return w.lower() in wSpecial
#This function takes a single list of verbs and returns a list of
#of those verbs in past tense form. All modifications appear in
#lowercase.
def past_tense(l):
  newL = len(l)*[0]
  for w in l:
    lastC = w[len(w)-1]; wIdx = l.index(w)
    if(isSpecialCase(w)): # check if in special case dictionary
       newL[wIdx] = specialCases[w.lower()]
    elif(isCons(w[len(w)-3]) and isVowel(w[len(w)-2]) and isCons(lastC)):
      newL[wIdx] = w.replace(lastC,lastC+lastC.lower()+'ed')
    elif(lastC == 'y'):
      newL[wIdx] = w.replace('y','ied')
    elif(isVowel(lastC)):
      newL[wIdx] = w+'d'
    else: # all other cases (excluding other special cases)
      newL[wIdx] = w+'ed'
  return newL

def main():
  f = open('a1examplesplus.txt','w')
  f.write( """This file contains the input and output of all functions within a1.py.""" )
  f.write( '\n\n#############\n#Problem A.1#\n#############\n\n')
  f.write( "six_x_cubed_plus_5(2)\n>>> "+str(six_x_cubed_plus_5(2))+"\n" )
  f.write( "six_x_cubed_plus_5(-10)\n>>> "+str(six_x_cubed_plus_5(-10))+"\n" )
  f.write( "six_x_cubed_plus_5(2/3)\n>>> "+str(six_x_cubed_plus_5(-2/3))+"\n" )
  f.write( '\n\n#############\n#Problem A.2#\n#############\n\n')
  f.write( "quadruples([2, 5, 1.5, 100, 3, 8, 7, 1, 1])\n>>> "+ \
         str(quadruples([2, 5, 1.5, 100, 3, 8, 7, 1, 1]))+"\n" )
  f.write( "quadruples([2, 5, 1.5, 100, 3, 8])\n>>> "+ \
         str(quadruples([2, 5, 1.5, 100, 3, 8]))+"\n" )
  f.write( "quadruples([2, 5, 1.5, 100, 3, 8, 7, 1, 1, 1, 2, -5, 3, 'c'])\n>>> "+ \
         str(quadruples([2, 5, 1.5, 100, 3, 8, 7, 1, 1, 1, 2, -5, 3, 'c']))+"\n" )
  f.write( '\n\n#############\n#Problem A.3#\n#############\n\n')
  f.write( "past_tense(['program', 'debug', 'execute', 'crash', 'repeat', 'eat']\n>>> "+ \
         str(past_tense(['program', 'debug', 'execute', 'crash', 'repeat', 'eat']))+"\n" )
  f.write( "past_tense(['to have', 'to be', 'to go','to eat']\n>>> "+ \
         str(past_tense(['to have', 'to be', 'to go','to eat']))+"\n" )
  f.write( "past_tense(['try', 'DEBUG', 'EXECUTE', 'crASH', 'repEAt', 'Eat']\n>>> "+ \
         str(past_tense(['try', 'DEBUG', 'execute', 'crASH', 'repEAt', 'Eat']))+"\n" )
  f.write( '\n\n#############\n#Problem A.4#\n#############\n\n')
  f.write( "mystery_code(\'abc Iz th1s Secure? n0, no, 9!\',21)\n>>> "+\
         mystery_code("abc Iz th1s Secure? n0, no, 9!", 21)+"\n" )
  f.write( "mystery_code(\'abc Iz th1s Secure? n0, no, 9!\',-1)\n>>> "+\
         mystery_code("abc Iz th1s Secure? n0, no, 9!", -1)+"\n" )
  f.write( "mystery_code(\'this has   tabs  only\', 21.1)\n>>> "+\
         mystery_code("this has   tabs  only", 21.1)+"\n" )

main()
