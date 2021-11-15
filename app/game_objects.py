from random import choice
from typing import Dict, NamedTuple

# Added to spice things up!
COLORS = [
    "\u001b[31m",  # Red
    "\u001b[32m",  # Green
    "\u001b[33m",  # Yellow
    "\u001b[34m",  # Blue
    "\u001b[35m",  # Magenta
    "\u001b[36m",  # Cyan
]
ENDC = "\033[0m"


class Thrown:
    """
    Objects a user will 'throw' for the game (rock, paper, scissors, etc).

    ...

    Attributes
    ----------
    name : str
        The name of the Thrown object.
    strong_vs : dict[str, str]
        The other Thrown objects that self beats, written as the other Thrown's
        name followed by the verb that self performs when beating it, i.e.:
        Thrown("Paper", {"Rock": "covers"}) for "Paper covers Rock".
    """
    def __init__(self, name: str, strong_vs: Dict[str, str]) -> None:
        self.name = name
        self.strong_vs = strong_vs

    def describe(self, key: str):
        """
        Describes the result of the round,
        adding a random color to the action text.
        """
        print(f"{self.name} {choice(COLORS)}{self.strong_vs[key]}{ENDC} {key}!")

    def battle(self, opponent):
        """
        Compares self vs. another Thrown object and determines the winner.

        Returns
        -------
        result: tuple
        """
        # self wins
        if opponent.name in self.strong_vs:
            self.describe(opponent.name)
            return (1, 0)
        # opponent wins
        elif self.name in opponent.strong_vs:
            opponent.describe(self.name)
            return (0, 1)
        # else tie
        else:
            print("You tie!")
            return (0, 0)


class Score(NamedTuple):
    name: str
    points: int

    def __str__(self):
        return f"{self.name} - {self.points}"
