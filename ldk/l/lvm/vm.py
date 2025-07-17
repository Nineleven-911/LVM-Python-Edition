import struct
import sys
import threading
from enum import IntFlag
from typing import Optional

from hairinne.utils.Incomplete import incompleted
from ldk.l.lvm.module import Module


class ByteCode:
    # 标志位常量
    ZERO_MARK = 0b01
    CARRY_MARK = 0b10
    UNSIGNED_MARK = 0b100

    # 寄存器编号常量
    PC_REGISTER = 39
    SP_REGISTER = 38
    BP_REGISTER = 37

    # 类型大小常量
    BYTE_TYPE = 0
    SHORT_TYPE = 1
    INT_TYPE = 2
    LONG_TYPE = 3

    # 线程控制指令
    TC_STOP = 0  # TC = Thread Control
    TC_WAIT = 1
    TC_GET_REGISTER = 2
    TC_SET_REGISTER = 3

    # 指令码定义
    NOP = 0x00
    PUSH_1 = 0x01
    PUSH_2 = 0x02
    PUSH_4 = 0x03
    PUSH_8 = 0x04
    POP_1 = 0x05
    POP_2 = 0x06
    POP_4 = 0x07
    POP_8 = 0x08
    LOAD_1 = 0x09
    LOAD_2 = 0x0a
    LOAD_4 = 0x0b
    LOAD_8 = 0x0c
    STORE_1 = 0x0d
    STORE_2 = 0x0e
    STORE_4 = 0x0f
    STORE_8 = 0x10
    CMP = 0x11
    ATOMIC_CMP = 0x12
    MOV_E = 0x13
    MOV_NE = 0x14
    MOV_L = 0x15
    MOV_LE = 0x16
    MOV_G = 0x17
    MOV_GE = 0x18
    MOV_UL = 0x19
    MOV_ULE = 0x1a
    MOV_UG = 0x1b
    MOV_UGE = 0x1c
    MOV = 0x1d
    MOV_IMMEDIATE1 = 0x1e
    MOV_IMMEDIATE2 = 0x1f
    MOV_IMMEDIATE4 = 0x20
    MOV_IMMEDIATE8 = 0x21
    JUMP = 0x22
    JUMP_IMMEDIATE = 0x23
    JE = 0x24
    JNE = 0x25
    JL = 0x26
    JLE = 0x27
    JG = 0x28
    JGE = 0x29
    JUL = 0x2a
    JULE = 0x2b
    JUG = 0x2c
    JUGE = 0x2d
    MALLOC = 0x2e
    FREE = 0x2f
    REALLOC = 0x30
    ADD = 0x31
    SUB = 0x32
    MUL = 0x33
    DIV = 0x34
    MOD = 0x35
    AND = 0x36
    OR = 0x37
    XOR = 0x38
    NOT = 0x39
    NEG = 0x3a
    SHL = 0x3b
    SHR = 0x3c
    USHR = 0x3d
    INC = 0x3e
    DEC = 0x3f
    ADD_DOUBLE = 0x40
    SUB_DOUBLE = 0x41
    MUL_DOUBLE = 0x42
    DIV_DOUBLE = 0x43
    MOD_DOUBLE = 0x44
    ADD_FLOAT = 0x45
    SUB_FLOAT = 0x46
    MUL_FLOAT = 0x47
    DIV_FLOAT = 0x48
    MOD_FLOAT = 0x49
    ATOMIC_ADD = 0x4a
    ATOMIC_SUB = 0x4b
    ATOMIC_MUL = 0x4c
    ATOMIC_DIV = 0x4d
    ATOMIC_MOD = 0x4e
    ATOMIC_AND = 0x4f
    ATOMIC_OR = 0x50
    ATOMIC_XOR = 0x51
    ATOMIC_NOT = 0x52
    ATOMIC_NEG = 0x53
    ATOMIC_SHL = 0x54
    ATOMIC_SHR = 0x55
    ATOMIC_USHR = 0x56
    ATOMIC_INC = 0x57
    ATOMIC_DEC = 0x58
    ATOMIC_ADD_DOUBLE = 0x59
    ATOMIC_SUB_DOUBLE = 0x5a
    ATOMIC_MUL_DOUBLE = 0x5b
    ATOMIC_DIV_DOUBLE = 0x5c
    ATOMIC_MOD_DOUBLE = 0x5d
    ATOMIC_ADD_FLOAT = 0x5e
    ATOMIC_SUB_FLOAT = 0x5f
    ATOMIC_MUL_FLOAT = 0x60
    ATOMIC_DIV_FLOAT = 0x61
    ATOMIC_MOD_FLOAT = 0x62
    CAS = 0x63
    INVOKE = 0x64
    INVOKE_IMMEDIATE = 0x65
    RETURN = 0x66
    GET_RESULT = 0x67
    SET_RESULT = 0x68
    TYPE_CAST = 0x69
    LONG_TO_DOUBLE = 0x6a
    DOUBLE_TO_LONG = 0x6b
    DOUBLE_TO_FLOAT = 0x6c
    FLOAT_TO_DOUBLE = 0x6d
    OPEN = 0x6e
    CLOSE = 0x6f
    READ = 0x70
    WRITE = 0x71
    CREATE_FRAME = 0x72
    DESTROY_FRAME = 0x73
    EXIT = 0x74
    EXIT_IMMEDIATE = 0x75
    GET_FIELD_ADDRESS = 0x76
    GET_LOCAL_ADDRESS = 0x77
    GET_PARAMETER_ADDRESS = 0x78
    CREATE_THREAD = 0x79
    THREAD_CONTROL = 0x7a

    instruction_names = {
        NOP: "NOP",
        PUSH_1: "PUSH_1",
        PUSH_2: "PUSH_2",
        PUSH_4: "PUSH_4",
        PUSH_8: "PUSH_8",
        POP_1: "POP_1",
        POP_2: "POP_2",
        POP_4: "POP_4",
        POP_8: "POP_8",
        LOAD_1: "LOAD_1",
        LOAD_2: "LOAD_2",
        LOAD_4: "LOAD_4",
        LOAD_8: "LOAD_8",
        STORE_1: "STORE_1",
        STORE_2: "STORE_2",
        STORE_4: "STORE_4",
        STORE_8: "STORE_8",
        CMP: "CMP",
        ATOMIC_CMP: "ATOMIC_CMP",
        MOV_E: "MOV_E",
        MOV_NE: "MOV_NE",
        MOV_L: "MOV_L",
        MOV_LE: "MOV_LE",
        MOV_G: "MOV_G",
        MOV_GE: "MOV_GE",
        MOV_UL: "MOV_UL",
        MOV_ULE: "MOV_ULE",
        MOV_UG: "MOV_UG",
        MOV_UGE: "MOV_UGE",
        MOV: "MOV",
        MOV_IMMEDIATE1: "MOV_IMMEDIATE1",
        MOV_IMMEDIATE2: "MOV_IMMEDIATE2",
        MOV_IMMEDIATE4: "MOV_IMMEDIATE4",
        MOV_IMMEDIATE8: "MOV_IMMEDIATE8",
        JUMP: "JUMP",
        JUMP_IMMEDIATE: "JUMP_IMMEDIATE",
        JE: "JE",
        JNE: "JNE",
        JL: "JL",
        JLE: "JLE",
        JG: "JG",
        JGE: "JGE",
        JUL: "JUL",
        JULE: "JULE",
        JUG: "JUG",
        JUGE: "JUGE",
        MALLOC: "MALLOC",
        FREE: "FREE",
        REALLOC: "REALLOC",
        ADD: "ADD",
        SUB: "SUB",
        MUL: "MUL",
        DIV: "DIV",
        MOD: "MOD",
        AND: "AND",
        OR: "OR",
        XOR: "XOR",
        NOT: "NOT",
        NEG: "NEG",
        SHL: "SHL",
        SHR: "SHR",
        USHR: "USHR",
        INC: "INC",
        DEC: "DEC",
        ADD_DOUBLE: "ADD_DOUBLE",
        SUB_DOUBLE: "SUB_DOUBLE",
        MUL_DOUBLE: "MUL_DOUBLE",
        DIV_DOUBLE: "DIV_DOUBLE",
        MOD_DOUBLE: "MOD_DOUBLE",
        ADD_FLOAT: "ADD_FLOAT",
        SUB_FLOAT: "SUB_FLOAT",
        MUL_FLOAT: "MUL_FLOAT",
        DIV_FLOAT: "DIV_FLOAT",
        MOD_FLOAT: "MOD_FLOAT",
        ATOMIC_ADD: "ATOMIC_ADD",
        ATOMIC_SUB: "ATOMIC_SUB",
        ATOMIC_MUL: "ATOMIC_MUL",
        ATOMIC_DIV: "ATOMIC_DIV",
        ATOMIC_MOD: "ATOMIC_MOD",
        ATOMIC_AND: "ATOMIC_AND",
        ATOMIC_OR: "ATOMIC_OR",
        ATOMIC_XOR: "ATOMIC_XOR",
        ATOMIC_NOT: "ATOMIC_NOT",
        ATOMIC_NEG: "ATOMIC_NEG",
        ATOMIC_SHL: "ATOMIC_SHL",
        ATOMIC_SHR: "ATOMIC_SHR",
        ATOMIC_USHR: "ATOMIC_USHR",
        ATOMIC_INC: "ATOMIC_INC",
        ATOMIC_DEC: "ATOMIC_DEC",
        ATOMIC_ADD_DOUBLE: "ATOMIC_ADD_DOUBLE",
        ATOMIC_SUB_DOUBLE: "ATOMIC_SUB_DOUBLE",
        ATOMIC_MUL_DOUBLE: "ATOMIC_MUL_DOUBLE",
        ATOMIC_DIV_DOUBLE: "ATOMIC_DIV_DOUBLE",
        ATOMIC_MOD_DOUBLE: "ATOMIC_MOD_DOUBLE",
        ATOMIC_ADD_FLOAT: "ATOMIC_ADD_FLOAT",
        ATOMIC_SUB_FLOAT: "ATOMIC_SUB_FLOAT",
        ATOMIC_MUL_FLOAT: "ATOMIC_MUL_FLOAT",
        ATOMIC_DIV_FLOAT: "ATOMIC_DIV_FLOAT",
        ATOMIC_MOD_FLOAT: "ATOMIC_MOD_FLOAT",
        CAS: "CAS",
        INVOKE: "INVOKE",
        INVOKE_IMMEDIATE: "INVOKE_IMMEDIATE",
        RETURN: "RETURN",
        GET_RESULT: "GET_RESULT",
        SET_RESULT: "SET_RESULT",
        TYPE_CAST: "TYPE_CAST",
        LONG_TO_DOUBLE: "LONG_TO_DOUBLE",
        DOUBLE_TO_LONG: "DOUBLE_TO_LONG",
        DOUBLE_TO_FLOAT: "DOUBLE_TO_FLOAT",
        FLOAT_TO_DOUBLE: "FLOAT_TO_DOUBLE",
        OPEN: "OPEN",
        CLOSE: "CLOSE",
        READ: "READ",
        WRITE: "WRITE",
        CREATE_FRAME: "CREATE_FRAME",
        DESTROY_FRAME: "DESTROY_FRAME",
        EXIT: "EXIT",
        EXIT_IMMEDIATE: "EXIT_IMMEDIATE",
        GET_FIELD_ADDRESS: "GET_FIELD_ADDRESS",
        GET_LOCAL_ADDRESS: "GET_LOCAL_ADDRESS",
        GET_PARAMETER_ADDRESS: "GET_PARAMETER_ADDRESS",
        CREATE_THREAD: "CREATE_THREAD",
        THREAD_CONTROL: "THREAD_CONTROL"
    }

    @staticmethod
    def get_instruction_name(code: int) -> str:
        if code in ByteCode.instruction_names:
            return ByteCode.instruction_names[code]
        else:
            raise ValueError(f"Unknown instruction code: {code}")

    @staticmethod
    def parse_instruction(code_str: str) -> str:
        upper_code = code_str.upper()
        if upper_code in ByteCode.instruction_names.values():
            return {v: k for k, v in ByteCode.instruction_names}[upper_code]
        else:
            raise ValueError(f"Unknown instruction code: {code_str}")

    @staticmethod
    def is_jump(code):
        return ByteCode.JUMP <= code <= ByteCode.JUGE

    @staticmethod
    def is_conditional_jump(code):
        return ByteCode.JE <= code <= ByteCode.JUGE

    @staticmethod
    def is_unconditional_jump(code):
        return code == ByteCode.JUMP or code == ByteCode.JUMP_IMMEDIATE

    @staticmethod
    def is_arithmetic(code):
        return ByteCode.ADD <= code <= ByteCode.DEC


