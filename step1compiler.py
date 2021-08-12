"""
The compiler is the first step in the process
It compiles luka code into their Grammar representaions,
    where the program is stored in a nested-object way
This compiler takes in Luka (.luka) files and outputs python (.py) files
"""

import sys
import argparse
from Grammar import decode_command, Program, print_specs
from params import default_compiler_output, luka_version

def get_file_contents(filename, warnings, errors):
    """
    opens the specified file, exiting if it isn't found,
    and returning the lines of that file
    @input filename: the name or path of the file to read from
    @input - warning: the existing list of warnings to append our warnings to
    @input - errors: the existing list of errors to append ours to
    @return lines: a list of the lines of the file
    """
    # check if it's a .luka extension
    if filename[-5:] != ".luka":
        warnings.append("Given file name does not end in .luka")
        filename += ".luka"
    try:
        with open(filename) as file:
            lines = file.read().split("\n")
    except FileNotFoundError:
        errors.append(f"Failed to find the file {filename}")
        return None
    except:
        errors.append(f"Failed to open the file {filename}")
        return None
    return lines


def decode_lines(lines, warnings, errors, debugMode=False):
    """
    decodes the given lines into a grammar style program
    @input - lines: a list of the lines of a program
    @input - warning: the existing list of warnings to append our warnings to
    @input - errors: the existing list of errors to append ours to
    @input showLines: whether the compiler should print its decision for each line or not
    @return (prog): a Program object representing the final program
    """
    commands = []
    for i, line in enumerate(lines):
        # the line numbers usually start at 1
        i = i+1
        # check for line comments
        comment = line.split("//")
        if len(comment) > 1: line = comment[0]
        # remove white space
        line = line.strip()
        # ignore if empty
        if len(line) == 0:
            # commands.append(Noop())
            continue

        # split the line into the commands by semicolons, warning if it doesn't end with one
        commands_in_line = line.split(";")
        if commands_in_line[-1] != "":
            warnings.append(f"Line {i} does not end in a semicolon")
        else:
            commands_in_line = commands_in_line[:-1]

        # decode each command in that line
        decode_hist = []
        for command in commands_in_line:
            command = command.strip()
            try:
                decoded = decode_command(command)
            except Exception as err:
                errors.append(f"Error decoding command '{command}' (line {i}): {err}")
                return None
            decode_hist.append(decoded)
        
        # give them all line numbers
        for command in decode_hist:
            command.line_number = i
        
        # add the commands for that line into our total list
        commands += decode_hist

        if debugMode:
            decode_hist = " ".join([(str(dec)+";") for dec in decode_hist])
            print(f"Line {i}: {decode_hist}")
    
    if debugMode: print()
    return Program(commands)


def output_to_file(program, filename, classes_needed):
    """
    take in a program and write it to the given python file
    @input program: a Program object representing our compiled program's grammar
    @input filename: the location to write our grammar to
    @input classesNeeded: a list of the classes in our program that we will need to import (as just strings, no <class ''>)
    @return: none
    """
    if filename[-3:] != ".py": filename += ".py"
    with open("output/" + filename, 'w') as outFile:
        outFile.write("from Grammar import " + ", ".join(classes_needed))
        outFile.write("\nprogram = " + str(program) + "\n")
        # poi


def main(args):
    """
    performs all of the main functionality of the compiler
    @input args: the argparse command line arguments, stored as a Namespace
        filename: a string of the filename or relative path to the file we want to compile
        debug: a boolean flag for whether we are in debugging mode or not, and should print more information
    @input showLines: whether the compiler should print its decision for each line or not
    @return: the final status of the program, 0 if okay
    """
    # variables to log our compiler errors and warnings
    warnings = []
    errors = []

    if args.debug:
        print_specs()
        print()
    
    if args.debug: print("Opening the file")
    lines = get_file_contents(args.filename, warnings, errors)
    if len(errors) > 0:
        print("Encountered the following errors in opening the file:")
        for err in errors:
            print(err)
        return 1
    
    if args.debug:
        print()
        print("Compiling...")
    
    program = decode_lines(lines, warnings, errors, args.debug)
    if len(errors) > 0:
        print("Encountered the following errors in compiling:")
        for err in errors:
            print(err)
        return 1

    if args.debug:
        print("Checking the data types...")

    if not program.type_check(errors, args.debug):
        print("Type error encountered during compilation:")
        for err in errors:
            print(err)
        return 1
    
    if args.debug:
        print()
        print("Final grammar:")
        print(str(program))
        print()

    if args.execute:
        if args.debug: print("Executing...")
        print("Execution results:\n---")
        program.py_run()
        print("---\n")
    
    if args.debug: print("Outputting results into a file...")
    classes_needed = program.classes_used()
    # convert them to a string and cut off the beginning <class 'Grammar. and ending '>
    classes_needed = [str(item)[16:-2] for item in classes_needed]
    output_to_file(program, args.o, classes_needed)
    if args.debug: print()

    if len(warnings) > 0:
        print("Encountered the following warnings during compilation:")
        for warn in warnings:
            print(warn)
        print()
    
    if args.debug: print("Done!")
    return 0

if __name__ == "__main__":
    # to parse the command line arguments nicely
    parser = argparse.ArgumentParser(description = "Compiler for Luka code files")
    parser.add_argument("--version", "-v", action='version', version='Luka version ' + luka_version, help="Gets the version info")
    parser.add_argument("--debug", "-d", action='store_true', help="Turn on debugging mode to print more information")
    parser.add_argument("--execute", "-e", action='store_true', help="Execute the code in python to test its functionality")
    parser.add_argument("-o", metavar="output", action='store', default=default_compiler_output, help="The file name or path to store the results into")
    parser.add_argument("filename", action='store', help="The name or relative path to a file to compile (.luka file)")
    args = parser.parse_args()

    sys.exit(main(args))