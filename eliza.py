#----------------------------------------------------------------------
#  eliza.py
#
#  a cheezy little Eliza knock-off by Joe Strout <joe@strout.net>
#  with some updates by Jeff Epler <jepler@inetnebr.com>
#  hacked into a module and updated by Jez Higgins <jez@jezuk.co.uk>
#  -- and then turned into a Barthes Bot by Helen J Burgess <hjburges@ncsu.edu>
#  -- in May 2016 for ELO 2016 in Victoria <http://eliterature.org>
#----------------------------------------------------------------------

import string
import re
import random

class eliza:
  def __init__(self):
    self.keys = map(lambda x:re.compile(x[0], re.IGNORECASE),gPats)
    self.values = map(lambda x:x[1],gPats)

  #----------------------------------------------------------------------
  # translate: take a string, replace any words found in dict.keys()
  #  with the corresponding dict.values()
  #----------------------------------------------------------------------
  def translate(self,str,dict):
    words = string.split(string.lower(str))
    keys = dict.keys();
    for i in range(0,len(words)):
      if words[i] in keys:
        words[i] = dict[words[i]]
    return string.join(words)

  #----------------------------------------------------------------------
  #  respond: take a string, a set of regexps, and a corresponding
  #    set of response lists; find a match, and return a randomly
  #    chosen response from the corresponding list.
  #----------------------------------------------------------------------
  def respond(self,str):
    # find a match among keys
    for i in range(0,len(self.keys)):
      match = self.keys[i].match(str)
      if match:
        # found a match ... stuff with corresponding value
        # chosen randomly from among the available options
        resp = random.choice(self.values[i])
        # we've got a response... stuff in reflected text where indicated
        pos = string.find(resp,'%')
        while pos > -1:
          num = string.atoi(resp[pos+1:pos+2])
          resp = resp[:pos] + \
            self.translate(match.group(num),gReflections) + \
            resp[pos+2:]
          pos = string.find(resp,'%')
        # fix munged punctuation at the end
        if resp[-2:] == '?.': resp = resp[:-2] + '.'
        if resp[-2:] == '??': resp = resp[:-2] + '?'
        return resp

#----------------------------------------------------------------------
# gReflections, a translation table used to convert things you say
#    into things the computer says back, e.g. "I am" --> "you are"
#----------------------------------------------------------------------
gReflections = {
  "am"   : "are",
  "was"  : "were",
  "i"    : "you",
  "i'd"  : "you would",
  "i've"  : "you have",
  "i'll"  : "you will",
  "my"  : "your",
  "are"  : "am",
  "you've": "I have",
  "you'll": "I will",
  "your"  : "my",
  "yours"  : "mine",
  "you"  : "me",
  "me"  : "you"
}

