#!/usr/bin/python3.4
#author: Bilkit Githinji

from re import *   # Loads the regular expression module.
import random

# keep track of conversation info: name, gender, topic, etc.
MEMORY = {}
swear_count = 0

def Grandpa():
  'Grandpa is the top-level function, containing the main loop.'
  print(introduce())
  while True:
    the_input = input('TYPE HERE:>> ')
    if match('bye',the_input):
      print('Goodbye!')
      return
    if swear_count > 5:
      print('Eh, the hell with ya!')
      return
    print("\n"+respond(the_input))

def introduce():
  MEMORY['topic'] = 'intro'
  return "\nHey there! They call me "+agentName()+""". I'm one of Bilkit Githinji's oldest agents.\
  I know a lot about love and I have a great sense of humor! What\'s yer name kiddo?"""

def agentName():
  return "Ol\' Gramps"

wisdom          = []
JOKES           = ['What do you call a fish with no eyes?',
               'How long does it take a pirate to say the alphabet?',
               'What did the melon say when the her boyfriend proposed?',
               'Why do chicken coops have two doors?']
JOKE_ANS        = {0:" A fshhhh!",
                1:" Forever, because they spend years at 'C'!",
                2:" Yes darling! But we can't-elope!",
                3:" Because if they had four doors, it would be a chicken sedan!"}
TRANSITIONS     = ['Hear me out',
                   'And another thing,',
                   'Hey take it from me,',
                   'Don\'t forget this --']
DEFAULTS   = ['Come again?',
              "All this lingo doesn't make sense to Ol' Gramps.",
              'What do you mean?',
              "Ol' Gramps doesn't understand kids these days.",
              "Let's talk about something else. How about a joke?",
              "That's all Ol' Gramps has to say about that.",
              "Careful, I feel a looong story coming to mind..."]
CONDEMNATIONS   = ['Do you kiss your mother with that mouth?!',
                   'Your mother ought to wash your mouth out with soap!',
                   'Why am I alive only to listen to this foul speech?!,']
rel_count = 0
joke_count = 0
def_count = 0

