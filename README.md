# Command-Line-Calculator
Just a simple calculator app you can use just by typing.

I wrote this because I seldom used the Windows calculator and instead typed calculations right into the windows search bar because I found the calculator slow and cumbersome to open and use. Most of the time, this shows up as a bing search which has the result. The advantage of this is that all I need to do is quickly hit the windows key and start typing. The problem is that this uses bing 🤮 and it doesn't work all of the time (sometimes it thinks you're trying to search for files). On my PC, I have this calculator linked to run whenever I type a keyboard shortcut.

**Known Issues**
* When the expression begins with a parenthesis, it thinks it's an operator with an implicit initial operand and get's confused.
* When an unknown function name is used, the program crashes rather than shows an error message.
* When an open parenthesis follows an operand, the program crashes rather than showing an error message.

**The basic features include:**

* Standard scientific calculator operations 

* Functions

* Boolean comparison operators

* Variables

* Assignment operators


**Variables**
By default "pi", "tau", "e", "inf", "true", and "false" have their values set.
Booleans are represented by true=1 and false=0.
"@" is a variable that holds the result of the previous calculation.
Starting an expression with an operator will leave @ as an implicit first operand.
a-z, A-Z, _, and 0-9 can be used in varialbe names, but they cannot start with 0-9.

**Operators:**

Normal Ones

\*  : Multiplication

/  : Division

// : Integer Division

%  : Modulo (Remainder)

\+  : Addition

\-  : Subtraction (also unary negation operator)

^  : Exponentiation

! : Factorial

Assignment Operators

=  : Sets the value (Also used to create new variables)

+= : Increments by the variable

-= : Decrements by the variable

*= : Multiplies the variable by the given value

/= : Divides the variable by the given value

++ : Increments variable by 1

-- : Decrements variable by 1

(All assignment operators evaluate to the newly assigned value)

Boolean Operators

! : Not (prefix)

== : Equal to

\>= : Greater than or equal to

<= : Less than or equal to

!= : Not equal to

<  : Less than

\>  : Greater than


**Functions**

sin   : Sine

cos   : Cosine

tan   : Tangent

atan  : Arctangent

atan2 : Arctangent, but takes two inputs

asin  : Arcsine

acos  : Arccosine

deg   : Converts radians to degrees

rad   : Converts Degrees to radians

floor : Rounds down

ceil  : Rounds up

abs   : Absolute value

sign  : Returns -1 if the input is negative and 1 if it is positive

log10 : Log of base 10 

log2  : Log of base 2 

loge  : Log of base e

logbase : Log of base n, supplied as an argument 

sqrt : Square root

root : Nth root, supplied by an argument 

dot2 : Takes dot product of two 2d vectors (x1, y1, x2, y2)

dot3 : Takes dot product of two 3d vectors (x1, y1, z1, x2, y2, z2)