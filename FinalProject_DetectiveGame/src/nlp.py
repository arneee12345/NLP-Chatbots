import spacy
import random
import re
from .models import Suspect

class DetectiveBrain:
    def __init__(self):
        print("Loading brain... please wait.")
        # I am using the medium model because the small one was too dumb
        # Make sure to run: python -m spacy download en_core_web_md
        self.nlp = spacy.load("en_core_web_md")

        self.threshold = 0.35 

        self.greetings = ["hi", "hello", "hey", "greetings", "yo", "morning", "evening"]
        
        # words that trigger defensive mode
        self.accusations = ["kill", "murder", "guilty", "arrest", "confess", "stab", "poison", "hurt", "harm", "shoot", "did you do it"]

        # TODO: Add more weapon synonyms later if needed
        self.synonyms = {
            # Actions
            "do": ["doing", "action", "activity", "working", "busy"], 
            "doing": ["working", "busy", "polishing", "waiting", "setting"],
            "where": ["kitchen", "garden", "club", "downtown", "study", "office", "room", "sapphire", "outside", "hallway"],
            "been": ["kitchen", "garden", "club", "downtown", "study", "office", "room", "sapphire", "outside"],
            
            # Motives
            "motive": ["pension", "inheritance", "money", "debt", "merger", "business", "reason", "pay", "gambling", "share"],
            "reason": ["pension", "inheritance", "money", "debt", "merger", "business", "share"],
            "why": ["pension", "inheritance", "money", "debt", "merger", "business", "share", "shark", "harmless", "wreck", "disaster", "reckless"],
            "think": ["shark", "company", "harmless", "stealing", "wine", "disaster", "furious", "wreck", "nervous", "reckless", "terrifying", "cold", "annoying", "suspects", "others", "julian", "veronica"],
            
            # Emotions
            "angry": ["shouting", "yelling", "argued", "furious", "disagreement", "negotiation", "spirited", "temper", "cruel"],
            "argument": ["shouting", "yelling", "argued", "furious", "disagreement", "cruel"],
            
            # Witnessing
            "see": ["saw", "witnessed", "noticed", "look", "anyone", "empty", "quiet"],
            "saw": ["witnessed", "noticed", "look", "anyone", "empty", "quiet"],
            "anyone": ["julian", "veronica", "alfred", "suspects", "else", "someone", "people"],
            
            # Money stuff
            "money": ["pension", "inheritance", "cash", "paid", "wealth", "fortune", "debt", "gambling", "offshore", "accounts"],
            "debt": ["gambling", "owe", "money", "cash", "bad", "people"],
            
            # Weapon
            "weapon": ["knife", "gun", "opener", "poison", "object", "item", "jade", "handle", "sharp", "objects"],
            "kill": ["harm", "hurt", "murder", "dead", "died", "violent", "killed", "reckless", "temper", "shark", "cruel"],
            
            # Time / Event
            "happened": ["found", "dead", "body", "scene", "study", "dreadful", "scream", "9"],
            "when": ["9", "pm", "evening", "scream", "found", "time"], 
            "body": ["master", "dead", "corpse", "scene", "study", "dreadful", "slumped"],
            
            # People
            "alfred": ["wine", "stealing", "harmless", "annoying", "twitchy", "butler", "wreck", "nervous", "pension"],
            "butler": ["wine", "stealing", "harmless", "annoying", "twitchy", "alfred", "wreck", "nervous", "pension"],
            "veronica": ["shark", "company", "merger", "partner", "furious", "yelling", "cold", "terrifying"],
            "partner": ["shark", "company", "merger", "veronica", "furious", "cold", "terrifying"],
            "julian": ["heir", "son", "gambling", "debt", "club", "disaster", "temper", "reckless", "shouting"],
            
            # Blame
            "who": ["killer", "murderer", "guilty", "suspect", "julian", "veronica", "alfred", "someone", "anyone"],
            "killer": ["shark", "company", "stealing", "harmless", "innocent", "suspect", "temper", "julian", "veronica"], 
            
            # Clues
            "silver": ["polishing", "kitchen", "cutlery"],
            "smoke": ["cigarette", "garden", "break", "habit"],
            "club": ["sapphire", "bar", "drinking", "downtown", "alibi"],
            "files": ["offshore", "accounts", "merger", "records"],
        }

    def get_time(self, text):
        # looks for regex numbers
        match = re.search(r'\b(6|7|8|9|10|11|12|18|19|20|21|22|23|0|00)\b', text)
        if match:
            num = int(match.group(1))
            if num == 6 or num == 18: return "18:00"
            if num == 7 or num == 19: return "19:00"
            if num == 8 or num == 20: return "20:00"
            if num == 9 or num == 21: return "21:00"
            if num == 10 or num == 22: return "22:00"
            if num == 11 or num == 23: return "23:00"
            if num == 12 or num == 0 or num == 00: return "00:00"
        
        # manual mapping
        if "8:30" in text or "eight thirty" in text: return "20:30"
        if "8:45" in text or "eight forty" in text: return "20:45"
        if "earlier" in text: return "18:00"
        if "later" in text: return "22:00"
        return None

    def parse(self, msg, suspect):
        # main parsing function
        doc = self.nlp(msg.lower().strip())
        
        # 1. Check for time
        t = self.get_time(msg)
        if t and t in suspect.timeline:
            return self.build_response(suspect.timeline[t], suspect)

        # 2. Greetings (NOW CHECKS FOR REPETITION)
        if doc[0].text in self.greetings:
             if suspect.last_match == "greeting":
                 suspect.decrease_willingness(10) # Smaller penalty for saying hi
                 return f"(Annoyed) We have established that. Ask your questions."
             
             suspect.last_match = "greeting"
             return f"({suspect.personality_style.replace('_', ' ')}) I am listening."

        # 3. Accusations
        accused = False
        for token in doc:
            if token.lemma_ in self.accusations:
                if "you" in msg.lower() or "did you" in msg.lower():
                    accused = True
        
        if "killer" in msg.lower() and "you" in msg.lower():
             accused = True
             
        # If they ask "who", they aren't accusing the person they are talking to
        if "who" in msg.lower():
            accused = False

        if "where" in msg.lower() or "when" in msg.lower() or "time" in msg.lower():
            accused = False

        if accused:
             return f"(Defensively) {suspect.defense_statement}"

        # 4. Check story
        if suspect.story_text:
            return self.check_story(doc, suspect)
        
        return f"({suspect.personality_style.replace('_', ' ')}) {suspect.fallback_statement}"

    def check_story(self, doc, suspect):
        best_sent = None
        best_score = 0.0

        story = self.nlp(suspect.story_text)
        
        q_lemmas = []
        # keep these words even if they are stop words
        keep = ["i", "you", "he", "she", "who", "what", "where", "doing", "anyone", "else", "think", "kill", "killed"]
        
        for t in doc:
            if not t.is_stop or t.text in keep:
                if not t.is_punct:
                    q_lemmas.append(t.lemma_)
        
        search_terms = set(q_lemmas)
        for lemma in q_lemmas:
            if lemma in self.synonyms:
                search_terms.update(self.synonyms[lemma])

        for sent in story.sents:
            score = doc.similarity(sent)
            s_lemmas = [t.lemma_ for t in sent]
            matches = 0
            
            # check for keyword matches
            for term in search_terms:
                if term in s_lemmas:
                    matches += 1
            
            # boost score if keywords match
            if matches > 0:
                score += (matches * 3.0) 

            # print(f"DEBUG: {sent.text[:20]}... Score: {score}")

            if score > best_score:
                best_score = score
                best_sent = sent.text

        # check for repetition loop
        last = getattr(suspect, "last_match", None)

        if best_score > self.threshold and best_sent:
            
            if best_sent == last:
                
                annoyed_phrases = [
                    "I already answered that!", 
                    "Are you not listening? I am not repeating myself.", 
                    "I told you already!", 
                    "Do not waste my time with the same questions."
                ]
                
                # Return ONLY the refusal
                return f"(Annoyed) {random.choice(annoyed_phrases)}"
            
            suspect.last_match = best_sent
            return self.build_response(best_sent, suspect)
        
        return f"({suspect.personality_style.replace('_', ' ')}) {suspect.fallback_statement}"

    def build_response(self, text, suspect):
        # adds flavor text to the response
        prefix = ""
        if suspect.prefixes and random.random() > 0.5:
            prefix = random.choice(suspect.prefixes) + " "
        suffix = ""
        if suspect.suffixes and random.random() > 0.5:
            suffix = " " + random.choice(suspect.suffixes)
        
        if text and suffix and text.endswith("."):
            text = text[:-1]
            
        return f"{prefix}{text}{suffix}"