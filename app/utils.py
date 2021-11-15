import configparser
from operator import attrgetter
from pathlib import Path
import types
from typing import List

from app.game_objects import Thrown, Score
from app.texts import rules, enhanced_rules


def generate_scores(conf: dict, hi_score: Score) -> List[Score]:
    scores = []
    for v in conf.values():
        if v:
            v = v.split("-")
            scores.append(Score(v[0].strip(), int(v[1])))
    scores.append(hi_score)
    scores = sorted(scores, key=attrgetter('points'), reverse=True)[:10]
    return scores


def print_rules() -> None:
    print(rules)


def print_enhanced_rules() -> None:
    print(enhanced_rules)


def print_leaderboard() -> None:
    """Prints the leaderboard as it is currently found in the config.ini"""
    config = configparser.ConfigParser()
    config_path = Path('app', 'config.ini')
    config.read(config_path)
    lb = config['LEADERBOARD']
    if len(lb) == 0:
        print("\n" * 5)
        print("Unfortunately, there isn't anyone on the leaderboard yet.")
        print("\n" * 5)
    else:
        print("\nLEADERBOARD:\n")
        # sorts the leaderboard dict by highest values first
        for k, v in lb.items():
            print(f"{k}: {v}")
        print("\n")


def validate_game_input(input: str, rules: dict) -> Thrown:
    """Attempts to interpret the player's game input as best it can
    and return the dict key that corresponds to the player's input.

    Args:
        input: the player input, as a string.
        rules: the dictionary of game objects to reference.

    Returns:
        A Thrown class if the player's game input is valid; False otherwise.
    """
    error_message = "Sorry, I didn't understand that input, " \
                    "try one of the following inputs:\n" \
                    f"{', '.join([v.name for v in rules.values()])}.\n" \
                    "You can also type 'q' to quit."

    names_checklist = [str(n.name).lower() for n in rules.values()]
    if input not in names_checklist and input not in rules.keys():
        print(error_message)
        return False
    else:
        try:
            choice = rules.get(input[0])
        except KeyError:
            print(error_message)
            return False
    return choice


def validate_menu_input(input: str, rules: dict) -> types.FunctionType:
    """Attempts to interpret the player's menu input as best it can
    and return the dict key that corresponds to the player's input.

    Args:
        input: the player input, as a string.
        rules: the dictionary of game objects to reference.

    Returns:
        True if no exceptions occur; False otherwise.
    """
    error_message = "Sorry, I didn't understand that input, " \
                    "try one of the following inputs:\n" \
                    f"{', '.join([k for k in rules.keys()])}.\n" \
                    "You can also type 'q' to quit."
    checklist = ['start', 'read', 'check', 'rules']
    if len(input) > 0:
        if input in checklist or input in rules.keys():
            choice = rules.get(input[0], error_message)
        else:
            print(error_message)
            return False
    else:
        print("Type one of the options, or 'q' to quit.")
        return False
    try:
        return choice()
    except TypeError:
        print(choice)
        return False
