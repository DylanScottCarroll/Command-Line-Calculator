# Command  Line Calculator
# Dylan Carroll
# Nov 28 2020
#
# A shell-interface for a calculator

import math

NUMBER_CHARS = "1234567890."
OP_CHARS = "=+-/*()%<>!^,"
WHITESPACE_CHARS = [" ", "\n", "\t", "\v", "\r", ""]

MULTI_OPS = ["--", "++", "-=", "+=", "//", "==", ">=", "<=", "!="]

ALLOWED_UNARY_OPS = ["-", "!", "++", "!"]

OP_PRECEDENCE = {
    "--U" : 50, #unary
    "++U" : 50, 
    "-U" : 50,
    "!U" : 50,
    
    "^" : 40, #Exp

    "*" : 30, #mult and div
    "/" : 30,
    "//" : 30,
    "%" : 30,
    
    "+" : 20, ##add and sub
    "-" : 20,
    
    "==" : 17, #comparison
    ">=" : 17,
    "<=" : 17,
    "!=" : 17,
    "<" : 17,
    ">" : 17,


    "(C" : 15, #Parens
    "(" : 15,

    "=" : 10, #assignment
    "+=" : 10,
    "-=" : 10  }

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
    "nthroot" : (2, (lambda x, n : x**(1.0/n)) ),
}



def char_type(char: str) -> str:
    """Returns a string identifying the type of a given character"""
    
    #if the character is a number
    if char in NUMBER_CHARS:
        return "num"
    #if it is an operator
    elif char in OP_CHARS:
        return "ops"
    #if it is a character A-Z or a-z
    elif (char >= "A" and char <= "Z") or (char >= "a" and char <= "z"):
        return "abc"
    elif char in WHITESPACE_CHARS:
        return "wht"
    #if the character is unidentified
    else:
        return "etc"

def token_is_not_operand(token, direction):
    """Returns True if the token in the given direction could not be part of an operand"""

    if direction == "left":
        return ( char_type(token[0]) == "ops" and not(token in [")", "++", "--", "!"] ) )
    else:
        return ( char_type(token[0]) == "ops" and not(token in ["(", "-"] ) )
        

def token_is_multi_op(token: str) -> bool:
    """Returns true if the token is a valid multiple-char operator"""
    return token in MULTI_OPS

def token_is_op(token):
    """Returns true if the given token is a valid operator"""

    return (token in OP_PRECEDENCE.keys())

def op_can_be_unary(op):
    return (op in ALLOWED_UNARY_OPS)

def op_has_precedence(op1, op2):
    return (OP_PRECEDENCE[op1] >= OP_PRECEDENCE[op2])

def split_tokens(line: str):
    """Splits the input string into tokens and maintains the order"""

    #
    # SPLIT THE TOKENS INTO GROUPS
    #
    tokens = []
    current_token = ""
    last_type = "etc"
    for char in line:
        current_type = char_type(char)

        #ignore whitespace
        if current_type == "wht":
            if current_token != "":
                tokens.append(current_token)

            current_token = ""
        #chars of same type form tokens together
        elif current_type == last_type or (current_type == "num" and last_type == "abc"):
            current_token += char
        #chars of different types spit tokens
        else:
            if current_token != "":
                tokens.append(current_token)

            current_token = char

        last_type = current_type

    #flush the last token into the list
    if current_token != "":
        tokens.append(current_token)
    
    #
    #SPLIT OP TOKENS THAT DON'T FORM MULTI-CHARACTER OPS
    #
    new_tokens = []
    for token in tokens:
        if char_type(token[0]) == "ops" and len(token) > 1:
            
            i = 0
            op = ""
            while i < len(token):
                char = token[i]
                if len(op) < 2:
                    op += char
                    i += 1
                else:
                    #if the current pair of operators forms a multi_op add it to the list
                    #otherwise just add the first op to the list
                    if token_is_multi_op(op):
                        new_tokens.append(op)
                        op = ""
                    else:
                        new_tokens.append(op[0])
                        op = op[1:]
            
            if token_is_multi_op(op):
                new_tokens.append(op)
            else:
                for char in op:
                    new_tokens.append(char)

        else:
            new_tokens.append(token)
    tokens = new_tokens
   
    #
    #TAG UNARY OPERATORS AND CALLING PARENS
    #CHECK FOR ILLEGAL ADJACENT OPERANDS
    #

    for i, token in enumerate(tokens):
        
        #Only test ops that can be unary
        if op_can_be_unary(token):
            #if any operator is the first or last token in a line, it must be unary
            if (i == 0) or (i == len(tokens)-1):
                tokens[i] = token + "U"

            #for "-" if the previous token is an operand it must be unary
            if token == "-":
                if token_is_not_operand(tokens[i-1], "left"):
                    tokens[i] = token + "U"
            elif op_can_be_unary(token):
                tokens[i] = token + "U"
        
        #if an open paren comes after an operand, it calls that operand
        elif token == "(" and i !=0:
            #If the previous token is an operand
            if not token_is_not_operand(tokens[i-1], "left"):
                tokens[i] = token + "C"

        #Check for adjacent operands
        #If the current token is an operand
        elif (char_type(token[0]) != "ops") and i !=0:
             #And  the previous token is not an operand
            if not token_is_not_operand(tokens[i-1], "left"):
                return "SYNTAX_ERROR:\nCan't have adjecent operands without an operator."

    return tokens

