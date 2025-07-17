from enum import Enum


class Endian(Enum):
    LITTLE_ENDIAN = 0
    BIG_ENDIAN = 1


def toBytearray(
        a: int,
        range_: int = 8,
        endian: Endian = Endian.LITTLE_ENDIAN
) -> bytearray:
    res = bytearray()
    for i in range(range_):
        print(a)
        res.append((a >> (i * 8)) & 0xFF)
    return res if endian is Endian.LITTLE_ENDIAN else res[::-1]
