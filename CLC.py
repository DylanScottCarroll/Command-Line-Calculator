# Command  Line Calculator
# Dylan Carroll
# Nov 28 2020
#
# A shell-interface for a calculator

import math, re, readline

TOKENIZATION_REGEX = "(([0-9|.]+)|([A-Za-z|_|@][A-Za-z|_|0-9|@]*)|([\-|!|\+|\*|\||\/|&|=|<|>|!]){1,2}|([\(|\)|\^|%|,]))"
VALUE_REGEX = "[0-9|.]{1,}|[A-z|_|@][A-z|_|0-9|@]*"


#(Operator string, number of operands, prefix=-1 infix=0 postfix=1, precedence)
OPERATORS = [
    ("(", None, 0, 7), #Function call 
    
    #Prefix Ops
    ("-", 1, -1, 6),
    ("!", 1, -1, 6), #boolean not

    #Postfix Ops
    ("!", 1, 1, 5), #Factorial
    ("--", 1, 1, 5),
    ("++", 1, 1, 5),

    #Exponentiation
    ("^", 2, 0, 4),


    ("*", 2, 0, 3),
    ("/", 2, 0, 3),
    ("//", 2, 0, 3),
    ("%", 2, 0, 3),

    
    ("+", 2, 0, 2),
    ("-", 2, 0, 2),
    
    #Logical operators
    ("&&", 2, 0, 2),
    ("||", 2, 0, 2),
    
    #Logical Comparison operators
    ("==", 2, 0, 1),
    ("<=", 2, 0, 1),
    (">=", 2, 0, 1),
    ("!=", 2, 0, 1),
    ("<", 2, 0, 1),
    (">", 2, 0, 1),
    
    #Assignment Operators
    ("=", 2, 0, 0),
    ("+=", 2, 0, 0),
    ("-=" , 2, 0, 0),
    ("*=" , 2, 0, 0),
    ("/=" , 2, 0, 0)
]

def get_matching_op(string, operand_count = None, position = None, precedence = None):
    """With the given operator properties, returns the operator that matches.
        If there are multiple matching operators, returns a list."""

    matching_ops = []

    for operator in OPERATORS:
        op_string, op_count, op_pos, op_precedence = operator
        matches = True
        
        if string != op_string: matches = False
        if operand_count is not None and operand_count != op_count: matches = False
        if position is not None and position != op_pos: matches = False
        if precedence is not None and precedence != op_precedence: matches = False

        if matches: matching_ops.append(operator)

    if len(matching_ops) == 1:
        return matching_ops[0]
    else:
        return matching_ops

def get_multichar_ops():
    """Returns a list of all of the valid multichar ops"""
    ops = []
    for op, n, p, r in OPERATORS:
        if len(op) == 2:
            ops.append(op)
    return ops


def Perm(n, r):
    return math.factorial(n) // (math.factorial(n-r))
    
def Chose(n, r):
    return math.factorial(n) // (math.factorial(n-r) * math.factorial(r))

def dot2(ax, ay, bx, by):
    return ax*bx + ay*by

def dot3(ax, ay, az, bx, by, bz):
    return ax*bx + ay*by + az*bz

def mag(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)

def vecangle(ax, ay, az, bx, by, bz):
    return math.acos( (dot3(ax, ay, az, bx, by, bz)) / (mag(ax, ay, az) * mag(bx, by, bz)) )

def cross(ax, ay, az, 
          bx, by, bz):

        print("<", end="")
        print(ay*bz-az*by, az*bx-ax*bz, ax*by-ay*bx, sep="," , end=">\nmag: ")
    
        return mag(ay*bz-az*by, az*bx-ax*bz, ax*by-ay*bx)

