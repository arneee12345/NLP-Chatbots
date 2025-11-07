# Short absurd news headline

import tracery
from tracery.modifiers import base_english

# 1. Defining Grammar
grammar = tracery.Grammar({
    # starting rule: A location reports an absurd event
    'origin': ["#Location# reports: #Subject# #Verb# #Object# because of #Reason#."],
    
    # Word lists
    'Location': ["Hamburg", "Berlin", "Moon Base Alpha", "Mars Colony", "The North Pole", "A Sunken Submarine"],
    'Subject': ["A Squirrel", "An AI", "The Last Programmer", "A Hamster", "The Rumor", "The Mayor"],
    'Verb': ["kidnapped", "digitized", "refuses", "hypnotizes", "clones", "swapped"],
    'Object': ["the Key", "the Password", "the Cat", "the Coffee", "the Truth", "the Final Mug"],
    'Reason': ["too many Emojis", "forgotten Passwords", "unexplained Silence", "the attempt to fly", "a missing Semicolon", "a faulty algorithm"]
})

for i in range(10):
    output = grammar.flatten('#origin#')
    print(f"{i+1}. {output}")