class FileHandle:
    FH_READ = 1
    FH_WRITE = 1 << 1
    FH_PREOPEN = 1

    def __init__(self, path, flags, mode, input_stream=None, output_stream=None):
        self.path = path
        self.flags = flags | self.FH_PREOPEN
        self.mode = mode
        self.input_stream = input_stream
        self.output_stream = output_stream

        if input_stream is None and (flags & self.FH_READ):
            try:
                self.input_stream = open(path, 'rb')
            except FileNotFoundError as e:
                raise RuntimeError(e)
        if output_stream is None and (flags & self.FH_WRITE):
            try:
                self.output_stream = open(path, 'wb')
            except FileNotFoundError as e:
                raise RuntimeError(e)

    def read(self, buffer, count):
        if self.input_stream is None:
            raise RuntimeError("File not open for reading")
        try:
            data = self.input_stream.read(count)
            buffer[:len(data)] = data
            return len(data)
        except IOError as e:
            raise RuntimeError(e)

    def write(self, buffer):
        if self.output_stream is None:
            raise RuntimeError("File not open for writing")
        try:
            self.output_stream.write(buffer)
        except IOError as e:
            raise RuntimeError(e)

    def close(self):
        if self.flags & self.FH_PREOPEN:
            return
        try:
            if self.input_stream:
                self.input_stream.close()
            if self.output_stream:
                self.output_stream.close()
        except IOError as e:
            raise RuntimeError(e)


