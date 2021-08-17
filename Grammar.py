from abc import ABC, abstractmethod
from enum import Enum

# the different final data types Luka supports
type_names = {"void": None}
type_classes = {None: ""}

class priority(Enum):
    """
    the priority/ ordering in which to search for commands in the spec list
    ie, PEMDAS but for computers
    Goes outside to in, so not quite the same order as expected
    """
    v = 1 # variable assignments
    p = 2 # parentheses
    f = 3 # function
    c = 4 # comparison operators
    a = 5 # addition / subtraction
    m = 6 # multiplication / division
    i = 7 # constant / Identifiers (variables)
# the nice names for them all
priority_names = {
    priority.v: "variableAssignments",
    priority.p: "parentheses",
    priority.f: "function",
    priority.c: "comparisons",
    priority.a: "addition/subtraction",
    priority.m: "multiplication/division",
    priority.i: "constant/identifiers"
}

# the specifications for each command we can encounter
# it maps the evaluation priority to a list of Spec objects
command_specs = {clas:[] for clas in priority}
# command_specs.append(Spec(, start="", end=""))

class Spec:
    """
    a specification for how to represent a command in Luka
    useful for translating from Luka to the grammar
    """
    def __init__(self, command, validate, convert):
        # the class for that given command
        self.command_type = command
        # the function which takes in a string and returns whether it is vaild or not
        # @input string: the string to check if it's valid
        # @return boolean: whether it is valid under this Spec or not
        self.validate = validate
        # the convert function takes in a luka string that is valid under this spec and
        # does the necessary conversions on it, returning a completed Command object
        # @input string: the entire string of the command to convert
        # @return Command: the Command form of that string
        # @throw: whatever decode_command throws, due to a string found not matching a spec
        self.convert = convert

    def __str__(self):
        return str(self.command_type)[16:-2] + "Spec"


def print_specs():
    """
    a utility for debugging that prints all of the specifications that we've generated
    @input: none
    @return: none
    """
    print("Generated the following specs:")
    for clas in command_specs:
        lst = command_specs[clas]
        if len(lst) > 0:
            lst = [str(i) for i in lst]
            print(f"Class {priority_names[clas]} contains specs for:", ", ".join(lst))

    
def function_type_spec(command_type, start, minlen, end):
    """
    call this to generate the validation and conversion functions for a function type of Command
    this means it starts with some string, ends with some string, and has some minimum length string in the middle
    that must recursively be decoded
    @input command_type: the class name of the specific command
    @input start: the string that the input should begin with
    @input minlen: the minimum length of the string in the middle
    @input end: the string that the input should end with
    @return: a created spec with the needed validation and conversion elements
    """
    startlen = len(start)
    endlen = len(end)

    def function_type_validation(string):
        """
        interpret the given string according to the known specifications,
        returning the middle string and None otherwise
        @input string: the string to decode
        @return middle: the string left over in the middle of the spec after removing and validating the other parts
        """
        # match start
        if not string.startswith(start):
            return False

        # match ending
        # find the first occurrence of the ending sequence
        earliest_end = string.find(end)
        if earliest_end == -1: return False
        # # make sure it's at the end
        # if earliest_end != len(string) - endlen:
        #     return False

        # middle length
        middle = len(string) - startlen - endlen
        if middle < minlen:
            raise SyntaxError(f"Command {command_type} expects syntax of {start}<len {minlen}+>{end}")
        
        return True

    def function_type_conversion(string):
        middle = string[startlen:-endlen]
        return command_type(decode_command(middle))

    return Spec(command_type, function_type_validation, function_type_conversion)


