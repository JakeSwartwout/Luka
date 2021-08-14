"""
The assembler is the second step in the process
It assembles the grammar into a list of machine instructions
This assembler takes in Python (.py) files and outputs JSON (.json) files
"""

import Grammar
from Instructions import Instruction, poss_instructions
from params import default_compiler_output, default_assembler_output, luka_version
import json
import argparse
import sys


def check_errors(errors, printIt=False):
    """
    check if there are any errors in the list, printing them if yes, returning whether there were or not
    @input errors: a list of all of the errors encountered
    @output: a boolean of whether there were errors (True) or not (False)
    """
    if len(errors) > 0:
        if printIt:
            print("Assembler: Encountered the following fatal errors:")
            for err in errors:
                print(err)
        return True
    return False


def import_program_grammar(filename, errors, warnings):
    """
    open the python file at the location and retrieve the grammar
    stored in the "program" variable there
    @input filename: the name or path of the file to open
    @input errors: a pre-existing list of errors to append our errors to
    @input warnings: a pre-existing list of warnings to append our issues to
    @return program: a Program object representing the program grammar
    """
    # remove .py from the file name
    if filename[-3:] == ".py": filename = filename[:-3]

    # convert any slashes into periods
    # filename = filename.replace("/", ".").replace("\\", ".").strip(".")
    filename = "output." + filename

    # import the program from the file
    try:
        gram = __import__(filename, globals(), locals(), ["program"])
    except Exception as err:
        errors.append(f"Error importing the grammar: {err}")
        return None
    try:
        return gram.program
    except Exception as err:
        # error handling
        errors.append(f"Error finding the program in the grammar: {err}")
        return None


def get_instrs_from_program(program, errors, warnings):
    """
    take in a program's grammar and fake execute it, getting a queue of the operations
    it needs to perform and the order it needs to perform them in
    @input program: a Program object representing the program to assemble
    @input errors: a pre-existing list to append our errors to
    @input warnings: a pre-existing list to append our warnings to
    @return instr_queue: a list of Instruction objects representing the instructions 
    """
    instr_queue = []

    for comm in program.commands:
        # get the instructions for that command
        partial_instrs = get_instrs_from_command(comm, errors, warnings)
        if not partial_instrs: return []
        # shift the references accordingly
        curr_len = len(instr_queue)
        for part in partial_instrs:
            part.ref_ids = [i+curr_len if type(i) is not str else i for i in part.ref_ids]
        # append them to the list
        instr_queue += partial_instrs
        if check_errors(errors): return []

    return instr_queue


bool_to_int = {True: 1, False: 0}


