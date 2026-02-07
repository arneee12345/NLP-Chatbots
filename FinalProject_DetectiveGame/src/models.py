class KnowledgeBase:
    def __init__(self):
        self.facts = {}

class Suspect:
    def __init__(self, id, name, bio, personality_style, knowledge, story_text, timeline, prefixes, suffixes, defense_statement, fallback_statement, is_guilty=False):
        self.id = id
        self.name = name
        self.bio = bio
        self.personality_style = personality_style
        self.knowledge = knowledge
        self.story_text = story_text
        self.timeline = timeline
        self.prefixes = prefixes
        self.suffixes = suffixes
        self.defense_statement = defense_statement
        self.fallback_statement = fallback_statement
        self.is_guilty = is_guilty
        
        # Game State
        self.last_match = None
        self.willingness = 100  # Starts at 100%

    def decrease_willingness(self, amount):
        """Reduces willingness score, clamping it at 0."""
        self.willingness -= amount
        if self.willingness < 0:
            self.willingness = 0

    def __repr__(self):
        return f"<Suspect: {self.name}>"