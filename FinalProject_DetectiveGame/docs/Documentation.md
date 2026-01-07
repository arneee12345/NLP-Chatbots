# 📂 Project Documentation

## 1. Project Concept & Ideas
My initial idea was to gamify the chatbot experience. Instead of a standard Q&A bot, I wanted to create a non-linear narrative where the user acts as a detective in a murder mystery and asks questions to different bots (suspects) to find out who the killer is. 

**The Core Idea:**
"The Detective Game" is a twist on the board game *Cluedo*. My goal was to use NLP to bridge the gap of understanding the *intent* rather than just the words.

## 2. Development Process
I chose a modular architecture to separate the story data from the logic processing.

* **Phase 1: The Data Structure:** I started by writing the backstories. I created a `Suspect` class to hold not just the name and basic information, but a dictionary of "Knowledge" and a "Timeline." This allowed me to map specific times (e.g., "19:00") to specific alibis.
* **Phase 2: The Logic (spaCy):** I implemented `en_core_web_md` because I needed vector similarity. I wrote a script to compare the user's input vector against the suspect's known sentences.
* **Phase 3: The UI:** I added the `Rich` library late in the process because the standard terminal output felt kinda dry. The panels and colors help the user distinguish between the "Narrator" and the "Suspects."

## 3. Reflection & Challenges
* **Challenge:** Handling "Who" questions. Initially, asking "Who killed him?" would trigger defensive responses because the model detected the word "kill" (which is usually an accusation).
* **Solution:** I added logic to detect interrogative pronouns. If the user asks "Who", the bot knows it is an inquiry, not an accusation.
* **Challenge:** It was difficult to write enough content to cover every possible user question, without the bot being confused or answering in the wrong context.
* **Solution:** I implemented a "Fallback" system and a "Keyword Boost." If the vector score is low, but a specific keyword (like "money") is present, the system forces a relevant response.

## 4. References
* **spaCy Documentation:** https://spacy.io/usage/vectors-similarity (Used for the cosine similarity logic).
* **Rich Library:** https://rich.readthedocs.io/ (Used for terminal UI).
* **Course Materials**

## 5. Sketches
![Logic Flowchart](Game_Logic.jpg)
Game Logic