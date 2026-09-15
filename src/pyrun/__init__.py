import types
import inspect
import dis
import sys
import collections
import operator

Block = collections.namedtuple("Block", "type, handler, stack_height")

"""
Blocks are responsible for handling stuff like loops, exception handling etc.

>>> Block(
...     type, -> the type of block, eg. loop
...     handler, -> the instruction code which will be run after the ending or breaking of the loop
...     stack_height -> number of elements in data stack when the block was creation
    )

Stack height is saved because during the execution of a block, some temporary values might be added into the data stack which shall be removed afterwards.

"""

class VirtualMachineException(Exception):
    pass

class VirtualMachine:
    """The virtual machine class"""

    def __init__(self):
        self.frames = [] # call stack of rames
        self.frame = None # current frame
        self.return_value = None # return values
        self.last_exeption = None # exception states

    def run_code(self, code, global_names = None, local_names = None):
        """Entry point for the execution of the code"""

        frame = self.make_frame(code, global_names, local_names)
        self.run_frame(frame)
    
    # Frame manipulation
    def make_frame(self, code, callargs = {}, global_names = None, local_names = None):
        """Creates a new frame"""

        if global_names is not None and local_names is not None:
            local_names = global_names
        elif self.frames:
            global_names = self.frame.global_names
            local_names = {}
        else:
            global_names = local_names = {
                '__builtins__' : __builtins__,
                '__name__' : '__main__',
                '__docs__' : None,
                '__package__' : None,
            }
        local_names.update(callargs)
        frame = Frame(code, global_names, local_names, self.frame)
        return frame

    def push_frame(self, frame):
        """Pushes a frame into the call stack"""

        self.frames.append(frame)
        self.frame = frame
    
    def pop_frame(self):
        """Removes a frame from the call stack"""

        self.frame.pop()

        if self.frames:
            self.frame = self.frames[-1]
        
        else: 
            self.frame = None
    
    def run_frame(self, frame):
        """Runs a frame until it returns something
        Exceptions are raised and return values are returned"""

        self.push_frame(frame)
        while True:
            byte_name. arguments = self.parse_bytes_and_args()

            why = self.dispatch(byte_name, arguments)

            # Dealing with block management.
            while why and frame.block_stack:
                why = self.manage_block_stack(why)
            
            if why: # something is returned
                break
        
        self.pop_frame()

        if why == 'exception':
            exc, val, tb = self.last_exeption
            e = exc(val)
            e.__traceback__ = tb
            raise e
    
        return self.return_value


    # data stack manipulation
    def top(self):
        return self.frame.stack[-1]
    
    def pop(self):
        return self.frame.stack.pop()
    
    def push(self, values):
        self.frame.stack.extend(values)
    
    def popn(self, n):
        """Pop a number of values from the data stack
        A list of n values is returned with the deepest value first.
        """

        if n:
            ret = self.frame.stack[-n:]
            self.frame.stack[-n:] = []
            return ret
        else:
            return []

    def parse_bytes_and_args(self):
        """Takes a bytecode instruction, checks it it has arguments, if so, then parses it and returns the final argument."""
        f = self.frame
        opoffset = f.last_instruction # operation off set
        byteCode = f.code_obj.co_code[opoffset]
        f.last_instruction += 1
        byte_name = dis.opname[byteCode]

        if byteCode >= dis.HAVE_ARGUMENT: # checking if this particular instruction requires any argument

            # indexing into the bytecode
            arg = f.code_obj.co_code[f.last_instruction : f.last_instruction + 2]
            f.last_instruction += 2 # incrementing the instruction offset to the next one
            arg_val = arg[0] + (arg[1] * 256) # formula to calculate the actual argument value

            # checking what the argument corresponds to.
            if byteCode in dis.hasconst:
                args = f.code_obj.co_consts[arg_val]
            elif byteCode in dis.hasname:
                args = f.code_obj.co_name[arg_val]
            elif byteCode in dis.haslocal:
                args = f.code_obj.co_varnames[arg_val]
            elif byteCode in dis.hasjrel: # Calculating a relative jump
                args = f.last_instruction + arg_val # jumping forward by the argument value
            else: # if the argument itself is to be the input argument
                args = arg_val

            argument = [args] 
        
        else:
            argument = []
        
        return byte_name, argument

    def dispatch(self, byte_name, argument):
        """Looks for an operation for a given instruction and executes it.
        Exceptions has caught and set on the virtual machine class.
        """

        why = None # this is what is returned by the corrsponding functions for the instructions
        try:
            bytecode_func = getattr(self, f"byte_{byte_name}", None)
            if bytecode_func is None:
                if byte_name.startswith('UNARY_'):
                    self.unaryOperator(byte_name[6:])
                elif byte_name.startswith('BINARY_'):
                    self.binaryOperator(byte_name[7:])
                else:
                    raise VirtualMachineException(
                        "Unsupported bytecode type: {}".format(byte_name)
                    )
        
            else:
                why = bytecode_func(*argument) # we will pass in not the list, but rather the unpacked arguments. Because the function 
                # doesn't expect list of arguments
        
        except:
            # dealing with the exception encountered while dispatching
            self.last_exeption = sys.exc_info()[:2] + (None,)
            why = 'exception'
        
        return why

    # Block stack manipulation
    def push_block(self, b_type, handler = None):
        stack_height = len(self.frame.stack)
        self.frame.block_stack.append(Block(b_type, handler, stack_height))
    
    def pop_block(self):
        return self.frame.block_stack.pop()
    
    def unwind_block(self, block):
        """It cleans data stack back to the initial state.
        This function is ran when we need to exit the current block (loop or except block.)

        Therefore, the continue keyword won't trigger the unwind as it doesn't leave the loop.

        """
        if block.type == 'exception-handler':
            # The exception itself is on the stack as type, value, and traceback.
            offset = 3
        else:
            offset = 0
        
        while len(self.frame.stack) > block.stack_height + offset:
            self.frame.stack.pop() # removing unwanted entries from the data stack
        
        if block.type == 'exception-handler':
            traceback, value, exctype = self.popn(3)
            self.last_exeption = exctype, value, traceback
    
    def manage_block_stack(self, why):
        """Takes the necessary actions based on the reason for leaving the current block (why)"""

        # getting the current block
        frame = self.frame
        block = self.frame.block_stack[-1]

        if block.type == 'loop' and why == 'continue': # its a loop and broke the flow because of continue keyword
            why = None
            self.jump(self.return_value) # jumping to the continuation point in the loop -> do not take the name at face value
            # it is being used to store where the interpreter has to return to, to continue the execution of the loop.
            return why # returning why = None here to emphasize that no extra actions is needed on this.

        # Now after we have handelled the scenerio of continue - i.e. the only scenerio that involved staying inside of the loop 
        # (as it just jumps to another instruction, i.e. no need to pop the block or unwind)

        # For all other scenerios, we eventually need to remove the block from the block stack and revert the data stack to its correct state.

        self.pop_block() # removing the block
        self.unwind_block(block) # unwinding the changes.

        # handling break keyword.
        if block.type == 'loop' and why == 'break':
            why = None # no further action needed
            self.jump(block.handler) # jumping to the code after the loop
            return why
        
        if (block.type in ['setup-except', 'finally'] and why == 'exception'): # means we are leaving a try/finally related block because of an exception

            self.push_block('exception-handler') # outsourcing handling of exception to exception handler block (created anew)
            # why? -> because we need a new control flow region for exception handling.

            exctype, value, tb = self.last_exeption
            self.push(exctype, value, tb)
            self.push(exctype, value, tb)

            why = None # exception is already outsourced to the exception handler so nothing more to worry about here.
            self.jump(block.handler) # jumping to the exception handler.
            return why
        
        elif block.type == 'finally':
            if why in ['return', 'continue']: # finally must always run whether the flow breaks because of continue or return.
                '''Here we are only pushing a return value in case of return or continue. 
                   A 'break' why need not require any return value to be pushed into the data stack.'''
                self.push(self.return_value) # adding the return value to the data stack
            
            self.push(why) # pushing the why to the data stack too
            # why is pushed onto the data stack so that finally block might know what caused the break in the block.
            # it is popped off afterwards 

            why = None # It is a way to postpone the unwinding to a later stage after the finally block is executes
            # the older state of why was stored in the data stack to go back and resume the needed unwinding process for that 'why'
            # So firstly we save the current state of things inside the data stack and then jump to the finally block.
            self.jump(block.handler) # jumping to the finally block
            return why
        
        return why

    # Instructions

    ## Stack manipulation
    
    def byte_LOAD_CONST(self, const):
        self.push(const)
    
    def byte_POP_TOP(self):
        return self.pop()
    
    ## Names:
    def byte_LOAD_NAME(self, name):
        frame = self.frame
        if name in frame.local_names:
            val = frame.local_names[name]
        elif name in frame.global_names:
            val = frame.global_names[name]
        elif name in frame.builtin_names:
            val = frame.builtin_names[name]
        else:
            raise NameError(f"Name {name} is not defined")

        self.push(val) # pushing the name value onto the data stack

    def byte_STORE_NAME(self, name):
        self.frame.local_names[name] = self.pop() # storing the latest most value from the data stack in the variable name

    def byte_LOAD_FAST(self, name):
        """Checks for the variable name in the local namespace"""
        if name in self.frame.local_names:
            self.push(self.frame.local_names[name])
        else:
            raise UnboundLocalError(
                f"local variable {name} referenced before assignment."
            )

    def byte_STORE_FAST(self, name): 
        """Stores a variable and its value in the local namespace"""
        self.frame.local_names[name] = self.pop()

    def byte_LOAD_GLOBAL(self, name):
        """Checks for the value of a variables in the global and builtin namespace"""
        f = self.frame
        if name in f.global_names:
            val = f.global_names[name]
        elif: name in f.builtin_names:
            val = f.builtin_names[name]
        else:
            raise NameError(f"global name {name} is not defined.")
        
        self.push(val)
    
    ## Operators

    BINARY_OPERATORS = {
        'POWER': pow,
        'MULTIPLY': operator.mul,
        'FLOOR_DIVIDE': operator.floordiv,
        'TRUE_DIVIDE':  operator.truediv,
        'MODULO':   operator.mod,
        'ADD':      operator.add,
        'SUBTRACT': operator.sub,
        'SUBSCR':   operator.getitem,
        'LSHIFT':   operator.lshift,
        'RSHIFT':   operator.rshift,
        'AND':      operator.and_,
        'XOR':      operator.xor,
        'OR':       operator.or_, 
    }

    def binaryOperator(self, op):
        x, y = self.popn(2) # getting the top 2 values to operate on
        self.push(self.BINARY_OPERATORS[op](x,y))
    

    COMPARE_OPERATORS = [
        operator.lt,
        operator.le,
        operator.eq,
        operator.ne,
        operator.gt,
        operator.ge,
        lambda x, y: x in y,
        lambda x, y: x not in y,
        lambda x, y: x is y,
        lambda x, y: x is not y,
        lambda x, y: issubclass(x, Exception) and issubclass(x, y),
    ]

    def byte_COMPARE_OP(self, opnum):
        x, y = self.popn(2)
        self.push(self.COMPARE_OPERATORS[opnum](x, y))

    UNARY_OPERATORS = {
        'POSITIVE' : operator.pos,
        'NEGATIVE' : operator.neg,
        'NOT' : operator.not_,
        'CONVERT' : repr,
        'INVERT' : operator.invert,
    }

    def unaryOperator(self, op):
        x = self.pop()
        self.push(self.UNARY_OPERATORS[op](x))
        
