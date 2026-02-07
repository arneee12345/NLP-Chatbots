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
from src.generator import generate_mystery, save_scenario

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu(console):
    """
    Handles the startup choice.
    Returns True if a valid scenario exists and we should play.
    Returns False (or exits) if the user quits.
    """
    while True:
        clear_screen()
        if HAS_RICH:
            console.print(Panel.fit("[bold magenta]🕵️  AI DETECTIVE ENGINE[/bold magenta]", border_style="magenta"))
        else:
            print("--- AI DETECTIVE ENGINE ---")

        has_save = os.path.exists("data/scenario_generated.json")
        
        # --- RENDER MENU ---
        if HAS_RICH:
            if has_save:
                console.print("1. [bold green]Play Current Mystery[/bold green]")
                console.print("2. [bold cyan]Generate NEW Mystery[/bold cyan]")
            else:
                console.print("[dim]No mystery found. You must generate one.[/dim]")
                console.print("1. [bold cyan]Generate NEW Mystery[/bold cyan]")
            
            console.print("3. Exit")
            choice = Prompt.ask("\nSelection")
        else:
            if has_save:
                print("1. Play Current Mystery")
                print("2. Generate NEW Mystery")
            else:
                print("1. Generate NEW Mystery")
            print("3. Exit")
            choice = input("\nSelection: ")

        # --- HANDLE SELECTION ---
        if choice == "3" or (choice.lower() == "exit"):
            sys.exit(0)

        is_generating_new = (has_save and choice == "2") or (not has_save and choice == "1")
        is_playing_existing = (has_save and choice == "1")

        # GENERATE NEW
        if is_generating_new:
            if HAS_RICH:
                console.print("\n[bold cyan]🎭 Create Your Mystery[/bold cyan]")
                theme = Prompt.ask("[yellow]Enter a theme, setting, or era[/yellow] (or press [bold]Enter[/bold] for a random surprise)")
            else:
                print("\n--- Create Your Mystery ---")
                theme = input("Enter a theme, setting, or era (or press Enter for a random surprise): ")
            
            if not theme.strip():
                print("🎲 No theme selected... choosing a random one!")
                theme = "A murder mystery with a unique, randomly selected theme and setting."
            
            try:
                data = generate_mystery(theme)
                if save_scenario(data):
                    input("\nScenario saved! Press Enter to start the case...")
                    return True 
                else:
                    input("\n❌ Save failed. Press Enter to try again...")
                    continue
            except Exception as e:
                print(f"\n❌ Generation Error: {e}")
                input("Press Enter to return to menu...")
                continue

        # PLAY EXISTING
        if is_playing_existing:
            return True 

def interrogate_suspect(console, brain, suspect, turns_left, score):
    """
    Handles the loop of questioning a single suspect.
    Returns updated (turns_left, score).
    """
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
        if turns_left <= 0:
            break

        if HAS_RICH:
            user_input = Prompt.ask(f"[bold cyan]Question[/bold cyan]")
        else:
            user_input = input(f"Question: ")
        
        if user_input.lower() in ["back", "return", "exit", ""]:
            break

        turns_left -= 1
        score -= 10

        # Insult check
        insults = ["idiot", "stupid", "dumb", "liar", "shut up", "ugly", "crazy", "fuck", "shit"]
        user_lower = user_input.lower()
        is_pure_insult = any(word in user_lower for word in insults)
        
        if is_pure_insult:
            suspect.decrease_willingness(15)
            score -= 50
            msg = f"! {suspect.name} is offended by your language."
            if HAS_RICH:
                console.print(f"[bold red]{msg}[/bold red]")
            else:
                print(msg)
        
        if suspect.willingness <= 0:
            msg = f"{suspect.name}: I am done talking to you."
            if HAS_RICH:
                console.print(Panel(f"[red]{msg}[/red]"))
            else:
                print(msg)
            continue 
            
        response = brain.parse(user_input, suspect)
        
        if HAS_RICH:
            console.print(f"[bold blue]{suspect.name}[/bold blue]: {response}")
            console.print(f"[dim](Turns: {turns_left})[/dim]")
        else:
            print(f"{suspect.name}: {response}")
            print(f"(Turns: {turns_left})")

    return turns_left, score