# keep a list of the symbols we have to go by the longest ones first (to not break them up)
# maps {len(symb) : [symb, othr, more, else]}
comparison_symbols_list = {}
def comparison_type_spec(command_type, symbol):
    """
    call this to generate the validation and conversion functions for a Comparison Command
    should have 2 inputs split by some symbol
    @input command_type: the class name of the specific command
    @input symbol: the string that the input should search for
    @return: a created spec with the needed validation and conversion elements
    """
    # add this new symbol to the list
    global symbols_list
    if len(symbol) in comparison_symbols_list:
        comparison_symbols_list[len(symbol)].append(symbol)
    else:
        comparison_symbols_list[len(symbol)] = [symbol]

    def comparison_type_validation(string):
        global symbols_list
        # go through those symbols larger than this one
        this_len = len(symbol)
        for othr_len in sorted(comparison_symbols_list.keys(), reverse=True):
            # stop once we reach this length
            if othr_len <= this_len: break
            # make sure the larger symbols doesn't match
            if any([othr in string for othr in comparison_symbols_list[othr_len]]): return False
        # check if this symbol matches
        return symbol in string

    def comparison_type_conversion(string):
        part1, part2 = tuple(string.rsplit(symbol, 1))
        part1 = decode_command(part1)
        part2 = decode_command(part2)
        return command_type(part1, part2)

    return Spec(command_type, comparison_type_validation, comparison_type_conversion)


def decode_command(string):
    """
    takes in a single command in luka format and decodes what it's supposed to be in grammar format
    @input string: the input command in luka file format (a string)
    @return command: the interpreted command as a Command object
    """
    global command_specs

    # clean it up a little bit
    string = string.strip()

    # go in order of the priorities:
    for clss in priority:
        # check it against each spec
        for spec in command_specs[clss]:
            if spec.validate(string):
                return spec.convert(string)

    # haven't found anything, not a valid command
    raise ValueError(f"Unrecognized command '{string}'")


class Program():
    """
    the overall program
    consists of any number of expressions to perform
    """
    def __init__(self, commands=[]):
        """
        @input commands: a list of Command objects representing the program
        """
        self.commands = [comm for comm in commands if isinstance(comm, Command)]
        diff = len(commands) - len(self.commands)
        assert diff == 0, f"Program created with {diff} non-Command item(s)"

    def __str__(self):
        output = "Program([\n\t"
        command_strs = [str(command) for command in self.commands]
        output += ",\n\t".join(command_strs)
        # for command in self.commands:
        #     output += "\n  " + str(command)
        return output + "\n])"
    
    def add_command(self, command):
        """
        adds a new command to the end of the current list of commands
        @input command: the Command object to be added
        @return: none
        """
        self.commands.append(command)
    
    def py_run(self):
        """
        run/evaluate each command in the program in python
        @input: none
        @return: the return value generated
        @throw: RuntimeError if something could not be evaluated
        """
        # starts with an empty environment
        env = {}
        for command in self.commands:
            val, env = command.py_eval(env)
        return val

    def type_check(self, errors, debug_mode=False):
        """
        evaluate the program to ensure all of the data types match and join correctly
        @input - errors: the existing list of errors to append ours to
        @input - debug_mode: True if we should show/print our process, False to not print anything
        @return: True if there are no errors, False if something failed (info on how stored in the errors list)
        """
        env = {}
        for command in self.commands:
            if debug_mode: print("- " + str(command))
            try:
                _, env = command.type_eval(env)
            # TODO: add other non-fatal exception types to show mutliple type errors at once
            except Exception as e:
                err_response = "Data type failure"
                if command.line_number:
                    err_response += " for command on line " + str(command.line_number)
                err_response += ": " + str(e)
                errors.append(err_response)
                return False
        return True
    
    def classes_used(self):
        """
        gets a list of the classes used by recursively searching all commands in the program
        @input: none
        @return classes: a Set() object of the classes (as classes, not strings)
        """
        classes = set([Program])
        for comm in self.commands:
            sub_classes = comm.classes_used()
            classes.update(sub_classes)
        return classes



def merge_2_subclasses(clas, sub1, sub2):
    classes = set([clas])
    sub_classes1 = sub1.classes_used()
    classes.update(sub_classes1)
    sub_classes2 = sub2.classes_used()
    classes.update(sub_classes2)
    return classes



class Element(ABC):
    """
    the base class for all other code Elements to inherit from
    any type of element, could be a single command, a group of commands in a scope, or something to change the flow of execution
    """
    def __init__(self):
        self.line_number = None
        pass
    
    @abstractmethod
    def __str__(self):
        return "Element"
    
    @abstractmethod
    def py_eval(self, env):
        """
        evaluates the value of this expression in python
        @input env: the environment under which to evaluate this statement
        @return: the result of the evaluation
        @return: the new environment after evaluation
        """
        pass

    @abstractmethod
    def type_eval(self, env):
        """
        evaluates the data type of this command
        @input env: the environment under which to evaluate this statement
        @return: the result of the evaluation
        @return: the new environment after evaluation
        @throw: throws an exception if there is a type mismatch error
        """
        pass

    @abstractmethod
    def classes_used(self):
        """
        gets a list of the classes used by recursively searching all commands that may be stored inside this one
        @input: none
        @return classes: a Set() object of the classes (as classes, not strings)
        """
        return set([Element])


