#!/usr/bin/python3
import os
import sys
import yaml
from yaml.scanner import ScannerError

from cook import cook_session
from recipe import InvalidRecipeError, Session

if __name__ == "__main__":
    try:
        recipe_name = sys.argv[1]
    except IndexError:
        print("You should specify a recipe!")
        sys.exit()

    try:
        with open(os.path.expanduser(f"~/.matemux/{recipe_name}.yml"), "r") as ymlfile:
            recipe = yaml.safe_load(ymlfile)
    except FileNotFoundError:
        print(f"{recipe_name}.yml not found!")
        sys.exit()
    except ScannerError:
        print(f"{recipe_name}.yml is not a valid .yml file!")
        sys.exit()


    try:
        session = Session(recipe)
    except InvalidRecipeError as e:
        print(e)
        sys.exit()

    cook_session(session)
