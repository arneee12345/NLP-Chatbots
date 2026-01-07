# simple class to hold facts
class KnowledgeBase:
    def __init__(self):
        self.facts = {}
        self.secrets = {}

class Suspect:
    def __init__(self, id, name, bio, personality_style, knowledge, story_text, timeline, prefixes=None, suffixes=None, defense_statement="I didn't do it!", fallback_statement="I don't understand.", is_guilty=False):
        self.id = id
        self.name = name
        self.bio = bio
        self.personality_style = personality_style
        self.knowledge = knowledge
        
        # Timeline: {"19:00": "I was...", "20:00": "I went..."}
        self.timeline = timeline
        
        self.story_text = story_text
        
        # Lists for randomizing speech
        self.prefixes = prefixes if prefixes else []
        self.suffixes = suffixes if suffixes else []
        
        self.defense_statement = defense_statement
        self.fallback_statement = fallback_statement
        
        self.is_guilty = is_guilty
        
        # Used to remember what they said last (avoids repetition)
        self.last_match = None

    def __repr__(self):
        return f"<Suspect: {self.name}>"