class Command(Element):
    """
    the base Command class for most others to inherit from
    any type of single-action command to perform
    """
    def __init__(self):
        pass
    
    @abstractmethod
    def __str__(self):
        return "Command"
    
    @abstractmethod
    def py_eval(self, env):
        pass

    @abstractmethod
    def type_eval(self, env):
        pass

    @abstractmethod
    def classes_used(self):
        return set([Command])


class NoReturnCommand(Command):
    """
    an expression which doesn't have any return
    """
    @abstractmethod
    def __str__(self):
        return "NoReturnCommand"
    def py_eval(self, env):
        return None, env
    def type_eval(self, env):
        return None, env
    @abstractmethod
    def classes_used(self):
        return set([NoReturnCommand])


class Noop(NoReturnCommand):
    """
    a no-operation action
    does nothing
    """
    def __str__(self):
        return "Noop"
    def classes_used(self):
        return set([Noop])
# purely Grammar side, won't show up in code


class Print(NoReturnCommand):
    """
    a shortcut to run python's print function
    """
    def __init__(self, value):
        assert isinstance(value, ReturnCommand), f"Input to print is not a returning command, it's a {type(value)}"
        self.value = value
    def __str__(self):
        return "Print(" + str(self.value) + ")"
    def py_eval(self, env):
        val, new_env = self.value.py_eval(env)
        print(val)
        return None, new_env
    def type_eval(self, env):
        tipe, new_env = self.value.type_eval(env)
        assert tipe in type_names.values(), str(tipe) + " is not a printable data type"
        return None, new_env
    def classes_used(self):
        classes = set([Print])
        sub_classes = self.value.classes_used()
        classes.update(sub_classes)
        return classes
command_specs[priority.f].append( function_type_spec(Print, "print(", 1, ")") )


class ReturnCommand(Command):
    """
    the base class for commands that return some value
    """
    @abstractmethod
    def __str__(self):
        return "ReturnCommand"
    
    @abstractmethod
    def py_eval(self, env):
        """
        evaluates the value of this expression in python
        """
        return 0, env
    @abstractmethod
    def classes_used(self):
        return set([ReturnCommand])


class Expression(ReturnCommand):
    """
    the base expression for doing math
    can be thought of as a type of command that does nothing, but returns a value
    with the introduction of functions, Expressions will be able to perform actions
    Noop : NoReturnCommand :: Expression : ReturnCommand
    It must evaluate to a numerical result, otherwise it is some other form of ReturnCommand
    """
    @abstractmethod
    def __str__(self):
        return "Expression"
    @abstractmethod
    def classes_used(self):
        return set([Expression])


class BooleanExpression(ReturnCommand):
    """
    the base expression for doing boolean algebra
    Integer : Expression :: Boolean : BooleanExpression
    It must evaluate to a boolean result, otherwise it is some other form of ReturnCommand
    """
    @abstractmethod
    def __str__(self):
        return "BooleanExpression"
    @abstractmethod
    def py_eval(self, env):
        return False, env
    @abstractmethod
    def classes_used(self):
        return set([BooleanExpression])


class Integer(Expression):
    """
    just an integer number
    """
    def __init__(self, val):
        assert type(val) == int
        self.value = val

    def __str__(self):
        return "Integer(" + str(self.value) + ")"

    def py_eval(self, env):
        return self.value, env
    
    def type_eval(self, env):
        return Integer, env
    
    def classes_used(self):
        return set([Integer])
def integer_validate(string):
    # @input string: the string to check if it's valid
    # @return boolean: whether it is valid under this Spec or not
    try:
        int(string)
        return True
    except:
        return False
