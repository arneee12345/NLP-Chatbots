import spacy
import random
import re
from .models import Suspect

class DetectiveBrain:
    def __init__(self):
        print("Loading brain... please wait.")
        # Ensure you run: python -m spacy download en_core_web_md
        try:
            self.nlp = spacy.load("en_core_web_md")
        except OSError:
            print("⚠️ Model not found. Downloading 'en_core_web_md'...")
            from spacy.cli import download
            download("en_core_web_md")
            self.nlp = spacy.load("en_core_web_md")

        self.threshold = 0.35 

        self.greetings = ["hi", "hello", "hey", "greetings", "yo", "morning", "evening"]
        
        # Words that trigger defensive mode
        self.accusations = ["kill", "murder", "guilty", "arrest", "confess", "stab", "poison", "hurt", "harm", "shoot", "did you do it"]

        # generic synonyms 
        self.synonyms = {
            # Actions
            "do": ["doing", "action", "activity", "working", "busy"], 
            "doing": ["working", "busy", "waiting", "setting", "preparing"],
            "where": ["location", "place", "room", "spot", "area", "scene"],
            
            # Motives
            "motive": ["money", "revenge", "love", "debt", "business", "reason", "benefit", "will", "inheritance"],
            "reason": ["motive", "why", "explanation", "cause"],
            "money": ["cash", "debt", "paid", "wealth", "fortune", "gambling", "inheritance", "accounts", "funds", "payment"],
            
            # Emotions/Conflict
            "angry": ["shouting", "yelling", "argued", "furious", "disagreement", "fight", "conflict", "mad", "upset"],
            "fight": ["argument", "disagreement", "struggle", "yelling", "clash"],
            
            # Witnessing
            "see": ["saw", "witnessed", "noticed", "look", "anyone", "observe", "spot"],
            "saw": ["witnessed", "noticed", "look", "anyone", "observed"],
            
            # Weapon/Crime
            "weapon": ["gun", "knife", "poison", "object", "item", "tool", "murder weapon", "blade"],
            "kill": ["harm", "hurt", "murder", "dead", "died", "violent", "killed", "attack"],
            "body": ["victim", "dead", "corpse", "scene", "murder"],
            
            # Time
            "when": ["time", "hour", "moment", "long", "ago"],
            "happened": ["occurred", "took place", "event", "incident"]
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
            if num == 12 or num == 0: return "00:00"
        
        # manual mapping
        if "8:30" in text or "eight thirty" in text: return "20:30"
        if "8:45" in text or "eight forty" in text: return "20:45"
        if "earlier" in text: return "18:00"
        if "later" in text: return "22:00"
        return None

    def parse(self, msg, suspect):
        doc = self.nlp(msg.lower().strip())
        
        # 1. Check for time queries
        t = self.get_time(msg)
        if t and t in suspect.timeline:
            return self.build_response(suspect.timeline[t], suspect)

        # 2. Greetings
        if len(doc) > 0 and doc[0].text in self.greetings:
             if suspect.last_match == "greeting":
                 suspect.decrease_willingness(10)
                 return f"(Annoyed) We have established that. Ask your questions."
             
             suspect.last_match = "greeting"
             return f"({suspect.personality_style.replace('_', ' ')}) I am listening."

        # 3. Accusations
        accused = False
        for token in doc:
            if token.lemma_ in self.accusations:
                # Only accuse if they say "you" or imply the listener is the subject
                if "you" in msg.lower() or "did you" in msg.lower():
                    accused = True
        
        if "killer" in msg.lower() and "you" in msg.lower():
             accused = True
             
        # "Who" usually asks for a third party, not an accusation of the listener
        if "who" in msg.lower():
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
            
            for term in search_terms:
                if term in s_lemmas:
                    matches += 1
            
            if matches > 0:
                score += (matches * 3.0) 

            if score > best_score:
                best_score = score
                best_sent = sent.text

        last = getattr(suspect, "last_match", None)

        if best_score > self.threshold and best_sent:
            
            if best_sent == last:
                annoyed_phrases = [
                    "I already answered that!", 
                    "Are you not listening? I am not repeating myself.", 
                    "I told you already!", 
                    "Do not waste my time with the same questions."
                ]
                return f"(Annoyed) {random.choice(annoyed_phrases)}"
            
            suspect.last_match = best_sent
            return self.build_response(best_sent, suspect)
        
        return f"({suspect.personality_style.replace('_', ' ')}) {suspect.fallback_statement}"

    def build_response(self, text, suspect):
        prefix = ""
        if suspect.prefixes and random.random() > 0.5:
            prefix = random.choice(suspect.prefixes) + " "
        suffix = ""
        if suspect.suffixes and random.random() > 0.5:
            suffix = " " + random.choice(suspect.suffixes)
        
        if text and suffix and text.endswith("."):
            text = text[:-1]
            
        return f"{prefix}{text}{suffix}"