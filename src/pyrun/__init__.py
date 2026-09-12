# A tiny interpreter

"""
This simple interpreter is built to understand three instructions -

LOAD_VALUE - appends a number into the stack
ADD_TWO_VALUES - pops the numbers one by one from the stack and append them again after adding them
PRINT_ANSWER - pops the result out of the stack and prints it.

"""

class Interpreter:

    def __init__(self):
        self.stack = [] # creating the stack

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
    
    # Now we just need one more thing, something to tie everything together and run the code.

    def run_code(self, what_to_execute):
        """Takes in the instructions and executes them"""

        instructions = what_to_execute["instructions"]
        numbers = what_to_execute["numbers"]

        for each_step in instructions: # here we can see that instructions are executed one by one - thus its an interpreter
            instruction, argument = each_step

            if instruction == "LOAD_VALUE":
                self.LOAD_VALUE(numbers[argument])
            
            elif instruction == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            
            else:
                self.PRINT_ANSWER()

def main():
    """Running the interpreter"""
    global Interpreter

    Interpreter = Interpreter()
    Interpreter.run_code(
        what_to_execute= {
    "instructions": [("LOAD_VALUE", 0),  # the first number
                     ("LOAD_VALUE", 1),  # the second number
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [7, 5] }
    )

"""

Here we can see that for every instruction, there are two things required. 
The instructions itself and an argument, for eg. telling the interpreter where to find the number to load .

So our instruction set has two pieces: the instructions themselves, plus a list of constants the instructions will need.
 
(In Python, what we're calling "instructions" is the bytecode, and the "what to execute" object below is the code object.)

"""