def integer_convert(string):
    # the convert function takes in a luka string that is valid under this spec and
    # does the necessary conversions on it, returning a completed Command object
    # @input string: the entire string of the command to convert
    # @return Command: the Command form of that string
    # @throw: whatever decode_command throws, due to a string found not matching a spec
    return Integer(int(string))
command_specs[priority.i].append(Spec(Integer, integer_validate, integer_convert))
type_names["int"] = Integer
type_classes[Integer] = "Integer"

bool_options = {"true": True, "false": False}
class Boolean(BooleanExpression):
    """
    just the base boolean value
    """
    def __init__(self, val):
        assert type(val) == bool
        self.value = val

    def __str__(self):
        return "Boolean(" + str(self.value) + ")"

    def py_eval(self, env):
        return self.value, env
    
    def type_eval(self, env):
        return Boolean, env
    
    def classes_used(self):
        return set([Boolean])
def boolean_validate(string):
    # @input string: the string to check if it's valid
    # @return boolean: whether it is valid under this Spec or not
    return string in bool_options
def boolean_convert(string):
    # the convert function takes in a luka string that is valid under this spec and
    # does the necessary conversions on it, returning a completed Command object
    # @input string: the entire string of the command to convert
    # @return Command: the Command form of that string
    # @throw: whatever decode_command throws, due to a string found not matching a spec
    return Boolean(bool_options[string])
command_specs[priority.i].append(Spec(Boolean, boolean_validate, boolean_convert))
type_names["bool"] = Boolean
type_classes[Boolean] = "Boolean"


class Add(Expression):
    """
    add two numbers together
    """
    def __init__(self, v1, v2):
        assert isinstance(v1, ReturnCommand), f"Value 1 ({v1}) is not a returning command, it is a {type(v1)}"
        assert isinstance(v2, ReturnCommand), f"Value 2 ({v2}) is not a returning command, it is a {type(v2)}"
        self.v1 = v1
        self.v2 = v2

    def __str__(self):
        return f"Add({self.v1}, {self.v2})"

    def py_eval(self, env):
        v1, new_env = self.v1.py_eval(env)
        v2, new_env = self.v2.py_eval(new_env)
        return v1 + v2, new_env
        
    def type_eval(self, env):
        tipe1, new_env = self.v1.type_eval(env)
        tipe2, new_env = self.v2.type_eval(new_env)
        assert tipe1 is Integer, str(tipe1) + " is not a numerical data type, cannot add"
        assert tipe2 is Integer, str(tipe2) + " is not a numerical data type, cannot add"
        return Integer, new_env
    
    def classes_used(self):
        return merge_2_subclasses(Add, self.v1, self.v2)
def add_validate(string):
    # @input string: the string to check if it's valid
    # @return boolean: whether it is valid under this Spec or not
    return "+" in string
def add_convert(string):
    # the convert function takes in a luka string that is valid under this spec and
    # does the necessary conversions on it, returning a completed Command object
    # @input string: the entire string of the command to convert
    # @return Command: the Command form of that string
    # @throw: whatever decode_command throws, due to a string found not matching a spec
    part1, part2 = tuple(string.rsplit("+", 1))
    part1 = decode_command(part1)
    part2 = decode_command(part2)
    return Add(part1, part2)
command_specs[priority.a].append(Spec(Add, add_validate, add_convert))


class Sub(Expression):
    """
    subtract the second number from the first
    """
    def __init__(self, v1, v2):
        assert isinstance(v1, ReturnCommand), f"Value 1 ({v1}) is not a returning command, it is a {type(v1)}"
        assert isinstance(v2, ReturnCommand), f"Value 2 ({v2}) is not a returning command, it is a {type(v2)}"
        self.v1 = v1
        self.v2 = v2

    def __str__(self):
        return f"Sub({self.v1}, {self.v2})"

    def py_eval(self, env):
        v1, new_env = self.v1.py_eval(env)
        v2, new_env = self.v2.py_eval(new_env)
        return v1 - v2, new_env
        
    def type_eval(self, env):
        tipe1, new_env = self.v1.type_eval(env)
        tipe2, new_env = self.v2.type_eval(new_env)
        assert tipe1 is Integer, str(tipe1) + " is not a numerical data type, cannot sub"
        assert tipe2 is Integer, str(tipe2) + " is not a numerical data type, cannot sub"
        return Integer, new_env
    
    def classes_used(self):
        return merge_2_subclasses(Sub, self.v1, self.v2)