def get_instrs_from_command(command, errors, warnings):
    """
    take in a command and fake execute it, gettings a list of the operations it needs
    to perform and the order it needs to perform them in
    to be done recursively, unwrapping the commands one by one
    @input program: a Program object representing the program to assemble
    @input errors: a pre-existing list to append our errors to
    @input warnings: a pre-existing list to append our warnings to
    @return instr_queue: a list of Instruction objects representing the instructions
    """
    
    # the final answer/return value should always be stored in the last instruction, for references

    tipe = type(command)

    if tipe == Grammar.Print:
        # make sure the value inside returns something
        if not isinstance(command.value, Grammar.ReturnCommand):
            errors.append(f"Attempting to print something without a value: {command}")
            return []
        # if the inside is just an integer, then this is an immediate
        if type(command.value) == Grammar.Integer:
            return [Instruction("prnti", imm=command.value.value)]
        # booleans turn into immediates of 0 or 1
        elif type(command.value) == Grammar.Boolean:
            return [Instruction("prnti", imm=bool_to_int[command.value.value])]
        # if the inside is an identifier, then just access that register
        elif type(command.value) == Grammar.Ident:
            return [Instruction("prnt", ref_ids=[command.value.name])]
        # otherwise, is a calculation, get any sub instructions we need to perform
        sub_instrs = get_instrs_from_command(command.value, errors, warnings)
        if check_errors(errors): return []
        return sub_instrs + [Instruction("prnt", ref_ids=[len(sub_instrs)-1])]

    elif tipe == Grammar.Add:
        # make sure both values inside return something
        if not isinstance(command.v1, Grammar.ReturnCommand):
            errors.append("Must Add two values together, but found: " + command.v1)
            return []
        if not isinstance(command.v2, Grammar.ReturnCommand):
            errors.append("Must Add two values together, but found: " + command.v2)
            return []
        # check if either value is an immediate
        is_imm = False
        if type(command.v2) in [Grammar.Integer, Grammar.Boolean]:
            is_imm = True
            imm = command.v2
            imm = bool_to_int[imm.value] if type(imm) == Grammar.Boolean else imm.value
            other = command.v1
        elif type(command.v1) in [Grammar.Integer, Grammar.Boolean]:
            is_imm = True
            imm = command.v1
            imm = bool_to_int[imm.value] if type(imm) == Grammar.Boolean else imm.value
            other = command.v2
        if is_imm:
            # know it's an immediate
            # check if the other is an ident, and just reference that
            if type(other) == Grammar.Ident:
                return [Instruction("addi", ref_ids=[other.name], imm=imm)]
            # otherwise, need to decode the rest
            sub_instrs = get_instrs_from_command(other, errors, warnings)
            if check_errors(errors): return []
            return sub_instrs + [Instruction("addi", ref_ids=[len(sub_instrs)-1], imm=imm)]
        # both are values, check if either one is an Ident
        instrs = []
        p2offset = 0
        if type(command.v1) == Grammar.Ident:
            # just link up immediately
            ref1 = command.v1.name
        else:
            # need to decode (and eval those commands) before linking
            sub_instrs1 = get_instrs_from_command(command.v1, errors, warnings)
            if check_errors(errors): return []
            instrs += sub_instrs1
            ref1 = len(sub_instrs1) - 1
            p2offset = ref1 + 1
        if type(command.v2) == Grammar.Ident:
            ref2 = command.v2.name
        else:
            sub_instrs2 = get_instrs_from_command(command.v2, errors, warnings)
            if check_errors(errors): return []
            ref2 = p2offset + len(sub_instrs2) - 1
            # shift the second instruction references to start at the end of the first
            for part in sub_instrs2:
                # make sure to skip the shifting if it's a variable reference
                part.ref_ids = [i+p2offset if type(i) is int else i for i in part.ref_ids]
            # combine the final lists of instructions with an add on the end
            instrs += sub_instrs2
        # add the final instruction to add the two together
        return instrs + [Instruction("add", ref_ids=[ref1, ref2])]

    elif tipe == Grammar.Sub:
        # make sure both values inside return something
        if not isinstance(command.v1, Grammar.ReturnCommand):
            errors.append("Must Sub two values together, but found: " + command.v1)
            return []
        if not isinstance(command.v2, Grammar.ReturnCommand):
            errors.append("Must Sub two values together, but found: " + command.v2)
            return []
        # check if the second value is an immediate
        # first must always be a register, only have (reg - reg) or (reg - imm)
        if type(command.v2) in [Grammar.Integer, Grammar.Boolean]:
            imm = bool_to_int[command.v2.value] if type(command.v2) == Grammar.Boolean else command.v2.value
            # check if the other is an ident, and just reference that
            if type(command.v1) == Grammar.Ident:
                return [Instruction("subi", ref_ids=[command.v1.name], imm=imm)]
            # otherwise, need to decode the rest
            sub_instrs = get_instrs_from_command(command.v1, errors, warnings)
            if check_errors(errors): return []
            return sub_instrs + [Instruction("subi", ref_ids=[len(sub_instrs)-1], imm=imm)]
        # both are values, check if either one is an Ident
        instrs = []
        p2offset = 0
        if type(command.v1) == Grammar.Ident:
            # just link up immediately
            ref1 = command.v1.name
        else:
            # need to decode (and eval those commands) before linking
            sub_instrs1 = get_instrs_from_command(command.v1, errors, warnings)
            if check_errors(errors): return []
            instrs += sub_instrs1
            ref1 = len(sub_instrs1) - 1
            p2offset = ref1 + 1
        if type(command.v2) == Grammar.Ident:
            ref2 = command.v2.name
        else:
            sub_instrs2 = get_instrs_from_command(command.v2, errors, warnings)
            if check_errors(errors): return []
            ref2 = p2offset + len(sub_instrs2) - 1
            # shift the second instruction references to start at the end of the first
            for part in sub_instrs2:
                # make sure to skip the shifting if it's a variable reference
                part.ref_ids = [i+p2offset if type(i) is int else i for i in part.ref_ids]
            # combine the final lists of instructions with an add on the end
            instrs += sub_instrs2
        # add the final instruction to add the two together
        return instrs + [Instruction("sub", ref_ids=[ref1, ref2])]
    
    elif tipe == Grammar.Val:
        # make sure value inside returns something
        if not isinstance(command.value, Grammar.ReturnCommand):
            errors.append("Value must be set to something that returns, but found: " + command.value)
            return []
        if not isinstance(command.ident, Grammar.Ident):
            errors.append("Must use an identifier, found: " + command.ident)
            return []
        # check if the value is an immediate
        if type(command.value) in [Grammar.Integer, Grammar.Boolean]:
            # know it's just an li
            imm = bool_to_int[command.value.value] if type(command.value) == Grammar.Boolean else command.value.value
            return [Instruction("li", ref_ids=[], imm=imm, tags=[command.ident.name])]
        # or if it's another ident
        elif type(command.value) == Grammar.Ident:
            # know it's just a mv command (move from one register to another, also a copy)
            return [Instruction("mv", ref_ids=[command.value.name], tags=[command.ident.name])]
        else:
            # need to do the calculations for it
            sub_instrs = get_instrs_from_command(command.value, errors, warnings)
            if check_errors(errors): return []
            # no extra commands, last command should produce our value
            # so just tag the last item with this variable name
            sub_instrs[-1].tags.add(command.ident.name)
            return sub_instrs

    elif tipe in [Grammar.Eq, Grammar.NotEq, Grammar.Gr, Grammar.Ls, Grammar.GrEq, Grammar.LsEq]:
        # make sure both values inside return something
        if not isinstance(command.v1, Grammar.ReturnCommand):
            errors.append("Must compare two values, but found: " + command.v1)
            return []
        if not isinstance(command.v2, Grammar.ReturnCommand):
            errors.append("Must compare two values, but found: " + command.v2)
            return []
        # check if either value is an immediate
        is_imm = False
        if type(command.v2) is Grammar.Integer:
            is_imm = True
            imm = command.v2.value
            other = command.v1
        elif type(command.v1) is Grammar.Integer:
            is_imm = True
            imm = command.v1.value
            other = command.v2
        if is_imm:
            # know it's an immediate
            # check if the other is an ident, and just reference that
            if type(other) == Grammar.Ident:
                sub_instrs = []
                reference = other.name
            else:
                # otherwise, need to decode the rest
                sub_instrs = get_instrs_from_command(other, errors, warnings)
                if check_errors(errors): return []
                reference = len(sub_instrs)-1
            # add on the final instructions depending on the comparison
            if tipe is Grammar.Eq:
                return sub_instrs + [
                    Instruction("xori", ref_ids=[reference], imm=imm),      # 0 if the same, trash if different
                    Instruction("sltiu", ref_ids=[reference+1], imm=1)      # 1 if the same, 0 if different
                ]
            elif tipe is Grammar.NotEq:
                return sub_instrs + [
                    Instruction("xori", ref_ids=[reference], imm=imm),      # 0 if the same, trash if different
                    Instruction("sltiu", ref_ids=[reference+1], imm=1),     # 1 if the same, 0 if different
                    Instruction("xori", ref_ids=[reference+2], imm=1)       # 0 if the same, 1 if different
                ]
            elif tipe is Grammar.Ls:
                return sub_instrs + [
                    Instruction("slti", ref_ids=[reference], imm=imm)       # 1 if a < b, 0 if a >=b
                ]
            elif tipe is Grammar.GrEq:
                return sub_instrs + [
                    Instruction("slti", ref_ids=[reference], imm=imm),      # 1 if a < b, 0 if a >= b
                    Instruction("xori", ref_ids=[reference+1], imm=1)       # 0 if a < b, 1 if a >= b
                ]
            elif tipe is Grammar.LsEq:
                return sub_instrs + [
                    Instruction("subi", ref_ids=[reference], imm=imm),      # negative if a < b, 0 if a == b, positive if a > b
                    Instruction("slti", ref_ids=[reference+1], imm=1)       # 1 if a <=b, 0 if a > b
                ]
            elif tipe is Grammar.Gr:
                return sub_instrs + [
                    Instruction("subi", ref_ids=[reference], imm=imm),      # negative if a < b, 0 if a == b, positive if a > b
                    Instruction("slti", ref_ids=[reference+1], imm=1),      # 1 if a <= b, 0 if a > b
                    Instruction("xori", ref_ids=[reference+2], imm=1)       # 0 if a <= b, 1 if a > b
                ]
            else:
                errors.append("Unrecognized comparison type: " + tipe)
                return []
        # both are values, check if either one is an Ident
        sub_instrs = []
        p2offset = 0
        if type(command.v1) == Grammar.Ident:
            # just link up immediately
            ref1 = command.v1.name
        else:
            # need to decode (and eval those commands) before linking
            sub_instrs1 = get_instrs_from_command(command.v1, errors, warnings)
            if check_errors(errors): return []
            sub_instrs += sub_instrs1
            ref1 = len(sub_instrs1) - 1
            p2offset = ref1 + 1
        if type(command.v2) == Grammar.Ident:
            ref2 = command.v2.name
        else:
            sub_instrs2 = get_instrs_from_command(command.v2, errors, warnings)
            if check_errors(errors): return []
            ref2 = p2offset + len(sub_instrs2) - 1
            # shift the second instruction references to start at the end of the first
            for part in sub_instrs2:
                # make sure to skip the shifting if it's a variable reference
                part.ref_ids = [i+p2offset if type(i) is int else i for i in part.ref_ids]
            # combine the final lists of instructions with an add on the end
            sub_instrs += sub_instrs2
        # add the final instructions to compare the two results
        reference = len(sub_instrs)-1
        # return instrs + [Instruction("add", ref_ids=[ref1, ref2])]
        if tipe is Grammar.Eq:
            return sub_instrs + [
                Instruction("xor", ref_ids=[ref1, ref2]),           # 0 if the same, trash if different
                Instruction("sltiu", ref_ids=[reference+1], imm=1)  # 1 if the same, 0 if different
            ]
        elif tipe is Grammar.NotEq:
            return sub_instrs + [
                Instruction("xor", ref_ids=[ref1, ref2]),           # 0 if the same, trash if different
                Instruction("sltiu", ref_ids=[reference+1], imm=1), # 1 if the same, 0 if different
                Instruction("xori", ref_ids=[reference+2], imm=1)   # 0 if the same, 1 if different
            ]
        elif tipe is Grammar.Ls:
            return sub_instrs + [
                Instruction("slt", ref_ids=[ref1, ref2])            # 1 if a < b, 0 if a >=b
            ]
        elif tipe is Grammar.GrEq:
            return sub_instrs + [
                Instruction("slt", ref_ids=[ref1, ref2]),           # 1 if a < b, 0 if a >= b
                Instruction("xori", ref_ids=[reference+1], imm=1)   # 0 if a < b, 1 if a >= b
            ]
        elif tipe is Grammar.Gr:
            return sub_instrs + [
                Instruction("slt", ref_ids=[ref2, ref1])            # 1 if b < a, 0 if b >= a
            ]
        elif tipe is Grammar.LsEq:
            return sub_instrs + [
                Instruction("slt", ref_ids=[ref2, ref1]),           # 1 if b < a, 0 if b >= a
                Instruction("xori", ref_ids=[reference+1], imm=1)   # 0 if b < a, 1 if b >= a
            ]
        else:
            errors.append("Unrecognized comparison type: " + tipe)
            return []
    
    

    # do this last so we don't unnecessarily fill registers when immediates would work
    # (later me: don't think that's how that works??)
    elif tipe == Grammar.Integer:
        return [Instruction("li", imm=command.value)]
        
    elif tipe == Grammar.Boolean:
        return [Instruction("li", imm=bool_to_int[command.value])]

    elif tipe == Grammar.Ident:
        errors.append("Shouldn't ever try to convert an identifier to an instruction, yet decoding identifier " + command.name)
        return None

    else:
        errors.append(f"Unrecognized command type {command}")
        return None


