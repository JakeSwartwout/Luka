"""
The encoder is the third step in the process
It encodes the assembly instructions as binary for the processor
This assembler takes in JSON (.json) files and outputs System Verilog Header (.vh) files
"""

import Instructions
from params import default_assembler_output, default_decoder_output, luka_version
from Encodings import choose_type, get_all_defined_instrs
import json
import argparse
import sys
import math


def check_errors(errors, printIt=False):
    """
    check if there are any errors in the list, printing them if yes, returning whether there were or not
    @input errors: a list of all of the errors encountered
    @input printIt: a boolean of whether we should print an error message or not
        useful since we only print 1 error message in the main function, then immediately exit, others will get passed back
    @return: a boolean of whether there were errors (True) or not (False)
    """
    if len(errors) > 0:
        if printIt:
            print("Decoder: Encountered the following fatal errors:")
            for err in errors:
                print("X -", err)
        return True
    return False


def build_default_specs():
    """
    generates the default specification variables for our Processor
    @input: none
    @return: a dict mapping {"PARAM_NAME": "PARAM_VALUE"}, both strings
    """
    return {
        "VALUE_W": "16",

        "INSTR_W": "19",

        "NUM_REG": "16",
        "REG_ADDR_W": "4",

        "IMM_W": "5",
        "UIMM_W": "11",

        "NUM_INSTRS": "0",
        "INSTR_ADDR_W": "0",
    }


def get_opcode_values():
    """
    generates the default specification variables for our Processor
    @input: none
    @return: a dict mapping {"OPCODE": "VALUE"}, both strings
    """
    # get the instruction types we support
    all_instrs = get_all_defined_instrs()
    
    # get the fn3 and opcode values for each
    def choose_and_get(instr):
        tipe = choose_type(instr)
        return tipe.get_opcode(tipe, instr)
    opcodes = {instr: choose_and_get(instr) for instr in all_instrs}

    # get the first instruction opcode to know how long each one should be
    op_w = len(opcodes[all_instrs[0]][1])

    # start a dict of all the params we'll have
    all_opcodes = {
        "OPTYPE_W": str(op_w)
    }

    # get all of the fn3 and opcode values
    for instr in opcodes.keys():
        fn3, opcode = opcodes[instr]
        assert len(opcode) == op_w, f"Opcode for instruction {instr} is not the correct size of {op_w}, got the value {opcode}"
        all_opcodes["OPCODE_"+instr] = opcode
        if len(fn3) > 0:
            all_opcodes["FN3_"+instr] = fn3

    return all_opcodes


def build_parameters_file(params, definition, errors, warnings):
    """
    builds the lines needed for the specs file
    @input params: a dict of the parameter values, mapped as {"PARAM_NAME": "PARAM_VALUE"}
    @definition: what to call the definition for these values, None to not define them
    @input errors: a pre-existing list of errors to append ours to
    @input warnings: a pre-existing list of warnings to append ours to
    @return lines: a list of the lines for the parameters file
    """
    define_lines = ["`ifndef " + definition, "`define " + definition, ""]

    normal_lines = {name: f"parameter {name} = {params[name]};" for name in params}

    # check if we can give it a description
    known_descriptions = {
        "VALUE_W": "the width of a value",
        "NUM_REG": "the number of registers",
        "REG_ADDR_W": "the number of bits to address a register",
        "IMM_W": "the length of an immediate",
        "UIMM_W": "the length of an upper immediate",
        "NUM_INSTRS": "how many instructions we have",
        "INSTR_ADDR_W": "how many bits the address of the instruction is (pc length)",
        "INSTR_W": "the length of an instruction",
        "OPTYPE_W": "how many bits to describe the type of instruction",
        "FN3_W": "the number of bits for the fn3 code",
        "OPCODE_W": "how many total bits of the instruction the opcode takes",
        "ALU_OP_W": "the log2 of the number of operations the ALU can perform"
    }
    for name in normal_lines:
        if name in known_descriptions:
            normal_lines[name] += " // " + known_descriptions[name]
    
    if definition is not None:
        return define_lines + [line for line in normal_lines.values()] + ["", "`endif"]
    else:
        return [line for line in normal_lines.values()]


