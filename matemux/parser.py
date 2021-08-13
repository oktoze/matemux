from typing import Dict


class ArgParser:
    def __init__(self, defaults: Dict[str, str], args: Dict[str, str]):
        self.__args = args.copy()

        default_set = set(defaults.keys())
        arg_set = set(args.keys())

        unprovided_args = default_set - arg_set

        for i in unprovided_args:
            self.__args[i] = defaults[i]

        self.__replacements = []
        for key, value in self.__args.items():
            pattern = "{{%s}}" % key
            replacement = "%s" % value
            self.__replacements.append({"pattern": pattern, "replacement": replacement})

    def parse(self, s: str):
        for r in self.__replacements:
            s = s.replace(r["pattern"], r["replacement"])

        return s
