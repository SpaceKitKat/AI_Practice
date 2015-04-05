#!/usr/bin/python3.4
#author: Bilkit Githinji

from re import *   # Loads the regular expression module.
# keep track of conversation info: name, gender, topic, etc.
MEMORY = {}
swear_count = 0

def Grandpa():
  'Grandpa is the top-level function, containing the main loop.'
  print(intro())
  while True:
    the_input = input('TYPE HERE:>> ')
    if match('bye',the_input):
      print('Goodbye!')
      return
    if swear_count > 5:
      print('Eh, the hell with ya!')
      return
    print("\n"+respond(the_input)+"\n")

def intro():
  MEMORY['topic'] = 'intro'
  return "Hey there! They call me "+agentName()+""". I'm one of Bilkit Githinji's oldest agents.\
  I know a lot about love and I have a great sense of humor! What\'s yer name kiddo?"""

def agentName():
  return "Ol\' Gramps"

wisdom = []
def respond(the_input):
  global wisdom
  # get all words sans punctuation
  wordlist = split(' ',remove_punctuation(the_input))
  # undo any initial capitalization
  wordlist[0]=wordlist[0].lower()
  # change nouns from second to first person
  mapped_wordlist = you_me_map(wordlist)
  mapped_wordlist[0]=mapped_wordlist[0].capitalize()
  print("memory: "+str(MEMORY)) ## INFO ##
  # process word list and compile response
  if containsSwears(wordlist):
    return condemn_swearing()
  # start off with introduction: learn about gender
  if MEMORY['topic'] == 'intro':
    if 'boy' in wordlist: # switch topic to relationship
      MEMORY['gender'] = 'male'
      MEMORY['topic']  = 'relationship_intro'
      return "Aww, I bet you are handsome. Do you have a girlfriend? What's her name?"
    if 'girl' in wordlist: # switch topic to relationship
      MEMORY['gender'] = 'female'
      MEMORY['topic']  = 'relationship_intro'
      return "Aww, I bet you are pretty. Do you have a boyfriend? What's his name?"
    if len(wordlist) == 1:
      MEMORY['name'] = wordlist[0]
      return MEMORY['name'].capitalize()+"? What kinda names are they giving you kids nowadays?!"\
          " So "+MEMORY['name'].capitalize()+", are you a boy or girl?"
    if ['my','name'] == wordlist[0:2]:
      MEMORY['name'] = wordlist[3]
      return "Nice to meet ya, "+ MEMORY['name'].capitalize()+"! So "+MEMORY['name'].capitalize()+\
             ", are you a boy or girl?"
    return "Come again?" # intro default
  # decide what advice to offer; relationship or dating
  if MEMORY['topic'] == 'relationship_intro':
    if 'no' in wordlist or 'don\'t' in wordlist or 'do not' in wordlist: # switch topic to dating advice
      MEMORY['topic'] = 'dating_advice'
      return #dating advice
    if wordlist[0] == 'yes' or 'name' in wordlist: # save partner's name
      MEMORY['topic'] = 'relationship_advice'
      if 'name' in wordlist:                       # capitalize their partner's name
        MEMORY['partner'] = wordlist[wordlist.index('name')+2]; MEMORY['partner'].capitalize()
      else:
        MEMORY['partner'] = 'your honey bunny'     # if no name, call assume a silly one
      # initialize advice including partner's name
      wisdom = ['You should say \"I love you\" to '+MEMORY['partner']+' every day.',
                'Hey, take it from me. Don\'t rush into having kids with '+MEMORY['partner']+'.']
      return relationship_advice(wisdom)
  # give relationship advice cyclically. Ol' Gramps wants the other agent to get his point!
  if MEMORY['topic'] == 'relationship_advice':
    # handle questions
    if 'i' in wordlist[0]:
      return "I hope you really "+stringify(mapped_wordlist[1:])
    # change topics
    if 'thanks' in wordlist or 'thank you' in wordlist:

      return "Sure thing! What else "
    if 'ok' == wordlist[0] or 'okay' == wordlist[0] or 'yeah' == wordlist[0] or 'sure' == wordlist[0]:
      moreAdvice = relationship_advice(wisdom);
      return 'And another thing, '+moreAdvice.lower()


    return relationship_advice(wisdom)
  # give dating advice randomly; it's been a while since Ol' Gramps had a date
  if MEMORY['topic'] == 'dating_advice':


    return # dating advice default
  # otherwise tell jokes to cheer up the agents and Ol' Gramps himself
  if 'sorry' in wordlist:
    return "Don't be sorry! Let's have a laugh. "+tell_joke()
  if 'health' in wordlist or 'healthy' in wordlist:
    return "Well, my friends are all dead :(. Unlike them, I still feel alive! Yipee!"
  #
  if verbp(wordlist[0]):
      print("I'm afraid I'm too old to " +\
            stringify(mapped_wordlist) + '?')
      return
  # default: punt phrase
  return "Time for a laugh. "+tell_joke()

def stringify(wordlist):
  'Create a string from wordlist, but with spaces between words.'
  return ' '.join(wordlist)

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")

def remove_punctuation(text):
  'Returns a string without any punctuation.'
  return sub(punctuation_pattern,'', text)

def wpred(w):
  'Returns True if w is one of the question words.'
  return (w in ['when','why','where','how'])

def dpred(w):
  'Returns True if w is an auxiliary verb.'
  return (w in ['do','can','should','would'])

WISDOM_DATING   = ['']
CONDEMNATIONS   = ['Do you kiss your mother with that mouth?!',
                   'Your mother ought to wash your mouth out with soap!',
                   'Why am I alive only to listen to this foul speech?!,']
rel_count = 0
# cyclic responses
def relationship_advice(wisdom):
  'Returns one from a list of wise responses. Uses cyclic selection.'
  global rel_count
  rel_count += 1
  return wisdom[rel_count % len(wisdom)]
def condemn_swearing():
  global swear_count
  swear_count += 1
  return CONDEMNATIONS[(swear_count-1)%len(CONDEMNATIONS)]
# random responses
def dating_advice():
  'Returns one from a list of wise responses. Uses cyclic selection.'
  global dat_count
  dat_count += 1
  return WISDOM_DATING[dat_count % len(WISDOM_DATING)]
DADJOKES = ['What do you call a fish with no eyes? A fshhhh.'
            'How long does it take a pirate to say the alphabet? Forever, because they spend years at \'C\'']
def tell_joke():
  'Returns one from a list of default responses.'
  global joke_count
  joke_count += 1
  return DADJOKES[joke_count % len(DADJOKES)]


CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'me',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are'}

def you_me(w):
  'Changes a word from 1st to 2nd person or vice-versa.'
  try:
      result = CASE_MAP[w]
  except KeyError:
      result = w
  return result

def you_me_map(wordlist):
  'Applies YOU-ME to a whole sentence or phrase.'
  return [you_me(   w) for w in wordlist]
def containsSwears(wl):
  'Returns True if wl contains a bad word or phrase.'
  swear = False
  for w in wl:
    if w in ['shit', 'fuck', 'damn', 'fucker', 'suck','bullshit']: swear = True
  return swear
def swears(w):
  return ()
def verbp(w):
  'Returns True if w is one of these known verbs.'
  return (w in ['go', 'have', 'be', 'try', 'play', 'take', 'help',
                'make', 'get', 'jump', 'write', 'type', 'fill',
                'put', 'turn', 'compute', 'hike', 'drink',
                'drive', 'crash', 'crunch', 'add'])

Grandpa() # Launch the program.