def open_instructions(filename, errors, warnings):
    """
    open the json file at the location and retrieve the instructions list
    the instructions will take the form {"op": "<command>", "rd:":<val>, "rs1":<val>, "rs2":<val>, "imm":<val>}
    @input filename: the name or path of the file to open
    @input errors: a pre-existing list of errors to append our errors to
    @input warnings: a pre-existing list of warnings to append our issues to
    @input debug: if we are in debugging mode or not
    @return instructions: a list of dicts representing the program instructions
    """
    # remove .json from the file name
    if filename[-5:] != ".json":
        warnings.append("Given filename doesn't end with .json")
        filename += ".json"

    # look in the right folder
    filename = "output/" + filename

    # load the json
    try:
        with open(filename) as file:
            instructions = json.load(file)
    except FileNotFoundError as err:
        errors.append(f"Failed to find the file {filename}: {err}")
        return None
    except Exception as err:
        errors.append(f"Failed to open or load the file {filename}: {err}")
        return None
    return instructions


def convert_instruction(instruction, errors, warnings, debug=False):
    """
    converts a single instruction into binary code
    @input instruction: a dict representing the instruction
    @input errors: a pre-existing list to append our errors to
    @input warnings: a pre-existing list to append our warnings to
    @input debug: if we are in debugging mode or not
    @return binary: a string of 1s and 0s of our instruction
    """
    if "op" not in instruction:
        errors.append("Instruction does not contain op field")
        return ""

    if debug: print("Got instruction:", instruction)
    try:
        instr_class = choose_type(instruction["op"])
        instantiation = instr_class(instruction)
        binary = instantiation.get_binary()
    except ValueError as err:
        errors.append("Value Error in converting the instruction: " + str(err))
        return ""
    except Exception as err:
        errors.append("Unrecognized error in instruction conversion: " + str(err))
        return ""

    return binary


def convert_all_instructions(instructions, errors, warnings, debug=False):
    """
    converts an entire list of instructions into their binary code
    @input instructions: a list of all of the instructions as dicts
    @input errors: a pre-existing list to append our errors to
    @input warnings: a pre-existing list to append our warnings to
    @input debug: if we are in debugging mode or not
    @return binary: a list of binary instruction strings
    """
    binary = []
    # loop through all of our instructions
    for instr in instructions:
        # convert it to binary
        bin_instr = convert_instruction(instr, errors, warnings, debug=False)
        if check_errors(errors): return []
        binary.append(bin_instr)

    return binary


def convert_binary_to_verilog(binaries, specs, errors, warnings, debug=False):
    """
    given all of the binary instructions, convert it to a format that
    system verilog can recognize in the form of a .vh file
    @input binaries: a list of strings for the binaries
    @input specs: a dict mapping "PARAM_NAME":"PARAM_VALUE" (both strings) of specs for our program
    @input errors: a pre-existing list to append our errors to
    @input warnings: a pre-existing list to append our warnings to
    @input debug: if we are in debugging mode or not
    @return lines: a list of strings for the lines of our system verilog header file
    """
    # the size of one instruction
    bnry_len = len(binaries[0])
    
    # start with a noop
    noop_binary = "".join(["0" * bnry_len])
    noop = "    " + str(bnry_len) + "'b" + noop_binary
    lines = [noop]

    # check that they all are the same length and add commas to the lines
    for i, bnry in enumerate(binaries):
        if len(bnry) != bnry_len:
            errors.append("Binary instruction number " + str(i) + " is not the same length as the ones so far")
            return []
        lines.append("    " + str(bnry_len) + "'b" + bnry + ",") # ex:    32'b0010010011...010100100,
    
    # reverse them, as the first instruction will be last in the list due to [max:0] ordering
    lines = [line for line in reversed(lines)]

    # define some parameters for the instructions
    define_lines = ["`ifndef INSTRUCTIONS", "`define INSTRUCTIONS", "", '`include "Specs/specs.vh"']

    
    # update our specs
    num_instrs = len(lines)
    specs["NUM_INSTRS"] = str(num_instrs)

    instr_w = str(bnry_len)
    specs["INSTR_W"] = instr_w

    instr_addr_w = str(int(math.ceil(math.log2(num_instrs))))
    specs["INSTR_ADDR_W"] = instr_addr_w

    var_def_line = "logic [NUM_INSTRS-1:0][INSTR_W-1:0] instr_mem = {"
    
    # close and return the variable
    return define_lines + ["", var_def_line] + lines + ["};", "", "`endif"]