def find_open_reg(registers, scopes, curr_ndx):
    """
    goes through the registers and finds the first open one
    @input registers: a list that maps the register number to the index of an instruction,
        the one which generated the number now stored in that register
    @input scopes: a list that maps an instruction index to the index of the last instruction
        that uses its value
    @input curr_ndx: the current instruction index we are on to know where the scope is
    @return reg_num: the register number of the first one that is open for storing data
    """
    # loop through each register number (skipping 0)
    # could use enumerate, but this is clearer to me
    for reg_num in range(1, len(registers)):
        # get the source of the value there
        instr_source = registers[reg_num]
        # get the last time this value is needed
        final_ref = scopes[instr_source]
        # is the last time we needed that value already passed
        # if this is '<' : doesn't allow for register into register writing, ex addi x1, x1, 4 
        if final_ref <= curr_ndx: return reg_num
    # if none of the registers are available, throw an error
    raise RuntimeError("No registers left!")


def find_in_list(lst, item):
    """
    finds the index of a list where some item is located
    @input lst: a list to search through
    @input item: the item to search for (any type, as long as it matches lst)
    @return ndx: the index of the item
    """
    for ndx, val in enumerate(lst):
        if val == item:
            return ndx
    raise RuntimeError(f"Unable to find item {str(item)}")


