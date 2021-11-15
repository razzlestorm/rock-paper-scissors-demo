import sys

try:
    from app.game import run_menu
except ModuleNotFoundError:
    print("This program is meant to be run as a package, please move up"
          " one directory and try running it with 'python -m app' ")
    sys.exit()

if __name__ == "__main__":
    run_menu()
