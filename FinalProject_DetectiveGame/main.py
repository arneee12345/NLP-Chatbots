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
from src.suspect_data import load_scenario
from src.nlp import DetectiveBrain  

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
    scenario_data = load_scenario()
    
    if not scenario_data:
        print("Critical Error: Could not load scenario data.")
        return

    # Unpack data from JSON
    suspects = scenario_data["suspects"]
    meta = scenario_data["meta"]
    outcomes = scenario_data["outcomes"]
    solution = meta["solution"]
    
    if len(suspects) < 3:
        print("Warning: Suspect data incomplete.")
    
    # Game State
    turns_left = 30
    score = 1000

    # Intro Screen
    clear_screen()
    if HAS_RICH:
        console.print(Panel.fit(f"[bold cyan]{meta['title']}[/bold cyan]", border_style="blue"))
        console.print(meta['intro_text'])
        console.print(f"\n[bold yellow]MISSION: Solve the case in {turns_left} turns.[/bold yellow]")
        console.print("[italic]Press Enter to enter the interrogation room...[/italic]")
    else:
        print(f"--- {meta['title']} ---")
        print(meta['intro_text'])
        print(f"\nMISSION: Solve the case in {turns_left} turns.")
        print("\nPress Enter to begin...")
        
    input() 
    
    # Main Game Loop
    while True:
        clear_screen()
        
        # Check Game Over
        if turns_left <= 0:
            if HAS_RICH:
                console.print(Panel(outcomes['timeout'], title="[bold red]GAME OVER[/bold red]", border_style="red"))
                console.print(f"Final Score: {score}")
            else:
                print("GAME OVER")
                print(outcomes['timeout'])
                print(f"Final Score: {score}")
            break

        can_accuse = turns_left <= 15
        # Display Menu
        if HAS_RICH:
            console.print(f"[bold yellow]TURNS: {turns_left} | SCORE: {score}[/bold yellow]")
            console.print("[bold]SUSPECT LIST:[/bold]")
            for i, s in enumerate(suspects):
                console.print(f"{i + 1}. {s.name}")
            
            if can_accuse:
                console.print("\n[dim]Options: Type number to talk, 'accuse' to solve, 'exit' to quit.[/dim]")
            else:
                console.print(f"\n[dim]Options: Type number to talk. (Accusation unlocks in {turns_left - 15} turns)[/dim]")
                
            choice = Prompt.ask("Selection")
        else:
            print(f"TURNS: {turns_left} | SCORE: {score}")
            print("SUSPECT LIST:")
            for i, s in enumerate(suspects):
                print(f"{i + 1}. {s.name}")
            
            if can_accuse:
                print("\nOptions: Type number to talk, 'accuse' to solve.")
            else:
                print(f"\nOptions: Type number to talk. (Accusation unlocks in {turns_left - 15} turns)")

            choice = input("\nSelection: ")
        
        # Exit
        if choice.lower() in ["exit", "quit"]:
            print("Case closed (Unsolved).")
            break
            
        # Accusation Logic
        if choice.lower() == "accuse":
            print("\nWHO IS THE KILLER?")
            guess = input("Type the name: ")
            
            # Check against solution
            if solution["killer"].lower() in guess.lower():
                score += 500  # Win Bonus
                
                # Determine Rank
                rank = "Rookie"
                if score > 1200: rank = "Master Detective"
                elif score > 800: rank = "Private Investigator"

                if HAS_RICH:
                    console.print(Panel(outcomes['success'], title="[bold green]CASE SOLVED[/bold green]", border_style="green"))
                    console.print(f"[bold yellow]FINAL SCORE: {score} ({rank})[/bold yellow]")
                else:
                    print("CASE SOLVED")
                    print(outcomes['success'])
                    print(f"FINAL SCORE: {score} ({rank})")
                
                print(f"Motive: {solution['motive']}")
                break
            else:
                score -= 300 # Wrong guess penalty
                if HAS_RICH:
                    console.print(Panel(outcomes['failure'], title="[bold red]WRONG ACCUSATION[/bold red]", border_style="red"))
                    console.print(f"[bold red]FINAL SCORE: {score}[/bold red]")
                else:
                    print("WRONG ACCUSATION")
                    print(outcomes['failure'])
                    print(f"FINAL SCORE: {score}")
                
                break # Game Ends on failure

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
            # Main loop handles the game over message
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