def find_registers(instructions, errors, warnings):
    """
    given a list of Instruction objects, line up register values for them
    and store this in each instruction
    @input instructions: a list of Instruction objects
    @input errors: a pre-existing list to append our errors to
    @input warnings: a pre-existing list to append our warnings to
    @return: none
    """
    # strip the tags out from the instructions
    tags = [[ref for ref in instr.tags if type(ref) is str] for instr in instructions]
    # create a helper function
    def last_tag(tag, index):
        """find the latest tag of a certain name before a certain index"""
        for ndx in reversed(range(index)):
            if tag in tags[ndx]: return ndx
        return None
    # convert the tag references into index references
    for ndx, instr in enumerate(instructions):
        new_ids = [last_tag(tag, ndx) if type(tag) is str else tag for tag in instr.ref_ids]
        if not all([noo is not None for noo in new_ids]):
            broken = [str(old_id) for (old_id, new_id) in zip(instr.ref_ids, new_ids) if not new_id]
            errors.append("Unable to find a needed reference tag(s) " + ", ".join(broken) + " for instruction number " + str(ndx))
            return
        instr.ref_ids = new_ids

    # find the final instruction where we use a value to know when to let it go out of scope
    # will map the instruction index to the instruction index where the return value is last used
    scopes = [-1 for _ in instructions]
    # go through and update the scopes and tags according to the references
    # by starting at the beginning and going to the end, we overwrite any scope values with the last time they're needed
    for ndx, instr in enumerate(instructions):
        refs = instr.ref_ids
        if refs is not None and len(refs) > 0:
            for ref in refs:
                # # str ref: references an ident/tag
                # if type(ref) is str:
                #     ref_id = last_tag(ref, ndx)
                #     if not ref_id:
                #         errors.append(f"Can't find tag {ref} before where it's needed for instruction number {ndx}")
                #         return
                #     scopes[ref_id] = ndx
                # # int ref: references an index
                # else:
                scopes[ref] = ndx
    
    # a list that maps register number to the reference index of which instruction generated the number stored in it
    registers = [-1 for _ in range(16)]
    registers[0] = len(instructions) # never goes out of scope

    # can use both scopes and registers to get an array that maps the register to its latest scope
    # this is changing though and a waste to update, so just calculate as needed
    # reg2scope = [scope[instr_ndx] for instr_ndx in registers]

    # go through the instructions and link them up
    for i, instr in enumerate(instructions):
        # set a bunch of flags to show what parts we need to decode/store
        # does the instruction have a return value to store in a register rd
        hasReturn = False
        # does the instruction take in an input value from rs1
        hasInput = False
        # does the instruction have a second value from rs2
        hasInput2 = False
        # the immediate should already be stored in the instruction
        op = instr.op
        if op is "li":
            hasReturn = True
        elif op is "mv":
            hasInput = True
            hasReturn = True
        elif op is "prnti":
            pass
        elif op is "prnt":
            hasInput = True
        elif op in ["addi", "subi", "xori", "slti", "sltiu"]:
            hasInput = True
            hasReturn = True
        elif op in ["add", "sub", "xor", "slt"]:
            hasInput = True
            hasInput2 = True
            hasReturn = True
        else:
            errors.append("Unrecognized instruction " + instr.op)
            return

        if hasInput:
            # get the reference to the input value
            val_ref1 = instr.ref_ids[0]
            # find which register holds a value generated by this reference
            try:
                src1 = find_in_list(registers, val_ref1)
            except Exception as e:
                errors.append(e)
                return
            # set the rs1 to this register we found
            instr.rs1 = src1
        if hasInput2:
            # same as for rs1
            try:
                instr.rs2 = find_in_list(registers, instr.ref_ids[1])
            except Exception as e:
                errors.append(e)
                return
        # check the return last so we don't overwrite anything
        if hasReturn:
            # find an open register (can fail and throw if there are none)
            try:
                open_reg = find_open_reg(registers, scopes, i)
            except Exception as err:
                errors.append(f"Error while decoding instruction {str(instr)}: {err}")
                return
            # set this as the output
            instr.rd = open_reg
            # log that this register holds this instruction
            registers[open_reg] = i
    
    # nothing to return, instructions are updated in place


