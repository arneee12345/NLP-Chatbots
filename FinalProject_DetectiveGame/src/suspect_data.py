import json
import os
from .models import Suspect, KnowledgeBase

def load_suspects(filename="data/scenario_01.json"):
    """
    Parses the JSON scenario file and initializes Suspect objects.
    """
    # Construct absolute path to the data file
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Scenario file not found at {file_path}")
        return []

    loaded_suspects = []

    for s_data in data["suspects"]:
        # Join sentence list into a single text block for NLP vectorization
        full_story_text = " ".join(s_data["knowledge_sentences"])

        new_suspect = Suspect(
            id=s_data["id"],
            name=s_data["name"],
            bio=s_data["bio"],
            personality_style=s_data["personality_style"],
            knowledge=KnowledgeBase(), 
            story_text=full_story_text,
            timeline=s_data["timeline"],
            prefixes=s_data["prefixes"],
            suffixes=s_data["suffixes"],
            defense_statement=s_data["defense_statement"],
            fallback_statement=s_data["fallback_statement"],
            is_guilty=s_data.get("is_guilty", False)
        )
        
        new_suspect.last_match = None
        loaded_suspects.append(new_suspect)

    return loaded_suspects