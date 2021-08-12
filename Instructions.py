# in dict form, the instructions should take the form:
# {"op": "<command>", "rd:":<val>, "rs1":<val>, "rs2":<val>, "imm":<val>}
# using only the fields needed

# instruction expansion to add:
# prnt <rs1> : prints the value in rs1
# prnti <imm> : prints the value in the immediate

# pseudo instructions: (converted to real instruction in step 2's convert_pseudo)
# li <rd>, <imm> : loads the immediate into rs1 == addi <rd>, x0, <imm>
# bng <rs1>, <rs2>(<imm>) : branch if the item is negative == blt <rs1>, x0, <rs2>(imm)
# bps <rs1>, <rs2>(<imm>) : branch if the item is positive == blt x0, <rs1>, <rs2>(imm)


# a set of all possible instructions as we generate them
# mostly for debugging purposes
poss_instructions = set()

class Instruction():
    """
    a class representation of a risc-v assembly instruction
    """
    def __init__(self, op, ref_ids=[], imm=None, tags=[]):
    # def __init__(self, op, ref_ids=[], imm=None, tags=[], ref_tags=[]):
        """
        @input op: the operation name for the instruction
        @input ref_ids: a list of index-references to other instructions needed to evaluate this one
        @input imm: the value of the immediate (as an integer)
        @input tags: the list of value/variable names to tag this register value with
        """
        global poss_instructions

        assert type(op) == str, "Operation type must be a string"
        poss_instructions.add(op)
        self.op = op
        self.ref_ids = ref_ids
        self.imm = imm
        self.tags = set(tags)
        # self.ref_tags = ref_tags

        # the actual register values (to be filled in once a full program is created)
        self.rd = None
        self.rs1 = None
        self.rs2 = None
    def __str__(self):
        ret = self.op
        if len(self.tags) > 0: ret += ' "' + ", ".join(self.tags) + '"'
        if not (self.rd or self.rs1 or self.rs2) and len(self.ref_ids) > 0:
            ret += " (refs: " + ", ".join([str(i) for i in self.ref_ids]) + ")"
        # if not (self.rd or self.rs1 or self.rs2) and len(self.ref_tags) > 0:
        #     ret += " (ref tags: " + ", ".join([str(t) for t in self.ref_tags]) + ")"
        if self.rd is not None:  ret += " (rd: " + str(self.rd) + ")"
        if self.rs1 is not None: ret += " (rs1: " + str(self.rs1) + ")"
        if self.rs2 is not None: ret += " (rs2: " + str(self.rs2) + ")"
        if self.imm is not None: ret += " (imm: " + str(self.imm) + ")"
        return ret
    def to_json(self):
        """
        converts the necessary contents to a dict that is ready to be stored as a json
        @input: none
        @return: a dict of the format {"op": "<command>", "rd:":<val>, "rs1":<val>, "rs2":<val>, "imm":<val>}
        """
        output = {}
        output["op"] = self.op

        if self.rd is not None: output["rd"] = self.rd
        if self.rs1 is not None: output["rs1"] = self.rs1
        if self.rs2 is not None: output["rs2"] = self.rs2
        
        if self.imm is not None: output["imm"] = self.imm

        return output