#The dictionary stores a tuple with the numver of arguments a function has
#   and the function that it calls
FUNCTIONS = {
    "sin" : (1, math.sin),
    "cos" : (1, math.cos),
    "tan" : (1, math.tan),
    "atan" : (1, math.atan),
    "atan2" : (2, math.atan2),
    "asin" : (1, math.asin),
    "acos" : (1, math.acos),
    "deg" : (1 , math.degrees),
    "rad" : (1, math.radians),

    "floor" : (1, math.floor), #numerical
    "ceil"  : (1, math.ceil),
    "abs" : (1, abs),
    "sign" : (1, (lambda x : x/abs(x)) ),

    "log10" : (1, math.log10), #Exp and log
    "log2" : (1, math.log2),
    "loge"  : (1, math.log),
    "logbase" : (2, math.log),
    "sqrt" : (1, math.sqrt),
    "root" : (2, (lambda x, n : n**(1.0/x)) ),
    "perm" : (2, Perm),
    "chose" : (2, Chose),

    "dot2" : (4, dot2),
    "dot3" : (6, dot3),
    "mag" : (3, mag),
    "vecangle" : (6, vecangle),
    "cross" : (6, cross)
}





def tokenize(line: str):
    """Splits the input string into tokens with a REGEX and maintains the order"""

    matches = re.findall(TOKENIZATION_REGEX, line)
    tokens = [ match[0] for match in matches]
    
   
    #If any grouped pair of operators can't form a multichar operator, break them up
    all_ops = [op for op, n, p, r in OPERATORS]
    multichar_ops = get_multichar_ops()
    
    fixed_tokens = [] 
    for token in tokens:
        if len(token) == 2 and token[0] in all_ops and not (token in multichar_ops):
            fixed_tokens.append(token[0])
            fixed_tokens.append(token[1])
        else:
            fixed_tokens.append(token)

    return fixed_tokens

class Parser():
    def __init__(self, var, body, terminal_list, parent=None):
        self.var = var
        self.body = body
        self.children = []
        self.parent = parent
        self.terminal_list = terminal_list
    
    def __str__(self):
        return "{" + str(self.var) + "," +  str(self.body) + "}"

    def parse(self):
        """Parses the body of the parser"""

        if self.body == []:
            if not self.is_nullable():
                return "Error: Unexpected end of expression."
            else:
                return 0

        if self.is_terminal():
            if Parser.check_terminal(self.var, self.body[0]):

                self.body = self.body[0]
                
                self.terminal_list.append(self)

                return 1
            else:
                return f"Error: {self.body[0]} is not a valid terminal."

        
        body_len = 0
        remaining_body = self.body[:]
        
        #Find what this var subsitutes out to given the first token in its body
        children_vars = Parser.find_sub(self.var, self.body[0])
        
        #Return if there is an error
        if type(children_vars) == str:
            return children_vars

        #Parse each child var recursively and find how much of the body that makes uo
        #Pass the remaining body onto the next one.

        for child_var in children_vars:
            new_parser = Parser(child_var, remaining_body, self.terminal_list, self)
            
            parse_result = new_parser.parse()


            #Return if there is an error
            if type(parse_result) == str:
                return parse_result

            body_len += parse_result
            
            remaining_body = self.body[body_len:]
            
            self.children.append(new_parser)

        #The current body is only the parts of the body used by the children
        self.body = self.body[:body_len]

        return len(self.body)

    def is_terminal(self):
        return self.var in ["Pr", "In", "Po", "V", "Op", "Cp", "Cm"]

    def is_nullable(self):
        return self.var in ["Re", "Fb", "Fa"]

    @staticmethod
    def find_sub(var, token):
        """A lookup table that returns what the substitution will be for any given var with a first token of token"""

        if var == "Mn":
            if token == "(":
                return ["Ex"]
            elif Parser.check_op_pos(token, -1):
                return ["Pr", "Ex"]
            elif Parser.check_op_pos(token, 0):
                return ["In", "Ex"]
            else:
                return ["Ex"]

        if var == "Ex":
            if token == "(":
                return ["Op", "Ex", "Cp", "Re"]
            
            elif Parser.check_op_pos(token, -1):
                return ["Pr", "Ex"]
            elif Parser.check_if_value(token):
                return ["V", "Re"]
            else:
                return f"Error: {token} cannot begin an expression"

        elif var == "Re":
            if token == "(":
                return ["Fc", "Re"]
            elif Parser.check_op_pos(token, 0):
                return ["In", "Ex"]
            elif Parser.check_op_pos(token, 1):
                return ["Po", "Re"]
            else:
                return []

        elif var == "Fc":
            if token == "(":
                return ["Op", "Fb", "Cp"]
            else:
                return f"Error: {token} cannot begin a function call"
        
        elif var == "Fb":
            if token == "(" or Parser.check_op_pos(token, -1) or Parser.check_if_value(token):
                return ["Ex", "Fa"]
            elif token == ")":
                return []
            else:
                return f"Error: {token} cannot begin a function body."

        elif var == "Fr":
            if token == "(" or Parser.check_op_pos(token, -1) or Parser.check_if_value(token):
                return ["Ex", "Fa"]
            else:
                return f"Error: {token} cannot begin a function argument."

        elif var == "Fa":
            if token == ",":
                return ["Cm", "Fr"]
            else:
                return []
    
    @staticmethod
    def check_op_pos(op, pos):
        """Check if the given operator can correspond to the given position
        pos
            pos = -1: prefix
            pos = 0: infix
            pos = 1: postfix"""
        result = False

        for operator in OPERATORS:
            string, operands, position, precedence = operator
            if op == string and position == pos:
                result = True
        return result

    @staticmethod
    def check_if_value(token):
        """Return true if the given token is a number or name"""
        return re.fullmatch(VALUE_REGEX, token)

    @staticmethod
    def check_terminal(var, token):
        """Returns true if the given var matches the given token"""
        if var == "Pr":
            return Parser.check_op_pos(token, -1)
        elif var == "In":
            return Parser.check_op_pos(token, 0)
        elif var == "Po":
            return Parser.check_op_pos(token, 1)  
        elif var == "V":
            return Parser.check_if_value(token)
        elif var == "Op":
            return token == "("
        elif var == "Cp":
            return token == ")"
        elif var == "Cm":
            return token == ","
        else:
            return False

    @staticmethod
    def get_operand_position(var):
        """Convert the name of a variable to the operator position it corresponds to"""
        if var.var == "Pr":
            return -1
        if var.var == "In":
            return 0
        if var.var == "Po":
            return 1

