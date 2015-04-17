#!/usr/bin/python3.4
# Linneus3.py
# Implements storage and inference on an ISA hierarchy
# This Python program goes with the book "The Elements of Artificial
# Intelligence".
# This version runs under Python 3.x.

# Steven Tanimoto
# (C) 2012.

# The ISA relation is represented using a dictionary, ISA.
# There is a corresponding inverse dictionary, INCLUDES.
# Each entry in the ISA dictionary is of the form
#  ('turtle' : ['reptile', 'shelled-creature'])

from re import *   # Loads the regular expression module.

ISA = {}
INCLUDES = {}
ARTICLES = {}
SYNONYMS = {}

def store_isa_fact(category1, category2):
    'Stores one fact of the form A BIRD IS AN ANIMAL'
    # That is, a member of CATEGORY1 is a member of CATEGORY2
    # find rep and store isa fact using the rep
    try :
        c1list = ISA[get_rep(category1)]
        c1list.append(category2)
    except KeyError :
        ISA[get_rep(category1)] = [category2]
    try :
        c2list = INCLUDES[get_rep(category2)]
        c2list.append(category1)
    except KeyError :
        INCLUDES[get_rep(category2)] = [category1]

def get_isa_list(category1):
    'Retrieves any existing list of things that CATEGORY1 is a'
    # find rep
    category1 = get_rep(category1)
    try:
        c1list = ISA[category1]
        return c1list
    except:
        return []

def get_includes_list(category1):
    'Retrieves any existing list of things that CATEGORY1 includes'
    # find rep
    category1 = get_rep(category1)
    try:
        c1list = INCLUDES[category1]
        return c1list
    except:
        return []

def isa_test1(category1, category2):
    'Returns True if category 2 is (directly) on the list for category 1.'
    # find reps
    c1list = [get_rep(x) for x in get_isa_list(category1)]
    category2 = get_rep(category2)
    return c1list.__contains__(category2)

def isa_test(category1, category2, depth_limit = 10):
    'Returns True if category 1 is a subset of category 2 within depth_limit levels'
    # find reps
    category1 = get_rep(category1); category2 = get_rep(category2)
    if category1 == category2 : return True
    if isa_test1(category1, category2) : return True
    if depth_limit < 2 : return False
    for intermediate_category in get_isa_list(category1):
        if isa_test(intermediate_category, category2, depth_limit - 1):
            return True
    return False

def store_article(noun, article):
    'Saves the article (in lower-case) associated with a noun.'
    ARTICLES[noun] = article.lower()

def get_article(noun):
    'Returns the article associated with the noun, or if none, the empty string.'
    try:
        article = ARTICLES[noun]
        return article
    except KeyError:
        return ''

def get_rep(noun):
  'returns representative of noun'
  rep = isAnotherNameFor(noun)
  if( rep != ''):
    return rep
  else:
    return noun

def linneus():
    'The main loop; it gets and processes user input, until "bye".'
    print('This is Linneus.  Please tell me "ISA" facts and ask questions.')
    print('For example, you could tell me "An ant is an insect."')
    while True :
        info = input('Enter an ISA fact, or "bye" here: ')
        if info == 'bye': return 'Goodbye now!'
        process(info)

