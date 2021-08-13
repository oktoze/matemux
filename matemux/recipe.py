from os import path
from typing import List, Union

from matemux.parser import ArgParser


def validate_directory(dir: Union[str, None], field: str):
    if dir is not None and not path.isdir(path.expanduser(dir)):
        raise InvalidRecipeError(f"'{field}' contains invalid path: {dir}")


NoneType = type(None)

types_verbose = {
    str: "string",
    int: "integer",
    float: "float",
    dict: "dictionary",
    list: "list",
    bool: "boolean",
    NoneType: "none",
}


def assert_type(value: object, allowed_types: List[type], field: str):
    conditions = [isinstance(value, t) for t in allowed_types]

    if not any(conditions):
        types_len = len(allowed_types)

        if types_len == 1:
            err = f"'{field}' should be a {types_verbose[allowed_types[0]]}"
        elif types_len > 1:
            err = f"'{field}' should has one of the following types: {[types_verbose[t] for t in allowed_types]}"
        else:
            err = "no allowed type is specified"

        raise InvalidRecipeError(err)


def assert_dict_value_type(d: dict, allowed_types: List[type], field: str):
    for value in d.values():
        try:
            assert_type(value, allowed_types, "")
        except InvalidRecipeError:
            err = f"each value in '{field}' should be one of the following types: {[types_verbose[t] for t in allowed_types]}"
            raise InvalidRecipeError(err)


def assert_list_type(l: list, allowed_type: type, field: str):
    for item in l:
        if not isinstance(item, allowed_type):
            err = f"All items of '{field}' should be a {types_verbose[allowed_type]}"
            raise InvalidRecipeError(err)


class InvalidRecipeError(Exception):
    pass


class Pane:
    DEFAULT_PANE_RECIPE = {"root": None, "commands": [], "next-split-vertical": False}

    def __init__(self, recipe: dict):
        self.next_split_vertical = recipe.get("next-split-vertical", False)
        assert_type(self.next_split_vertical, [bool], "next-split-vertical")

        self.root = recipe.get("root", None)
        assert_type(self.root, [str, NoneType], "root")
        validate_directory(self.root, "root")

        self.commands = recipe.get("commands", [])
        assert_type(self.commands, [list], "commands")
        assert_list_type(self.commands, str, "commands")


class Window:
    DEFAULT_WINDOW_RECIPE = {
        "window": "0",
        "root": None,
        "commands": [],
        "focus": "0",
    }

    def __init__(self, recipe: dict):
        self.name = recipe.get("window", "")
        assert_type(self.name, [str, int], "window")
        self.name = str(self.name).replace(" ", "")

        self.root = recipe.get("root", None)
        validate_directory(self.root, "root")

        self.commands = recipe.get("commands", [])
        assert_type(self.commands, [list], "commands")
        assert_list_type(self.commands, str, "commands")

        pane_recipes = recipe.get("panes", [Pane.DEFAULT_PANE_RECIPE.copy()])
        self.panes = [Pane(r) for r in pane_recipes]

        self.focus = recipe.get("focus", "0")
        assert_type(self.focus, [str, int], "focus")
        self.focus = str(self.focus).replace(" ", "")


class Session:
    def __init__(self, recipe: dict, args: dict):
        self.name = recipe.get("session", "")
        assert_type(self.name, [str, int], "session")
        self.name = str(self.name).replace(" ", "")

        self.root = recipe.get("root", "~")
        validate_directory(self.root, "root")

        defaults = recipe.get("defaults", {})
        assert_type(defaults, [dict], "defaults")
        assert_dict_value_type(defaults, [str, int, float], "defaults")

        self.arg_parser = ArgParser(defaults, args)

        self.commands = recipe.get("commands", [])
        assert_type(self.commands, [list], "commands")
        assert_list_type(self.commands, str, "commands")

        windows_recipes = recipe.get("windows", [Window.DEFAULT_WINDOW_RECIPE.copy()])
        self.windows = [Window(r) for r in windows_recipes]

        self.focus = recipe.get("focus", "0")
        assert_type(self.focus, [str, int], "focus")
        self.focus = str(self.focus).replace(" ", "")

        self.parse_commands()

    def parse_commands(self):
        self.commands = [self.arg_parser.parse(c) for c in self.commands]

        for w in self.windows:
            w.commands = [self.arg_parser.parse(c) for c in w.commands]

            for p in w.panes:
                p.commands = [self.arg_parser.parse(c) for c in p.commands]
