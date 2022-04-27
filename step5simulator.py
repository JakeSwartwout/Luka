import os
from params import processor_inputs_file, default_outfile, luka_version
import argparse
import os
import subprocess
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


def get_needed_files(inputs_file):
    """
    collects a list of the files that will be needed to compile the verilog processor
    to pass to IVerilog with -c
    """
    return [
        "Processor.sv",
        # "Simulator.sv",
        inputs_file,
        "Stages/stg_1_IF.sv",
        "Stages/stg_2_ID.sv",
        "Stages/stg_3_EX.sv",
        "Stages/stg_4_ME.sv",
        "Stages/stg_5_WB.sv",
        "Specs/specs.vh",
        "Specs/opcodes.vh",
        "Specs/SDRAM_interface.sv",
        "Specs/enums.vh",
        "Helpers/bin2bcd.sv",
        "Helpers/clockDivider.sv",
        "Helpers/instructionDecoder.sv",
        "Helpers/registerFile.sv",
        "Helpers/instructionMemory.sv"
        "Helpers/sevenSegToValue.sv",
        "Helpers/valueToDisplay.sv",
        "Helpers/valueToSevenSeg.sv"
    ]


def write_output(filename, lines, errors, warnings, debug=False):
    """
    open the file and write the binary there
    @input filename: the file name or path of where to save our data (should end in .vh)
    @input lines: a list of strings to print to the file (with no newlines at the end)
    @input errors: a pre-existing list of errors to append ours to
    @input warnings: a pre-existing list of warnings to append ours to
    @input debug: whether we are in debug mode or not (to print more information)
    @return: none
    """
    if filename[-4:] != ".txt":
        warnings.append("File " + filename + " does not end in txt, adding it")
        filename += ".txt"

    # add new-lines to each line
    lines = [line + "\n" for line in lines]

    try:
        with open(filename, "w") as outFile:
            outFile.writelines(lines)
    except Exception as err:
        errors.append(f"Error while writing the output: {err}")


def compile_code(files_list_filename, out_filename, errors, warnings, debug=False):
    """
    run the command to compile the verilog processor (using iverilog) into a .out file
    @input files_list_filename: the file that holds a list of files we need to import
    @input out_filename: what we would like to name the output
    @input errors: a pre-existing list to append our errors to
    @input warnings: a pre-existing list to append our warnings to
    @input debug: whether we are in debug mode or not (to print more information)
    @return: none
    """
    # check the ending to make sure it's a .out file
    if out_filename[-4:] != ".out":
        warnings.append("Resulting out-file's name does not end in .out, it is '" + out_filename + "'")
        out_filename += ".out"

    # run the command
    # -g2012 uses a newer version of iverilog
    # -Dimports defines the imports flag, so that we ignore our imports and pass in the files ourselves
    # -o {out_filename} names the resulting file what we want
    # -c {files_list_filename} lists out the files to take modules from
    # Simulator.sv   the top file we are compiling
    command = f"iverilog -g2012 -Dimports -o ../output/{out_filename} -c {files_list_filename} Simulator.sv"
    if debug: print(">", command)
    try:
        iverilog_output = subprocess.run(command, cwd="Verilog/", shell=True, capture_output=True, check=False);
        if iverilog_output.returncode is not 0:
            err = iverilog_output.stderr
            if type(err) is bytes:
                err = err.decode('UTF-8')
            errors.append("Issue with iverilog:\n" + str(err))
            return
    except Exception as e:
        errors.append("Error compiling processor/simulator: " + str(e))


def simulate_code(out_filename, txt_filename, errors, warnings, debug=False):
    """
    run the command to simulate the compiled processor, both capturing the result into a file and generating a vcd
    @input out_filename: the name of our processor and simulator compiled by Iverilog, as a .out file
    @input txt_filename: the name of the file we would like to store the results into, or None to not save or print
    @input errors: a pre-existing list to append our errors to
    @input warnings: a pre-existing list to append our warnings to
    @input debug: whether we are in debug mode or not (to print more information)
    @return: none
    """
    # check the ending to make sure it's a .out file
    if out_filename[-4:] != ".out":
        warnings.append("out-file's name does not end in .out, it is '" + out_filename + "'")
        out_filename += ".out"

    if txt_filename is not None:
        # check the ending to make sure it's a .txt file
        if txt_filename[-4:] != ".txt":
            warnings.append("txt-file's name does not end in .txt, it is '" + txt_filename + "'")
            txt_filename += ".txt"

        # run the command
        command = f"vvp {out_filename} > {txt_filename}"
    # if txt_filename is None:
    else:
        command = f"vvp {out_filename}"

    if debug: print(">", command)

    try:
        vvp_output = subprocess.run(command, cwd="output/", shell=True, capture_output=True, check=False);
        if vvp_output.returncode is not 0:
            errors.append("Issue with vvp: " + str(vvp_output.stderr))
            return
    except Exception as e:
        errors.append("Error during simulation: " + str(e))