class Frame:
    """The frame class containing the various attributes of the code object"""

    def __init__(
        self,
        code_obj,
        global_names,
        local_names,
        prev_frame,
    ):
        self.code_obj = code_obj
        self.global_names = global_names
        self.local_names = local_names
        self.prev_frame = prev_frame

        self.stack = [] # the data stack for this frame
        self.block_stack = [] # the block stack for this Frame

        # setting up the builtins
        if prev_frame:
            self.builtin_names = self.prev_frame.builtin_names
        else:
            self.builtin_names = local_names['__builtins__']
            if hasattr(self.builtin_names, '__dict__'):
                self.builtin_names = self.builtin_names.__dict__

        self.last_instruction = 0
        
class Function:
    """
    Create a realistic function object, defining the things the interpreter expects.

    Essentially this is the class that would be created when the user uses the def keyword
    """
    __slots__ = [ # list of allowed attributes for the objects of this class
    'func_code', 'func_name', 'func_defaults', 'func_globals',
    'func_locals', 'func_dict', 'func_closure', 
    '__name__', '__dict__', '__doc__',
    '_vm', '_frame'
    ]        

    '''
    NOTE: All the different attributes we define inside the __slots__ list get there own dedicated storage slots.
    Any other attribute we define will be added inside the __dict__ dictionary.
    '''

    # every class has a __dict__ attribute that is essentially a dictionary that contains all the various attributes associated with 
    # an object of this class.

    def __init__(self, name, code, globs, defaults, closure, vm):

        self._vm = vm
        self.func_code = code # this is the code object
        self.func_name = name or code.co_name # setting the name of the function
        self.func_defaults = tuple(defaults) # this stores the default values for the arguments of the function
        '''
        NOTE: when we define something like name = "Add" in default argument, it defaules to a tuple ("Add", ) within the inner workings of python
        '''
        self.func_globals = globs # the global namespace
        self.func_locals = self._vm.frame.local_names # the local namespace grabbed from the current frame 
        self.__dict__ = {} # stores any other arbitrary attribute for the class (if needed)
        self.func_closure = closure # stores the function's closure, more on it later.
        self.__doc__ = code.co_consts[0] if code.co_consts else None # storing the doc string for the function
        '''
        NOTE- Inside every code block, code.co_consts gives a list of all the constant defined inside that code block. This includes both int, str, or float
        Now, when we define a function, in its constant list, the first element is the doc string of the function.
        That's why we are looking for the first element in the constants list.
        '''

        # Now we need to use the builtin python functions to help with parsing the passed arguments.
        # To match the argument : value pairs to be exact

        kw = { # keyword arguments
            'argdefs' : self.func_defaults, # argdefs - default arguments
        }

        if closure:
            kw['closure'] = tuple(make_cell(0) for _ in closure) 
            # here we are just creating a dummy cell entry for each required closure because it is needed to create the function object
            # here we do not need to worry about the legitimacy of the cell, because we are not actually going to execute the function object
            # rather we are only using it to get the mappings of the arguments with their values.
        
        self._func = types.FunctionType(code, globs, **kw) # basically creates a function object from the compiled raw python code, the 
        # global variables and the keyword arguments.
    
    def __call__(self, *args, **kwargs):
        """When calling a function, it creates a new frame and runs it"""

        callargs = inspect.getcallargs(self._func, *args, **kwargs) # returns the mappings of the values and arguments as a dict

        frame = self._vm.make_frame(self.func_code, callargs, self.func_globals, {})
        # here the local_namespace = {} to ensure that each new function gets its own unique local namespace.
        return self._vm.run_frame(frame)

def make_cell(value):
    """Creates a new cell for an arbitrary closure"""

    function = (lambda x: lambda: x)(value)
    '''
    Equivalent to
    >>> def outer(value):
    ...     def inner():
    ...         return value
    ...     return inner

    Thus function becomes
    >>> function = outer(value)
    '''

    return function.__closure__[0]
    # Here as there is need for a closure inside the function, thus it would make one (because there only one dependent var between inner and outer)
    # and we can access its particular cell with index 0 - (only one cell thus index 0)