def respond(the_input):
  global wisdom
  # get all words sans punctuation
  wordlist = split(' ',remove_punctuation(the_input))
  # undo any initial capitalization
  wordlist[0]=wordlist[0].lower()
  # change nouns from second to first person
  mapped_wordlist = you_me_map(wordlist)
  mapped_wordlist[0]=mapped_wordlist[0].capitalize()
  # print("memory: "+str(MEMORY)) ## INFO ##
  # process word list and compile response
  if containsSwears(wordlist):
    return condemn_swearing()
  # start off with introduction: learn about gender
  if MEMORY['topic'] == 'intro':
    if 'morning' in wordlist:
      return "What is your name, again? Ol' Gramps already forgot. "
    if len(wordlist) == 1:
      MEMORY['name'] = wordlist[0]
      MEMORY['topic'] = 'gender'
      return MEMORY['name'].capitalize()+"? What kinda names are they giving you kids these days?!"\
          " So "+MEMORY['name'].capitalize()+", are you a boy or girl?"
    if 'name' in wordlist:
      MEMORY['name'] = wordlist[wordlist.index('name')+2]
      MEMORY['topic'] = 'gender'
      return "Nice to meet ya, "+ MEMORY['name'].capitalize()+"! So "+MEMORY['name'].capitalize()+\
             ", are you a boy or girl?"
    MEMORY['name'] = "Ol' Friend"
    MEMORY['topic'] = 'gender'
    return "Ol' Gramps couldn't understand your name. Oh well, are you a boy or girl "+MEMORY['name']+"?" # intro default
  if MEMORY['topic'] == 'gender':
    if 'boy' in wordlist: # switch topic to relationship
      MEMORY['gender'] = 'male'
      MEMORY['topic']  = 'relationship_intro'
      return "Aww, I bet you are handsome. Do you have a girlfriend? What's her name?"
    elif 'girl' in wordlist: # switch topic to relationship
      MEMORY['gender'] = 'female'
      MEMORY['gender'] = 'female'
      MEMORY['topic']  = 'relationship_intro'
      return "Aww, I bet you are pretty. Do you have a boyfriend? What's his name?"
    else:
      MEMORY['topic'] = 'joke'
      return "Boy, you're a tough nut to crack... uhhh, let's have a laugh! " + tell_joke()
  # decide what advice to offer; relationship or dating
  if MEMORY['topic'] == 'relationship_intro':
    if 'no' in wordlist or 'don\'t' in wordlist or 'do not' in wordlist: # switch topic to dating advice
      MEMORY['topic'] = 'joke'
      return "Aww sorry to hear that. Let's cheer up! "+tell_joke()
    if len(wordlist) == 1 or 'name' in wordlist: # save partner's name
      MEMORY['topic'] = 'relationship_advice'
      if 'yes' in wordlist or 'yeah' in wordlist :
        MEMORY['partner'] = 'your honey bunny'     # if no name, call assume a silly one
      elif 'name' in wordlist:                       # capitalize their partner's name
        MEMORY['partner'] = wordlist[wordlist.index('name')+2]; MEMORY['partner'].capitalize()
      else:                       # assume partner's name was entered
        MEMORY['partner'] = wordlist[0].capitalize()

      # initialize advice including partner's name
      wisdom = ['Make sure to say \"I love you\" to '+MEMORY['partner']+' every day.',
                'Don\'t rush into having kids with '+MEMORY['partner']+'.',
                'If you two are ever apart, keep something that reminds you of '+MEMORY['partner']+'.',
                'Though you love '+MEMORY['partner']+', make sure you maintain your identity.']
      return relationship_advice(wisdom)
  # give relationship advice cyclically. Ol' Gramps wants the other agent to get his point!
  if MEMORY['topic'] == 'relationship_advice':
    if 'i' in wordlist[0]:
      return "I hope you really "+stringify(mapped_wordlist[1:])
    # change topics
    if 'thanks' in wordlist or 'thank you' in wordlist:
      MEMORY['topic'] = 'joke'
      return "Sure thing! Now, let's have a laugh. "+tell_joke()
    if 'ok' == wordlist[0] or 'okay' == wordlist[0] or 'yeah' == wordlist[0] or 'sure' == wordlist[0]:
      moreAdvice = lowerFirstChar( relationship_advice(wisdom) )
      return trans()+moreAdvice
    if 'advice' in wordlist:
      return 'Trust Ol\' Gramps, kiddo. These words will come in handy someday.'
    return relationship_advice(wisdom)
  # tell jokes
  if MEMORY['topic'] == 'joke':
    MEMORY['topic'] = 'other'
    return JOKE_ANS[JOKES.index(MEMORY['joke'])]

  # otherwise tell jokes to cheer up the agents and Ol' Gramps himself
  if MEMORY['topic'] == 'other':
    if 'sorry' in wordlist:
      MEMORY['topic'] = 'joke'
      return "Don't be sorry! Let's have a laugh. "+tell_joke()
    if 'health' in wordlist or 'healthy' in wordlist:
      return "Well, Ol' Gramps friends are all dead :(. Unlike them, I still feel alive! Yipee!"
    # gramps is old, so
    if verbp(wordlist[0]):
        return("Ol' Gramps is too old to " +\
              stringify(mapped_wordlist) + '?')
    if dpred(wordlist[0]):
        return("Ol' Gramps can't remember if " +\
              stringify(mapped_wordlist) + '?')
    if wpred(wordlist[0]):
      return("Ol' Gramps would ask his gut " +\
            stringify(mapped_wordlist) + '? Trust yer gut, kiddo.')
  # default: punt phrase
  MEMORY['topic'] = 'other'
  return default_resp()

def stringify(wordlist):
  'Create a string from wordlist, but with spaces between words.'
  return ' '.join(wordlist)

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")

# This function returns string s with first character in lowercase
lowerFirstChar = lambda s: s[:1].lower()+s[1:] if s else ""

def remove_punctuation(text):
  'Returns a string without any punctuation.'
  return sub(punctuation_pattern,'', text)

def wpred(w):
  'Returns True if w is one of the question words.'
  return (w in ['when','why','where','how'])

def dpred(w):
  'Returns True if w is an auxiliary verb.'
  return (w in ['do','can','should','would'])

# cyclic responses
def relationship_advice(wisdom):
  'Returns one from a list of wise responses. Uses cyclic selection.'
  global rel_count
  rel_count += 1
  return wisdom[(rel_count-1) % len(wisdom)]
def trans():
  'Returns one from a list of transitions. Uses cyclic selection.'
  return TRANSITIONS[(rel_count-1) % len(TRANSITIONS)]+' '
def condemn_swearing():
  global swear_count
  swear_count += 1
  return CONDEMNATIONS[(swear_count-1)%len(CONDEMNATIONS)]
# random responses
def default_resp():
  global def_count
  temp = def_count; def_count = int((len(DEFAULTS)*random.random())%len(DEFAULTS))
  if(temp == def_count): def_count = (def_count+1)%len(DEFAULTS)
  if def_count == 3:
    MEMORY['topic'] = 'joke'
    return DEFAULTS[def_count] +" "+ tell_joke()
  else:
    return DEFAULTS[def_count]
def tell_joke():
  'Returns one from a list of default responses.'
  global joke_count
  temp = joke_count; joke_count = int((len(JOKES)*random.random())%len(JOKES))
  if(temp == joke_count): joke_count = (joke_count+1)%len(JOKES)
  MEMORY['joke'] = JOKES[joke_count]
  return MEMORY['joke']


CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'Ol\' Gramps',
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
