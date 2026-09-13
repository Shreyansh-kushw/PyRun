# A tiny interpreter

"""
Building upon the foundation to add variable support -

LOAD_VALUE - appends a number into the stack
ADD_TWO_VALUES - pops the numbers one by one from the stack and append them again after adding them
PRINT_ANSWER - pops the result out of the stack and prints it.
STORE_NAME - instruction for storing the value of a variable.
LOAD_NAME - instruction for retrieving it.

>>> def s():
...     a = 1
...     b = 2
...     print(a + b)
# a friendly compiler transforms `s` into:
    what_to_execute = {
        "instructions": [("LOAD_VALUE", 0), # -> first we load the value
                         ("STORE_NAME", 0), # -> then we store the value into the variable
                         ("LOAD_VALUE", 1),
                         ("STORE_NAME", 1),
                         ("LOAD_NAME", 0), # -> first we load the variables and their values
                         ("LOAD_NAME", 1),
                         ("ADD_TWO_VALUES", None), # -> then we perform the operations
                         ("PRINT_ANSWER", None)],
        "numbers": [1, 2],
        "names":   ["a", "b"] }

Now one more thing to note here is this, different instructions have argument corresponding to different things, 
like STORE_NAME, LOAD_NAME refer to the variable names 
while LOAD_VALUES and others refer to the values inside the numbers stack. 
thus we now need to make a function to parse the arguments based on the type of instructions we are executing

"""

class Interpreter:

    def __init__(self):
        self.stack = [] # creating the stack
        self.environment = {} # the environment dictionary that would store the different variables and their values 

    def STORE_NAME(self, name):
        val = self.stack.pop() # getting the value to be assigned to the variable name by popping it out of the stack``
        self.environment[name] = val # adding the value and name to the environment dictionary
    
    def LOAD_NAME(self, name):
        val = self.environment[name] # getting the value for the variable name from the environment dictionary
        self.stack.append(val) # appending the value into the stack to perform operations

    def LOAD_VALUE(self, number):
        self.stack.append(number)
    
    def ADD_TWO_VALUES(self):
        a = self.stack.pop()
        b = self.stack.pop()
        answer = a + b
        self.stack.append(answer)

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def parse_arguments(self, instruction, argument, what_to_execute):
        """Understanding what the argument for a instruction means."""

        numbers = ["LOAD_VALUE"] # list of instructions whose arguments correspond to the numbers list.
        names = ["STORE_NAME", "LOAD_NAME"] # list of instructions whose arguments correspond to the variables names list.

        if instruction in numbers:
            argument = what_to_execute["numbers"][argument]
        elif instruction in names:
            argument = what_to_execute["names"][argument]
        
        return argument 

        # basically we are converting the index of the corresponding argument into the definite argument the 
        # instruction need to operate on.

    # Now we just need one more thing, something to tie everything together and run the code.

    def run_code(self, what_to_execute):
        """Takes in the instructions and executes them"""

        instructions = what_to_execute["instructions"]
        numbers = what_to_execute["numbers"]

        for each_step in instructions: # here we can see that instructions are executed one by one - thus its an interpreter
            instruction, argument = each_step
            argument = self.parse_arguments(instruction, argument, what_to_execute)

            if instruction == "LOAD_VALUE":
                self.LOAD_VALUE(argument)
            
            elif instruction == "STORE_NAME":
                self.STORE_NAME(argument)
            
            elif instruction == "LOAD_NAME":
                self.LOAD_NAME(argument)

            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            
            elif instruction == "PRINT_ANSWER":
                self.PRINT_ANSWER()

def main():
    """Running the interpreter"""
    global Interpreter

    Interpreter = Interpreter()
    Interpreter.run_code(
        what_to_execute = {
        "instructions": [("LOAD_VALUE", 0),
                         ("STORE_NAME", 0),
                         ("LOAD_VALUE", 1),
                         ("STORE_NAME", 1),
                         ("LOAD_NAME", 0),
                         ("LOAD_NAME", 1),
                         ("ADD_TWO_VALUES", None),
                         ("PRINT_ANSWER", None)],
        "numbers": [1, 2],
        "names":   ["a", "b"] }
    )

"""

Here we can see that for every instruction, there are two things required. 
The instructions itself and an argument, for eg. telling the interpreter where to find the number to load .

So our instruction set has two pieces: the instructions themselves, plus a list of constants the instructions will need.
 
(In Python, what we're calling "instructions" is the bytecode, and the "what to execute" object below is the code object.)

"""