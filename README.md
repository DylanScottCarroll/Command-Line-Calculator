# Command-Line-Calculator
Just a simple calculator app you can use just by typing.

I wrote this because I seldom used the Windows calculator and instead typed calculations right into the windows search bar because I found the calculator slow and cumbersome to open and use. Most of the time, this shows up as a bing search which has the result. The advantage of this is that all I need to do is quickly hit the windows key and start typing. The problem is that this uses bing 🤮 and it doesn't work all of the time (sometimes it thinks you're trying to search for files). On my PC, I have this linked to run whenever I type a keyboard shortcut.


**The basic features include:**
*Standard scientific calculator operations 
*Functions
*Boolean comparison operators
*Variables
*Assignment operators

**Operators:**
Normal Ones
\*  : Multiplication
/  : Division
// : Integer Division
%  : Modulo (Remainder)
\+  : Addition
\-  : Subtraction (Also unary negation operator)
^  : Exponentiation

Assignment Operators
=  : Sets the value (Also used to create new variables)
+= : Increments by the value
-= : Decrements by the value
++ : Increments by 1
-- : Decraments by 1

Boolean Comparison Operators
== : Equal to
\>= : Greater than or equal to
<= : Less than or equal to
!- : Not equal to
<  : Less than
\>  : Greater than

**Functions**
Trig
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
loge  : Log of base 4 
logbase : Log of base n, supplied as an argument 
sqrt : Square root
nthroot : Nth root, supplied by an argument 


**Known Issues**
*Functions were hacked together. It does not check if you supplied the correct number of arguments and will select values outside of the function call in unpredictable ways if not enough arguments are given.
*You can't use more than one unary operator in a row.
*If you type just one number and hit enter, it prints the number twice.
*If you try to assign a number as if it were a variable
*You can have decimal points in variable names
*There are no logical operators such ac && or ||