def sub_validate(string):
    # @input string: the string to check if it's valid
    # @return boolean: whether it is valid under this Spec or not
    # TODO: add something to distinguish between subtraction and negatives
    return "-" in string
def sub_convert(string):
    # the convert function takes in a luka string that is valid under this spec and
    # does the necessary conversions on it, returning a completed Command object
    # @input string: the entire string of the command to convert
    # @return Command: the Command form of that string
    # @throw: whatever decode_command throws, due to a string found not matching a spec
    part1, part2 = tuple(string.rsplit("-", 1))
    part1 = decode_command(part1)
    part2 = decode_command(part2)
    return Sub(part1, part2)
command_specs[priority.a].append(Spec(Sub, sub_validate, sub_convert))


class Ident(ReturnCommand):
    """
    the string that represents a value or variable
    """
    def __init__(self, name):
        # TODO: also specify the type of this ident
        assert isinstance(name, str), f"Given name must be a string, {name} is of type {type(name)}"
        self.name = name

    def __str__(self):
        return f'Ident("{self.name}")'

    def py_eval(self, env):
        if self.name in env:
            return env[self.name], env
        else:
            raise RuntimeError(f"Identifier {self.name} is not in scope")
        
    def type_eval(self, env):
        if self.name in env:
            return env[self.name], env
        else:
            raise RuntimeError(f"Identifier {self.name} is not in scope")

    def classes_used(self):
        return set([Ident])
def ident_validate(string):
    # @input string: the string to check if it's valid
    # @return boolean: whether it is valid under this Spec or not
    if not isinstance(string, str): return False
    name = string.strip()
    unaccepted_list = " ,'\"()!@#$%^&*[]}{\\|?<>.`~-=+"
    return not any([nono in name for nono in unaccepted_list])
command_specs[priority.i].append(Spec(Ident, ident_validate, lambda string: Ident(string.strip())))


class Val(NoReturnCommand):
    """
    store a static immutable value, to be referenced by the given string
    """
    def __init__(self, tipe, ident, value):
        assert tipe in type_names.values(), f"{tipe} is not a valid/available data type"
        assert isinstance(ident, Ident), f"Value name must be an identifier, it is of type {type(ident)}"
        assert isinstance(value, ReturnCommand), f"Attempting to store something with no value, it is of type {type(value)}"
        self.tipe = tipe
        self.ident = ident
        self.value = value

    def __str__(self):
        if self.tipe:
            return "Val(" + type_classes[self.tipe] + ", " + str(self.ident) + ", " + str(self.value) + ")"
        else:
            return "Val(" + str(self.ident) + ", " + str(self.value) + ")"

    def py_eval(self, env):
        val, new_env = self.value.py_eval(env)
        expanded_env = new_env.copy()
        expanded_env[self.ident.name] = val
        return None, expanded_env

    def type_eval(self, env):
        tipe, new_env = self.value.type_eval(env)
        # if editing the value (instead of overwriting it), check the previous environment to ensure the types match
        if self.tipe:
            assert tipe is self.tipe, f"Value '{self.ident.name}' of type {self.tipe} fails to store a value of type {tipe}"
        else:
            self.tipe = tipe
        expanded_env = new_env.copy()
        expanded_env[self.ident.name] = tipe
        return None, expanded_env

    def classes_used(self):
        classes = set([Val, Ident])
        if self.tipe: classes.add(self.tipe)
        sub_classes = self.value.classes_used()
        classes.update(sub_classes)
        return classes
val_start = "val "
val_type_split = ":"
val_equals = "="
def val_validate(string):
    # @input string: the string to check if it's valid
    # @return boolean: whether it is valid under this Spec or not
    
    # starts with the right stuff
    if not string.startswith(val_start): return False
    string = string[len(val_start):]
    # split on the first equals sign
    eq_parts = string.split(val_equals, 1)
    if len(eq_parts) != 2: return False
    # split on the type if it exists
    type_parts = eq_parts[0].split(val_type_split, 1)
    if len(type_parts) > 2 or len(type_parts) == 0: return False
    ident = type_parts[0]
    tipe = type_parts[1].strip() if len(type_parts) == 2 else None
    # do need to check the identifier here
    if not ident_validate(ident): return False
    # and make sure it's a real data type
    if tipe and tipe not in type_names.keys(): return False
    # second part will be checked for whatever it ends up being
    return True