def parse(tokens : list):
    """Pareses a list of tokens into a parse tree"""
    terminal_list = []
    parser = Parser("Mn", tokens, terminal_list)
    parse_result = parser.parse()

    string = ""
    if type(parse_result) == int and parse_result < len(tokens):
        parse_result = f"Error: Unexpected symbols \"{ string.join([x for x in tokens[parse_result:] ])}\""

    if type(parse_result) == str:
        return parse_result
    return terminal_list


def replace_operators(terminal_vars: list):
    """Replaces operators with their tuple representation and inserts function call operators"""

    tokens = []

    for terminal in terminal_vars:
        
        if terminal.var in ["Pr", "In", "Po"]:
            
            if terminal.parent.var == "Mn":
                tokens.append("@")
            
            position = Parser.get_operand_position(terminal)
            match = get_matching_op(terminal.body, position=position)

            if type(match) == list:
                if len(match) == 0:
                    return f"Error: Operator \"{terminal.body}\" cannot be in that position."
                else:
                    return f"Error: Not enough context to determine operator type of \"{terminal.body}\""
            else:
                tokens.append(match)

        elif terminal.var == "Op":
            if terminal.parent.var == "Fc":

                #Check down the tree and count the number of arguments in the function call
                arg_count = 0
                current = terminal.parent.children[1]
                if current.children != []:
                    current = current.children[1]
                    arg_count+=1
                    while current.body != []:
                        current = current.children[1].children[1]
                        arg_count+=1

                string, n, p, r = get_matching_op("(")
                function_call = (string, arg_count, p, r)

                tokens.append(function_call)

            else:
                tokens.append("(")
                

        elif len(terminal.body) > 0:
            tokens.append(terminal.body)
    
    return tokens

