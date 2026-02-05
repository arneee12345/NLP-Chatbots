import sys
import os

# Rich for better terminal UI
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("NOTE: Install 'rich' for better colors (pip install rich)")

# Project modules
from src.suspect_data import load_suspects
from src.nlp import DetectiveBrain  
from src.story import INTRO_TEXT, CASE_TITLE, SOLUTION

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    if HAS_RICH:
        console = Console()
    else:
        console = None
        
    # Initialize NLP engine
    brain = DetectiveBrain()
    
    # Load Scenario Data
    suspects = load_suspects()
    
    if len(suspects) < 3:
        print("Warning: Suspect data incomplete.")
    
    # Game State
    turns_left = 30
    score = 1000

    # Intro Screen
    clear_screen()
    if HAS_RICH:
        console.print(Panel.fit(f"[bold cyan]{CASE_TITLE}[/bold cyan]", border_style="blue"))
        console.print(INTRO_TEXT)
        console.print(f"\n[bold yellow]MISSION: Solve the case in {turns_left} turns.[/bold yellow]")
        console.print("[italic]Press Enter to enter the interrogation room...[/italic]")
    else:
        print(f"--- {CASE_TITLE} ---")
        print(INTRO_TEXT)
        print(f"\nMISSION: Solve the case in {turns_left} turns.")
        print("\nPress Enter to begin...")
        
    input() 
    
    # Main Game Loop
    while True:
        clear_screen()
        
        # Check Game Over
        if turns_left <= 0:
            if HAS_RICH:
                console.print("[bold red]GAME OVER: You ran out of time![/bold red]")
                console.print(f"Final Score: {score}")
            else:
                print("GAME OVER: You ran out of time!")
                print(f"Final Score: {score}")
            break

        # Display Menu
        if HAS_RICH:
            console.print(f"[bold yellow]TURNS: {turns_left} | SCORE: {score}[/bold yellow]")
            console.print("[bold]SUSPECT LIST:[/bold]")
            for i, s in enumerate(suspects):
                console.print(f"{i + 1}. {s.name}")
            console.print("\n[dim]Options: Type number to talk, 'accuse' to solve, 'exit' to quit.[/dim]")
            choice = Prompt.ask("Selection")
        else:
            print(f"TURNS: {turns_left} | SCORE: {score}")
            print("SUSPECT LIST:")
            for i, s in enumerate(suspects):
                print(f"{i + 1}. {s.name}")
            choice = input("\nSelection (number/accuse/exit): ")

        # Exit
        if choice.lower() in ["exit", "quit"]:
            print("Case closed (Unsolved).")
            break
            
        # Accusation Logic
        if choice.lower() == "accuse":
            print("\nWHO IS THE KILLER?")
            guess = input("Type the name: ")
            
            # Check against solution
            if SOLUTION["killer"].lower() in guess.lower() or "julian" in guess.lower():
                score += 500  # Win Bonus
                
                # Determine Rank
                rank = "Rookie"
                if score > 1200: rank = "Master Detective"
                elif score > 800: rank = "Private Investigator"

                if HAS_RICH:
                    console.print(f"\n[bold green]CORRECT! {SOLUTION['killer']} is guilty![/bold green]")
                    console.print(f"[bold yellow]FINAL SCORE: {score} ({rank})[/bold yellow]")
                else:
                    print(f"\nCORRECT! {SOLUTION['killer']} is guilty!")
                    print(f"FINAL SCORE: {score} ({rank})")
                
                print(f"Motive: {SOLUTION['motive']}")
                break
            else:
                score -= 300 # Wrong guess penalty
                if HAS_RICH:
                    console.print("\n[bold red]WRONG! The killer got away...[/bold red] [-300 Points]")
                else:
                    print("\nWRONG! The killer got away... [-300 Points]")
                input("Press Enter...")
                # We continue loop if turns are left

        # Select Suspect
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(suspects):
                active_suspect = suspects[idx]
                # Pass stats IN, get stats OUT
                turns_left, score = interrogate_suspect(console, brain, active_suspect, turns_left, score)
            else:
                print("Invalid number.")
                input("Press Enter...")
        else:
            # Handles non-digit inputs that aren't exit/accuse
            if choice.lower() not in ["accuse", "exit", "quit"]:
                print("Invalid input.")
                input("Press Enter...")

def interrogate_suspect(console, brain, suspect, turns_left, score):
    clear_screen()
    
    if HAS_RICH:
        console.print(f"[bold green]Interrogating: {suspect.name}[/bold green]")
        console.print(f"[dim]{suspect.bio}[/dim]")
        console.print(f"[bold yellow]Turns Left: {turns_left} | Score: {score}[/bold yellow]")
        console.print("[italic]Type 'back' to return.[/italic]\n")
    else:
        print(f"Interrogating: {suspect.name}")
        print(f"Bio: {suspect.bio}")
        print(f"Turns: {turns_left} | Score: {score}")
        print("Type 'back' to return.\n")
    
    while True:
        # Force exit if out of turns
        if turns_left <= 0:
            if HAS_RICH:
                console.print("\n[bold red]TIME IS UP! The police are here.[/bold red]")
            else:
                print("\nTIME IS UP! The police are here.")
            input("Press Enter...")
            break

        if HAS_RICH:
            user_input = Prompt.ask(f"[bold cyan]Question ({turns_left} left)[/bold cyan]")
        else:
            user_input = input(f"Question ({turns_left} left): ")
        
        if user_input.lower() in ["back", "return", "exit"]:
            break

        # Cost per question
        turns_left -= 1
        score -= 10

        # Willingness to talk logic
        insults = ["idiot", "stupid", "dumb", "liar", "shut up", "ugly", "crazy"]
        user_lower = user_input.lower()

        is_pure_insult = any(word in user_lower for word in insults)
        is_accusation = ("you" in user_lower) and any(verb in user_lower for verb in ["kill", "murder", "stab", "do it"])

        if is_pure_insult or is_accusation:
            suspect.decrease_willingness(15)
            score -= 50 # Insult penalty
            if HAS_RICH:
                if is_accusation:
                    console.print(f"[bold red]! {suspect.name} gets defensive at the accusation.[/bold red] (Willingness: {suspect.willingness}%)")
                else:
                    console.print(f"[bold red]! {suspect.name} is offended by your language.[/bold red] (Willingness: {suspect.willingness}%)")
                console.print("[red][-50 Points][/red]")
            else:
                print(f"! {suspect.name} looks offended. (Willingness: {suspect.willingness}%)")
                print("[-50 Points]")
        
        # Check Refusal
        if suspect.willingness <= 0:
            if HAS_RICH:
                console.print(Panel(f"[red]{suspect.name}:[/red] I am done talking to you. Get out of my face!"))
            else:
                print(f"{suspect.name}: I am done talking to you. Get out of my face!")
            continue 
            
        # Low Willingness Warning
        if suspect.willingness < 40 and suspect.willingness > 0:
            if HAS_RICH:
                console.print(f"[italic dim]({suspect.name} seems reluctant to answer...)[/italic dim]")
            else:
                print(f"({suspect.name} seems reluctant to answer...)")

        # Process NLP
        response = brain.parse(user_input, suspect)
        
        if HAS_RICH:
            console.print(f"[bold blue]{suspect.name}[/bold blue]: {response}")
        else:
            print(f"{suspect.name}: {response}")

    return turns_left, score

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)