def val_convert(string):
    # the convert function takes in a luka string that is valid under this spec and
    # does the necessary conversions on it, returning a completed Command object
    # @input string: the entire string of the command to convert
    # @return Command: the Command form of that string
    # @throw: whatever decode_command throws, due to a string found not matching a spec

    # cut off the starting "val"
    string = string[len(val_start):]
    # then split on the first equals
    front, value_string = tuple(string.split(val_equals, 1))
    # then split on the type
    type_split = front.split(val_type_split, 1)
    ident_string = type_split[0]
    type_string = type_split[1].strip() if len(type_split) == 2 else None
    if type_string == "void": raise Exception("Cannot have a value store a void result")
    # then decode each of the individual strings
    ident = decode_command(ident_string) # should be an Ident class
    tipe = type_names[type_string] if type_string else None # should be a class name
    value = decode_command(value_string) # should be some ReturnCommand
    return Val(tipe, ident, value)
command_specs[priority.v].append(Spec(Val, val_validate, val_convert))


class Comparison(BooleanExpression):
    """
    base for comparing two values and producing a boolean result
    """
    def __init__(self, v1, v2):
        assert isinstance(v1, ReturnCommand), f"Value 1 ({v1}) is not a returning command, it is a {type(v1)}"
        assert isinstance(v2, ReturnCommand), f"Value 2 ({v2}) is not a returning command, it is a {type(v2)}"
        self.v1 = v1
        self.v2 = v2
        # the variables to distinguish between each comparison operator
        self.clas = Comparison
        self.name = "Comparison"
        self.py_op = None # a lambda function

    def __str__(self):
        return f"{self.name}({self.v1}, {self.v2})"

    def py_eval(self, env):
        v1, new_env = self.v1.py_eval(env)
        v2, new_env = self.v2.py_eval(new_env)
        return self.py_op(v1, v2), new_env
        
    def type_eval(self, env):
        tipe1, new_env = self.v1.type_eval(env)
        tipe2, new_env = self.v2.type_eval(new_env)
        assert tipe1 is Integer, str(tipe1) + " is not a numerical data type, cannot compare"
        assert tipe2 is Integer, str(tipe2) + " is not a numerical data type, cannot compare"
        return Boolean, new_env
    
    def classes_used(self):
        return merge_2_subclasses(self.clas, self.v1, self.v2)


class Eq(Comparison):
    """
    comparing if two values are equal, ==
    """
    def __init__(self, v1, v2):
        super().__init__(v1, v2)
        self.clas = Eq
        self.name = "Eq"
        self.py_op = lambda a, b: a == b
command_specs[priority.c].append( comparison_type_spec(Eq, "==") )


class NotEq(Comparison):
    """
    comparing if two values are not equal, !=
    """
    def __init__(self, v1, v2):
        super().__init__(v1, v2)
        self.clas = NotEq
        self.name = "NotEq"
        self.py_op = lambda a, b: a != b
command_specs[priority.c].append( comparison_type_spec(NotEq, "!=") )


class Gr(Comparison):
    """
    comparing if value a is greater than value b, a > b
    """
    def __init__(self, v1, v2):
        super().__init__(v1, v2)
        self.clas = Gr
        self.name = "Gr"
        self.py_op = lambda a, b: a > b
command_specs[priority.c].append( comparison_type_spec(Gr, ">") )


class Ls(Comparison):
    """
    comparing if value a is less than value b, a < b
    """
    def __init__(self, v1, v2):
        super().__init__(v1, v2)
        self.clas = Ls
        self.name = "Ls"
        self.py_op = lambda a, b: a < b
command_specs[priority.c].append( comparison_type_spec(Ls, "<") )


class GrEq(Comparison):
    """
    comparing if value a is greater than or equal to value b, a >= b
    """
    def __init__(self, v1, v2):
        super().__init__(v1, v2)
        self.clas = GrEq
        self.name = "GrEq"
        self.py_op = lambda a, b: a >= b
command_specs[priority.c].append( comparison_type_spec(GrEq, ">=") )


