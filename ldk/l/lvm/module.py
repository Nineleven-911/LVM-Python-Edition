from hairinne.utils.Incomplete import incompleted
from hairinne.utils.byteAndLong import toBytearray
from ldk.l.lvm.vm import VirtualMachine


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
        byte_buffer = bytearray()
        byte_buffer.extend([ord(i) for i in "lvme"])
        byte_buffer.extend(toBytearray(VirtualMachine.LVM_VERSION))
        byte_buffer.extend(toBytearray(len(self.text)))
