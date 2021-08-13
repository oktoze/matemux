#!/usr/bin/python3
import os
import sys
import yaml
from yaml.scanner import ScannerError

from matemux.cook import cook_session
from matemux.recipe import InvalidRecipeError, Session

MATEMUX_DIR = os.environ.get("MATEMUX_DIR", "~/.matemux")


def show_help():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f"{dir_path}/help.txt", "r") as helpfile:
        print("".join(helpfile.readlines()))


def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit()

    try:
        recipe_name = sys.argv[1]
    except IndexError:
        print("You should specify a recipe!")
        sys.exit()

    args = sys.argv[2:]
    try:
        args = args[args.index("--args") + 1 :]
    except ValueError:
        args = []

    args_dict = {}
    for i, a in enumerate(args[::2]):
        if len(args) > (2 * i + 1):
            if a.startswith("--"):
                args_dict[a[2:]] = args[2 * i + 1]

    try:
        with open(
            os.path.expanduser(f"{MATEMUX_DIR}/{recipe_name}.yml"), "r"
        ) as ymlfile:
            recipe = yaml.safe_load(ymlfile)
    except FileNotFoundError:
        print(f"{recipe_name}.yml not found!")
        sys.exit()
    except ScannerError:
        print(f"{recipe_name}.yml is not a valid .yml file!")
        sys.exit()

    try:
        session = Session(recipe, args_dict)
    except InvalidRecipeError as e:
        print(e)
        sys.exit()

    cook_session(session)


if __name__ == "__main__":
    main()
