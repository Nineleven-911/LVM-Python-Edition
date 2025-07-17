import sys

from ldk.l.util.option import (
    OptionsParser, Options
)

from ldk.l.lvm.vm import (
    VirtualMachine
)

void = None
DEFAULT_STACK_SIZE = 4194304


def getOptionsParser() -> OptionsParser:
    return (OptionsParser()
            .add(["--help", "-h"], "help", bool, False)
            .add(["--version", "-v"], "version", bool, False)
            .add(["--verbose", "-verbose"], "verbose", bool, False)
            .add(["--stackSize", "--s"], "stackSize", int, DEFAULT_STACK_SIZE)
            )


def main(args: list[str]) -> void:
    options = getOptionsParser().parse(args)
    virtual_machine = VirtualMachine()


if __name__ == '__main__':
    main(sys.argv)
