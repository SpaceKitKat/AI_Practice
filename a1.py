#!/usr/bin/python3.4
#############
#Problem 1.1#
#############
def cube(x):
  return int(x**3)
#This function returns the output for the function 6*n^3 + 5
def six_x_cubed_plus_5(n):
  return 6*cube(n)+5
#############
#Problem 1.2#
#############
#This function takes a coded message and an integer then returns
#a decoded message.
def mystery_code(msg,num):
  cIter = iter(msg)
  #while iterator is not empty
  #  get next value
  #  check if digit, or lowercase, etc

  # differences between ascii values are either for odd: n,n-2,(n+1)/2,(n+1)/2+2
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
specialCases = {'have':'had','be':'been','eat':'ate','go':'went'}
vowels       = {'a','e','i','o','u'}
def isVowel(c):
  return c.lower() in vowels
def isCons(c):
  caseInSens = c.lower()
  return caseInSens.isalpha() and not isVowel(caseInSens)
def isSpecialCase(w):
  isSpecial = [x for x in specialCases]
  return w.lower() in isSpecial
#This function takes a single list of verbs and returns a list of
#of those verbs in past tense form. All modifications appear in
#lowercase.
def past_tense(l):
  newL = len(l)*[0]
  for w in l:
    lastC = w[len(w)-1]; wIdx = l.index(w)
    if(isSpecialCase(w)):
       newL[wIdx] = specialCases[w.lower()]
    elif(isCons(w[len(w)-3]) and isVowel(w[len(w)-2]) and isCons(lastC)):
      newL[wIdx] = w.replace(lastC,lastC+lastC.lower()+'ed')
    elif(lastC == 'y'):
      newL[wIdx] = w.replace('y','ied')
    elif(isVowel(lastC)):
      newL[wIdx] = w+'d'
    else:
      newL[wIdx] = w+'ed'
  return newL

def main():
  # Probelm 1: test
  # print( "six_x_cubed_plus_5(2) --> "+str(six_x_cubed_plus_5(2)) )
  # print( "six_x_cubed_plus_510) --> "+str(six_x_cubed_plus_5(10)) )
  # print( "six_x_cubed_plus_5(59.4) --> "+str(six_x_cubed_plus_5(59.4)) )
  # print( "quadruples --> "+ str(quadruples([2, 5, 1.5, 100, 3, 8, 7, 1, 1])) )
  # print( "quadruples --> "+ str(quadruples([2, 5, 1.5, 100, 3, 8])) )
  # print( "quadruples --> "+ str(quadruples([2, 5, 1.5, 100, 3, 8, 7, 1, 1, 1, 2, -5, 3, 'c'])) )
  # print( "past_tense --> "+ str(past_tense(['program', 'debug', 'execute', 'crash', 'repeat', 'eat'])) )
  # print( "past_tense --> "+ str(past_tense(['have', 'be', 'go','eat'])) )
  print( "past_tense --> "+ str(past_tense(['prograM', 'DEBUG', 'execute', 'crASH', 'repEAt', 'Eat'])) )

main()