def convert_pseudo(instructions, errors, warnings):
    """
    converts the pseudo instructions in the instructions list into
    their real instructions (in place)
    @input instructions: a list of Instruction objects with registers already set
    @input errors: a pre-existing list to append our errors to
    @input warnings: a pre-existing list to append our warnings to
    @return: none
    """
    for instr in instructions:
        # TODO: replace the "addi" with "ori" to increase proportion of simple commands
        if instr.op == "li":
            # li <rd>, <imm> : loads the immediate into rs1 == addi <rd>, x0, <imm>
            instr.op = "addi"
            instr.rs1 = 0
        elif instr.op == "mv":
            # mv <rd>, <rs1> : copies (moves) the value is rs1 into rd == addi <rd>, <rs1>, 0x0
            instr.op = "addi"
            instr.imm = 0
        # won't hit every case, only those that are pseudo
    # no returns, updated in place


def write_output(filename, instructions, errors, warnings):
    """
    open the file and output the instructions as a json there
    @input filename: the file name or path of where to save our data (should end in .json)
    @input instructions: a list of dicts, each dict representing one single risc-v instruction
    @input errors: a pre-existing list of errors to append ours to
    @input warnings: a pre-existing list of warnings to append ours to
    @return: none
    """
    if filename[-5:] != ".json": filename += ".json"
    try:
        with open("output/" + filename, "w") as outFile:
            json.dump(instructions, outFile, indent=2)
    except Exception as err:
        errors.append(f"Error during writing the output: {err}")


