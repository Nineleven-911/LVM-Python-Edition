from hairinne.utils.Incomplete import incompleted


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
    FH_WRITE = 2
    FH_PREOPEN = 1

    @incompleted
    def __init__(self, path: str, flags: int, mode: int):
        pass


class Memory:
    pass


class ThreadHandle:
    pass


class VirtualMachine:
    LVM_VERSION = 0  # Range: long range ( 2^63-1=9223372036854775807 )


class ExecutionUnit:
    def __init__(self, virtual_machine: VirtualMachine):
        self.registers: list[int] = []
        self.threadID: int = 0
        self.virtual_machine = virtual_machine

    def init(self, threadID: int, stack_start: int, entrypoint: int):
        self.threadID = threadID
        self.registers = [0 for _ in range(40)]
        self.registers[ByteCode.BP_REGISTER] = stack_start
        self.registers[ByteCode.SP_REGISTER] = stack_start
        self.registers[ByteCode.PC_REGISTER] = entrypoint

    @incompleted
    def execute(self):
        running = True
        while running:
            pc = self.registers[ByteCode.PC_REGISTER]
            # TODO

    def run(self):
        self.execute()
