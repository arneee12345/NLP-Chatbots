# 🕵️ Detective Game

> **Project Title:** An NLP-Driven Murder Mystery
> **Course:** As We May Speak: From NLP to Chatbot

## 📝 Project Description
This is an interactive text-based murder mystery game that explores the potential of Natural Language Processing (NLP) in narrative gaming. Unlike traditional adventure games that rely on rigid, pre-defined dialogue trees (where players just select A, B, or C), this project utilizes the `spaCy` library to allow players to interrogate suspects using open-ended natural language questions.

The core technical challenge was implementing a **cosine similarity algorithm** that matches user input against a predefined knowledge base. This allows the game to understand the *intent* of a question (e.g., matching "Where were you?" with "I was in the garden") rather than relying on exact string matching. The game features three suspects. The Nervous Butler, the Arrogant Heir, and the Cold Partner. Each with unique linguistic patterns and alibis. I also integrated the `Rich` library for a the terminal visualization to make the user experience a little more game like.

---

## ⚙️ Installation

### 1. Prerequisites
Ensure you have **Python 3.9** or higher installed on your system.

### 2. Install Dependencies
Navigate to the project folder and run:
```bash
pip install -r requirements.txt
```

### 3. Download the Language Brain
This project uses spaCy's medium English model (`en_core_web_md`) for vector similarity. You **must** run this command for the game to work:
```bash
python -m spacy download en_core_web_md
```

## 🚀 How to Run
To start the investigation, simply run the main script:

```bash
python FinalProject_DetectiveGame/main.py
```

## 🔍 Detective's Handbook (How to Play)
You will act as the detective. You can type open-ended questions to the suspects. However, keep in mind that the suspects are sensitive to specific topics.

### 1. Interrogation Guide
The NLP engine focuses on keywords and intent.

* **Be Specific:** Instead of "What happened?", ask "What happened at 9 PM?"
* **Focus on Nouns:** The suspects respond best to physical evidence or people.
    * Try asking about: "Money", "Weapon", "Argument", "Study", "Garden".
* **Cross-Reference:** Ask suspects about each other.
    * Example: "Do you like Julian?" or "What do you think of Veronica?"

### 2. The Mechanics
* **Repetition:** If a suspect repeats themselves, they likely don't know more about that specific topic. Try changing the subject.
* **Defensiveness:** If you accuse them (e.g., "Did you kill him?"), they will get defensive and deny everything.
* **Alibis:** Pay close attention to times (6 PM vs 9 PM). One timeline doesn't add up.

### 3. Solving the Case
When you think you know the truth:

1. Type `back` or `exit` to return to the main menu.
2. Type `accuse`.
3. Enter the name of the killer.

## 🛠️ Tech Stack
* **Python:** Core logic and game loop management.
* **spaCy:** Natural Language Processing (Tokenization, Lemmatization, Cosine Similarity) for dialogue matching.
* **Rich:** Library for terminal formatting, colors, and panels to create an immersive UI.