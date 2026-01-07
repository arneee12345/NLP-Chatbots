# Game constants and story text

CASE_TITLE = "The Silent Estate"

# Using rich tags for colors
INTRO_TEXT = """
[bold yellow]CASE FILE #892: THE SILENT ESTATE[/bold yellow]

[bold]VICTIM:[/bold] Lord Arthur Hetherington (Age 68)
[bold]LOCATION:[/bold] Hetherington Manor, The Study
[bold]TIME OF DEATH:[/bold] Between 8:00 PM and 10:00 PM last night.
[bold]CAUSE:[/bold] Blunt force trauma / Stab wound (Unclear).

[bold]BRIEFING:[/bold]
Lord Hetherington was found dead in his study. The storm outside has trapped everyone 
in the manor. You have arrived just in time. The local police are stuck 
on the other side of the collapsed bridge.

There are [bold]3 suspects[/bold] currently being held in the library. 
They all have secrets. Only one is the killer.

Your goal:
1. Interrogate the suspects.
2. Find inconsistencies in their stories.
3. Type [bold red]'accuse'[/bold red] when you know who did it.
"""

# The correct solution used for validation
SOLUTION = {
    "killer": "Julian The Heir",
    "motive": "Gambling debts and impatience for inheritance.",
    "weapon": "The antique letter opener (hidden in Veronica's bag, but planted there)."
}