def is_open_paren(token):
    """For the purposes of conversion to postfix,
        tests whether the token is either "(" or a operator tuple that contains a "(" """
    if token == "(":
        return True
    elif type(token) == tuple:
        return (token[0] == "(")
    else:
        return False

def to_postfix(tokens):
    """Converts an in-order list of tokens into a postfix-formatted list
    using the shunting-yard algorithm"""

    output = []
    op_stack = []
    for i, token in enumerate(tokens):

        if is_open_paren(token) :
            op_stack.append(token)
        
        elif token == ")":
            while len(op_stack) != 0 and (not is_open_paren(op_stack[-1])) :
                output.append(op_stack[-1])
                del op_stack[-1]
            
            if len(op_stack) == 0:
                return "Error, unbalanced parenthesis encountered."
            
            if type(op_stack[-1]) == tuple:
                output.append(op_stack[-1])

            del op_stack[-1]


        elif type(token) == tuple:
            
            while len(op_stack) != 0 and (not is_open_paren(op_stack[-1]) ) and not(token[2]==-1 and op_stack[-1][2]==-1) and token[3] <= op_stack[-1][3]:
                output.append(op_stack[-1])
                del op_stack[-1]

            op_stack.append(token)

        elif token == ",":
            while len(op_stack) != 0 and (not is_open_paren(op_stack[-1]) ):
                output.append(op_stack[-1])
                del op_stack[-1]
            
        else:
            output.append(token)  
    
    while len(op_stack) != 0:
        output.append(op_stack[-1])
        del op_stack[-1]

    
    return output

def execute_postfix(tokens, global_vars):
    stack = []
    for token in tokens:
        
        if type(token) == tuple:
            result = 0
            error = None
            
            #FIND THE OPERATOR AND EXECUTE IT
                        
            string, operand_count, position, precedence = token

            if string == "(":
                arguments = []
                for i in range(operand_count):
                    raw_arg = stack[-1]
                    del stack[-1]
                    arg = get_value(raw_arg, global_vars)

                    arguments.append(arg)
                    
                arguments.reverse()

                function_name = stack[-1]
                del stack[-1]

                if function_name not in FUNCTIONS.keys():
                    return f"Error: The function, \"{function_name}\", is not a known function name"
                    
                expected_args, function = FUNCTIONS[function_name]

                if expected_args != operand_count:
                    return f"Error: The function, \"{function_name}\", expected {expected_args} arguments. {operand_count} were provided."
                
                result = function(*arguments)

            elif token == ("=", 2, 0, 0):
                raw2 = stack[-1]
                op2 = get_value(raw2, global_vars)
                del stack[-1]
                if type(op2) == str:
                    return op2

                raw1 = stack[-1]
                del stack[-1]
                
                error = set_variable(raw1, op2, global_vars)

                result = raw1

            elif operand_count == 2:
                raw2 = stack[-1]
                op2 = get_value(raw2, global_vars)
                del stack[-1]
                if type(op2) == str:
                    return op2

                raw1 = stack[-1]
                op1 = get_value(raw1, global_vars)
                del stack[-1]
                if type(op1) == str:
                    return op1
                
                if token == ("^", 2, 0, 4):
                    result = op1 ** op2
                if token == ("*", 2, 0, 3):
                    result = op1 * op2
                elif token == ("/", 2, 0, 3):
                    try:
                        result = op1 / op2
                    except ZeroDivisionError:
                        return "Error: Cannot divide by zero, silly guy."

                elif token == ("//", 2, 0, 3):
                    try:
                        result = op1 // op2
                    except ZeroDivisionError:
                        return "Error: Cannot divide by zero, silly guy."

                elif token == ("%", 2, 0, 3):
                    try:
                        result = op1 % op2
                    except ZeroDivisionError:
                        return "Error: Cannot divide by zero, silly guy."

                elif token == ("+", 2, 0, 2):
                    result = op1 + op2
                elif token == ("-", 2, 0, 2):
                    result = op1 - op2
                elif token == ("&&", 2, 0, 2):
                    result = int(op1 and op2)
                elif token == ("||", 2, 0, 2):
                    result = int(op1 or op2)
                elif token == ("==", 2, 0, 1):
                    result = int(op1 == op2)
                elif token == ("<=", 2, 0, 1):
                    result = int(op1 <= op2)
                elif token == (">=", 2, 0, 1):
                    result = int(op1 >= op2)
                elif token == ("!=", 2, 0, 1):
                    result = int(op1 != op2)
                elif token == ("<", 2, 0, 1):
                    result = int(op1 < op2)
                elif token == (">", 2, 0, 1):
                    result = int(op1 > op2)
                elif token == ("+=", 2, 0, 0):
                    result = op1 + op2
                    error = set_variable(raw1, result, global_vars)
                elif token == ("-=" , 2, 0, 0):
                    result = raw1
                    error = set_variable(raw1, op1 - op2, global_vars)
                elif token == ("*=" , 2, 0, 0):
                    result = raw1
                    error = set_variable(raw1, op1 * op2, global_vars)
                elif token == ("/=" , 2, 0, 0):
                    try:
                        result = raw1
                        error = set_variable(raw1, op1 / op2, global_vars)
                    except ZeroDivisionError:
                        return "Error: Cannot divide by zero, silly guy."


            elif operand_count == 1:
                raw = stack[-1]
                op = get_value(raw, global_vars)
                del stack[-1]
                if type(op) == str:
                    return op

                if token == ("-", 1, -1, 6):
                    result = -op
                elif token == ("!", 1, -1, 6):
                    result = int(not op)
                elif token == ("!", 1, 1, 5):
                    if int(op) != op:
                        return "Error: Factorial only supports integer operands." 
                    result = math.factorial(op)
                elif token == ("--", 1, 1, 5):
                    result = raw    
                    error = set_variable(raw, op-1, global_vars)
                elif token == ("++", 1, 1, 5):
                    result = raw
                    error = set_variable(raw, op+1, global_vars)

            if(error):
                return error

            stack.append(result)
        
        else:
            #Is an integer
            if re.fullmatch("[0-9]{1,}", token):
                stack.append(int(token))
            #Is a float
            elif re.fullmatch("[0-9]*\.[0-9]{1,}", token):
                stack.append(float(token))
            else:
                stack.append(token)

    return stack[-1]