class MemoryPageFlag(IntFlag):
    MP_READ = 1
    MP_WRITE = 1 << 1
    MP_EXEC = 1 << 2
    MP_PRESENT = 1 << 3


class MemoryPage:
    PAGE_SIZE = 4096

    def __init__(self, flags: MemoryPageFlag):
        self.flags = flags
        self.ref_count = 0
        self._data = None
        self._lock = threading.RLock()

    def initialize(self):
        """延迟初始化内存页"""
        with self._lock:
            if self.flags & MemoryPageFlag.MP_PRESENT:
                return

            self._data = bytearray(MemoryPage.PAGE_SIZE)
            self.flags |= MemoryPageFlag.MP_PRESENT

    def retain(self):
        with self._lock:
            self.ref_count += 1

    def release(self):
        with self._lock:
            self.ref_count -= 1
            if self.ref_count == 0:
                self.destroy()

    def destroy(self):
        with self._lock:
            self._data = None
            self.flags &= ~MemoryPageFlag.MP_PRESENT

    # 内存读取方法
    def get_byte(self, offset: int) -> int:
        self._check_access(offset, MemoryPageFlag.MP_READ, 1)
        return self._data[offset]

    def get_short(self, offset: int) -> int:
        self._check_access(offset, MemoryPageFlag.MP_READ, 2)
        return struct.unpack('<h', self._data[offset:offset + 2])[0]

    def get_int(self, offset: int) -> int:
        self._check_access(offset, MemoryPageFlag.MP_READ, 4)
        return struct.unpack('<i', self._data[offset:offset + 4])[0]

    def get_long(self, offset: int) -> int:
        self._check_access(offset, MemoryPageFlag.MP_READ, 8)
        return struct.unpack('<q', self._data[offset:offset + 8])[0]

    def get_float(self, offset: int) -> float:
        self._check_access(offset, MemoryPageFlag.MP_READ, 4)
        return struct.unpack('<f', self._data[offset:offset + 4])[0]

    def get_double(self, offset: int) -> float:
        self._check_access(offset, MemoryPageFlag.MP_READ, 8)
        return struct.unpack('<d', self._data[offset:offset + 8])[0]

    # 内存写入方法
    def set_byte(self, offset: int, value: int):
        self._check_access(offset, MemoryPageFlag.MP_WRITE, 1)
        self._data[offset] = value & 0xFF

    def set_short(self, offset: int, value: int):
        self._check_access(offset, MemoryPageFlag.MP_WRITE, 2)
        self._data[offset:offset + 2] = struct.pack('<h', value)

    def set_int(self, offset: int, value: int):
        self._check_access(offset, MemoryPageFlag.MP_WRITE, 4)
        self._data[offset:offset + 4] = struct.pack('<i', value)

    def set_long(self, offset: int, value: int):
        self._check_access(offset, MemoryPageFlag.MP_WRITE, 8)
        self._data[offset:offset + 8] = struct.pack('<q', value)

    def set_float(self, offset: int, value: float):
        self._check_access(offset, MemoryPageFlag.MP_WRITE, 4)
        self._data[offset:offset + 4] = struct.pack('<f', value)

    def set_double(self, offset: int, value: float):
        self._check_access(offset, MemoryPageFlag.MP_WRITE, 8)
        self._data[offset:offset + 8] = struct.pack('<d', value)

    # 辅助方法
    def _check_access(self, offset: int, flag: MemoryPageFlag, size: int):
        """检查内存访问权限和边界"""
        with self._lock:
            # 确保页已初始化
            if not (self.flags & MemoryPageFlag.MP_PRESENT):
                self.initialize()

            # 检查访问权限
            if not (self.flags & flag):
                raise RuntimeError(f"Page does not have {flag.name} permission")

            # 检查边界
            if offset < 0 or offset + size > MemoryPage.PAGE_SIZE:
                raise RuntimeError(f"Invalid offset {offset} for {size}-byte access")