def write_output(filename, lines, errors, warnings, debug=False):
    """
    open the file and write the binary there
    @input filename: the file name or path of where to save our data (should end in .vh)
    @input lines: a list of strings to print to the file (with no newlines at the end)
    @input errors: a pre-existing list of errors to append ours to
    @input warnings: a pre-existing list of warnings to append ours to
    @return: none
    """
    if filename[-3:] != ".vh": filename += ".vh"

    # add new-lines to each line
    lines = [line + "\n" for line in lines]

    try:
        with open(filename, "w") as outFile:
            outFile.writelines(lines)
    except Exception as err:
        errors.append(f"Error while writing the output: {err}")


def main(args):
    errors = []
    warnings = []

    if args.debug: print("Reading the instructions...")
    instruction_dicts = open_instructions(args.filename, errors, warnings)
    if check_errors(errors, True): return 1
    if args.debug:
        print("\nGot the following instructions:")
        for instr in instruction_dicts:
            print(" -", str(instr))

    if args.debug: print("\nGetting the default specs values...")
    specs = build_default_specs()

    if args.debug: print("\nConverting the instructions into binary...")
    binary = convert_all_instructions(instruction_dicts, errors, warnings, args.debug)
    if check_errors(errors, True): return 1
    if args.debug:
        print("The binary is:")
        for bnry in binary:
            print(" -", bnry)

    if args.debug: print("\nConverting into System Verilog format...")
    verilog = convert_binary_to_verilog(binary, specs, errors, warnings, args.debug)
    if check_errors(errors, True): return 1

    if args.debug:
        print("\nWriting the verilog binary to a file...")
        print("Got verilog lines:")
        for line in verilog:
            print(line)
    write_output("output/" + args.o, verilog, errors, warnings, args.debug)
    if check_errors(errors, True): return 1

    if args.debug: print("\nWriting the specs file...")
    specs_file = build_parameters_file(specs, "PARAMETERS", errors, warnings)
    if check_errors(errors, True): return 1
    if args.debug:
        print("Got lines:")
        for line in specs_file:
            print(line)
    write_output("Verilog/Specs/specs.vh", specs_file, errors, warnings, args.debug)
    if check_errors(errors, True): return 1

    if args.debug: print("\nWriting the opcodes file...")
    opcodes = get_opcode_values()
    opcodes_lines = build_parameters_file(opcodes, "opcodes", errors, warnings)
    write_output("Verilog/Specs/opcodes.vh", opcodes_lines, errors, warnings, args.debug)
    if check_errors(errors, True): return 1

    if args.debug: print()
    
    if len(warnings) > 0:
        print("Encountered the following warnings during decoding:")
        for warn in warnings:
            print(warn)
    
    if args.debug: print("Done!")
    return 0


if __name__ == "__main__":
    # to parse the command line arguments nicely
    parser = argparse.ArgumentParser(description = "Encoder for Luka code files")
    parser.add_argument("--version", "-v", action='version', version='Luka version ' + luka_version, help="Gets the version info")
    parser.add_argument("--debug", "-d", action='store_true', help="Turn on debugging mode to print more information")
    parser.add_argument("-o", metavar="output", action='store', default=default_decoder_output, help="The file name or path to store the results into")
    parser.add_argument("filename", action='store', help="The name or relative path to a file to encode (.json file)")
    args = parser.parse_args()

    sys.exit(main(args))