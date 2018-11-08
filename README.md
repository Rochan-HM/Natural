# Natural

My own language (interpreter) program using the Python implementations of yacc and flex.
I am using the tokenizer and parser from `ply` module's updated version, `sly`. 


## Nomenclature
I tried to make this language as natural as possible. Hence the name **'Natural'**.

## Variable Assignment

    Syntax: assign var_name = value
    
    Ex: assign i = 0


## Code Blocks

    Syntax: 
    expression
    start
	statement
    end
		
    Ex: 
    for assign i = 0 to 10
    start
	display 15
    end

## If Statement

    Syntax: 
    check if expression
    start
    	statement
    end
		
    Ex: 
    check if 1 equals 2
    start
	assign i = 5
    end
## If - Else Statements

    Syntax: 
    check if expression
    start
    	statement
    end
			
    else
    start
	statement
    end
		
    Ex:
    check if 1 equals 2
    start
    	assign i = 5
    end
			
    else 
    start
    	assign i = 65
    end
## If - Else if - Ladder 

    Syntax: 
    check if expression
    start
    	statement
    end

    or if expression
    start
	statement
    end
    ....   ** As many or if's required
			
    else
    start
	statement
    end
		
    Ex:
    check if 1 equals 2
    start
	assign i = 5
    end

    or if 1 equals 1
    start
	assign i = 100
    end

    else
    start
	assign i = 87
    end

## Equals

    Syntax: expression equals expression
	    
    Ex: 1 equals 2 **Returns False
## Comments

    Syntax: **Comment goes here. This will not be evaluated
## For Loop

    Syntax: 
    for var_assign to value
    start
    	statement
    end

    Ex:	
    for assign i = 0 to 10
    start
    	display 5
    end 
## Functions

    Syntax: 
    function name takes ()
    start 
    	statement
    end
			
    Ex:
    function x takes ()
    start
	assign j = 0
    end
## Calling a function

    Syntax: func_name()
    
    Ex: 
    **From above example,
	    x() 
    ** after calling this, the value of j will be 0
## Mathematical Functions
Just like any interpreter, this too can perform mathematical operations such as addition (+), subtraction (-), multiplication (*), division (/), modulus (%), greater than (>), lesser than (<), greater than equals (>=), and lesser than equals (<=).

    Ex: 1 + 1 **Returns 2
## Note
Due to the nature of the program, multiple line inputs are not yet supported. I am working to add these features soon. I am also working to add function parameters and some sort of generator functions.
In future versions, I plan on using sys.argv to take input via the command shell.
## Example Program

    >>> ** Program to print a number 10 times
    >>> for assign i = 0 to 11 start display n end
    q
    >>> **Program using functions
    >>> function hello takes() start assign z = 56 end
    >>> hello()
    >>> z **Returns 56
## Credits
This was developed my Rochan. Please email any further modifications to 

> rochana.hm3@gmail.com
