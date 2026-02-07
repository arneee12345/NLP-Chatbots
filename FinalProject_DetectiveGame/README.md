# 🕵️ Detective Game

> **Project Title:** An NLP-Driven Murder Mystery  
> **Course:** As We May Speak: From NLP to Chatbot

## 📝 Project Description

This is an interactive text-based murder mystery game that explores the potential of Natural Language Processing (NLP) in narrative gaming. Unlike traditional adventure games that rely on rigid, pre-defined dialogue trees (where players just select A, B, or C), this project utilizes the `spaCy` library to allow players to interrogate suspects using open-ended natural language questions.

**The Evolution:**
While the initial prototype relied on hardcoded scenarios, the final version has evolved into an **Infinite Mystery Engine**.

* **The Writer (Generative AI):** The system now uses the Google Gemini API to generate unique murder cases, suspects, and clues on the fly.
* **The Detective (Local NLP):** Once the story is generated, the game switches to a local NLP engine (spaCy) to handle the gameplay loop.

The core technical challenge was implementing the **cosine similarity** that matches user input against this generated knowledge base. This allows the game to understand the *intent* of a question (e.g., matching "Where were you?" with "I was in the garden") rather than relying on exact string matching. I also integrated the `Rich` library for terminal visualization to make the user experience more immersive.

---

## ⚙️ Installation

### 1. Prerequisites
Ensure you have **Python 3.9** or higher installed on your system.

### 2. Install Dependencies
Navigate to the project folder and run:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

### 3. API Configuration
To use the generator feature (creating new mysteries), you need a Google Gemini API Key.

1.  Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Start the game (see "How to Run" below).
3.  When you select **"Generate NEW Mystery"**, the game will ask you to paste your key. It will be saved securely for future sessions.

*(If you do not have a key, you can still play the last generated case in "Offline Mode".)*

## 📚 Detailed Documentation
For a comprehensive breakdown of the development process and the logic sketch please see the project folder: **docs**.

## 🚀 How to Run

To start the investigation, simply run the main script:

```bash
python main.py
```

**First Time Setup:**
If this is your first time generating a story, the terminal will prompt you to enter your **API Key**. Simply paste it when asked.

You will now see a Start Menu where you can choose to:
* **Play Current Mystery** (Load the existing save file).
* **Generate NEW Mystery** (Create a brand new case from a theme).

## 🔍 Detective's Handbook (How to Play)

You will act as the detective. You can type open-ended questions to the suspects. However, keep in mind that the suspects are sensitive to specific topics.

### 1. Interrogation Guide
The NLP engine focuses on keywords and intent.

* **Be Specific:** Instead of "What happened?", ask "What happened at 9 PM?"
* **Focus on Nouns:** The suspects respond best to physical evidence or people mentioned in their bios.
* **Try asking about:** "Money", "Weapon", "Argument", "Motive", or specific names found in the story.
* **Cross-Reference:** Ask suspects about each other.
    * *Example:* "Do you like [Suspect Name]?" or "What do you think of [Victim Name]?"

### 2. The Mechanics
* **Repetition:** If a suspect repeats themselves, they likely don't know more about that specific topic. Try changing the subject.
* **Defensiveness:** If you accuse them (e.g., "Did you kill him?"), they will get defensive. If you insult them, their "Willingness" to talk will drop.
* **Alibis:** Pay close attention to times (e.g., 6 PM vs 9 PM). One timeline usually doesn't add up.

### 3. Solving the Case
When you think you know the truth:

1.  Type `back` or `exit` to return to the main menu.
2.  Select `accuse`.
3.  Enter the name of the killer.

## 🛠️ Tech Stack

* **Python:** Core logic and game loop management.
* **Google Gemini (GenAI):** Dynamic generation of narratives, characters, and logic structure.
* **spaCy:** Natural Language Processing (Tokenization, Lemmatization, Cosine Similarity, NLU, Intent Analysis) for dialogue matching.
* **Rich:** Library for terminal formatting, colors, and panels to create an immersive UI.

## 🤖 Statement on AI Usage

I used AI tools in the following capacity for this project:

* **Coding Assistance:** AI was sometimes used to debug (especially with the API Integration) and help formatting the code nicely.
* **Core Feature:** The project explicitly uses Generative AI (Gemini API) as a feature to create the story content dynamically.
* **Documentation:** AI assisted in formatting this README and structuring the documentation for clarity.