def main():
    if HAS_RICH:
        console = Console()
    else:
        console = None
        
    if not main_menu(console):
        return
    
    # Initialize Game
    clear_screen()
    print("Initializing Detective AI System...")
    
    try:
        brain = DetectiveBrain()
    except Exception as e:
        print(f"\nCRITICAL ERROR: Could not load NLP model. {e}")
        print("Make sure you ran: python -m spacy download en_core_web_md")
        return

    scenario_data = load_scenario("data/scenario_generated.json")
    if not scenario_data:
        print("\n❌ FAILED: No generated story found.")
        return

    suspects = scenario_data["suspects"]
    meta = scenario_data["meta"]
    outcomes = scenario_data["outcomes"]
    solution = meta["solution"]
    
    START_TURNS = 30
    turns_left = START_TURNS
    score = 1000

    # Intro
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
        
        if turns_left <= 0:
            if HAS_RICH:
                console.print(Panel(outcomes['timeout'], title="[bold red]GAME OVER[/bold red]", border_style="red"))
                console.print(f"Final Score: {score}")
            else:
                print("GAME OVER")
                print(outcomes['timeout'])
                print(f"Final Score: {score}")
            break

        # lock logic
        can_accuse = turns_left <= (START_TURNS - 10)
        turns_until_unlock = turns_left - (START_TURNS - 10)
        
        # Display Menu
        if HAS_RICH:
            console.print(f"[bold yellow]TURNS: {turns_left} | SCORE: {score}[/bold yellow]")
            console.print("[bold]SUSPECT LIST:[/bold]")
            for i, s in enumerate(suspects):
                console.print(f"{i + 1}. {s.name}")
            
            if can_accuse:
                console.print("\n[dim]Options: Type number to talk, 'accuse' to solve, 'exit' to quit.[/dim]")
            else:
                console.print(f"\n[dim]Options: Type number to talk. (Accusation unlocks in {turns_until_unlock} turns)[/dim]")
            
            choice = Prompt.ask("Selection")
        else:
            print(f"TURNS: {turns_left} | SCORE: {score}")
            print("SUSPECT LIST:")
            for i, s in enumerate(suspects):
                print(f"{i + 1}. {s.name}")
            
            if can_accuse:
                print("\nOptions: Type number to talk, 'accuse' to solve.")
            else:
                print(f"\nOptions: Type number to talk. (Accusation unlocks in {turns_until_unlock} turns)")

            choice = input("\nSelection: ")
        
        # HANDLE INPUT
        if choice.lower() in ["exit", "quit"]:
            print("Case closed (Unsolved).")
            break
            
        if choice.lower() == "accuse":
            if not can_accuse:
                print(f"\n❌ You need to gather more evidence! Come back in {turns_until_unlock} turns.")
                input("Press Enter...")
                continue
                
            print("\nWHO IS THE KILLER?")
            guess = input("Type the name: ")
            
            if solution["killer"].lower() in guess.lower():
                score += 500
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
                
                print(f"\nMotive: {solution['motive']}")
                break
            else:
                score -= 300 
                if HAS_RICH:
                    console.print(Panel(outcomes['failure'], title="[bold red]WRONG ACCUSATION[/bold red]", border_style="red"))
                    console.print(f"[bold red]FINAL SCORE: {score}[/bold red]")
                else:
                    print("WRONG ACCUSATION")
                    print(outcomes['failure'])
                    print(f"FINAL SCORE: {score}")
                break 

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(suspects):
                active_suspect = suspects[idx]
                turns_left, score = interrogate_suspect(console, brain, active_suspect, turns_left, score)
            else:
                print("Invalid number.")
                input("Press Enter...")
        else:
            if choice.lower() not in ["accuse", "exit", "quit"]:
                print("Invalid input.")
                input("Press Enter...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)