def get_value(token, global_vars):
    """If the value is already a valid operand, like a number or boolean, it's just returned
        If it is a variable name, then its value is retrieved from global scope and returned"""
    if type(token) in [int, float]:
        return token

    elif type(token) == bool:
        return token
    
    elif token in global_vars.keys():
        return global_vars[token]

    else:
        return f"Error, \"{token}\" is not recognized."

def set_variable(var, val, global_vars):
    """Add a varialbe to global_vars with the name var and the value val.
        var must be a valid variable name"""
    
    if type(var)==str and re.fullmatch("([A-z|_|@][A-z|_|0-9|@]*)", var):
        global_vars[var] = val
    else:
        return f"Error: \"{var}\" is not a valid variable name."

global_vars = {
    "pi" : math.pi,
    "e" : math.e,
    "tau" : math.tau,
    "inf" : math.inf,
    "@" : 0,
    "true" : 1,
    "false" : 0,
}

if __name__ == "__main__":
    print("Welcome to calculator.")
    last_line = ""
    while True:
        line = input("\n>> ")
        
        if line == "":
            line = last_line
        else:
            last_line = line

        tokens = tokenize(line)

        terminal_vars = parse(tokens)
        if type(terminal_vars) == str:
            print(terminal_vars)
            continue

        tokens = replace_operators(terminal_vars)


        if type(tokens) == str:
            print(tokens)
            continue

        postfix = to_postfix(tokens)
        #If postfix threw an error
        if type(postfix) == str:
            print(postfix)
            continue

        result = execute_postfix(postfix, global_vars)
        
        if type(result) == str:
            if result in global_vars.keys():
                value = get_value(result, global_vars)
                print(result, " : ", value)
                result = value

            else:
                print(result)
                continue
        else:
            print(result)

        set_variable("@", result, global_vars) #update the answer variable