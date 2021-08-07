class InvalidRecipeError(Exception):
    pass


default_pane_recipe = {
    "root": None,
    "commands": [],
    "next-split-vertical": False
}

default_window_recipe = {
    "window": "0",
    "root": None,
    "commands": [],
    "focus": "0",
    "panes": []
}

class Pane:
    def __init__(self, recipe: dict):
        self.next_split_vertical = recipe.get("next-split-vertical", False)

        self.root = recipe.get("root", None)
        if self.root is not None and not isinstance(self.root, str):
            raise InvalidRecipeError("'root' should be a string")

        self.commands = recipe.get("commands", [])
        if not isinstance(self.commands, list):
            raise InvalidRecipeError("'commands' should be a list")
        if len([m for m in self.commands if not isinstance(m, str)]):
            raise InvalidRecipeError("'commands' should be all strings")

class Window:
    def __init__(self, recipe: dict):
        self.name = recipe.get("window", "")
        if not isinstance(self.name, str):
            raise InvalidRecipeError("'window' should be a string")

        self.root = recipe.get("root", None)
        if self.root is not None and not isinstance(self.root, str):
            raise InvalidRecipeError("'root' should be a string")

        self.commands = recipe.get("commands", [])
        if not isinstance(self.commands, list):
            raise InvalidRecipeError("'commands' should be a list")
        if len([m for m in self.commands if not isinstance(m, str)]):
            raise InvalidRecipeError("'commands' should be all strings")

        pane_recipes = recipe.get("panes", [default_pane_recipe.copy()])
        self.panes = [Pane(r) for r in pane_recipes]

        self.focus = recipe.get("focus", "0")
        if not isinstance(self.focus, str):
            raise InvalidRecipeError("'focus' should be a string")

class Session:
    def __init__(self, recipe: dict):
        self.name = recipe.get("session", "")
        if not isinstance(self.name, str):
            raise InvalidRecipeError("'session' should be a string")

        self.root = recipe.get("root", "~")
        if not isinstance(self.root, str):
            raise InvalidRecipeError("'root' should be a string")

        self.commands = recipe.get("commands", [])
        if not isinstance(self.commands, list):
            raise InvalidRecipeError("'commands' should be a list")
        if len([m for m in self.commands if not isinstance(m, str)]):
            raise InvalidRecipeError("'commands' should be all strings")

        windows_recipes = recipe.get("windows", [default_window_recipe])
        self.windows = [Window(r) for r in windows_recipes]

        self.focus = recipe.get("focus", self.windows[0].name)
        if not isinstance(self.focus, str):
            raise InvalidRecipeError("'focus' should be a string")