class MemoryPageFreeMemory:
    __slots__ = ('start', 'end', 'next')

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.next: Optional[MemoryPageFreeMemory] = None


class Memory:
    MAX_MEMORY_ADDRESS = 0x0000ffffffffffff
    PAGE_TABLE_SIZE = 512
    PAGE_SIZE = MemoryPage.PAGE_SIZE
    PAGE_OFFSET_MASK = MemoryPage.PAGE_OFFSET_MASK

    class FreeMemory:
        __slots__ = ('start', 'end', 'next')

        def __init__(self, start: int, end: int):
            self.start = start
            self.end = end
            self.next = None

    def __init__(self):
        self.memory_page_table: dict[int, dict[int, dict[int, dict[int, MemoryPage]]]] = {}
        self.free_memory_list: Optional[Memory.FreeMemory] = None
        self.lock = threading.RLock()

    def init(self, text: bytes, rodata: bytes, data: bytes, bss_section_length: int):
        with self.lock:
            self.memory_page_table = {}
            self.free_memory_list = self.FreeMemory(0, 0)
            address = 0

            # 初始化text段
            self._set_memory_page(address, MemoryPageFlag.MP_READ | MemoryPageFlag.MP_EXEC | MemoryPageFlag.MP_WRITE)
            current_page = self._get_memory_page(address)
            address += self.PAGE_SIZE

            offset = 0
            for b in text:
                current_page.set_byte(offset, b)
                offset += 1
                if offset == self.PAGE_SIZE:
                    current_page.flags &= ~MemoryPageFlag.MP_WRITE
                    self._set_memory_page(address,
                                          MemoryPageFlag.MP_READ | MemoryPageFlag.MP_EXEC | MemoryPageFlag.MP_WRITE)
                    current_page = self._get_memory_page(address)
                    address += self.PAGE_SIZE
                    offset = 0

            # 初始化rodata段
            current_page.flags = MemoryPageFlag.MP_READ
            for b in rodata:
                current_page.set_byte(offset, b)
                offset += 1
                if offset == self.PAGE_SIZE:
                    self._set_memory_page(address, MemoryPageFlag.MP_READ)
                    current_page = self._get_memory_page(address)
                    address += self.PAGE_SIZE
                    offset = 0

            # 初始化data段
            current_page.flags = MemoryPageFlag.MP_READ | MemoryPageFlag.MP_WRITE
            for b in data:
                current_page.set_byte(offset, b)
                offset += 1
                if offset == self.PAGE_SIZE:
                    self._set_memory_page(address, MemoryPageFlag.MP_READ | MemoryPageFlag.MP_WRITE)
                    current_page = self._get_memory_page(address)
                    address += self.PAGE_SIZE
                    offset = 0

            # 初始化bss段
            mapped = 0
            while mapped < bss_section_length:
                mapped += self.PAGE_SIZE
                self._set_memory_page(address, MemoryPageFlag.MP_READ | MemoryPageFlag.MP_WRITE)
                address += self.PAGE_SIZE

            # 设置空闲内存链表
            self.free_memory_list.next = self.FreeMemory(
                address - self.PAGE_SIZE + (bss_section_length % self.PAGE_SIZE),
                self.MAX_MEMORY_ADDRESS
            )

    def allocate_memory(self, size: int) -> int:
        with self.lock:
            length = size + 8
            free_mem = self.free_memory_list

            while free_mem:
                if free_mem.end - free_mem.start >= length:
                    start = free_mem.start
                    free_mem.start += length

                    # 分配物理页
                    addr = start
                    remaining = length
                    while remaining > 0:
                        self._set_memory_page(addr & ~self.PAGE_OFFSET_MASK,
                                              MemoryPageFlag.MP_READ | MemoryPageFlag.MP_WRITE)
                        chunk = min(remaining, self.PAGE_SIZE - (addr & self.PAGE_OFFSET_MASK))
                        remaining -= chunk
                        addr += chunk

                    # 存储分配大小
                    self.set_long(start, size)
                    return start + 8
                free_mem = free_mem.next

            raise RuntimeError("Out of memory")

    def free_memory(self, address: int):
        with self.lock:
            addr = address - 8
            size = self.get_long(addr) + 8
            free_mem = self.free_memory_list

            # 查找合适的空闲块位置
            while free_mem.next:
                if free_mem.end == addr:
                    free_mem.end += size
                    break
                elif free_mem.next.start == addr + size:
                    free_mem.next.start -= size
                    break
                elif free_mem.end < addr and free_mem.next.start > addr + size:
                    new_block = self.FreeMemory(addr, addr + size)
                    new_block.next = free_mem.next
                    free_mem.next = new_block
                    break
                free_mem = free_mem.next

            # 释放物理页
            remaining = size
            while remaining > 0:
                page_addr = addr & ~self.PAGE_OFFSET_MASK
                page = self._get_memory_page(page_addr)
                if page:
                    page.release()
                    if page.ref_count <= 0:
                        self._remove_memory_page(page_addr)

                chunk = min(remaining, self.PAGE_SIZE - (addr & self.PAGE_OFFSET_MASK))
                remaining -= chunk
                addr += chunk

    # 私有方法实现
    def _get_indexes(self, address: int) -> tuple[int, int, int, int]:
        return (
            (address >> 39) & 0x1ff,
            (address >> 30) & 0x1ff,
            (address >> 21) & 0x1ff,
            (address >> 12) & 0x1ff
        )

    def _set_memory_page(self, address: int, flags: MemoryPageFlag):
        pgd, pud, pmd, pte = self._get_indexes(address)

        # 创建各级页表
        if pgd not in self.memory_page_table:
            self.memory_page_table[pgd] = {}
        if pud not in self.memory_page_table[pgd]:
            self.memory_page_table[pgd][pud] = {}
        if pmd not in self.memory_page_table[pgd][pud]:
            self.memory_page_table[pgd][pud][pmd] = {}

        # 创建或更新页表项
        if pte not in self.memory_page_table[pgd][pud][pmd]:
            page = MemoryPage(flags)
            self.memory_page_table[pgd][pud][pmd][pte] = page
        else:
            page = self.memory_page_table[pgd][pud][pmd][pte]
            page.flags |= flags

        page.retain()

    def _remove_memory_page(self, address: int):
        pgd, pud, pmd, pte = self._get_indexes(address)

        try:
            del self.memory_page_table[pgd][pud][pmd][pte]

            # 清理空表
            if not self.memory_page_table[pgd][pud][pmd]:
                del self.memory_page_table[pgd][pud][pmd]
            if not self.memory_page_table[pgd][pud]:
                del self.memory_page_table[pgd][pud]
            if not self.memory_page_table[pgd]:
                del self.memory_page_table[pgd]
        except KeyError:
            pass

    def _get_memory_page(self, address: int) -> MemoryPage:
        pgd, pud, pmd, pte = self._get_indexes(address)

        try:
            return self.memory_page_table[pgd][pud][pmd][pte]
        except KeyError:
            raise RuntimeError(f"Page not found at address 0x{address:016x}")

    # 内存读写方法 (简化实现)
    def get_byte(self, address: int) -> int:
        page = self._get_memory_page(address & ~self.PAGE_OFFSET_MASK)
        return page.get_byte(address & self.PAGE_OFFSET_MASK)

    def set_byte(self, address: int, value: int):
        page = self._get_memory_page(address & ~self.PAGE_OFFSET_MASK)
        page.set_byte(address & self.PAGE_OFFSET_MASK, value)

    def get_long(self, address: int) -> int:
        value = 0
        for i in range(8):
            value |= self.get_byte(address + i) << (i * 8)
        return value

    def set_long(self, address: int, value: int):
        for i in range(8):
            self.set_byte(address + i, (value >> (i * 8)) & 0xFF)


