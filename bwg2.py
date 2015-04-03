#!/usr/bin/python3.4
#author: Bilkit Githinji

from re import *   # Loads the regular expression module.

def Grandpa():
  'Grandpa is the top-level function, containing the main loop.'
  print(intro())
  while True:
    the_input = input('TYPE HERE:>> ')
    if match('bye',the_input):
        print('Eh, the hell with ya!')
        return

    respond(the_input)

def intro():
  return "Hey there! They call me "+agentName()+""". I'm one of Bilkit Githinji's
oldest agents. Boy, I cannot wait to rest these old bones.
What\'s yer name kiddo?"""

def agentName():
  return "Ol\' Gramps"


def respond(the_input):
  # get all words sans punctuation
  wordlist = split(' ',remove_punctuation(the_input))
  # undo any initial capitalization
  wordlist[0]=wordlist[0].lower()
  # change nouns from second to first person
  mapped_wordlist = you_me_map(wordlist)
  mapped_wordlist[0]=mapped_wordlist[0].capitalize()

  # process word list and compile response
  if wordlist[0]=='': #Rule1: nothing said
    print("Please say something.")
    return
  if wordlist[0:2] == ['i','miss']: #Rule2: sympathy
    print("Awww I miss " +\
          stringify(mapped_wordlist[2:]) + ', too. If only I were young again')
    return
  if ['what','up'] in wordlist: #Rule3: depressed
    print("All my friends are dead :(")

  print(punt())

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

PUNTS = ['Come again? These ol\' ears can\'t hears as good as they used to.',
         'Oh that is what my wife would always say.',
         '',
         'What does that indicate?',
         'But why be concerned about it?',
         'Just tell me how you feel.']

punt_count = 0
def punt():
  'Returns one from a list of default responses.'
  global punt_count
  punt_count += 1
  return PUNTS[punt_count % 6]

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
