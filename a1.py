#!/usr/bin/python3.4

def cube(x):
  return int(x**3)
#This function returns the output for the function 6*n^3 + 5
def six_x_cubed_plus_5(n):
  return 6*cube(n)+5
#This function takes a coded message and an integer then returns
#a decoded message.
def mystery_code(msg):
  cIter = iter(msg)
  #while iterator is not empty
  #  get next value
  #  check if digit, or lowercase, etc

  # differences between ascii values are either for odd: n,n-2,(n+1)/2,(n+1)/2+2

#This function takes a single list and returns a nested list with
#as many sublists of length 4 as possible.
def quadruples(l):
# watch out for dupes!
  temp  = [0]*len(l)
  while True:
    try:
      temp = temp.add( next(lIter))
    except StopIteration:
      return temp

def main():
  #print( "six_x_cubed_plus_5(2) --> "+str(six_x_cubed_plus_5(2)) )
  print( "quadruples --> "+ quadruples([2, 5, 1.5, 100, 3, 8, 7, 1, 1]) )



main()
