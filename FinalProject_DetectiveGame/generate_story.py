import os
import json
from google import genai
from google.genai import types

# configuration
API_KEY = "AIzaSyDnXjr2H9jLtt-jHRfYg2Sekv-56wcWp_g" 

OUTPUT_FILE = "data/scenario_generated.json"

# ai generated system prompt (by Google Gemini - giving it my project idea including all the code I wrote):
SYSTEM_PROMPT = """
You are a Lead Narrative Designer for a detective game. 
Your job is to generate a solvable murder mystery in strict JSON format.

THE RULES:
1. The setting must be a contained environment (e.g., a train, a mansion, a moon base, a yacht).
2. There must be exactly 3 suspects.
3. One suspect must be 'is_guilty': true.
4. The 'knowledge_sentences' are CRITICAL. They must contain keywords about:
   - Where they were (locations)
   - Who they saw (witnessing)
   - Motives (money, love, revenge)
   - The weapon (if they know about it)
5. Timelines must use "HH:00" format (18:00 to 00:00).
6. Do not include markdown formatting (like ```json). Just return the raw JSON string.

THE JSON STRUCTURE MUST MATCH THIS EXACTLY:
{
  "meta": {
    "title": "String (Creative Title)",
    "intro_text": "String (The backstory and setting)",
    "solution": {
      "killer": "String (Name of killer)",
      "motive": "String (Why they did it)"
    }
  },
  "outcomes": {
    "success": "String (What happens when player wins)",
    "failure": "String (What happens when player accuses wrong person)",
    "timeout": "String (What happens when time runs out)"
  },
  "suspects": [
    {
      "id": "unique_id",
      "name": "String (Full Name)",
      "bio": "String (Short description)",
      "personality_style": "String (e.g., nervous, arrogant, cold, drunk)",
      "is_guilty": Boolean,
      "knowledge_sentences": [
        "String (Fact 1)",
        "String (Fact 2 - Alibi)",
        "String (Fact 3 - Clue about others)",
        ... (Give them 8-10 sentences each)
      ],
      "timeline": {
        "18:00": "String (Where were they?)",
        "19:00": "String",
        "20:00": "String",
        "21:00": "String",
        "22:00": "String",
        "23:00": "String",
        "00:00": "String"
      },
      "prefixes": ["String", "String"],
      "suffixes": ["String", "String"],
      "defense_statement": "String (What they say if accused)",
      "fallback_statement": "String (Generic 'I dont know' response)"
    }
  ]
}
"""

import time

def generate_mystery(theme: str):
    """
    Calls Gemini API to generate the JSON content.
    """
    print(f"🕵️  Asking the AI to write a mystery about: '{theme}'...")
    print("⏳  This may take 10-20 seconds...")

    client = genai.Client(api_key=API_KEY)
    
    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash-001"]
    
    for model_name in models_to_try:
        try:
            print(f"   ... Attempting with model: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=f"{SYSTEM_PROMPT}\n\nTHEME REQUEST: {theme}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)

        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print("   ⚠️  Model is busy (Quota Limit). Waiting 60 seconds to retry...")
                time.sleep(60)
                # Try one more time with the same model
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=f"{SYSTEM_PROMPT}\n\nTHEME REQUEST: {theme}",
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json"
                        )
                    )
                    return json.loads(response.text)
                except:
                    print(f"   ❌  Retry failed. Moving to next model...")
                    continue
            elif "404" in error_msg:
                 print(f"   ❌  Model {model_name} not found. Trying next...")
                 continue
            else:
                print(f"\n❌ Unexpected Error: {e}")
                return None
    
    return None

def save_scenario(data):
    if not data:
        print("❌ Error: No data to save.")
        return
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ SUCCESS! New mystery saved to: {OUTPUT_FILE}")
    print(f"📜 Title: \"{data['meta']['title']}\"")
    
    print("\n" + "="*40)
    print("      🎮  HOW TO PLAY YOUR MYSTERY  🎮")
    print("="*40)
    print("1. The scenario is ready. DO NOT open the JSON file")
    print("   (unless you want to spoil the solution!).")
    print("\n2. Run your game engine to start playing:")
    print("   > python main.py") 
    print("="*40 + "\n")



if __name__ == "__main__":
    print("--- MYSTERY GENERATOR ---")
    user_theme = input("Enter a theme (or press Enter for 'Cyberpunk Space Station'): ")
    
    if not user_theme.strip():
        user_theme = "A murder on a Cyberpunk Space Station in the year 2099"
        
    scenario_data = generate_mystery(user_theme)
    save_scenario(scenario_data)