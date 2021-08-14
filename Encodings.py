"""
The different instructions in RISC-V fall into 5 main categories (plus two more for our prints)
Every instruction in a category is mapped to the binary in the same way
So, just create a conversion for each one and then specify where each instruction falls
"""

from abc import ABC, abstractmethod

# will map each instruction type to the instructions that are part of it
instr_types = {}

def int_to_binary(integer, length=4):
    """
    given an integer number, return a string of the number in binary
    @input integer: the number as an integer
    @return bin: the number as a string of binary
    """
    if integer >= 0:
        basic = bin(integer)[2:]
        assert len(basic) <= length, f"The bits needed for {integer} are more than the space to store it!"
        return basic.zfill(length)
    else:
        twos_comp = 1 - integer
        basic = bin(twos_comp)[2:]
        assert len(basic) <= length, f"The bits needed for {integer} are more than the space to store it!"
        sized = basic.zfill(length)
        return "".join(["1" if char == "0" else "0" for char in sized])
        # raise NotImplementedError("We do not currently support negative binary numbers")


class base_type(ABC):
    """
    the base instruction type, used to define the methods all of them will have
    """
    instr_codes = {}
    @abstractmethod
    def __init__(self, dic):
        """
        takes in a dict of the instruction and unwraps the needed values
        """
        # the mapping from the "instruction name" to the binary string code
        self.instr_codes = {}
        pass
    @abstractmethod
    def __str__(self):
        pass
    @abstractmethod
    def get_opcode(self, op=None):
        """
        for the stored op, find the relevant opcode
        if there is also a fn3 (and even fn7) return it as well in a tuple
        """
        pass
    @abstractmethod
    def get_binary(self):
        """
        using the internal values, outputs a list of ints representing the binary instruction
        """
        pass

class rtype:
    """
    Register type
    from two registers into a register
    """
    instr_codes = {
        "and": "000",
        "or": "001",
        "slt": "010",
        "xor": "011",
        "add": "100",
        "sub": "101",
        # "sll": "110",
        # "srl": "111",
    }

    def __init__(self, dic):
        """
        takes in a dict of the instruction and unwraps the needed values
        """
        # capture the op, for conversion to opcode
        assert "op" in dic, f"Rtype is missing op field, given {dic}"
        self.op = dic["op"]
        assert "rs1" in dic, f"Rtype {self.op} is missing rs1 field"
        self.rs1 = dic["rs1"]
        assert "rs2" in dic, f"Rtype {self.op} is missing rs2 field"
        self.rs2 = dic["rs2"]
        assert "rd" in dic, f"Rtype {self.op} is missing rd field"
        self.rd = dic["rd"]
    def __str__(self):
        return (self.op + " x" + self.rd + ", x" + self.rs1 + ", x" + self.rs2)
    def get_opcode(self, op=None):
        """
        for the stored op, find the relevant opcode, returning a tuple (fn3, opcode)
        """
        if op is None:
            op = self.op
        assert op in self.instr_codes, f"Operation {op} doesn't have an operation code assigned for an R-Type"
        return (self.instr_codes[op], "001")
    def get_binary(self):
        """
        using the internal values, outputs a list of ints representing the binary instruction
        """
        fn3, optype = self.get_opcode()
        rs1 = int_to_binary(self.rs1, 4)
        rs2 = int_to_binary(self.rs2, 4)
        rd = int_to_binary(self.rd, 4)
        return fn3 + "0" + rs2 + rs1 + rd + optype
instr_types[rtype] = ["add", "sub", "slt", "xor"]