class ThreadHandle:
    def __init__(self, eu: "ExecutionUnit"):
        self.eu = eu
        self.thread = threading.Thread(target=self.eu.run())


class VirtualMachine:
    LVM_VERSION = 0

    def __init__(self, stack_size: int):
        self.stack_size = stack_size
        self.memory = Memory()
        self.thread_id_to_handle: dict[int, ThreadHandle] = {}
        self.fd_to_file_handle: dict[int, FileHandle] = {}
        self.entry_point = 0
        self.running = False
        self.last_thread_id = 0
        self.last_fd = 2
        self.lock = threading.RLock()

    def init(self, module: Module) -> int:
        """初始化虚拟机并加载模块"""
        self.memory.init(
            module.text,
            module.rodata,
            module.data,
            module.bssSectionLength
        )
        self.entry_point = module.entrypoint

        # 初始化标准输入/输出/错误
        self.fd_to_file_handle[0] = FileHandle(
            "<stdin>",
            FileHandle.FH_READ,
            0,
            sys.stdin.buffer,
            None
        )
        self.fd_to_file_handle[1] = FileHandle(
            "<stdout>",
            FileHandle.FH_WRITE,
            0,
            None,
            sys.stdout.buffer
        )
        self.fd_to_file_handle[2] = FileHandle(
            "<stderr>",
            FileHandle.FH_WRITE,
            0,
            None,
            sys.stderr.buffer
        )
        return 0

    def run(self) -> int:
        """启动虚拟机主循环"""
        self.create_thread(self.entry_point)
        self.running = True

        # 等待所有线程完成
        while self.running and self.thread_id_to_handle:
            handles = list(self.thread_id_to_handle.values())
            for handle in handles:
                try:
                    handle.thread.join(timeout=0.1)
                    if not handle.thread.is_alive():
                        # 清理线程资源
                        handle.execution_unit.destroy()
                        with self.lock:
                            del self.thread_id_to_handle[handle.execution_unit.threadID]
                except Exception as e:
                    print(f"Thread join error: {e}")
        return 0

    def create_thread(self, entry_point: int) -> int:
        """创建新线程"""
        thread_id = self._get_thread_id()
        execution_unit = self._create_execution_unit(thread_id, entry_point)
        thread_handle = ThreadHandle(execution_unit)

        with self.lock:
            self.thread_id_to_handle[thread_id] = thread_handle

        thread_handle.thread.start()
        return thread_id

    def _create_execution_unit(self, thread_id: int, entry_point: int) -> "ExecutionUnit":
        """创建执行单元"""
        stack_start = self.memory.allocate_memory(self.stack_size)
        execution_unit = ExecutionUnit(self)
        execution_unit.init(
            thread_id,
            stack_start + self.stack_size - 1,
            entry_point
        )
        return execution_unit

    def open(self, path: str, flags: int, mode: int) -> int:
        """打开文件"""
        fd = self._get_fd()
        try:
            with self.lock:
                self.fd_to_file_handle[fd] = FileHandle(path, flags, mode)
            return fd
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            return -1

    def close(self, fd: int) -> int:
        """关闭文件"""
        with self.lock:
            file_handle = self.fd_to_file_handle.pop(fd, None)
            if file_handle:
                file_handle.close()
                return 0
        return -1

    def read(self, fd: int, buffer: bytearray, count: int) -> int:
        """读取文件"""
        with self.lock:
            file_handle = self.fd_to_file_handle.get(fd)

        if not file_handle:
            raise IOError(f"Invalid file descriptor: {fd}")

        try:
            return file_handle.read(buffer, count)
        except Exception as e:
            raise IOError(f"Read error: {e}")

    def write(self, fd: int, buffer: bytes) -> int:
        """写入文件"""
        with self.lock:
            file_handle = self.fd_to_file_handle.get(fd)

        if not file_handle:
            raise IOError(f"Invalid file descriptor: {fd}")

        try:
            file_handle.write(buffer)
            return len(buffer)
        except Exception as e:
            raise IOError(f"Write error: {e}")

    def exit(self, status: int):
        """退出虚拟机"""
        self.running = False
        # TODO: 实现完整的清理逻辑

    def _get_thread_id(self) -> int:
        """生成唯一线程ID"""
        with self.lock:
            self.last_thread_id += 1
            while self.last_thread_id in self.thread_id_to_handle:
                self.last_thread_id += 1
            return self.last_thread_id

    def _get_fd(self) -> int:
        """生成唯一文件描述符"""
        with self.lock:
            self.last_fd += 1
            while self.last_fd in self.fd_to_file_handle:
                self.last_fd += 1
            return self.last_fd