def to_postfix(tokens: str):
    """Converts an in-order list of tokens into a postfix-formatted list
    using the shunting-yard algorithm"""
    
    output = []
    op_stack = []

    for i, token in enumerate(tokens):
        #checking for operators that influence precedence
        if token in ["(", ")", "(C", ","]:
            if token == "(":
                op_stack.append(token)
            elif token == "(C":
                #place the function name on the stack below the calling paren
                func_name = output[-1]
                op_stack.append(func_name)
                del output[-1]
                op_stack.append(token)
                

                #check if the function exists
                if not(func_name in FUNCTIONS.keys()):
                    return "NAME_ERROR:\n\"" + func_name + "\" does not exist as a function."

                #Look forward and count the arguments
                args, func = FUNCTIONS[func_name]
                balance = 1
                count = 1
                current_arg = []
                for j in range(i+1, len(tokens)):
                    ahead_token = tokens[j]
                    if ahead_token == ",":
                        if len(current_arg) == 0:
                            return "ARGUMENT_ERROR:\nArgument " + str(count) + " of " + func_name + " is invalid."
                        
                        count += 1
                    elif ahead_token == "(" or ahead_token == "(C":
                        balance += 1
                    elif ahead_token == ")":
                        balance -= 1
                    else:
                        current_arg.append(ahead_token)
                    
                    if balance == 0:
                        break
                
                if len(current_arg) == 0:
                    return "ARGUMENT_ERROR:\nArgument " + str(count) + " of " + func_name + " is invalid."

                if args != count:
                    return ("ARGUMENT_ERROR:\n\"" + func_name + "\" takes " 
                    + str(args) + " arguments.\nYou gave " + str(count) + ".\n")


            #If it is a close paren or a comma, flush all of the operations until the open paren
            else:
                #work down the stack until an open paren is found
                while True:
                    #Keep going until an open paren is found
                    if  len(op_stack)>0 and not(op_stack[-1] == "(" or op_stack[-1] == "(C"):
                        output.append(op_stack[-1])
                        del op_stack[-1]
                    #Remove the open paren
                    elif token == ")": 
                        if len(op_stack) > 0:
                            if op_stack[-1] == "(C":
                                #place the function name and calling paren on the output stack
                                output.append(op_stack[-2])
                                output.append(op_stack[-1])
                                del op_stack[-1]
                            
                            del op_stack[-1]
                            
                            break
                        else:
                            return "SYNTAX_ERROR:\nMissing parenthesis."
                    #If it was a comma, jsut stop after the flush
                    else:
                        break

        
        #If token is not a paren and is an op
        elif token_is_op(token):
            
            #work down the stack until the token can be placed on it
            while True:
                #If the op on the stack has higher precedence, 
                #   pop it off the op_stack and put it onto the output
                if  len(op_stack)>0 and op_has_precedence(op_stack[-1],  token):
                    output.append(op_stack[-1])
                    del op_stack[-1]
                else:
                    op_stack.append(token)
                    break
        else:
            output.append(token)
    
    #flush the remaining op_stack
    while len(op_stack)>0:
        output.append(op_stack[-1])
        del op_stack[-1]
    
    return output

def get_value(token, global_vars):
    """Takes a token as input
    if it is a number, it is converted to a float
    otherwise it is assumed as a variable name and the value is retrieved"""
    
    try:
        return float(token)
    except ValueError:
        if token in global_vars.keys():
            return global_vars[token]
        else:
            return "NAME_ERROR:\n\"" + token + "\" does not exist as a variable name"

def set_value(token, value, global_vars):
    """Takes a variable name as input
    Sets the value of that variable
    If the variable doesn't exist, creates it"""
    global_vars[token] = value

def simple_op(stack, operator):
    if len(stack) < 2:
        return "SYNTAX_ERROR:\nNot enough operands."

    op2 = stack[-1]
    del stack[-1]
    op1 = stack[-1]
    del stack[-1]

    val1 = get_value(op1, global_vars)
    val2 = get_value(op2, global_vars)
    if type(val1) == str:
        return val1
    if type(val2) == str:
        return val2
    
    stack.append(str(operator(val1, val2)))

def call_func(func, args):
    return func(*args)

