import sys
import os

# "Safety first" imports - if rich isn't installed, we fall back to standard input/print
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("NOTE: Install 'rich' for better colors (pip install rich)")

# Custom modules
from src.suspect_data import load_suspects
from src.nlp import DetectiveBrain  # Changed from NLPProcessor
from src.story import INTRO_TEXT, CASE_TITLE, SOLUTION

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Setup console only if we have the library
    if HAS_RICH:
        console = Console()
    else:
        console = None
        
    # Initialize the "Brain" (Renamed from NLPProcessor)
    brain = DetectiveBrain()
    
    # 1. Load Data
    suspects = load_suspects()
    
    # Debug check
    if len(suspects) < 3:
        print("Warning: Suspects didn't load correctly.")
    
    # 2. Intro Screen
    clear_screen()
    if HAS_RICH:
        console.print(Panel.fit(f"[bold cyan]{CASE_TITLE}[/bold cyan]", border_style="blue"))
        console.print(INTRO_TEXT)
        console.print("\n[italic]Press Enter to enter the interrogation room...[/italic]")
    else:
        print(f"--- {CASE_TITLE} ---")
        print(INTRO_TEXT)
        print("\nPress Enter to begin...")
        
    input() 
    
    # 3. Main Game Loop
    while True:
        clear_screen()
        
        # Print menu
        if HAS_RICH:
            console.print("[bold]SUSPECT LIST:[/bold]")
            for i, s in enumerate(suspects):
                console.print(f"{i + 1}. {s.name}")
            console.print("\n[dim]Options: Type number to talk, 'accuse' to solve, 'exit' to quit.[/dim]")
            choice = Prompt.ask("Selection")
        else:
            print("SUSPECT LIST:")
            for i, s in enumerate(suspects):
                print(f"{i + 1}. {s.name}")
            choice = input("\nSelection (number/accuse/exit): ")

        # Handle Exit
        if choice.lower() in ["exit", "quit"]:
            print("Case closed (Unsolved).")
            break
            
        # Handle Accusation
        if choice.lower() == "accuse":
            print("\nWHO IS THE KILLER?")
            guess = input("Type the name: ")
            
            # Simple check against the solution in story.py
            if SOLUTION["killer"].lower() in guess.lower() or "julian" in guess.lower():
                if HAS_RICH:
                    console.print(f"\n[bold green]CORRECT! {SOLUTION['killer']} is guilty![/bold green]")
                else:
                    print(f"\nCORRECT! {SOLUTION['killer']} is guilty!")
                
                print(f"Motive: {SOLUTION['motive']}")
                break
            else:
                if HAS_RICH:
                    console.print("\n[bold red]WRONG![/bold red] The killer got away...")
                else:
                    print("\nWRONG! The killer got away...")
                break

        # Handle Suspect Selection
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(suspects):
                active_suspect = suspects[idx]
                interrogate_suspect(console, brain, active_suspect)
            else:
                print("Invalid number.")
                input("Press Enter...")
        else:
            print("Invalid input.")
            input("Press Enter...")

def interrogate_suspect(console, brain, suspect):
    # Sub-loop for talking to one specific person
    clear_screen()
    
    if HAS_RICH:
        console.print(f"[bold green]Interrogating: {suspect.name}[/bold green]")
        console.print(f"[dim]{suspect.bio}[/dim]")
        console.print("[italic]Type 'back' to return.[/italic]\n")
    else:
        print(f"Interrogating: {suspect.name}")
        print(f"Bio: {suspect.bio}")
        print("Type 'back' to return.\n")
    
    while True:
        if HAS_RICH:
            user_input = Prompt.ask(f"[bold cyan]Question[/bold cyan]")
        else:
            user_input = input("Question: ")
        
        if user_input.lower() in ["back", "return", "exit"]:
            break
            
        # Call the NLP logic (Updated method name: parse)
        response = brain.parse(user_input, suspect)
        
        if HAS_RICH:
            console.print(f"[bold blue]{suspect.name}[/bold blue]: {response}")
        else:
            print(f"{suspect.name}: {response}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Quit gracefully on Ctrl+C
        sys.exit(0)