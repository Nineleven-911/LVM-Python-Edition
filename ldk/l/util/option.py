class Options:
    def __init__(
            self,
            options: dict[str, int | str | bool | float],
            args: list[str],
            helps: dict[str, str]
    ):
        self.options = options
        self.args = args
        self.helps = helps

    def __contains__(self, name: str) -> bool:
        return self.options.__contains__(name)

    def contains(self, name: str):
        return self.__contains__(name)

    def get(self, name: str, clazz: type) -> type:
        return clazz(self.options.get(name))


class OptionsParser:
    def __init__(self, skip: bool = False):
        self.skip = skip
        self.flags2Name: dict[str, str] = {}
        self.name2Type: dict[str, type] = {}
        self.defaults: dict[str, int | str | bool | float] = {}
        self.helps: dict[str, str] = {}

    def add(
            self,
            flags: list[str],
            name: str,
            typ: type,
            default_value: int | str | bool | float = None,
            help_: str = ""
    ) -> "OptionsParser":
        for flag in flags:
            self.flags2Name[flag] = name
        self.name2Type[name] = typ
        self.defaults[name] = default_value
        self.helps[name] = help_
        return self

    def parse(self, args: list[str]) -> Options:
        options: dict[str, int | str | bool | float] = {}
        others: list[str] = []
        i = 0
        while i < len(args):
            arg = args[i]
            if arg not in self.flags2Name:
                others.append(arg)
                continue
            name = self.flags2Name[arg]
            typ = self.name2Type[name]
            if typ == bool:
                if i + 1 < len(args):
                    next_ = args[i + 1]
                    if next_ in ["true", "false"]:
                        options[name] = next_ == "true"
                        i += 1
                        break
                options[name] = True
            elif typ == str:
                if i + 1 < len(args):
                    options[name] = args[i + 1]
                    i += 1
                else:
                    raise ValueError(f"Missing argument for {name}")
            elif typ == int:
                if i + 1 < len(args):
                    options[name] = int(args[i + 1])
                    i += 1
                else:
                    raise ValueError(f"Missing argument for {name}")
            elif float:
                if i + 1 < len(args):
                    options[name] = float(args[i + 1])
                    i += 1
            if self.skip:
                break

        for i in range(i, len(args)):
            others.append(args[i])

        for name, value in self.defaults:
            if name not in options:
                options[name] = value
        return Options(options, others, self.helps)
