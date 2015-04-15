""" Tsz Yeung David Fung
    CSE 415
    Steven Tanimoto
    Assignment 1
    4/5/15
"""

from re import *   # Loads the regular expression module.
import random

memory = ['' for i in range(10)]  # 10 most recent topics discussed

def Chuck_Norris():
    'Chuck_Norris is the top-level function, containing the main loop.'
    global memory
    dialogTurns = 0
    index1 = 0
    index2 = 0
    askTopic = 0

    print(introduce())
    while True:

        # saves topic by user by giving them a prompt
        while askTopic == 0:
            theInput1 = input('What\'s the first word that comes to your mind: >> '.upper())

            # user entered a word
            if theInput1 and ' ' not in theInput1:
                print("'Kay")
                memory[index1 % len(memory)] = remove_punctuation(theInput1)
                index1 += 1
                askTopic = 1

            # user entered more than one word
            elif ' ' in theInput1:
                print("Hey! I said ONE word.")

            else:   # no topic was mentioned
                print('Say again?')

        # topic received, agent ready to answer
        theInput2 = input('STATE YOUR BUSINESS: >> ')

        if match('bye', theInput2) or match('end', theInput2):
            print('Get outta here!')
            return

        # Agent returns to an earlier topic introduce by the user every 10 dialog exchanges
        if dialogTurns % 10 < 9:
            print(respond(theInput2))                         # normal response from agent
            dialogTurns += 1
        else:
            print("Never mind that, I thought we were talking about " + memory[index2].lower() + "? " +\
                  "\nGo ahead and say another word.")
            memory[index2 % len(memory)] = ''                 # erase aforementioned topic
            index2 += 1                                       # keep looping through the "memory" of the agent
            askTopic = 0


cycle = 0  # cyclic variable for all rules in respond function

def respond(theInput):
    'Returns the response from the agent.'
    global cycle
    wordlist = split(' ', remove_punctuation(theInput))
    # undo any initial capitalization:
    wordlist[0] = wordlist[0].lower()
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0] = mapped_wordlist[0].capitalize()

    if wordlist[0]=='':
        noInput = ['What?', 'Come on, I don\'t time for this...']
        cycle += 1
        return noInput[cycle % 2]

    if wordlist[0:2] == ['i', 'am']:
        iAm = ['Ok, so what if you are ' + stringify(mapped_wordlist[2:]) + '?',
               'I am too, what a coincidence.',
               'Sure you are.']
        cycle += 1
        return iAm[cycle % 3]

    if wpred(wordlist[0]):
        w_pred = ['Don\'t worry, I\'m sure you will figure out ',
                  "You tell me "]
        cycle += 1
        return w_pred[cycle % 2] + wordlist[0] + '.'

    if wordlist[0:2] == ['i', 'have']:
        iHave = ['How long have you had ' + stringify(mapped_wordlist[2:]) + '?',
                 'Ok fine, I admit I had ' + stringify(mapped_wordlist[2:]) + ' at one time.']
        cycle += 1
        return iHave[cycle % 2]

    if wordlist[0:2] == ['i', 'feel']:
        iFeel = ['I\'m sure you feel ' + stringify(mapped_wordlist[2:]) + ' all the time.',
                 'I\'m definitely not feeling ' + stringify(mapped_wordlist[2:]) + '.']
        cycle += 1
        return iFeel[cycle % 2]

    if 'because' in wordlist:
        because = ['Is that really the reason?',
                   'C\'mon, I\'m not your therapist!'
                   'Well, is that so?']
        cycle += 1
        return because[cycle % 3]

    if 'yes' in wordlist:
        yes = ['Ah yes, I like the sound of that. :)',
               'Here you go again with all that optimism.']
        cycle += 1
        return yes[cycle % 2]

    if wordlist[0:2] == ['you', 'are']:
        uAre = ["Of course, I am " + stringify(mapped_wordlist[2:]) + '.',
                'So are you.']
        cycle += 1
        return uAre[cycle % 2]

    if verbp(wordlist[0]):
        verb = ["Chuck Norris takes no orders from anybody.",
                "Why do you want me to " + stringify(mapped_wordlist) + '?']
        cycle += 1
        return verb[cycle % 2]

    if wordlist[0:3] == ['do', 'you', 'think']:
        uThink = ["Chuck Norris doesn't think, he does.",
                  "Seek for the answer within."]
        cycle += 1
        return uThink[cycle % 2]

    if wordlist[0:2] == ['can', 'you'] or wordlist[0:2] == ['could', 'you']:
        request = ["I can but I won't. Don't ask me why.",
                   "Perhaps I " + wordlist[0] + ' ' + stringify(mapped_wordlist[2:]) + '.',
                   "Don't order me around!"]
        cycle += 1
        return request[cycle % 3]

    if 'dream' in wordlist:
        dream = ["I always dream about that.",
                 "Chuck Norris dreams nothing but world domination."]
        cycle += 1
        return dream[cycle % 2]

    if 'love' in wordlist:
        love = ["Good for you.",
                "You sure love it."]
        cycle += 1
        return love[cycle % 2]

    if 'no' in wordlist:
        no = ["Nobody says no to Chuck Norris.",
              "Don't be such a pessimist.",
              "'No' is not in Chuck Norris' dictionary."]
        cycle += 1
        return no[cycle % 3]

    if 'maybe' in wordlist:
        maybe = ["Chuck Norris don't second-guess.",
                 "Be more decisive."]
        cycle += 1
        return maybe[cycle % 2]

    if 'you' in mapped_wordlist or 'You' in mapped_wordlist:
        # Cyclic case between answering
        if cycle == 1:
            return "No comment."
        cycle += 1
        return stringify(mapped_wordlist) + '.'

    if 'chuck' in wordlist or 'Chuck' in wordlist:
        return "Told you Chuck Norris knows everything."

    # Random response if no other rules apply
    return rand()

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

randChoice = ['Yawn, I\'m bored.',
              'I think I\'m gonna have a restroom break.',
              'Well, don\'t you say.',
              'Speak in English.',
              'So, that\'s how it is.',
              'What?',
              'Speak in more detail,',
              'Why am I talking to you again?']


def rand():
    'Returns a randomly chosen response from a list of default responses.'
    return randChoice[random.randrange(0, len(randChoice)-1)]

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
    return [you_me(w) for w in wordlist]

def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add'])

def introduce():
    'Returns introductory phase of the agent and its programmer.'
    return """Yo, my name is Chuck Norris and Chuck Norris can do everything.
I was programmed by David Fung. If you get intimidated by my awesomeness,
post your complaints to dtyfung@u.\n
Well then, let me get out my crystal orb."""

def agentName():
    'Returns the nickname of agent.'
    return "Chuck_Norris"

#Chuck_Norris() # Launch the program.


