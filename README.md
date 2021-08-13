# Luka Programming Language
A from-scratch programming language to better understand the full process of compiling, assembling, encoding, and simulating processors.

Files written luka can be given the .luka file extension name.
Some example files are provided to both test that the compiler is running as expected, and to show what the language looks like in practice.
This file is then passed to the different python scripts to convert it step by step into a binary representation.
Running `python step<number><name>.py -o <output file> <input file>` will convert the files through each step of this process.
Running the script with either `-h` or `--help` flags will show the command line options available for that script.

## Compilation Steps

### Step 1: Compiler

Luka Code (.luka) -> Luka Grammar (.py)

The compiler is in charge of converting the code from it's string representation to an actual programmatical representation.
The Grammar.py file describes each piece of the grammar.
There are also "Spec"s built up for each possible class, which specify the class type, a validator to check if that string matches the spec, and a converter to turn the string into that type.
These Specs are prioritized to ensure that we translate the code in the correct ordering
(ex: seeing if it's wrapped in a function > before seeing if there's addition somewhere > before turning the rest into a variable name).

The compiler also includes two "evaluation" abilities.
One is the type checker, which is done automatically to ensure that the types line up correctly.
Specifying either `--execute` or `-e` on the command line will perform a python evaluation of the code, as a quick check if the code runs as expected and produces the desired results.


### Step 2: Assembler

Luka Grammar (.py) -> Modified RISC-V Assembly (.json)


### Step 3: Encoder

Assembly (.json) -> Binary Code (.vh)


### Step 4: Processor

Links up the processor


### Step 5: Simulator

Runs the simulator

## SystemVerilog Processor

Along with the python scripts, I have also built a simple computer processor in SystemVerilog (stored in the Verilog folder).
This is built for a RISC-V architecture, and is a 5 stage pipelined processor.
Since my main focus for this project is the coding language, the processor will likely lag behind the rest of the development.
The tools I've been using to run it are iverilog to compile it, and it's child program vvp to simulate it.
GDKWave has been a useful debugging tool to see the signal levels throughout the program, and I occassionally use a VSCode extension as well.

## Other Notes

params.py contains some notes on the language, like the version.
It also contains the typical names for the output files, if there isn't one specified.
These may be useful to see how the data is transformed and what file formats I use to represent each step.