import configparser
import logging
from pathlib import Path
import random
import sys
from time import sleep

from app.game_objects import Score
from app.rule_mappings import vanilla_table, enhanced_table
from app.texts import (basic_game_text, enhanced_game_text,
                       greeting_text, menu_text)
from app.utils import (generate_scores, print_leaderboard,
                       print_enhanced_rules, print_rules, validate_game_input,
                       validate_menu_input)

# read in from configs
config_path = Path('app', 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

# logging
logging.basicConfig(level=logging.INFO,
                    filename=Path('app', 'logs', 'results.log'),
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('player_input')


# defining some printing helpers
OPEN_WRAP = '\n--------------------'
CLOSE_WRAP = '--------------------\n\n'


def run_menu():
    """
    Provides an interface for player to interact
    with the leaderboard and rules.

    Options
    -------

    run_game: enters the main game logic loop.
    print_leaderboard: displays the leaderboard as found in the config.ini.
    print_rules: displays either the basic or enhanced version of the rules.
    quit_game: exits the game.
    """
    menu = {
        's': run_game,
        'c': print_leaderboard,
        'r': print_rules,
        'q': quit_game
    }
    print(greeting_text)
    while True:
        if config['UNLOCKABLES'].getboolean('enhanced'):
            menu['r'] = print_enhanced_rules
        print(menu_text)
        try:
            player_in = input().lower().strip()
            print(OPEN_WRAP)
            validate_menu_input(player_in, menu)
            print(CLOSE_WRAP)
        except KeyError:
            continue


def run_game():
    """
    Provides an interface for the player to interact with the game. "q" can be
    typed at any time to return to the main menu. When trying to quit, this
    function will prompt the player to enter their name to record their score.
    """
    game = True
    # initializes rules
    ruleset = vanilla_table
    game_text = basic_game_text
    # initializes player and computer score
    SCORES = {
        "player_1": 0,
        "player_2": 0
        }
    print("Welcome! Let's get started!")
    while game:
        if (SCORES['player_1'] == config['UNLOCKABLES'].getint('threshhold')
           and not config['UNLOCKABLES'].getboolean('enhanced')):
            config['UNLOCKABLES']['enhanced'] = "1"
            print("\n", OPEN_WRAP)
            print("This must be too easy! Let's take it to the next level!")
            print_enhanced_rules()
            print(CLOSE_WRAP, "\n")
            sleep(2)
        if config['UNLOCKABLES'].getboolean('enhanced'):
            ruleset.update(enhanced_table)
            game_text = enhanced_game_text
        try:
            player2_input = ruleset[random.choice(list(ruleset.keys()))]
            print(game_text)
            player_input = input().lower().strip()
            if player_input[0] == 'q':
                if input("Are you sure you want to quit? "
                         "Type 'q' again to confirm.\n").lower() == "q":
                    game = False
                    quit_to_menu(SCORES)
                else:
                    continue
            throw = validate_game_input(player_input, ruleset)
            try:
                print(OPEN_WRAP)
                print("You throw: ", throw.name)
                print("AI throws: ", player2_input.name)
                score1, score2 = throw.battle(player2_input)
                SCORES['player_1'] += score1
                SCORES['player_2'] += score2
                logger.info(f"Player: {throw.name}, AI: {player2_input.name}")
                print(CLOSE_WRAP)
                print("SCORES:")
                print(f"Player 1: {SCORES['player_1']}")
                print(f"Player 2: {SCORES['player_2']}")
            # validate_game_input has returned False
            except AttributeError:
                continue
        # incorrect inputs or empty inputs
        except (KeyError, IndexError):
            print("Sorry, I didn't understand that input.")
            print("Type 'q' to quit at any time.")
            continue


# revise this function to create a new score row regardless
# possibly with a Score object?


def quit_to_menu(scores: dict) -> None:
    name = input("Please type your name to save your score!\n")
    hi_score = Score("AI", scores['player_2']) if not name else \
        Score(name, scores['player_1'])

    scores = generate_scores(config['LEADERBOARD'], hi_score)
    config['LEADERBOARD'] = dict(zip(range(1, len(scores)+1), scores))
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    print_leaderboard()
    run_menu()


def quit_game() -> None:
    print("Thanks for playing!")
    sys.exit()