def main(args):
    errors = []
    warnings = []

    if args.debug: print("Importing the grammar...")
    program = import_program_grammar(args.filename, errors, warnings)
    if check_errors(errors, True): return 1

    if args.debug: print("\nConverting the grammar into a list of instructions...")
    instructions = get_instrs_from_program(program, errors, warnings)
    if check_errors(errors, True): return 1
    if args.debug:
        print("The instructions are:")
        # rough calculations to pad the instruction number with 0s
        fill = 3 if len(instructions) >= 100 else (2 if len(instructions) >= 10 else 1)
        for i, instr in enumerate(instructions):
            print(str(i).zfill(fill) + " - " + str(instr))

    if args.debug:
        print("\nFound instructions types:", ", ".join(poss_instructions))
        print()
        print("Linking the instructions to registers...")
    find_registers(instructions, errors, warnings)
    if check_errors(errors, True): return 1

    if args.debug: print("\nConverting pseudo instructions to real ones")
    convert_pseudo(instructions, errors, warnings)

    if args.debug:
        print("Instructions with their registers:")
        for instr in instructions:
            print(" - " + str(instr))
        print("\nCreating the dict format for each instruction")
    json_ready = [instr.to_json() for instr in instructions]

    if args.debug:
        print("The dicts are:")
        for instr in json_ready:
            print(instr)
        print("\nWriting the output to a file...")
    write_output(args.o, json_ready, errors, warnings)
    if check_errors(errors, True): return 1
    
    if len(warnings) > 0:
        print("\nEncountered the following warnings during assembly:")
        for warn in warnings:
            print(warn)
    
    if args.debug: print("Done!")
    return 0


if __name__ == "__main__":
    # to parse the command line arguments nicely
    parser = argparse.ArgumentParser(description = "Assembler for Luka code files")
    parser.add_argument("--version", "-v", action='version', version='Luka version ' + luka_version, help="Gets the version info")
    parser.add_argument("--debug", "-d", action='store_true', help="Turn on debugging mode to print more information")
    parser.add_argument("-o", metavar="output", action='store', default=default_assembler_output, help="The file name or path to store the results into")
    parser.add_argument("filename", action='store', help="The name or relative path to a file to assemble (.py file)")
    args = parser.parse_args()

    sys.exit(main(args))