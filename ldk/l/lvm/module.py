from hairinne.utils.Incomplete import incompleted


class Module:
    def __init__(
            self,
            text: bytes,
            rodata: bytes,
            data: bytes,
            bssSectionLength: int,
            entrypoint: int
    ):
        self.text = text
        self.rodata = rodata
        self.data = data
        self.bssSectionLength = bssSectionLength
        self.entrypoint = entrypoint

    @incompleted
    def raw(self):
        pass

Module(0,0,0,0,0).raw()