class LsEq(Comparison):
    """
    comparing if value a is less than or equal to value b, a <= b
    """
    def __init__(self, v1, v2):
        super().__init__(v1, v2)
        self.clas = LsEq
        self.name = "LsEq"
        self.py_op = lambda a, b: a <= b
command_specs[priority.c].append( comparison_type_spec(LsEq, "<=") )


class Scope(Element):
    """
    group several sub-elements into one block, giving them a different environment to execute under
    the scope will take on the value (or no value) of the last command in the scope that executes
    use a semicolon at the end to indicate that it is a no-value if statement
    """
    def __init__(self, sub_elements = []):
        assert type(sub_elements) is list, "sub_elements must be given as a list"
        assert all([isinstance(sub_elem, Element) for sub_elem in sub_elements]), "All sub elements must be of type element"
        self.sub_elements = sub_elements
    def __str__(self):
        return "Scope([" + ",\n".join(str(elem) for elem in self.sub_elements) + "])"
    def py_eval(self, env):
        new_env = env.copy()
        for elem in self.sub_elements:
            latest_val, new_env = elem.py_eval(new_env)
        # return the result of the last command, plus the original environment
        return latest_val, env
    def type_eval(self, env):
        new_env = env.copy()
        for elem in self.sub_elements:
            latest_type, new_env = elem.type_eval(new_env)
        # return the result of the last command, plus the original environment
        return latest_type, env
    def classes_used(self):
        classes = set([Scope])
        for elem in self.sub_elements:
            sub_classes = elem.classes_used()
            classes.update(sub_classes)
        return classes
# def scope_validate(string):
#     # @input string: the string to check if it's valid
#     # @return boolean: whether it is valid under this Spec or not

# def scope_convert()
#     #input string
#     return command
these have to be completely different things because they are multi-line


class ControlFlow(Element):
    """
    any element that will control the flow of program execution
    these include If statements, For loops, While loops, class declarations, and function declarations
    """
    def __str__(self):
        return "ControlFlow"
    def classes_used(self):
        return set([ControlFlow])


class If(ControlFlow):
    """
    the wrapper to create an if statement (or an if/else, or an if/else-if/else statement)
    chooses which sub scope to enter to execute based on a boolean condition
    the if statement will take on the value of the last command in the scope that executes
    use a semicolon at the end to indicate that it is a no-value if statement
    """
    def __init__(self, condition, if_scope, else_scope):
        assert isinstance(condition, BooleanExpression), "The condition must be a returning expression"
        assert isinstance(if_scope, Scope), "The commands given to an if block must be a scope, but it is: " + type(if_scope)
        assert isinstance(else_scope, Scope), "The commands given to an else block must be a scope, but it is: " + type(if_scope)
        self.condition = condition
        self.if_scope = if_scope
        self.else_scope = else_scope
    
    def __str__(self):
        return "If(" + str(self.condition) + ", " + str(self.if_scope) + ", " + str(self.else_scope) + ")"
    
    def py_eval(self, env):
        cond_result, new_env = self.condition.py_eval(env)
        if cond_result:
            return self.if_scope.py_eval(new_env)
        else:
            return self.else_scope.py_eval(new_env)

    def type_eval(self, env):
        cond_type, new_env = self.condition.type_eval(env)
        assert cond_type is Boolean, "The condition must result in a boolean value, but is a: " + cond_type
        # make sure the return of the scope is the same for both the if and the else
        sub_env = new_env.copy()
        if_type, if_env = self.if_scope.type_eval(sub_env)
        else_type, else_env = self.else_scope.type_eval(sub_env)
        assert if_type == else_type, f"Must have the same return type for the last statements in the if/else blocks; they are {if_type} and {else_type}"
        # return the environment after evaluating the condition, but before either block
        return if_type, new_env

    def classes_used(self):
        classes = set([If])
        for cmd_list in [[self.condition], self.if_commands, self.else_commands]:
            for cmd in cmd_list:
                sub_classes = cmd.classes_used()
                classes.update(sub_classes)
        return classes
command_specs[priority.hmm].append( function_type_spec(If, "if(", 1, ")") )
make it something like controlflow_specs?
because this isn't a command, ad we need to know to look for a scope afterwards