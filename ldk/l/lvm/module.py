from hairinne.utils.Incomplete import incompleted
from hairinne.utils.byteAndLong import toBytearray, toLong, getFromEnd
LVM_VERSION = 0  # Range: long range ( 2^63-1=9223372036854775807 )



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

    def raw(self) -> bytearray:
        byte_buffer = bytearray()
        byte_buffer.extend([ord(i) for i in "lvme"])
        byte_buffer.extend(toBytearray(LVM_VERSION))
        byte_buffer.extend(toBytearray(len(self.text)))
        byte_buffer.extend(self.text)
        byte_buffer.extend(toBytearray(len(self.rodata)))
        byte_buffer.extend(self.rodata)
        byte_buffer.extend(toBytearray(len(self.data)))
        byte_buffer.extend(self.data)
        byte_buffer.extend(toBytearray(self.bssSectionLength))
        byte_buffer.extend(toBytearray(self.entrypoint))
        return byte_buffer

    @staticmethod
    def fromRaw(raw: bytearray) -> "Module":
        if getFromEnd(raw, 4) != [ord(i) for i in "lvme"]:
            raise Exception("Invalid module format")
        if toLong(getFromEnd(raw, 8)) > LVM_VERSION:
            raise Exception("Unsupported module version")
        textLength = toLong(getFromEnd(raw, 8))
        text = getFromEnd(raw, textLength)
        rodataLength = toLong(getFromEnd(raw, 8))
        rodata = getFromEnd(raw, rodataLength)
        dataLength = toLong(getFromEnd(raw, 8))
        data = getFromEnd(raw, dataLength)
        bssLength = toLong(getFromEnd(raw, 8))
        entrypoint = toLong(getFromEnd(raw, 8))
        return Module(text, rodata, data, bssLength, entrypoint)
