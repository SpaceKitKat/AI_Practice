#!/usr/bin/python3.4
#author: Bilkit Githinji

from re import *   # Loads the regular expression module.

MEMORY = {} # keep track of conversation info
def Grandpa():
  'Grandpa is the top-level function, containing the main loop.'
  print(intro())
  while True:
    the_input = input('TYPE HERE:>> ')
    if match('bye',the_input):
        print('Eh, the hell with ya!')
        return

    print(respond(the_input))

def intro():
  MEMORY['topic'] = 'intro'
  return "Hey there! They call me "+agentName()+""". I'm one of Bilkit Githinji's
oldest agents. I know a lot about life and love.
What\'s yer name kiddo?"""

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
  if wordlist[0]=='':
    # tell a joke
    return tell_joke()
  if MEMORY['topic'] == 'intro':
    if 'boy' in wordlist: # switch topic to relationship
      MEMORY['gender'] = 'male'
      MEMORY['topic']  = 'relationship_intro'
      return "Do you have a girlfriend? What's her name?"
    if 'girl' in wordlist: # switch topic to relationship
      MEMORY['gender'] = 'female'
      MEMORY['topic']  = 'relationship_intro'
      return "Do you have a boyfriend? What's his name?"
    if len(wordlist) == 1:
      MEMORY['name'] = wordlist
      return wordlist.capitalize()+"? What kinda names are they giving you kids nowadays." \
                                         "So"+wordlist.capitalize()+", are you a boy or girl?"
    if ['my','name'] == wordlist[0:2]:
      MEMORY['name'] = wordlist[3]
      return "Nice to meet ya, "+ wordlist[3].capitalize()+"! So"+wordlist[3].capitalize()+\
             ", are you a boy or girl?"
    return punt() # intro default
  # yes and topic is relation ask about name
  # save name of partner and offer relationship advice
  if MEMORY['topic'] == 'relationship_intro':
    if 'no' in wordlist or 'don\'t' in wordlist or 'do not' in wordlist: # switch topic to dating advice
      return #dating advice
    if wordlist[0] == 'yes' or 'name' in wordlist: # save partner's name
      MEMORY['topic'] = 'relationship_advice'
      MEMORY['partner'] = wordlist[wordlist.index('name')+2]
      # initialize advice including partner's name
      wisdom = ['You should say \"I love you\" to '+MEMORY['partner'].capitalize()+' every day.',
                'Hey, take it from me. Don\'t rush into having kids with '+MEMORY['partner'].capitalize()+'.']
      return relationship_advice(wisdom)
  if MEMORY['topic'] == 'relationship_advice':
    # handle questions
    if 'i' in wordlist[0]:
      return "I hope you really "+stringify(mapped_wordlist[1:])
    if 'ok' in wordlist[0] or 'okay' in wordlist[0]:
      return # some change in topic
    return relationship_advice(wisdom)
  if MEMORY['topic'] == 'dating_advice':
    return # dating advice default
  if 'sorry' in wordlist:
    return "Don't be sorry! Let's have a laugh. "+tell_joke()
  if 'health' in wordlist or 'healthy' in wordlist:
    return "Well, my friends are all dead :(. Unlike them, I still feel alive! Yipee!"
  # default: punt phrase
  return punt()

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
# cyclical responses

PUNTS           = ['Come again?\n']
WISDOM_DATING   = []
punt_count = 0
def relationship_advice(wisdom):
  'Returns one from a list of wise responses. Uses cyclic selection.'
  global punt_count
  punt_count += 1
  return wisdom[punt_count % len(wisdom)]
def dating_advice():
  'Returns one from a list of wise responses. Uses cyclic selection.'
  global punt_count
  punt_count += 1
  return WISDOM_DATING[punt_count % len(WISDOM_DATING)]
def punt():
  'Returns one from a list of wise responses. Uses cyclic selection.'
  global punt_count
  punt_count += 1
  return PUNTS[punt_count % len(PUNTS)]

# random responses
DADJOKES = ['What do you call a fish with no eyes? A fshhhh.'
            'How long does it take a pirate to say the alphabet? Forever, because they spend years at \'C\'']
def tell_joke():
  'Returns one from a list of default responses.'
  global punt_count
  punt_count += 1
  return DADJOKES[punt_count % len(DADJOKES)]


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

def verbp(w):
  'Returns True if w is one of these known verbs.'
  return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                'make', 'get', 'jump', 'write', 'type', 'fill',
                'put', 'turn', 'compute', 'think', 'drink',
                'blink', 'crash', 'crunch', 'add'])

Grandpa() # Launch the program.
