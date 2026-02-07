import json
import os
from .models import Suspect, KnowledgeBase

def load_scenario(filename="data/scenario_generated.json"):
    """
    Parses the JSON file and initializes Suspect objects.
    Defaults to scenario_generated.json.
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Scenario file not found at {file_path}")
        print("Make sure you run 'generate_story.py' first!")
        return None

    loaded_suspects = []

    for s_data in data["suspects"]:
        # Safety Check: Ensure sentences end with punctuation before joining
        # otherwise "I went home" + "I ate" becomes "I went home I ate" which confuses NLP.
        clean_sentences = []
        for s in s_data["knowledge_sentences"]:
            s = s.strip()
            if s and not s.endswith(('.', '!', '?')):
                s += "."
            clean_sentences.append(s)
            
        full_story_text = " ".join(clean_sentences)

        new_suspect = Suspect(
            id=s_data["id"],
            name=s_data["name"],
            bio=s_data["bio"],
            personality_style=s_data["personality_style"],
            knowledge=KnowledgeBase(), 
            story_text=full_story_text,
            timeline=s_data["timeline"],
            prefixes=s_data.get("prefixes", []),
            suffixes=s_data.get("suffixes", []),
            defense_statement=s_data["defense_statement"],
            fallback_statement=s_data["fallback_statement"],
            is_guilty=s_data.get("is_guilty", False)
        )
        
        new_suspect.last_match = None
        loaded_suspects.append(new_suspect)

    return {
        "meta": data.get("meta", {}),
        "outcomes": data.get("outcomes", {}),
        "suspects": loaded_suspects
    }