# Some regular expressions used to parse the user sentences:
assertion_pattern = compile(r"^(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)
query_pattern = compile(r"^is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
what_pattern = compile(r"^What\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
why_pattern = compile(r"^Why\s+is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
reduce_flag = False
to_reduce = []
omitted = []

def process(info) :
    global items,x,y,reduce_flag
    'Handles the user sentence, matching and responding.'
    result_match_object = assertion_pattern.match(info)
    if result_match_object != None :
      items = result_match_object.groups()
      x = items[1];y = items[3]
      store_article(x, items[0])
      store_article(y, items[2])
      # check if fact produces antisymmetry before adding it
      if detected_cycle(x,y):
        if isa_test1(y,x): # direct relation
          print("Yes, but "+ report_link([y,x])+" because you told me that... I'm not going to remember that "+\
                 report_link([x,y]) +" unless you insist.")
        else: # transient relation
          print("Yes, but "+ report_link([y,x])+" because "+ report_chain(y,x)+\
                "... I'm not going to remember that "+ report_link([x,y]) +" unless you insist.")
      else:
        # avoid dupes
        if isa_test(get_rep(x),get_rep(y)):
          print('I already know that...')
        else:
          store_isa_fact(x,y)
          print("I understand.")
      print('***isa: '+str(ISA))
      print('***includes: '+str(INCLUDES))
      return

    'converts user sentence into wordlist'
    wordlist = info.split(' '); wordlist = [w.lower() for w in wordlist]
    if detected_cycle(x,y) and 'insist' in wordlist:
      print('user insists, so we are handling '+x+' and '+y)
      handle_cycle(x,y)
      print('***isa: '+str(ISA))
      print('***includes: '+str(INCLUDES))
      return
    if 'can\'t' in wordlist or 'not' in wordlist:
      x = wordlist[5]; y = wordlist[8]
      chain = find_chain(get_rep(x),get_rep(y))
      if chain != None:
        # perform reduction: remove sub class
        omitted.append([x,y])
        if(get_rep(x) != x):
          del ISA[get_rep(x)]
        else:
          del ISA[x]
        # note all possible links to remove
        if len(chain) > 1:
          for link in chain[1:]: to_reduce.append(link)
          # more reductions are possible - prompt for another reduction
          print('Shall I forget that '+get_article(to_reduce[0][0])+" "+to_reduce[0][0]+\
            " is "+get_article(to_reduce[0][1])+' '+to_reduce[0][1]+'?')
          reduce_flag = True
        else: #  direct relationship
          # perform reduction: remove general class
          if(get_rep(y) != y):
            del INCLUDES[get_rep(y)]
          else:
            del INCLUDES[y]
          print('Ok, it is no longer that '+report_link(omitted[0]))
      else:
        print('I already know that.')
      return
    # check if another reduction is possible
    if reduce_flag:
      report_omitted = report_link(omitted[0])
      # perform reduction if user agrees
      if 'yes' in wordlist: #delete link form isa and includes list
        omitted.append(to_reduce[0])
        del ISA[to_reduce[0][0]]
        del INCLUDES[to_reduce[0][1]]
      # delete link from to reduce regardless of response
      del to_reduce[0]
      # check if another reduction is possible - prompt for another reduction
      if to_reduce != []:
        print('Shall I forget that '+get_article(to_reduce[0][0])+" "+to_reduce[0][0]+\
              " is "+get_article(to_reduce[0][1])+' '+to_reduce[0][1]+'?')
      else:
        for link in omitted[1:-1]: report_omitted += ', '+report_link(link)
        print('Ok, it is no longer that '+report_omitted+", or "+report_link(omitted[-1]))
        # reset
        reduce_flag = False
      return
    else:
      del omitted[:]
      del to_reduce[:]
    result_match_object = query_pattern.match(info)
    if result_match_object != None :
      items = result_match_object.groups()
      answer = isa_test(items[1], items[3])
      x = get_rep(items[1]); y = get_rep(items[3])
      if answer :
          print("Yes, "+get_article(x)+" "+x+" is "+get_article(y)+" "+y)
      else :
          print("No, as far as I have been informed, it is not.")
      return
    result_match_object = what_pattern.match(info)
    if result_match_object != None :
      items = result_match_object.groups()
      #check if item is a synonym --> "another name for ..."
      rep = isAnotherNameFor(items[1])
      if( rep != ''):
        print(get_article(items[1])+" "+items[1]+\
              " is another name for "+get_article(rep)+" "+rep+'.')
        return
      supersets = get_isa_list(items[1])
      if supersets != [] :
        # use last for reps and first for others
          if items[1] in SYNONYMS: super = supersets[-1]
          else: super = supersets[0]
          a1 = get_article(items[1]).capitalize()
          a2 = get_article(super)
          print(a1 + " " + items[1] + " is " + a2 + " " + super + ".")
          return
      else :
          subsets = get_includes_list(items[1])
          if subsets != [] :
              first = subsets[0]
              a1 = get_article(items[1]).capitalize()
              a2 = get_article(first)
              print(a1 + " " + items[1] + " is something more general than " + a2 + " " + first + ".")
              return
          else :
              if items[1] in SYNONYMS: #if representative, then print synonym chain
                synonym_chain = SYNONYMS[items[1]][0]
                for ii in SYNONYMS[items[1]][1:-1]: synonym_chain += ','+ii
                synonym_chain += ', and '+SYNONYMS[items[1]][-1]
                print(get_article(items[1]).capitalize()+" "+items[1]+" is a representative of "+synonym_chain+'.')
              else:
                print("I don't know.")
      return
    result_match_object = why_pattern.match(info)
    if result_match_object != None :
      items = result_match_object.groups()
      if not isa_test(items[1], items[3]) :
          print("But that's not true, as far as I know!")
      else:
          answer_why(items[1], items[3])
      return

    print("I do not understand.  You entered: ")
    print(info)

def answer_why(x, y):
    'Handles the answering of a Why question.'
    answer = "Because "
    if x == y:
      print("Because they are identical.")
      return
    # if isa_test1(x, y):
    if(get_rep(x) == x and get_rep(y) == y):
      print("Because you told me that.")
    elif(get_rep(x) == x and get_rep(y) != y):
      answer+=get_article(x)+" "+x+" is another name for "+get_article(get_rep(x))+" "+get_rep(x)+\
      +", and "+report_chain(get_rep(x),y)+"."
    elif(get_rep(x) != x and get_rep(y) == y):
      answer+=report_chain(x,get_rep(y))+", and "+get_article(get_rep(y))+" "+get_rep(y)+" is another name for "+\
      get_article(y)+" "+y+"."
    else:
      answer+=get_article(x)+" "+x+" is another name for "+get_article(get_rep(x))+" "+get_rep(x)+", "+\
        report_chain(get_rep(x),y)+', and '+get_article(get_rep(y))+" "+get_rep(y)+\
              " is another name for "+get_article(y)+" "+y+"."
      print(answer)
      return
    print("Because " + report_chain(x, y))

from functools import reduce
def report_chain(x, y):
    'Returns a phrase that describes a chain of facts.'
    chain = find_chain(x, y)
    all_but_last = chain[0:-1]
    last_link = chain[-1]
    main_phrase = reduce(lambda x, y: x+", "+y, map(report_link, all_but_last))
    last_phrase = ", and " + report_link(last_link)
    return main_phrase + last_phrase

def report_link(link):
    'Returns a phrase that describes one fact.'
    x = link[0]
    y = link[1]
    a1 = get_article(x)
    a2 = get_article(y)
    return a1 + " " + x + " is " + a2 + " " + y

def find_chain(x, z):
    'Returns a list of lists, which each sublist representing a link.'
    if isa_test1(x, z):
        return [[x, z]]
    else:
        for y in get_isa_list(x):
            if isa_test(y, z):
                temp = find_chain(y, z)
                temp.insert(0, [x,y])
                return temp

def detected_cycle(x,y):
  'Returns true if x includes y'
  return isa_test(y,x)

def handle_cycle(x,y):
  'make x representative of y and all of it\'s super classes'
  chain = find_chain(y,x) # y < x
  INCLUDES[x] = [] # includes nothing because all items in chain are now synonyms
  if not x in SYNONYMS: SYNONYMS[x] = []
  if not x in ISA: ISA[x] = []
  for link in chain:
    isAnX = link[0]
    if isAnX in SYNONYMS: #if isAnX is a rep, transfer it's members under new rep -- it is no longer a rep
      for item in SYNONYMS[isAnX]: SYNONYMS[x].append(item)
      del SYNONYMS[isAnX]
    SYNONYMS[x].append(isAnX)

    #replace items in ISA and INCLUDE dict with representative
    for item in ISA[isAnX][1:]:
      ISA[x].append(item) #transfer transitive relations of subclass to rep
    # isAnX may be a leaf node
    if isAnX in INCLUDES:
      for item in INCLUDES[isAnX]:
        if item in ISA: # subclass, but not included in loop
          INCLUDES[x].append(item)
      del INCLUDES[isAnX]
    del ISA[isAnX]
    print('***synonyms: '+str(SYNONYMS)) #test#
  return True

def isAnotherNameFor(x):
  'Returns either an empty string or an item from SYNONYMS'
  for syn in SYNONYMS:
    if SYNONYMS[syn].__contains__(x):
      return syn
  return ''

def test() :
    process("A turtle is a reptile.")
    # process("A turtle is a shelled-creature.")
    # process("A reptile is an animal.")
    # process("An animal is a thing.")

test()
linneus()