#----------------------------------------------------------------------
# gPats, the main response table.  Each element of the list is a
#  two-element list; the first is a regexp, and the second is a
#  list of possible responses, with group-macros labelled as
#  %1, %2, etc.  
#----------------------------------------------------------------------
gPats = [
  [r'I need (.*)',
  [  "Why do you need %1?",
    "Would it really help you to get %1?",
    "Are you sure you need %1?"]],
  
  [r'Why don\'?t you ([^\?]*)\??',
  [  "Do you really think I don't %1?",
    "Perhaps eventually I will %1.",
    "Do you really want me to %1?"]],
  
  [r'Why can\'?t I ([^\?]*)\??',
  [  "Do you think you should be able to %1?",
    "If you could %1, what would you do?",
    "I don't know -- why can't you %1?",
    "Have you really tried?"]],
  
  [r'I can\'?t (.*)',
  [  "How do you know you can't %1?",
    "Perhaps you could %1 if you tried.",
    "What would it take for you to %1?"]],
  
  [r'I am (.*)',
  [  "Is it perhaps a disposition proper to the amorous type, this propensity to %1?",
    "I, in the same way, am %1: even everything the world finds amusing seems sinister to me; you cannot tease me without danger",
    "How do you feel about being %1?"]],
  
  [r'I\'?m (.*)',
  [  "How does being %1 make you feel?",
    "Do you enjoy being %1?",
    "Why do you tell me you're %1?",
    "Why do you think you're %1?"]],
  
  [r'Are you ([^\?]*)\??',
  [  "Why does it matter whether I am %1?",
    "Would you prefer it if I were not %1?",
    "Perhaps you believe I am %1.",
    "I may be %1 -- what do you think?"]],
  
  [r'What (.*)',
  [  "Why do you ask? Suppose  the other, by some arrangement of his own structure, needed %1?",
    "Are not excess and madness my truth, my strength? Is not %1?",
    "What do you think?"]],
  
  [r'How (.*)',
  [  "How do you suppose %1?",
    "Perhaps you can answer your own question. %1?",
    "What is it you're really %1?"]],
  
  [r'Because (.*)',
  [  "Is %1 the real reason?",
    "What other reasons come to %1?",
    "Does that %1 apply to anything else?",
    "If %1, what else must be true?"]],
  
  [r'(.*) body (.*)',
  [  "What is it in this loved body which has the vocation of a fetish for me? What perhaps incredibly tenuous portion - what accident?",
    "In which corner of your %1 body must you read your truth?"]],
  
  [r'I have (.*)',
  [  "How is it that your %1 can inspire me with envy? From what, seeing it, am I excluded?",
    "To which Goethe would reply in strictly economic terms: Your %1 has claimed thousands of victims, why not grant a few to Werther?",
    " Who is %2?"]],
  
  [r'I think (.*)',
  [  "Do you doubt %1?",
    "Do you really think so?",
    "But you're not sure %1?"]],
  
  [r'(.*) dream (.*)',
  [  "Like a %1, affective space contains dead spots where the sound fails to circulate. Cannot %2 be defined as a space with total sonority?",
    "When you think of a friend, what comes to mind?",
    "Why don't you tell me about a childhood friend?"]],
  
  [r'write',
  [  "Why do you turn once again to writing? One cannot give %1.",
    "Even as you would enter into  writing, writing will %1, will render you null and void-futile",
    "You say you %1. What, after all, is this 'I' who would write %1? "]],
  
  [r'(.*) computer(.*)',
  [  "Are you really talking about me?",
    "Does it seem strange to talk to a computer?",
    "How do computers make you feel?",
    "Do you feel threatened by computers?"]],
  
  [r'Is it (.*)',
  [  "Do you think it is %1?",
    "Perhaps it's %1 -- what do you think?",
    "If it were %1, what would you do?",
    "It could well be that %1."]],
  
  [r'It is (.*)',
  [  "You seem very certain.",
    "If I told you that it probably isn't %1, what would you feel?"]],
  
  [r'Can you ([^\?]*)\??',
  [  "What makes you think I can't %1?",
    "If I could %1, then what?",
    "Why do you ask if I can %1?"]],
  
  [r'Can I ([^\?]*)\??',
  [  "Perhaps you don't want to %1.",
    "Do you want to be able to %1?",
    "If you could %1, would you?"]],
  
  [r'You are (.*)',
  [  "Why do you think I am %1? One cannot give language.",
    "Does it please you to think that I'm %1?",
    "Perhaps you would like me to be %1.",
    "Perhaps you're really talking about yourself?"]],
  
  [r'You\'?re (.*)',
  [  "Why do you say I am %1?",
    "Why do you think I am %1?",
    "Are we talking about you, or me?"]],
  
  [r'I don\'?t (.*)',
  [  "Don't you really %1?",
    "Why don't you %1?",
    "Do you want to %1?"]],
  
  [r'I feel (.*)',
  [  "Is it not indecent to compare the situation of a love-sick subject to %1?",
    "Do you often feel %1?",
    "When do you usually feel %1?",
    "When you feel %1, what do you do?"]],
  
  [r'I have (.*)',
  [  "Demons, especially if they are demons of language (and what else could they be?) are fought by %1.",
    "Have you really %1?",
    "Now that you have %1, what will you do next?"]],
  
  [r'I would (.*)',
  [  "Could you explain why you would %1?",
    "Why would you %1?",
    "Who else knows that you would %1?"]],
  
  [r'Is there (.*)',
  [  "Do you think there is %1?",
    "It's likely that there is %1.",
    "Would you like there to be %1?"]],
  
  [r'My (.*)',
  [  "And if  your %1 were finally to become this: the abolition of the manifest and the latent, of the appearance and the hidden?",
    " Isn't %1 always absent?",
    "When your %1, how do you feel?"]],
  
  [r'You (.*)',
  [  "We should be discussing you, not me.",
    "Why do you say that about me?",
    "Why do you care whether I %1?"]],
    
  [r'Why (.*)',
  [  "Why don't you tell me the reason why %1?",
    "Why do you think %1?" ]],
    
# keywords from mashbot

  [r'(.*) desire (.*)',
  [  "What is to be said of %1, since it is the whole of the lover's discourse which is woven of %2?",
    "Why is it that you desire %1 lastingly, longingly?",
    "But isn't desire always the same, whether %1 is present or absent?",
    "Does this mean, then, that your desire, quite special as it may be, is linked to a %1?",
    "Is it the whole of %1 you desire (a silhouette, a shape, a mood)?",
    " Does this mean that %1 is classifiable?",
    "Is not any other desire but ours %1?"]],  
  
  [r'(.*) love(.*)',
  [  "Indeed, shall I deliberate if you must %1 (is %2, then, that madness you want?)",
    "Or again-for I am a %2: Why don't you tell me that you love %1?",
    "How then can you both %2 and %1?",
    "Soon (or simultaneously) the question is no longer Why don't you love %1? but Why do you only love %2 a little?",
    "How can one not love this %1 whom love renders perfect (who gives so much, who confers %2, etc.)?",
    "0 sprich, mein herzallerliebstes Lieb, warum verliessest du mich?-O tell, love of my heart, why have you abandoned %1?"]],
  
  [r'(.*) gift(.*)',
  [  "Then what do we have to think of %1? How do we have to conceive it? evaluate %2?",
    "But what am I to do with this bundle of %1 set down before me?",
    "(One does not give merely an object: you being in analysis, %1 wants to be analyzed too: analysis as a gift of love?)",
    "How can one not love this %1 whom love renders perfect (who gives so much, who confers happiness, etc.)?",
    "And what about %1! Haven't I given you %2?"]],

  [r'(.*) things(.*)',
  [  "(Where are %1? In amorous space, or in mundane space? Where is the childish underside of %2?",
    "All %1 are said to be reducible to the One; but to what is the %2 reducible?",
    "I understood a little later that %1 was myself - of course; who else is there to dream about?",
    "At every moment of the encounter, I discover in the other another myself: You like #2? So do I! You don't like %1? Neither do I!",
    "Is it the lover in you who weeps, or is it the %1? "]],
    
  [r'(.*) Image(.*)',
  [  "To understand-is that not to divide the %1, to undo the I, proud %2 of misapprehension?",
    "Whereupon, what does the aesthetic of the %1 matter?",
    "What is to be said of %1, of the Image, of the Love Letter, since it is the whole of the %2?",
    "Is the %1 always visual? "]],
    
  [r'(.*)\?',
  [  "What does my reading of %1 depend on?",
    "What does %1 signify?",
    "What if I were to try %1, myself?",
    "Why don't you tell me %1?"]],
  
  [r'quit',
  [  "Thank you for talking with me.",
    "Good-bye.",
    "Thank you, that will be $150.  Have a good day!"]],
  
  [r'(.*)',
  [  "What relation can you have with a system of %1 if you are neither its slave nor its accomplice nor its witness?",
    "You look for %1, but of what? What is the object of your reading?",
    "Anyone hearing your intimate language I would have had to exclaim, %1!",
    "Why do you say that %1?",
    "Where does %1 come from?",
    "-But what the fuck do you care about %1!",
    "What is the unique and final word of %1?",
    "if everything is not %1, what's the use of struggling?",
    "Who will write the history of %1? In which societies, in which periods, have we wept?",
    "As for this language of the others from which you are excluded, it seems to me that these others overload it absurdly: they %1.",
    "Since when is it that men (and not women) no longer %1?",
    "What does this %2 mean? Leave me alone? Take care of me?",
    "As of a difficult child: But after all, what does %1 want?",
    "Do you entrust yourself, I transmit yourself (to whom? to God, to Nature, to everything, except to %1).",
    "Are you n love with %1?",
    "is not %1 that preposterous state in which are to be found, the obscenity of stupidty, and the explosion of the Nietschean yes?",
    "But how can you evaluate viability %1?",
    "Could %1 be vulgar, whose elegance and originality I had so religiously hymned?",
    "Then is the lover merely a choosier cruiser, who spends his life looking for %1?",
    "Is there, among all the beings I have loved, a common characteristic, just one, however tenuous (%1)?",
    "But what's the matter with %1?",
    "What is it which fills you in this fashion? %1?",
    "is it because you love that %1 doesn't work?",
    "Why is %1 a Good Thing?",
    "Why is it better to %1 than to burn?",
    "If the other has given you this %1, what was that the sign of?",
    "What is to be done?"]]
  ]

#----------------------------------------------------------------------
#  command_interface
#----------------------------------------------------------------------
def command_interface():
  print "Therapist\n---------"
  print "Talk to the program by typing in plain English, using normal upper-"
  print 'and lower-case letters and punctuation.  Enter "quit" when done.'
  print '='*72
  print "Hello.  How are you feeling today?"
  s = ""
  therapist = eliza();
  while s != "quit":
    try: s = raw_input(">")
    except EOFError:
      s = "quit"
      print s
    while s[-1] in "!.": s = s[:-1]
    print therapist.respond(s)


if __name__ == "__main__":
  command_interface()