class itype:
    """
    immediate type
    from a register and an immediate into a register
    also includes loads and JALRs
    """
    # instr_codes = {
    #     "addi": "000",
    #     "subi": "001",
    #     "slti": "010",
    #     "addiu": "100",
    #     "subiu": "101",
    #     "sltiu": "110",
    #     "slli": "011",
    #     "srli": "111",
    # }
    instr_codes = {
        "andi": "000",
        "sltiu": "001",
        "xori": "010",
        "slti": "100",
        "addi": "101",
        "subi": "110",
        "slli": "011",
        "srli": "111",
    }
    def __init__(self, dic):
        """
        takes in a dict of the instruction and unwraps the needed values
        """
        # capture the op, for conversion to opcode
        assert "op" in dic, f"Itype is missing op field, given {dic}"
        self.op = dic["op"]
        assert "rs1" in dic, f"Itype {self.op} is missing rs1 field"
        self.rs1 = dic["rs1"]
        assert "imm" in dic, f"Itype {self.op} is missing imm field"
        self.imm = dic["imm"]
        assert "rd" in dic, f"Itype {self.op} is missing rd field"
        self.rd = dic["rd"]
    def __str__(self):
        if self.op in ["lw", "lh", "lb"]:
            return (self.op + " x" + self.rd + ", " + self.imm + "(" + self.rs1 + ")")
        else:
            return (self.op + " x" + self.rd + ", x" + self.rs1 + ", " + self.imm)
    def get_opcode(self, op=None):
        """
        for the stored op, find the relevant opcode, returning a tuple (fn3, opcode)
        """
        if op is None:
            op = self.op
        assert op in self.instr_codes, f"Operation {op} doesn't have an operation code assigned for an I-Type"
        return (self.instr_codes[op], "010")
    def get_binary(self):
        """
        using the internal values, outputs a list of ints representing the binary instruction
        """
        fn3, optype = self.get_opcode()
        rs1 = int_to_binary(self.rs1, 4)
        rd = int_to_binary(self.rd, 4)
        imm = int_to_binary(self.imm, 5)
        return fn3 + imm + rs1 + rd + optype
instr_types[itype] = ["addi", "subi", "xori", "slti", "sltiu"]

# class stype:
#     """
#     store type
#     from a register using a base and offset, but no writeback
#     """


# class btype:
#     """
#     branch type
#     two registers to compare and how far to jump, no writeback
#     """


# class utype:
#     """
#     upper immediate type
#     LUI and AUIPC only
#     have an immediate and where to put the result
#     """


# class jtype:
#     """
#     Jump type
#     only for JAL
#     has a special formatted immediate and where to put the results
#     """


class atype:
    """
    accept type
    only for prnt
    accepts an rs1 value and thats it, no returns
    """
    instr_codes = {
        "prnt": "0",
    }
    def __init__(self, dic):
        """
        takes in a dict of the instruction and unwraps the needed values
        """
        # capture the op, for conversion to opcode
        assert "op" in dic, f"Itype is missing op field, given {dic}"
        self.op = dic["op"]
        assert "rs1" in dic, f"Itype {self.op} is missing rs1 field"
        self.rs1 = dic["rs1"]
    def __str__(self):
        return (self.op + " x" + self.rs1)
    def get_opcode(self, op=None):
        """
        for the stored op, find the relevant opcode, returning the opcode
        """
        if op is None:
            op = self.op
        assert op in self.instr_codes, f"Operation {op} doesn't have an operation code assigned for an A-Type"
        return (self.instr_codes[op], "111")
    def get_binary(self):
        """
        using the internal values, outputs a list of ints representing the binary instruction
        """
        fn3, optype = self.get_opcode()
        rs1 = int_to_binary(self.rs1, 4)
        spacing1 = "".join(["0"] * 7)
        spacing2 = "".join(["0"] * 4)
        return fn3 + spacing1 + rs1 + spacing2 + optype
instr_types[atype] = ["prnt"]


class ptype:
    """
    perform type
    only for prnti
    operates only on the immediate with no returns
    """
    instr_codes = {}#"prnti":""}
    def __init__(self, dic):
        """
        takes in a dict of the instruction and unwraps the needed values
        """
        # capture the op, for conversion to opcode
        assert "op" in dic, f"Ptype is missing op field, given {dic}"
        self.op = dic["op"]
        assert "imm" in dic, f"Ptype {self.op} is missing imm field"
        self.value = dic["imm"]
    def __str__(self):
        return (self.op + " " + self.value)
    def get_opcode(self, op=None):
        """
        for the stored op, find the relevant opcode, returning just the opcode
        """
        if op is None:
            op = self.op
        assert op == "prnti", f"Operation {op} doesn't have an operation code assigned for an P-Type"
        return ("", "000")
    def get_binary(self):
        """
        using the internal values, outputs a list of ints representing the binary instruction
        """
        _, optype = self.get_opcode()
        value = int_to_binary(self.value, 16)
        return value + optype
instr_types[ptype] = ["prnti"]



def choose_type(op):
    """
    finds which type of instruction category this operation is
    @input op: a string representing the instruction name
    @return: the class of the type to use (a child of base_type)
    """
    for tipe in instr_types:
        if op in instr_types[tipe]:
            return tipe
    raise ValueError(f"Unable to find a matching type for op {op}")


def get_all_defined_instrs():
    """
    returns a list of all of the possible instruction types we have, as strings
    @input: none
    @return: a list of strings
    """
    return [instr for instr_list in instr_types.values() for instr in instr_list]