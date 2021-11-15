"""These are are where the rules of the game are defined, meaning where
each of the various Thrown options are mapped to each other, to define
which are stronger and which are weaker.
"""

from app.game_objects import Thrown

rock = Thrown("Rock",
              {"Lizard": "crushes",
               "Scissors": "crushes"})
paper = Thrown("Paper",
               {"Rock": "covers",
                "Spock": "disproves"})
scissors = Thrown("Scissors",
                  {"Paper": "cuts",
                   "Lizard": "decapitates"})
lizard = Thrown("Lizard",
                {"Paper": "eats",
                 "Spock": "poisons"})
spock = Thrown("Spock",
               {"Scissors": "smashes",
                "Rock": "vaporizes"})

vanilla_table = {"r": rock,
                 "p": paper,
                 "s": scissors}

enhanced_table = {"l": lizard,
                  "k": spock}
