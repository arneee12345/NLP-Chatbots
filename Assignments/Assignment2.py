import spacy
import tracery
from tracery.modifiers import base_english
import random
import sys
import time

# --- added a typing effect, because it looks better ---
def type_writer(text, speed=0.04):
    """
    Prints text one character at a time to simulate typing.
    Adjust 'speed' to make it faster (0.01) or slower (0.1).
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Forces the character to show up immediately
        time.sleep(speed)
    print() # Add a line break at the end

# --- loading spacy library and text ---
print("🔮 Gazing into the void (Loading spaCy)...")
nlp = spacy.load("en_core_web_md")

# Note for myself: using forward slashes to avoid errors (because in my explorer it shows backslashes)
file_path = "C:/Users/arne/Chatbots/NLP-Chatbots/texts/horoscope.txt"
text = open(file_path, encoding="utf-8", errors="ignore").read()
doc = nlp(text)

# --- banning some words, because of my lazy copying of the website texts ---
banned_words = [
    "horoscope", "daily", "weekly", "monthly", "november", "october", "december", 
    "2025", "2026", "astrotwins", "spiros", "halaris", "save", "article", 
    "advertisement", "reading", "continue", "week", "day", "year", "time",
    "bookmarks", "share", "options", "all"
]

# --- words ---

print("🔮 Harvesting stars and planets...")

adjectives = list(set([token.text.lower() for token in doc 
                       if token.pos_ == "ADJ" 
                       and token.is_alpha 
                       and token.text.lower() not in banned_words]))

nouns = list(set([token.text.lower() for token in doc 
                  if token.pos_ == "NOUN" 
                  and token.is_alpha 
                  and token.text.lower() not in banned_words]))

verbs = list(set([token.lemma_.lower() for token in doc 
                  if token.pos_ == "VERB" 
                  and token.is_alpha 
                  and token.text.lower() not in banned_words]))

# --- grammar ---
rules = {
    "origin": [
        "#prediction# #advice#",
        "#observation# #warning#",
        "#prediction# But #warning#",
        "The stars align: #prediction#"
    ],
    "prediction": [
        "The stars say you will #verb# a #adj# #noun#.",
        "Expect #adj.a# #noun# in your #noun#.",
        "A #adj# #noun# enters your #noun# zone.",
        "This cycle illuminates your #adj# #noun#."
    ],
    "observation": [
        "Your inner #noun# is feeling #adj# today.",
        "Mercury is in #noun#, so you might feel #adj#.",
        "The #noun# is in retrograde."
    ],
    "warning": [
        "Avoid #noun.s# at all costs.",
        "Do not #verb# with #adj# #noun.s#.",
        "Beware of the #adj# #noun#.",
        "Proceed with #noun#."
    ],
    "advice": [
        "Trust your #noun#.",
        "It is time to #verb# the #noun#.",
        "Focus on #adj# #noun.s#."
    ],
    "adj": adjectives,
    "noun": nouns,
    "verb": verbs
}

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)

# --- a little show before starting horoscope ---
type_writer("✨  CONNECTING TO THE COSMOS... FEELING THE COSMIC ENERGY  ✨", speed=0.05)
print("")

# output structure so there is not two "predictions" etc. makes duplication of sentence structure impossible
rules_outputs = ["origin", "prediction", "observation", "warning", "advice"]

for rule_name in rules_outputs:
    generated_text = grammar.flatten(f"#{rule_name}#")
    type_writer(f"🔮 {generated_text}")
    time.sleep(0.5) 
    print("")