def execute_postfix(tokens, global_vars):
    stack = []
    for token in tokens:
        

        if token_is_op(token):
            result = 0

            if len(stack) == 0:
                return "SYNTAX_ERROR:\nNot enough operands."

            #
            #FIND THE OPERATOR AND EXECUTE IT
            #
            if token == "--U":
                value = get_value(stack[-1], global_vars)
                
                if type(value) == str:
                    return value
                else:
                    set_value(stack[-1], value-1, global_vars)

            elif token == "++U":
                value = get_value(stack[-1], global_vars)
                
                if type(value) == str:
                    return value
                else:
                    set_value(stack[-1], value+1, global_vars)

            elif token == "-U":
                operand = stack[-1]
                del stack[-1]

                value = get_value(operand, global_vars)
                if type(value) == str:
                    return value
                
                stack.append(str(-value))

            elif token == "^":
                error = simple_op(stack, lambda x, y: x ** y)
                if type(error) == str:
                    return error

            elif token == "*":
                error = simple_op(stack, lambda x, y: x * y)
                if type(error) == str:
                    return error

            elif token == "/":
                error = simple_op(stack, lambda x, y: x / y)
                if type(error) == str:
                    return error

            elif token == "//":
                error = simple_op(stack, lambda x, y: x // y)
                if type(error) == str:
                    return error

            elif token == "%":
                error = simple_op(stack, lambda x, y: x % y)
                if type(error) == str:
                    return error

            elif token == "+":
                error = simple_op(stack, lambda x, y: x + y)
                if type(error) == str:
                    return error

            elif token == "-":
                error = simple_op(stack, lambda x, y: x - y)
                if type(error) == str:
                    return error

            elif token == "(C":
                func_name = stack[-1]
                del stack[-1]

                if not(func_name in FUNCTIONS.keys()):
                    return "NAME_ERROR:\n\"" + func_name + "\" does not exist as a function."

                arg_count, func = FUNCTIONS[func_name]
                
                args = []
                for n in range(arg_count):
                    if len(stack) == 0:
                        return "ARGUMENT_ERROR:\n\"" + func_name + "\" has an argument with an invalid operation."
                        
                    next_arg = get_value(stack[-1], global_vars)
                    del stack[-1]

                    if type(next_arg) == str:
                        return next_arg

                    args = [next_arg] + args
                
                output = call_func(func, args)

                stack.append(str(output))

            elif token == "=":
                op = stack[-1]
                del stack[-1]
                var = stack[-1]
                del stack[-1]

                val = get_value(op, global_vars)
                if type(val) == str:
                    return val

                set_value(var, val, global_vars)   
                stack.append(var)

            elif token == "+=":
                op2 = stack[-1]
                del stack[-1]
                var = stack[-1]
                del stack[-1]

                val2 = get_value(op2, global_vars)
                val1 = get_value(var, global_vars)
                if type(val1) == str:
                    return val1
                if type(val2) == str:
                    return val2
    
                set_value(var, (val1 + val2), global_vars)   

            elif token == "-=": 
                op2 = stack[-1]
                del stack[-1]
                var = stack[-1]
                del stack[-1]

                val2 = get_value(op2, global_vars)
                val1 = get_value(var, global_vars)
                if type(val1) == str:
                    return val1
                if type(val2) == str:
                    return val2
    
                set_value(var, (val1 - val2), global_vars)
            
            elif token == "==":
                error = simple_op(stack, lambda x, y: x == y) 
                if type(error) == str:
                    return error
            
            elif token == ">=":
                error = simple_op(stack, lambda x, y: x >= y) 
                if type(error) == str:
                    return error
            
            elif token == "<=":
                error = simple_op(stack, lambda x, y: x <= y) 
                if type(error) == str:
                    return error
            
            elif token == "!=":
                error = simple_op(stack, lambda x, y: x != y) 
                if type(error) == str:
                    return error
            
            elif token == ">":
                error = simple_op(stack, lambda x, y: x > y) 
                if type(error) == str:
                    return error

            elif token == "<":
                error = simple_op(stack, lambda x, y: x < y) 
                if type(error) == str:
                    return error

            elif token == "!U":
                op = stack[-1]
                del stack[-1]

                val = get_value(op, global_vars)
                if type(val) == str:
                    return val

                stack.append(str(not val))

            else:
                return "OP_ERROR:\n\"" + token + "\" is not an operator"

        else:
            if "U" in token and token_is_op(token[:-1]):
                return "OP_ERROR:\n\"" + token[:-1] +"\" cannot be used as a unary operator."
            elif token_is_op(token + "U"):
                return "OP_ERROR:\n\"" + token +"\" must be used as a unary operator."

            stack.append(token)

    if len(stack) > 1:
        return "SYNTAX_ERROR:\n" + "You are missing operator(s)."
    elif len(stack) == 0:
        return ""
    else:
        if stack[0] == "True" or stack[0] == "False":
            return stack[0]
        else:
            value = get_value(stack[0], global_vars)
            if stack[0] == str(value):
                return value
            else:
                return stack[0] + " : " + str(value)

global_vars = {
    "pi" : math.pi,
    "e" : math.e,
    "tau" : math.tau,
    "inf" : math.inf,
    "True": 1,
    "False": 0,
    "@" : 0
}

print("Welcome to calculator.")
last_line = ""
while True:
    line = input("\n>> ")
    
    if line == "":
        line = last_line
    else:
        last_line = line

    tokens = split_tokens(line)
    #If split_tokens threw an error
    if type(tokens) == str:
        print(tokens)
        continue

        print(tokens)

    postfix = to_postfix(tokens)

    #If postfix threw an error
    if type(postfix) == str:
        print(postfix)
        continue

    result = execute_postfix(postfix, global_vars)
    set_value("@", result, global_vars) #update the answer variable
    print(result)