def print_results(txt_filename, warnings):
    """
    opens the file that we stored our simulation results into and prints the contents
    @input txt_filename: the name of the file where we saved the simulation results, None to not print anything
    @input warnings: a pre-existing list to append our warnings to
    @return: none
    """
    if txt_filename is None:
        return
    
    # check the ending to make sure it's a .txt file
    if txt_filename[-4:] != ".txt":
        warnings.append("File given for printing does not end in .txt, it is '" + txt_filename + "'")
        txt_filename += ".txt"

    try:
        with open("output/" + txt_filename, "r", encoding="utf-8") as file:
            contents = file.read()
        print(contents)
    except Exception as e:
        warnings.append("Error while opening file: " + str(e))
    

def open_gtkwave(vcd_filename, errors, warnings, debug=False):
    """
    opens gtkwave with the specified vcd file
    @input vcd_filename: the filename of the .vcd file that we want to open
    @input errors: a pre-existing list to append our errors to
    @input warnings: a pre-existing list to append our warnings to
    @input debug: whether we are in debug mode or not (to print more information)
    @return: none
    """
    vcd_filename = str(vcd_filename)

    # check the ending to make sure it's a .txt file
    if vcd_filename[-4:] != ".vcd":
        warnings.append("Given file is not a vcd, assuming it is one anyway, it is '" + vcd_filename + "'")
        vcd_filename += ".vcd"

    command = "gtkwave " + vcd_filename
    if debug: print(">", command)
    try:
        gtk_output = subprocess.run(command, cwd="output/", shell=True, capture_output=True, check=False);
        if gtk_output.returncode is not 0:
            errors.append("Issue with gtkwave: " + str(gtk_output.stderr))
            return
    except Exception as e:
        warnings.append("Error opening gtkwave: " + str(e))


def main(args):
    """
    the main function to execute all other parts of the code
    @input args: an argparse namespace of our command line arguments
    @return: exit code, 0 if it's good
    """
    errors = []
    warnings = []

    s_necessary_files = "NecessaryFiles.txt"

    # generate the list of files
    if args.debug: print("Getting a list of the necessary files")
    files_list = get_needed_files(processor_inputs_file)
    write_output("./Verilog/" + s_necessary_files, files_list, errors, warnings, args.debug)
    if check_errors(errors, True): return 1

    # compile the code to a .out file
    if args.debug: print("Compiling the processor/simulator")
    compile_code(s_necessary_files, args.o, errors, warnings, args.debug)
    if check_errors(errors, True): return 1

    # run the .out file with vvp to generate a .vcd and a .txt of the printing
    if args.debug: print("Running the simulation")
    simulate_code(args.o, args.save, errors, warnings, args.debug)
    if check_errors(errors, True): return 1

    # print the results
    if args.debug: print("Printing the processor results:")
    print_results(args.save, warnings)

    # open gtkwave if we want
    if args.gtkwave:
        if args.debug: print("Opening gtkwave...")
        open_gtkwave("simulation.vcd", errors, warnings, args.debug)

    if len(warnings) > 0:
        print("\nEncountered the following warnings while simulating the processor:")
        for warn in warnings:
            print(warn)
    
    if args.debug: print("Done!")
    return 0


if __name__ == "__main__":
    # to parse the command line arguments nicely
    parser = argparse.ArgumentParser(description = "Simulate the Processor for Luka")
    parser.add_argument("--version", "-v", action='version', version='Luka version ' + luka_version, help="Gets the version info")
    parser.add_argument("--debug", "-d", action='store_true', help="Turn on debugging mode to print more information")
    parser.add_argument("-o", metavar="output", action='store', default=default_outfile, help="The file name or path to store the .out file")
    parser.add_argument("--gtkwave", "-g", action='store_true', help="Open gtkwave on the simulation results")
    parser.add_argument("--save", "-s", action='store', default=None, help="The name of the file to store the text-based simulation outputs")
    args = parser.parse_args()

    # parser.print_help()

    sys.exit(main(args))