from params import processor_inputs_file, luka_version
import argparse
import math
import sys

def check_errors(errors, printIt=False):
    """
    check if there are any errors in the given list, printing them if yes, returning whether there were or not
    @input errors: a list of all of the errors encountered
    @input printIt: a boolean of whether we should print an error message or not
        useful since we only print 1 error message in the main function, then immediately exit, others will get passed back
    @return: a boolean of whether there were errors (True) or not (False)
    """
    if len(errors) > 0:
        if printIt:
            print("Decoder: Encountered the following fatal errors:")
            for err in errors:
                print(err)
        return True
    return False


def build_inputs_file(filename, errors, warnings):
    """
    re/creates the inputs.vh file to import whatever our binary file is called
    allows us to keep our verilog files the same, and just change the 3 lines in this file
    the processor will import from the vh_params_file, which should be a single import of our binary filename
    @input filename: the file name or path that stores our binary verilog
    @input errors: a pre-existing list to append our errors to
    @input warnings: a pre-existing list to append our warnings to
    @return: none
    """
    # check the ending to make sure it's a .vh file
    if filename[-3:] != ".vh":
        warnings.append("Binary file's name does not end in .vh")
        filename += ".vh"
    return  [
        "// This file is dynamically generated to just point to the file where our binary is stored",
        "// the include path should be relative to the location of this file",
        f'`include "../output/{filename}"'
        ]


def write_output(filename, lines, errors, warnings, debug=False):
    """
    open the file and write the binary there
    @input filename: the file name or path of where to save our data (should end in .vh)
    @input lines: a list of strings to print to the file (with no newlines at the end)
    @input errors: a pre-existing list of errors to append ours to
    @input warnings: a pre-existing list of warnings to append ours to
    @input debug: should we print information for debugging purposes
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


def build_enums_file(warnings, debug=False):
    """
    @input warnings: a pre-existing list of warnings to append ours to
    @input debug: should we print information for debugging purposes
    @return: a list of strings, each representing a line of our file
    """
    # ALU enums
    ALU_ops = ["noop", "add"]
    if debug: print("Adding ALU enums for:", ALU_ops)
    alu_op_lines = ["parameter e_ALU_" + op + " = " + str(i) + ";" for i, op in enumerate(ALU_ops)]
    alu_lines = ["//ALU Enums"] + alu_op_lines + ["parameter ALU_OP_W = " + str(int(math.ceil(math.log(len(ALU_ops), 2)))) + ";"]

    defines = ["`ifndef ENUMS", "`define ENUMS", ""]
    
    lines = alu_lines # + [""] + 
    
    return defines + lines + ["", "`endif"]


def main(args):
    """
    the main function to execute all other parts of the code
    @input args: an argparse namespace of our command line arguments
    @return: exit code, 0 if it's good
    """
    errors = []
    warnings = []

    # generates the input file with a link to the binary file
    if args.debug: print("Building the linking inputs file")
    input_lines = build_inputs_file(args.filename, errors, warnings)
    if check_errors(errors, True): return 1

    # writes the file out
    if args.debug: print("Writing the linking inputs file")
    write_output(processor_inputs_file, input_lines, errors, warnings, args.debug)
    if check_errors(errors, True): return 1

    # builds the enums file, which enumerates our internal control signal enums for us
    if args.debug: print("Building the enums")
    enums_lines = build_enums_file(warnings, args.debug)

    # writes the file out
    if args.debug: print("Writing the enums file")
    write_output("Verilog/source/Specs/enums.vh", enums_lines, errors, warnings, args.debug)
    if check_errors(errors, True): return 1

    if len(warnings) > 0:
        print("\nEncountered the following warnings while simulating the processor:")
        for warn in warnings:
            print(warn)
    
    if args.debug: print("Done!")
    return 0


if __name__ == "__main__":
    # to parse the command line arguments nicely
    parser = argparse.ArgumentParser(description = "Link our binary vh file into the Processor for Luka")
    parser.add_argument("--version", "-v", action='version', version='Luka version ' + luka_version, help="Gets the version info")
    parser.add_argument("--debug", "-d", action='store_true', help="Turn on debugging mode to print more information")
    parser.add_argument("filename", action='store', help="The name or relative path to a file with the binary instructions (.vh file)")
    args = parser.parse_args()

    sys.exit(main(args))