class ExecutionUnit:
    def __init__(self, virtual_machine: VirtualMachine):
        self.virtual_machine = virtual_machine
        self.threadID = 0
        self.registers = [0] * 40
        self.flags = 0
        self.result = 0
        self.running = False

    def init(self, threadID: int, stack_start: int, entrypoint: int):
        self.threadID = threadID
        self.registers[ByteCode.BP_REGISTER] = stack_start
        self.registers[ByteCode.SP_REGISTER] = stack_start
        self.registers[ByteCode.PC_REGISTER] = entrypoint

    def get_register(self, register: int) -> int:
        return self.registers[register]

    def set_register(self, register: int, value: int):
        self.registers[register] = value

    def execute(self):
        self.running = True
        while self.running:
            pc = self.get_register(ByteCode.PC_REGISTER)
            code = self.virtual_machine.memory.get_byte(pc)
            pc += 1

            match code:
                case ByteCode.NOP:
                    self.set_register(ByteCode.PC_REGISTER, pc)

                # 内存操作指令
                case ByteCode.PUSH_1 | ByteCode.PUSH_2 | ByteCode.PUSH_4 | ByteCode.PUSH_8:
                    register = self.virtual_machine.memory.get_byte(pc)
                    pc += 1
                    self.set_register(ByteCode.PC_REGISTER, pc)

                    sp = self.get_register(ByteCode.SP_REGISTER)
                    size = 1 << (code - ByteCode.PUSH_1)
                    sp -= size
                    self.set_register(ByteCode.SP_REGISTER, sp)

                    value = self.get_register(register)
                    if size == 1:
                        self.virtual_machine.memory.set_byte(sp, value)
                    elif size == 2:
                        self.virtual_machine.memory.set_short(sp, value)
                    elif size == 4:
                        self.virtual_machine.memory.set_int(sp, value)
                    else:  # size == 8
                        self.virtual_machine.memory.set_long(sp, value)

                # 比较指令
                case ByteCode.CMP:
                    type_ = self.virtual_machine.memory.get_byte(pc)
                    operand1 = self.virtual_machine.memory.get_byte(pc + 1)
                    operand2 = self.virtual_machine.memory.get_byte(pc + 2)
                    pc += 3
                    self.set_register(ByteCode.PC_REGISTER, pc)

                    value1 = self.get_register(operand1)
                    value2 = self.get_register(operand2)

                    # 类型转换
                    if type_ == ByteCode.BYTE_TYPE:
                        value1 &= 0xFF
                        value2 &= 0xFF
                    elif type_ == ByteCode.SHORT_TYPE:
                        value1 &= 0xFFFF
                        value2 &= 0xFFFF
                    elif type_ == ByteCode.INT_TYPE:
                        value1 &= 0xFFFFFFFF
                        value2 &= 0xFFFFFFFF

                    # 设置标志位
                    if value1 == value2:
                        self.flags = (self.flags & ~ByteCode.ZERO_MARK &
                                      ~ByteCode.CARRY_MARK & ~ByteCode.UNSIGNED_MARK) | 1
                    else:
                        signed_result = value1 - value2
                        unsigned_result = (value1 & 0xFFFFFFFFFFFFFFFF) - (value2 & 0xFFFFFFFFFFFFFFFF)
                        carry = 1 if signed_result < 0 else 0
                        unsigned_flag = 1 if unsigned_result < 0 else 0
                        self.flags = (self.flags & ~ByteCode.ZERO_MARK &
                                      ~ByteCode.CARRY_MARK & ~ByteCode.UNSIGNED_MARK) | \
                                     (carry << 1) | (unsigned_flag << 2)

                # 移动指令
                case ByteCode.MOV:
                    source = self.virtual_machine.memory.get_byte(pc)
                    target = self.virtual_machine.memory.get_byte(pc + 1)
                    pc += 2
                    self.set_register(ByteCode.PC_REGISTER, pc)
                    self.set_register(target, self.get_register(source))

                # 立即数加载
                case ByteCode.MOV_IMMEDIATE1:
                    value = self.virtual_machine.memory.get_byte(pc)
                    target = self.virtual_machine.memory.get_byte(pc + 1)
                    pc += 2
                    self.set_register(ByteCode.PC_REGISTER, pc)
                    self.set_register(target, value)

                # 算术运算
                case ByteCode.ADD:
                    operand1 = self.virtual_machine.memory.get_byte(pc)
                    operand2 = self.virtual_machine.memory.get_byte(pc + 1)
                    result_reg = self.virtual_machine.memory.get_byte(pc + 2)
                    pc += 3
                    self.set_register(ByteCode.PC_REGISTER, pc)

                    val1 = self.get_register(operand1)
                    val2 = self.get_register(operand2)
                    self.set_register(result_reg, val1 + val2)

                # 跳转指令
                case ByteCode.JUMP:
                    address_reg = self.virtual_machine.memory.get_byte(pc)
                    pc += 1
                    self.set_register(ByteCode.PC_REGISTER, self.get_register(address_reg))

                case ByteCode.JE:
                    address_reg = self.virtual_machine.memory.get_byte(pc)
                    pc += 1
                    self.set_register(ByteCode.PC_REGISTER, pc)
                    if self.flags & ByteCode.ZERO_MARK:
                        self.set_register(ByteCode.PC_REGISTER, self.get_register(address_reg))

                # 系统调用
                case ByteCode.OPEN:
                    path_reg = self.virtual_machine.memory.get_byte(pc)
                    flags_reg = self.virtual_machine.memory.get_byte(pc + 1)
                    mode_reg = self.virtual_machine.memory.get_byte(pc + 2)
                    result_reg = self.virtual_machine.memory.get_byte(pc + 3)
                    pc += 4
                    self.set_register(ByteCode.PC_REGISTER, pc)

                    # 从内存读取路径字符串
                    address = self.get_register(path_reg)
                    path = bytearray()
                    while (byte_val := self.virtual_machine.memory.get_byte(address)) != 0:
                        path.append(byte_val)
                        address += 1

                    try:
                        fd = self.virtual_machine.open(
                            path.decode('utf-8'),
                            self.get_register(flags_reg),
                            self.get_register(mode_reg)
                        )
                        self.set_register(result_reg, fd)
                    except FileNotFoundError:
                        self.set_register(result_reg, -1)

                # 函数调用/返回
                case ByteCode.INVOKE:
                    address_reg = self.virtual_machine.memory.get_byte(pc)
                    pc += 1
                    sp = self.get_register(ByteCode.SP_REGISTER) - 8
                    self.virtual_machine.memory.set_long(sp, pc)
                    self.set_register(ByteCode.SP_REGISTER, sp)
                    self.set_register(ByteCode.PC_REGISTER, self.get_register(address_reg))

                case ByteCode.RETURN:
                    sp = self.get_register(ByteCode.SP_REGISTER)
                    return_addr = self.virtual_machine.memory.get_long(sp)
                    self.set_register(ByteCode.SP_REGISTER, sp + 8)
                    self.set_register(ByteCode.PC_REGISTER, return_addr)

                # 线程控制
                case ByteCode.CREATE_THREAD:
                    entry_point = self.virtual_machine.memory.get_long(pc)
                    result_reg = self.virtual_machine.memory.get_byte(pc + 8)
                    pc += 9
                    self.set_register(ByteCode.PC_REGISTER, pc)
                    thread_id = self.virtual_machine.create_thread(entry_point)
                    self.set_register(result_reg, thread_id)

                # 退出指令
                case ByteCode.EXIT:
                    exit_code_reg = self.virtual_machine.memory.get_byte(pc)
                    self.virtual_machine.exit(self.get_register(exit_code_reg))
                    self.running = False

                # 其他指令处理...
                case _:
                    # 默认处理：打印未实现指令并继续
                    try:
                        instr_name = ByteCode.get_instruction_name(code)
                        print(f"Unimplemented instruction: {instr_name} at PC={pc - 1}")
                        self.set_register(ByteCode.PC_REGISTER, pc)
                    except ValueError:
                        print(f"Unknown instruction code: {code} at PC={pc - 1}")
                        self.running = False

    def run(self):
        try:
            self.execute()
        except Exception as e:
            print(f"Thread {self.threadID} crashed: {e}")
            self.virtual_machine.exit(1)

