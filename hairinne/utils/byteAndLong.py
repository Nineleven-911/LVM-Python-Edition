from hairinne.utils.Incomplete import incompleted


@incompleted
def toBytearray(a: int, range_: int = 8):
    res = bytearray()
    for i in range(range_):
        res.append((a >> i) & 0xFF)
    return res


print(toBytearray(0xF0_00_00_00_00_00_00_00))
